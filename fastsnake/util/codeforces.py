from bs4 import BeautifulSoup
import os
import requests


def get_contest_problems(contest_id: int):
    url = f"https://codeforces.com/contest/{contest_id}"

    response = requests.get(url)
    problems = []

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="problems")

    for problem in table.find_all("tr")[1:]:

        problem = problem.find("td").find("a")
        data = problem.text.strip().strip("\n")

        problems.append(data)

    return problems


def get_contest_problem_test_cases(contest_id: int, problem: str):
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem}"

    response = requests.get(url)
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
