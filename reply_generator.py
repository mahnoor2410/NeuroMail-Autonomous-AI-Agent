import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY") or "#######"
genai.configure(api_key=api_key)

# Use Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

SYSTEM_PROMPT = (
    "You are a professional email assistant. Produce concise, polite, business-appropriate replies. "
    "Follow the requested tone strictly (empathetic / polite / formal). Keep replies <= 5 sentences."
)

PROMPT_TEMPLATE = """Email subject:
{subject}

Email body:
{body}

Detected tone: {tone}

Write:
1) A concise reply matching the tone requested.
2) At the end add a one-line suggested next action (e.g., 'Propose 3 interview slots' or 'Escalate to support').
Return plain text only.
"""

def generate_reply(subject: str, body: str, tone: str) -> str:
    # Format the user prompt
    prompt = PROMPT_TEMPLATE.format(subject=subject or "", body=body or "", tone=tone)

    # Combine system + user prompt for Gemini
    full_prompt = SYSTEM_PROMPT + "\n\n" + prompt

    # Call Gemini
    response = model.generate_content(full_prompt)
    return response.text.strip()

# ✅ Test the reply generator
if __name__ == "__main__":
    r = generate_reply("Delay of order", "I am disappointed by the delay.", "empathetic")
    print("🤖 Suggested Reply:\n", r)
