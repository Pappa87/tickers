from json_parse_approach.common import logger
import re
import json


class MatchReport:

    def __init__(self, json_path: str, cmpny_name_matches: dict, symbol_matches: dict):
        self.json_name = json_path.split("/")[-1]
        self.cmpny_name_matches = cmpny_name_matches
        self.symbol_matches = symbol_matches


def search_for_expression(searchable_text, expression):
    pattern = rf"(?:^|\W){re.escape(expression)}(?:\W|$)"
    return re.findall(pattern, searchable_text)


def simplify_ticker_name(name_of_ticker):
    if name_of_ticker.endswith("."):
        simplified_ticker = " ".join(name_of_ticker.split(" ")[:-1])
    else:
        simplified_ticker = name_of_ticker
    simplified_ticker = strip_edges(simplified_ticker)
    return simplified_ticker


def text_environment(file_path, search_word):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # Read all lines into a list

    line_matches = []
    for i, line in enumerate(lines):
        if search_word in line:
            line_matches.append(line)
    return line_matches


def strip_edges(text):
    # Regex to remove non-alphanumeric characters from the beginning and end
    stripped_text = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", "", text)
    return stripped_text


def extract_text_from_comment(comment):
    """
    Recursively extracts all 'text' values from a comment and its sub-comments.
    """
    texts = []
    if "text" in comment:
        texts.append(comment["text"])
    if "sub_comments" in comment:
        for sub_comment in comment["sub_comments"]:
            texts.extend(extract_text_from_comment(sub_comment))
    return texts


def extract_all_texts_from_json(json_data):
    """
    Extracts all 'text' values from the main post and all comments/sub-comments.
    """
    all_texts = []
    if "text" in json_data and json_data["text"]:  # Check if the main post has text
        all_texts.append(json_data["text"])
    if "comments" in json_data:
        for comment in json_data["comments"]:
            all_texts.extend(extract_text_from_comment(comment))
    return all_texts


def extract_texts_from_file(file_path):
    """
    Reads JSON data from a file and extracts all 'text' values.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
            json_data = json.load(file)
            text_list = extract_all_texts_from_json(json_data)
            return "\n".join(text_list)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        return []

