# Transform Worker.log into a list of URLs

from urllib.parse import urldefrag, urlsplit
from functools import cmp_to_key

LOG_PATH = '../Logs/Worker.log'

WORD_COUNT_PATH = '../Logs/report_word_frequencies.txt'
LONGEST_PAGE_PATH = '../Logs/report_longest_page.txt'

OUTPUT_PATH = '../Logs/assignment_2_report.txt'

def compareWordFrequencyEntries(item1, item2):
    if item1[1] > item2[1]:
        return -1
    elif item1[1] < item2[1]:
        return 1
    elif item1[0] < item2[0]:
        return -1
    else:
        return 1

def parse_logs():
    urls = []

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
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

    words = {}
    with open(WORD_COUNT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            splitted = line.split()
            words[splitted[0]] = int(splitted[1])

    longest_page_url = ""
    longest_page_words = 0
    with open(LONGEST_PAGE_PATH, 'r', encoding='utf-8') as f:
        longest_page_url = f.readline().strip()
        longest_page_words = f.readline().strip()

    sorted_freq = sorted(words.items(), key=cmp_to_key(compareWordFrequencyEntries))
    num_taken = 0
    top_50_words = {}
    for w, freq in sorted_freq:
        top_50_words[w] = freq
        num_taken += 1

        if num_taken >= 50:
            break

    sorted_top_50 = dict(sorted(top_50_words.items(), key=cmp_to_key(compareWordFrequencyEntries)))

    no_fragments = [urldefrag(url)[0] for url in urls]

    return (no_fragments, sorted_top_50, longest_page_url, longest_page_words)

def create_report(urls, common_words, longest_page_url, longest_page_words):
    report = "ASSIGNMENT 2 REPORT\n"
    report += '\n'

    unique_urls = set(urls)
    report += 'UNIQUE PAGE COUNT: ' + str(len(unique_urls)) + '\n'
    report += '\n'

    report += 'LONGEST PAGE: ' + longest_page_url + ' (' + str(longest_page_words) + ' words)' + '\n'
    report += '\n'

    report += 'MOST COMMON WORDS:\n'
    for word, freq in common_words.items():
        report += word + ', ' + str(freq) + '\n'

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
    parse_res = parse_logs()

    report = create_report(*parse_res)
    print(report)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print('Report written to ' + OUTPUT_PATH)
