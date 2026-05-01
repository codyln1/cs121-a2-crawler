import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup

VALID_NETLOC_SUFFIXES = {'ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu'}

TRAP_PAGE_PREFIXES = {
    # Low-value because contents are just photos with a thin HTML wrapper
    'https://ics.uci.edu/~eppstein/pix',
    # Low-value because this is source code, which are not webpages
    'https://flamingo.ics.uci.edu/releases/',
    # Married...
    'https://ics.uci.edu/~dhirschb/genealogy',
}

TRAP_PAGE_CONTAINS = {
    # Also auth-gated with a huge amount of low-value links
    'doku.php',
    # Valid HTML, but the page appears malformed and this is hard to detect programatically. Both https and http
    'ics.uci.edu/~cs224',
    # Low-value thin wrappers around pages
    'wscacchi/Presentations',
    # None of these are found
    'slides/node',
}

TRAP_PAGE_REGEXES = {
    # Infinite calendar traps (events/ ... YYYY-MM or events / ... YYYY-MM-DD)
    '.*events.*[0-9]{4}.[0-9]{2}.*',
    # Auth-gated and calendar-like traps
    '.*grape.ics.uci.edu\/.*\/timeline.*',
    # Thin wrapper around images that cannot be scraped
    # E.g. https://ics.uci.edu/~irus/twist/wisen98/presentations/Aggarwal/sld010.htm
    '.*sld.*htm.*',
    # Low-value because the majority of contents are auth-gated or very similar copies of pages
    '.*grape.ics.uci.edu\/wiki.*\/(cs|stats).*',
    # Unusable file directories
    '.*\?C=.;O=..*'
}

def scraper(url, resp, report):
    links = extract_next_links(url, resp, report)
    return [link for link in links if is_valid(link)]

def is_usable_response(resp):
    # Handle status codes that indicate an error (600-608)
    if resp.status in range(600, 609):
        print(f"[ERROR] {resp.url}: {resp.error}")
        return False
    if resp.status != 200:
        return False
    # Response must exist
    if not resp.raw_response or not resp.raw_response.content:
        return False
    # Response must have reasonable length (<3MB)
    if len(resp.raw_response.content) not in range(1, 3 * 1024 * 1024):
        return False
    # Response must be HTML
    content_type = resp.raw_response.headers.get('Content-Type')
    if not content_type or 'text/html' not in content_type:
        return False
    return True

def extract_next_links(url, resp, report) -> list:
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

    if not is_usable_response(resp):
        return next_links

    # Parse the content with BeautifulSoup and extract links
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    for link in soup.find_all("a"):
        try:
            next_href = link.get("href")
            joined = urljoin(resp.raw_response.url, next_href)
            next_links.append(urldefrag(joined)[0])
        except Exception:
            continue

    # DEBUG
    if 'gbowker' in url:
        with open('Logs/debug_log.txt', 'a', encoding='utf-8') as f:
            contents = '[dbg] resp.url: ' + resp.url + ', resp.raw_response.url: ' + resp.raw_response.url + ', found: ' + str(next_links) + '\n'
            f.write(contents)

    # Update report
    text = soup.get_text()
    if not report.is_duplicate(text):
        report.update_report(resp.raw_response.url, text)
        return next_links
    return []

def valid_netloc(netloc):
    for suffix in VALID_NETLOC_SUFFIXES:
        if netloc.endswith('.' + suffix) or netloc == suffix:
            return True
    return False

"""
Returns whether a page is a known trap or low-value page.
Uses the rules defined in constants above
Some low-value pages are already handled in is_valid
(e.g. avoid large datasets by ignoring zip files)
"""
def is_trap_page(url):
    for trap in TRAP_PAGE_PREFIXES:
        if url.startswith(trap):
            return True
    for trap in TRAP_PAGE_CONTAINS:
        if trap in url:
            return True
    for r in TRAP_PAGE_REGEXES:
        if re.search(r, url):
            return True
    return False

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not valid_netloc(parsed.netloc):
            return False
        if is_trap_page(url):
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

    except ValueError:
        # Invalid IP address (e.g. one can be found at https://grape.ics.uci.edu/wiki/public/wiki/cs122b-2017-winter-project3)
        print("[LOG] Invalid IP address found: " + url)
        return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
