import random
import time
from git import Repo
import os

remote_url = os.getenv('HTTPS_REMOTE_URL')
print(remote_url)

# Opens the fortunes file and reads a random line
with open('./fortunes.cookie', encoding='utf-8') as f:
    lines = f.readlines()

random_line_number = random.randint(2, len(lines) - 1)
fortune = lines[random_line_number]
print('Today fortune is: ' + fortune)

# Replace the fortune cookie sentence in the README
with open('../README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('> '):
        lines[i] = '> 🥠 ' + fortune
    elif line.startswith('Last update:'):
        lines[i] = 'Last update: ' + time.ctime()

with open('../README.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Commits the file
try:
    repo = Repo("..")
    repo.git.add(update=True)
    repo.index.commit("Updated cookie message")
    # origin = repo.remote(name='origin')
    remote = repo.create_remote("github", url=remote_url)
    remote.push(refspec='{}:{}'.format("master", "master"))
    # origin.push()
except Exception as e:
    print('Some error occured while pushing the code ' + e)

print("Updating")