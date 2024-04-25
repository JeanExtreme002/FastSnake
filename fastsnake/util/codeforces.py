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


def get_problems(id_: int, namespace: str = "contest") -> List[str]:
    url = f"https://codeforces.com/{namespace}/{id_}"

    response = requests.get(url, headers=headers)

    if response.status_code >= 300:
        raise ValueError(f"{namespace.capitalize()} not found. Status Code: {response.status_code}")

    problems = []

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="problems")

    if not table:
        raise ValueError(f"{namespace.capitalize()} not found")

    for problem in table.find_all("tr")[1:]:

        problem = problem.find("td").find("a")
        data = problem.text.strip().strip("\n")

        problems.append(data)

    return problems


def get_problem_test_cases(id_: int, problem: str, namespace: str = "contest") -> Tuple[List[str], List[str]]:
    url = f"https://codeforces.com/{namespace}/{id_}/problem/{problem}"

    response = requests.get(url, headers=headers)
    inputs, outputs = [], []

    if response.status_code >= 300:
        raise ValueError(f"{namespace.capitalize()} problem not found. Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")

    for input_data in soup.find_all("div", class_="input"):        
        pre = input_data.find("pre")

        if not pre: continue
        
        divs = pre.find_all("div")

        if divs:
            string = "\n".join(data.text for data in divs)
        else: 
            brs = pre.find_all("br")

            if brs:
                string = "\n".join([list(br.previous_siblings)[0] for br in brs])
            else:
                string = pre.text

        inputs.append(string)

    for output_data in soup.find_all("div", class_="output"):
        pre = output_data.find("pre")
        
        if pre:
            outputs.append(pre.text)

    return inputs, outputs