from utils.tokenize import tokenize, merge_with_input, simhash_tokens, hamming_distance

REPORT_LONGEST = "Logs/report_longest_page.txt";
REPORT_WORD_FREQ = "Logs/report_word_frequencies.txt";
REPORT_HASHES = "Logs/report_hashes.txt";

SIMHASH_HAMMING_THRESHOLD_PERCENT = 0.95 # edit this to change the threshold; default is 95% similarity b/t pages
SIMHASH_HAMMING_THRESHOLD_RAW = round(64 * (1 - SIMHASH_HAMMING_THRESHOLD_PERCENT)) # don't touch this! calculated value

"""
Handles reading/writing files for report contents (longest page and word frequencies)
Does NOT keep track of unique URLs or the number of subdomains, as those can be
obtained from Logs/Worker.log by scripts/GenerateReport.py
"""
class Report:
    def __init__(self):
        self.longest_page = {"url": "", "word_count": 0}
        self.word_frequencies = dict()
        self.hashes = set()

        self.load_report_files()

    def load_report_files(self):
        try:
            with open(REPORT_LONGEST, 'r') as f:
                url = f.readline().strip()
                word_count = int(f.readline())
                self.longest_page = {"url": url, "word_count": word_count}
            with open(REPORT_WORD_FREQ, 'r') as f:
                for line in f:
                    splitted = line.split()
                    self.word_frequencies[splitted[0]] = int(splitted[1])
            with open(REPORT_HASHES, 'r') as f:
                for line in f:
                    self.hashes.add(int(line.strip()))
        except:
            print('[LOG] Report files not found, report progress is starting from zero')

    def write_report_files(self):
        with open(REPORT_LONGEST, 'w') as f:
            content = self.longest_page['url'] + '\n' + str(self.longest_page['word_count']) + '\n'
            f.write(content)
        with open(REPORT_WORD_FREQ, 'w') as f:
            content = ''
            for key, val in self.word_frequencies.items():
                content += key + ' ' + str(val) + '\n'
            f.write(content)
        with open(REPORT_HASHES, 'w') as f:
            content = ''
            for h in self.hashes:
                content += str(h) + '\n'
            f.write(content)

    def update_report(self, url, page_text):
        page_frequencies = tokenize(page_text)
        page_word_count = sum(page_frequencies.values())

        if page_word_count > self.longest_page['word_count']:
            self.longest_page['url'] = url
            self.longest_page['word_count'] = page_word_count
        self.word_frequencies = merge_with_input(self.word_frequencies, page_frequencies)

        self.write_report_files()

    def is_duplicate(self, content):
        tokens = tokenize(content)
        fingerprint = simhash_tokens(tokens)

        for previous in self.hashes:
            if hamming_distance(previous, fingerprint) <= SIMHASH_HAMMING_THRESHOLD_RAW:
                return True

        self.hashes.add(fingerprint)
        return False
