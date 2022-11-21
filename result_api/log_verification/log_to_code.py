import logging
import requests
import urllib
import json

from fuzzywuzzy import fuzz

logger = logging.getLogger("logsight." + __name__)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def log_to_code(log, repository, github_token):
    query = f"{urllib.parse.quote(log)}+in:file+repo:{repository}"
    response = requests.get(f'https://api.github.com/search/code?q={query}',
                            auth=BearerAuth(github_token))
    try:
        file_url = json.loads(response.content)["items"][0]["html_url"]
        file_url_raw = json.loads(response.content)["items"][0]["html_url"] \
            .replace("/blob", "") \
            .replace("https://github.com", "https://raw.githubusercontent.com")
        file_content = requests.get(file_url_raw)
        return file_url + f"#L{str(find_log_in_file(file_content))}"
    except Exception:
        return None
        pass


def find_log_in_file(file_content):
    max_ratio = 0
    max_ratio_line_number = 1
    for i, line in enumerate(str(file_content.content).split("\\n")):
        fuzz_ratio = fuzz.partial_ratio(''.join(item for item in line if item.isalnum()),
                                        ''.join(item for item in log if item.isalnum()))
        if max_ratio < fuzz_ratio:
            max_ratio = fuzz_ratio
            max_ratio_line_number = i + 1
    return max_ratio_line_number
