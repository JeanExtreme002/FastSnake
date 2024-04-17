from bs4 import BeautifulSoup
from typing import List, Tuple

import os
import requests

headers = {
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "Sec-Ch-Ua-Arch": "\"x86\"",
    "Sec-Ch-Ua-Bitness": "\"64\"",
    "Sec-Ch-Ua-Full-Version": "\"123.0.6312.123\"",
    "Sec-Ch-Ua-Full-Version-List": "\"Google Chrome\";v=\"123.0.6312.123\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.123\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": "\"\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


def get_contest_problems(contest_id: int) -> List[str]:
    url = f"https://codeforces.com/contest/{contest_id}"

    response = requests.get(url, headers=headers)
    problems = []

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="problems")

    for problem in table.find_all("tr")[1:]:

        problem = problem.find("td").find("a")
        data = problem.text.strip().strip("\n")

        problems.append(data)

    return problems


def get_contest_problem_test_cases(contest_id: int, problem: str) -> Tuple[List[str], List[str]]:
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem}"

    response = requests.get(url, headers=headers)
    inputs, outputs = [], []
    
    soup = BeautifulSoup(response.content, "html.parser")

    for input_data in soup.find_all("div", class_="input"):        
        pre = input_data.find("pre")

        string = "\n".join(data.text for data in pre.find_all("div"))
        inputs.append(string)

    for output_data in soup.find_all("div", class_="output"):
        pre = output_data.find("pre")
        outputs.append(pre.text)

    return inputs, outputs
