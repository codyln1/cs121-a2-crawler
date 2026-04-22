from utils.tokenize import tokenize, merge_with_input

REPORT_UNIQUE_PAGES = "report_unique_pages.txt";
REPORT_LONGEST = "report_longest_page.txt";
REPORT_WORD_FREQ = "report_word_frequencies.txt";
REPORT_SUBDOMAIN_FREQ = "report_subdomain_frequencies.txt";

"""
Handles reading/writing files for report contents (longest page and word frequencies)
Does NOT keep track of unique URLs or the number of subdomains, as those can be
obtained from Logs/Worker.log by scripts/GenerateReport.py
"""
class Report:
    def __init__(self):
        self.unique_pages = set()
        self.unique_pages_count = 0
        self.longest_page = {"url": "", "word_count": 0}
        self.word_frequencies = dict()
        self.subdomain_frequences = dict()

        self.load_report_files()

    def load_report_files(self):
        # TODO: test
        try:
            with open(REPORT_UNIQUE_PAGES, 'r') as f:
                self.unique_pages_count = int(f.readline().strip())
                for line in f:
                    url = line.strip()
                    self.unique_pages.add(url)
        except:
            print('[LOG] REPORT_UNIQUE_PAGES file not found, file progress is starting from zero')

        try:
            with open(REPORT_LONGEST, 'r') as f:
                url = f.readline().strip()
                word_count = int(f.readline())
                self.longest_page = {"url": url, "word_count": word_count}
        except:
            print('[LOG] REPORT_LONGEST file not found, file progress is starting from zero')

        try:
            with open(REPORT_WORD_FREQ, 'r') as f:
                for line in f:
                    splitted = line.split()
                    self.word_frequencies[splitted[0]] = int(splitted[1])
        except:
            print('[LOG] REPORT_WORD_FREQ file not found, file progress is starting from zero')

        try:
            with open(REPORT_SUBDOMAIN_FREQ, 'r') as f:
                for line in f:
                    splitted = line.split()
                    self.subdomain_frequences[splitted[0]] = int(splitted[1])
        except: 
            print('[LOG] REPORT_SUBDOMAIN_FREQ file not found, file progress is starting from zero')

    def write_report_files(self):
        # TODO: test
        with open(REPORT_UNIQUE_PAGES, 'w') as f:
            content = self.unique_pages_count + '\n'
            for page in self.unique_pages:
                content += page + '\n' 
            f.write(content)
        with open(REPORT_LONGEST, 'w') as f:
            content = self.longest_page['url'] + '\n' + str(self.longest_page['word_count']) + '\n'
            f.write(content)
        with open(REPORT_WORD_FREQ, 'w') as f:
            # TODO: check performance
            content = ''
            for key, val in self.word_frequencies.items():
                content += key + ' ' + str(val) + '\n'
            f.write(content)
        with open(REPORT_SUBDOMAIN_FREQ, 'w') as f:
            content = ''
            for key, val in self.subdomain_frequences.items():
                content += key + ' ' + str(val) + '\n'
            f.write(content)

    def update_report(self, url, page_text):
        page_frequencies = tokenize(page_text)
        page_word_count = sum(page_frequencies.values())

        if (len(self.unique_pages) != self.unique_pages_count):
                print ('[LOG] self.unique_pages_count is not aligned with number of unique pages')
        is_unique_page = False
        defragmented_url = url.split("#")[0]
        self.unique_pages.add(defragmented_url)
        if(len(self.unique_pages) != self.unique_pages_count):
            if (len(self.unique_pages) != self.unique_pages_count+1):
                print ('[LOG] self.unique_pages_count is not aligned with number of unique pages')
            else:
                is_unique_page = True
                self.unique_pages_count += 1

        if page_word_count > self.longest_page['word_count']:
            self.longest_page['url'] = url
            self.longest_page['word_count'] = page_word_count
        self.word_frequencies = merge_with_input(self.word_frequencies, page_frequencies)

        if(is_unique_page):
            url_subdomain = url[url.find("\\")+2, url.find(".uci.edu")+8]
            if url_subdomain in self.subdomain_frequences:
                self.subdomain_frequences[url_subdomain] += 1
            else:
                self.subdomain_frequences[url_subdomain] = 1
                
        self.write_report_files()
