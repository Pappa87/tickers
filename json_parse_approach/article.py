import json
import sys

class Article:
    def __init__(self, subreddit_id, title, text, author, score, created_utc, comments):
        self.subreddit_id = subreddit_id
        self.title = title
        self.text = text
        self.author = author
        self.score = score
        self.created_utc = created_utc
        if comments is None:
            self.comments = []
        else:
            self.comments = comments

    def add_comments(self, comments):
        self.comments.extend(comments)

    def __str__(self):
        return (
            f"subreddit_id: {self.subreddit_id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Score: {self.score}\n"
            f"Upvotes: {self.ups}\n"
            f"Created UTC: {self.created_utc}\n"
            f"Text: {self.text[0:300]}\n"
            f"comments num: {len(self.comments)}"
        )

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "subreddit_id": self.subreddit_id,
            "title": self.title,
            "text": self.text,
            "author": self.author,
            "score": self.score,
            "created_utc": self.created_utc,
            "comments": [comment.to_dict() for comment in self.comments],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def parse_article(article_data_raw):
        subreddit_id = article_data_raw['subreddit_id']
        title = article_data_raw["title"]
        text = remove_empty_lines(article_data_raw["selftext"])
        author = article_data_raw["author"]
        score = article_data_raw["score"]
        created_utc = article_data_raw["created_utc"]
        comments = None
        article = Article(subreddit_id, title, text, author, score, created_utc, comments)
        return article

class Comment:
    def __init__(self, author, text, score, created_utc, sub_comments):
        self.author = author
        self.text = text
        self.score = score
        self.created_utc = created_utc
        if sub_comments is None:
            self.sub_comments = []
        else:
            self.sub_comments = sub_comments

    def __str__(self):
        return (
            f"\n"
            f"Author: {self.author}\n"
            f"Text: {self.text}\n"
            f"Score: {self.score}\n"
            f"Created UTC: {self.created_utc}\n"
            f"Upvotes: {self.ups}\n"
            f"sub comments num: {len(self.sub_comments)}\n"
        )

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "author": self.author,
            "text": self.text,
            "score": self.score,
            "created_utc": self.created_utc,
            "sub_comments": [comment.to_dict() for comment in self.sub_comments],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def parse_comments(comment_raw):
        parsed_comments = []
        for comment in comment_raw:
            comment_data = comment["data"]

            if "author" not in comment_data:
                continue

            author = comment_data["author"]
            text = remove_empty_lines(comment_data["body"])
            score = comment_data["score"]
            created_utc = comment_data["created_utc"]

            if "replies" in comment_data.keys() and type(comment_data["replies"]) == dict:
                sub_comments = Comment.parse_comments(comment_data["replies"]["data"]["children"])
            else:
                sub_comments = []

            parsed_comment = Comment(author, text, score, created_utc, sub_comments)
            parsed_comments.append(parsed_comment)
        return parsed_comments


def remove_empty_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())