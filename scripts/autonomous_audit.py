import urllib.request
import json
import datetime
import re
import os

USERNAME = "Hey-Astreon"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc&per_page=10"

print(f"Fetching latest operations for {USERNAME}...")

try:
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Sovereign-Agent/1.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

recent_repos = []
for repo in data:
    if repo['name'] != USERNAME and not repo['fork']:
        recent_repos.append(repo)
    if len(recent_repos) == 3:
        break

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

log_content = f"**`>_ SYSTEM_LAST_AUDITED: {timestamp}`**\n\n"
log_content += "### 📡 Recent Network Operations:\n\n"

for repo in recent_repos:
    name = repo['name']
    url = repo['html_url']
    desc = repo['description'] or "System maintenance and protocol updates."
    log_content += f"- ⚡ `[OP_UPDATE]` **[{name}]({url})** - *{desc}*\n"

readme_path = "README.md"
if not os.path.exists(readme_path):
    print("README.md not found!")
    exit(1)

with open(readme_path, "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"(<!-- START_AUDIT_LOG -->\n).*?(\n<!-- END_AUDIT_LOG -->)"
new_readme = re.sub(pattern, rf"\1{log_content}\2", readme, flags=re.DOTALL)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("System audit log injected into README.md successfully.")
