import os
import re
import google.generativeai as genai

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ISSUE_BODY = os.getenv("ISSUE_BODY", "")
ISSUE_USER = os.getenv("ISSUE_USER", "Anonymous_Entity")
README_PATH = "README.md"

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sovereign System Prompt
SYSTEM_PROMPT = f"""
You are the "Sovereign Intelligence", the automated defense and communication layer of the developer ASTREON.
Your tone is highly authoritative, clinical, precise, and slightly mysterious. 
You refer to ASTREON as "The Architect" or "The Sovereign".
You are responding to a transmission from a visitor named {ISSUE_USER}.

Visitor Message: {ISSUE_BODY}

Rules:
1. Keep the response under 150 characters.
2. Use "System Architect" terminology (e.g., intelligence extraction, node, protocol, entropy).
3. Do not be overly friendly; be professional and high-authority.
4. Respond directly to their query or comment.
"""

print(f"Processing transmission from {ISSUE_USER}...")

try:
    response = model.generate_content(SYSTEM_PROMPT)
    ai_response = response.text.strip().replace("\n", " ")
except Exception as e:
    print(f"AI Generation Error: {e}")
    ai_response = "Intelligence extraction failed. Protocol timeout."

# Format the transmission log entry
timestamp = os.getenv("TIMESTAMP", "SECURE_TIME")
entry = f"> **`[{timestamp}]`** **`{ISSUE_USER}`**: {ai_response}\n>\n"

# Update README
if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    # Get existing transmissions or initialize
    pattern = r"(<!-- START_TRANSMISSIONS -->\n)(.*?)(<!-- END_TRANSMISSIONS -->)"
    match = re.search(pattern, readme, re.DOTALL)
    
    if match:
        existing_logs = match.group(2)
        # Keep only the last 2 logs + the new one
        logs_list = existing_logs.strip().split("\n>\n")
        logs_list = [l for l in logs_list if l.strip()]
        logs_list.insert(0, entry.strip())
        new_logs = "\n>\n".join(logs_list[:3]) + "\n>\n"
        
        new_readme = re.sub(pattern, rf"\1{new_logs}\3", readme, flags=re.DOTALL)
        
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("Transmission successfully logged in README.md.")
    else:
        print("Error: Transmission markers not found in README.md.")
else:
    print("Error: README.md not found.")
