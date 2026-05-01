#!/bin/bash

# Clean up the file logs for restarting the crawler. Run from project root
rm frontier.shelve
rm Logs/Worker.log
rm Logs/report_hashes.txt
rm Logs/report_longest_page.txt
rm Logs/report_word_frequencies.txt
rm Logs/debug_log.txt
ls
ls Logs
