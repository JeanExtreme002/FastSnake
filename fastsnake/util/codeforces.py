from bs4 import BeautifulSoup
import os
import requests


def get_contest_problem(contest_id: int, problem: str = "A"):
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
