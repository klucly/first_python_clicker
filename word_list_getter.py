import requests

word_count = 10000

word_site = "https://www.mit.edu/~ecprice/wordlist.{}".format(word_count)

response = requests.get(word_site)
WORDS = response.content.splitlines()

for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].decode("utf-8")

with open("resources/word_list.json", "w") as file:
    file.write(str(WORDS).replace("'", '"'))

