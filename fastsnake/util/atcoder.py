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


def get_problems(id_: str, namespace: str = "contests") -> List[str]:
    url = f"https://atcoder.jp/{namespace}/{id_}/tasks"

    response = requests.get(url, headers=headers)

    if response.status_code >= 300:
        raise ValueError(f"{namespace.capitalize()} not found. Status Code: {response.status_code}")

    problems = []

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("tbody")

    if not table:
        raise ValueError(f"{namespace.capitalize()} not found")

    for problem in table.find_all("tr"):
        problem = problem.find("td").find("a")
        data = problem.text.strip().strip("\n").strip("\r")

        problems.append(data)

    return problems


def get_problem_test_cases(id_: str, problem: str, namespace: str = "contests") -> Tuple[List[str], List[str]]:
    url = f"https://atcoder.jp/{namespace}/{id_}/tasks/{id_}_{problem.lower()}"

    response = requests.get(url, headers=headers)
    inputs, outputs = [], []

    if response.status_code >= 300:
        raise ValueError(f"Problem {id_}_{problem.lower()} not found. Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    contest = soup.find("div", {"id": "task-statement"})

    if not contest:
        raise ValueError(f"Problem {id_}_{problem.lower()} not found.")
    
    contest = contest.find("span", class_="lang-en")

    input_turn = True

    for box in contest.find_all("div", class_="part"):        
        if "sample" not in box.find("section").find("h3").text.lower():
            continue

        string = box.find("pre").text.replace("\r", "")
        
        if input_turn: inputs.append(string)
        else: outputs.append(string)
            
        input_turn = not input_turn

    return inputs, outputs