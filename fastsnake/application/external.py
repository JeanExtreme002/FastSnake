import os
import requests


path = os.path.join(os.path.dirname(__file__), "..")


def add_external_module(module, name: str, is_url: bool = False) -> None:
    external_path = os.path.join(path, "external")
    content = ""

    name = name.lower().replace(".py", "")

    if is_url:
        response = requests.get(module)

        if response.status_code >= 300:
            return print(f"Received a {response.status_code} status code from the server.")
        
        content = response.text

    else:
        with open(module) as file:
            content = file.read()

    with open(os.path.join(external_path, name + ".py"), "w") as file:
        file.write(content)


def delete_external_module(name: str) -> None:
    name = name.lower().replace(".py", "")

    filename = os.path.join(path, "external", name + ".py")

    if os.path.exists(filename):
        os.remove(filename)