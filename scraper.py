import re
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    # TODO: save URL and web page?
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp) -> list:
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    next_links = []

    # Checks in place to make sure the response is valid before parsing
    # 1) check for status codes that indicate an error (600-608)
    if resp.status in range(600, 609):
        print(f"Error {resp.url}: {resp.error}")
        return next_links
    elif resp.status != 200:
        return next_links
    
    # 2) check for raw_response and content + length (only parse if content is not empty or too large >3MB)
    if not resp.raw_response or not resp.raw_response.content:
        return next_links
    elif len(resp.raw_response.content) not in range(1, 3 * 1024 * 1024):
        return next_links
    
    with open(resp.raw_response.content, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        for link in soup.find_all("a"):
            try:
                next_links.append(urldefrag(link.get("href"))[0])
            except Exception:
                continue
    return next_links

VALID_NETLOCS = {'ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu'}

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.netloc not in VALID_NETLOCS:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
