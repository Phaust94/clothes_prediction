import json

file_addr = "C:/Users/user/Downloads/city.list.json"
with open(file_addr, "r", encoding="utf-8") as file:
    lines = file.readlines()
json_file = json.loads("".join(lines))
kha = [el for el in json_file if el["name"] == 'Kharkiv']
print(kha)
