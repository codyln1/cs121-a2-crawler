# Transform Worker.log into a list of URLs

from urllib.parse import urldefrag, urlsplit

# TODO: collect from other crawler-generated report files as well
LOG_PATH = '../Logs/Worker.log'

OUTPUT_PATH = '../Logs/assignment_2_report.txt'

def parse_logs():

    urls = []

    with open(LOG_PATH, 'r') as f:
        for line in f:
            splitted = line.split()
            url_section = splitted[8]
            if url_section == 'is':
                continue
            # TODO: is status check needed?
            status_section = splitted[10]
            if status_section != '<200>,':
                continue

            urls.append(url_section[0:len(url_section)-1])

    no_fragments = [urldefrag(url)[0] for url in urls]

    # TODO: get other details
    return (no_fragments, 0, "UNIMPLEMENTED", 0)

def create_report(urls):
    report = "ASSIGNMENT 2 REPORT\n"
    report += '\n'

    unique_urls = set(urls)
    report += 'UNIQUE PAGE COUNT: ' + str(len(unique_urls)) + '\n'
    report += '\n'

    by_subdomain = {}
    for url in unique_urls:
        netloc = urlsplit(url).netloc
        if netloc in by_subdomain:
            by_subdomain[netloc] += 1
        else:
            by_subdomain[netloc] = 1

    report += 'FOUND ' + str(len(by_subdomain)) + ' SUBDOMAINS:\n'
    by_subdomain_sorted = dict(sorted(by_subdomain.items()))
    for key, val in by_subdomain_sorted.items():
        report += key + ', ' + str(val) + '\n'

    return report

if __name__ == "__main__":
    (urls, common_words, longest_page_url, longest_page_words) = parse_logs()

    report = create_report(urls)
    print(report)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(report)
    print('Report written to ' + OUTPUT_PATH)
