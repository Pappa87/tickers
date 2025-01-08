import os
from ticker_downloader import get_tickers
import re
from collections import Counter
import ahocorasick

DOWNLOAD_FOLDER = "C:\\tmp\\ticker_test_data"


tickers = get_tickers()
automaton = ahocorasick.Automaton()
for idx, word in enumerate(tickers):
    automaton.add_word(word, (idx, word))
automaton.make_automaton()


def search_for_tickers(searchable_text):
    matches = []
    for end_index, (idx, word) in automaton.iter(searchable_text):
        matches.append(word)

    return matches

def list_subfolders(directory):
    return [f.path for f in os.scandir(directory) if f.is_dir()]


# reddit_text = """
# First trade of the year: 0dte SPY puts -99%
# """
# print(search_for_tickers(reddit_text))


word_lengths = [len(word) for word in tickers]
length_counts = Counter(word_lengths)
print("Word Length Counts:")
for length, count in sorted(length_counts.items()):
    print(f"Length {length}: {count} words")
