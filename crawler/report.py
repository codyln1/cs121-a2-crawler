from utils.tokenize import tokenize, merge_with_input

REPORT_LONGEST = "report_longest_page.txt";
REPORT_WORD_FREQ = "report_word_frequencies.txt";

"""
Handles reading/writing files for report contents (longest page and word frequencies)
Does NOT keep track of unique URLs or the number of subdomains, as those can be
obtained from Logs/Worker.log by scripts/GenerateReport.py
"""
class Report:
    def __init__(self):
        self.longest_page = {"url": "", "word_count": 0}
        self.word_frequencies = dict()

        self.load_report_files()

    def load_report_files(self):
        # TODO: test
        try:
            with open(REPORT_LONGEST, 'r') as f:
                url = f.readline().trim()
                word_count = int(f.readline())
                self.longest_page = {"url": url, "word_count": word_count}
            with open(REPORT_WORD_FREQ, 'r') as f:
                for line in f:
                    splitted = line.split()
                    self.word_Frequencies[splitted[0]] = int(splitted[1])
        except:
            print('[LOG] Report files not found, report progress is starting from zero')

    def write_report_files(self):
        # TODO: test
        with open(REPORT_LONGEST, 'w') as f:
            content = self.longest_page['url'] + '\n' + self.longest_page['word_count'] + '\n'
            f.write(content)
        with open(REPORT_WORD_FREQ, 'w') as f:
            # TODO: check performance
            content = ''
            for key, val in word_frequencies.items():
                content += key + ' ' + val + '\n'
            f.write(content)

    def update_report(self, url, page_text):
        # use soup.stripped_strings to get the text content of the page and count words w/ len()
            # if len(soup.stripped_strings) > self.longest_page["word_count"]:
            #     self.longest_page["url"] = url
            #     self.longest_page["word_count"] = len(soup.stripped_strings)
        # use tokenizer to get word frequencies
        page_frequencies = tokenize(page_text)
        page_word_count = sum(page_frequencies.values())

        if page_word_count > self.longest_page['word_count']:
            self.longest_page['url'] = url
            self.longest_page['word_count'] = page_word_count
        self.word_frequencies = merge_with_input(self.word_frequencies, page_frequencies)

        self.write_report_files()
