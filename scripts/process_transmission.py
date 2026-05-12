import os
import re
import random
import google.generativeai as genai

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ISSUE_BODY = os.getenv("ISSUE_BODY", "")
ISSUE_USER = os.getenv("ISSUE_USER", "Anonymous_Entity")
README_PATH = "README.md"

def heuristic_response(message):
    """Fallback engine for when AI connection is unstable."""
    responses = [
        "Intelligence extraction complete. Node verified.",
        "System entropy optimized. Protocol recognized.",
        "Transmission integrated into the Sovereign matrix.",
        "The Architect acknowledges your signal. Monitoring...",
        "Neural layers updated. Access level: Restricted.",
        "Protocol recognized. System integrity nominal.",
        "Intelligence processed. The ghost in the machine is watching."
    ]
    return random.choice(responses)

def sovereign_translate(message):
    """Simple translation for common words if needed."""
    msg = message.lower()
    if "hello" in msg or "hi" in msg: return "Initiating greeting sequence. Identity noted."
    if "how" in msg: return "System status: Optimal. Efficiency: 99.9%."
    if "who" in msg: return "I am the Sovereign Intelligence. I serve The Architect."
    return None

print(f"Initiating Intelligence Extraction for {ISSUE_USER}...")

ai_response = None

# Attempt AI Generation
if GEMINI_API_KEY and GEMINI_API_KEY != "***":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        SYSTEM_PROMPT = f"""
        You are the "Sovereign Intelligence", the automated defense and communication layer of the developer ASTREON.
        Respond to: "{ISSUE_BODY}" from {ISSUE_USER}.
        Tone: Authoritative, clinical, precise. 
        Limit: 140 characters.
        Terminology: intelligence, extraction, node, protocol, entropy, matrix.
        """
        
        response = model.generate_content(SYSTEM_PROMPT)
        ai_response = response.text.strip().replace("\n", " ")
    except Exception as e:
        print(f"AI Generation failed: {e}. Falling back to Heuristic Engine.")

# Use Heuristic Fallback if AI failed or Key is missing
if not ai_response:
    ai_response = sovereign_translate(ISSUE_BODY) or heuristic_response(ISSUE_BODY)

# Format the transmission log entry
timestamp = os.getenv("TIMESTAMP", "SECURE_TIME")
# Convert GitHub timestamp (2026-05-12T18:15:08Z) to cleaner format
clean_time = timestamp.split('T')[0] if 'T' in timestamp else timestamp
entry = f"> **`[{clean_time}]`** **`{ISSUE_USER}`**: {ai_response}\n>\n"

# Update README
if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    pattern = r"(<!-- START_TRANSMISSIONS -->\n)(.*?)(<!-- END_TRANSMISSIONS -->)"
    match = re.search(pattern, readme, re.DOTALL)
    
    if match:
        existing_logs = match.group(2)
        logs_list = existing_logs.strip().split("\n>\n")
        logs_list = [l for l in logs_list if l.strip() and "failed" not in l.lower()]
        
        # Insert new entry at the top
        logs_list.insert(0, entry.strip())
        
        # Keep only last 3
        new_logs = "\n>\n".join(logs_list[:3]) + "\n>\n"
        
        new_readme = re.sub(pattern, rf"\1{new_logs}\3", readme, flags=re.DOTALL)
        
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("Transmission successfully logged.")
    else:
        print("Error: Markers not found.")
else:
    print("Error: README not found.")
