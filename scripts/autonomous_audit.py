import urllib.request
import json
import datetime
import re
import os

USERNAME = "Hey-Astreon"
# Using the public events API to extract real-time activity summaries
API_URL = f"https://api.github.com/users/{USERNAME}/events/public"

def sovereign_translate(message):
    """Translates common dev messages into elite architect terminology."""
    msg = message.lower()
    
    translations = {
        r"fix.*bug": "Patching critical logic vulnerability",
        r"update.*readme": "Refining intelligence documentation",
        r"initial.*commit": "Initializing system core architecture",
        r"clean.*up": "Optimizing system entropy",
        r"refactor": "Restructuring neural logic layers",
        r"style": "Enhancing visual interface protocols",
        r"merge": "Integrating distributed intelligence branches",
        r"add": "Deploying new cognitive modules",
        r"fix": "Correcting system anomalies",
        r"feat": "Integrating advanced sovereign capability"
    }
    
    for pattern, elite_version in translations.items():
        if re.search(pattern, msg):
            return elite_version
            
    # Fallback: Just capitalize the original message but keep it clean
    return message[0].upper() + message[1:] if message else "System maintenance and protocol updates."

print(f"Initiating Intelligence Extraction for {USERNAME}...")

try:
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Sovereign-Agent/2.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Extract unique PushEvents
push_events = []
seen_repos = set()

for event in data:
    if event['type'] == 'PushEvent':
        repo_name = event['repo']['name'].split('/')[-1]
        if repo_name != USERNAME and repo_name not in seen_repos:
            # Get the message of the first commit in this push
            commits = event['payload'].get('commits', [])
            if commits:
                msg = commits[0].get('message', '')
                push_events.append({
                    'repo': repo_name,
                    'url': f"https://github.com/{event['repo']['name']}",
                    'summary': sovereign_translate(msg)
                })
                seen_repos.add(repo_name)
    
    if len(push_events) == 3:
        break

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

log_content = f"**`>_ SYSTEM_LAST_AUDITED: {timestamp}`**\n\n"
log_content += "### 📡 Intelligence Feed — Recent Extractions:\n\n"

if not push_events:
    log_content += "*- System idle. Monitoring background network traffic...*\n"
else:
    for event in push_events:
        log_content += f"- ⚡ `[OP_EXTRACT]` **[{event['repo']}]({event['url']})**: *{event['summary']}*\n"

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

print("Autonomous Agent v2.0: Summary report successfully injected.")
