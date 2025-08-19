# 📧 NeuroMail — Autonomous AI Email Agent

**NeuroMail** is an autonomous AI Email Agent powered by Google Gemini LLM. It intelligently manages your inbox by fetching unread emails, generating context-aware replies, and maintaining thread-safe, duplicate-free drafts. Designed for efficiency and professionalism, NeuroMail automates routine email tasks with cutting-edge AI.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

---

## Project Overview

Managing emails manually is time-consuming and repetitive. **NeuroMail** automates this process by fetching unread emails, detecting their tone, generating context-aware replies using Google Gemini, and either sending them directly or saving drafts safely. It is thread-aware and prevents duplicate drafts, making email management efficient and professional.

---

## Features

- 📧 **Email Fetching**: Retrieves latest unread emails from Gmail.
- 🧠 **Tone Detection**: Detects tone (empathetic, polite, formal) of incoming emails.
- 🤖 **AI-Powered Replies**: Generates concise, context-aware email responses.
- 📝 **Safe Draft Creation**: Creates drafts with duplicate-check to avoid multiple drafts for the same thread.
- ✉️ **Auto Send Option**: Replies can be sent automatically if enabled.
- 🧷 **Thread-Aware**: Maintains replies in the correct conversation thread.

---

## Tech Stack

- **Backend & AI**: Python
- **Email API**: Gmail API
- **LLM**: Google Gemini
- **Embeddings / AI Processing**: transformers, LangChain (optional)
- **Environment Management**: dotenv

---

## System Architecture

- **🔁 Email Fetching**:
  - Agent fetches latest unread emails.
  - Email body/snippet/subject used for tone detection.

- **🧠 Tone Detection & Reply Generation**:
  - Tone is detected using transformer-based sentiment analysis.
  - Google Gemini generates context-aware reply based on tone.

- **📝 Drafts & Auto-Sending**:
  - Draft created if `AUTO_SEND=False` with duplicate check via `threadId`.
  - Direct send occurs if `AUTO_SEND=True`.
  - All replies maintain conversation threads using Gmail `threadId`.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Gmail API credentials (`credentials.json`)
- Google Gemini API Key
- pip

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/neuromail-agent.git
cd neuromail-agent
```

2. **Create and Activate Virtual Environment**

```bash
python -m venv venv  

# Activate (Linux / Mac)
source venv/bin/activate  

# Activate (Windows - PowerShell)
venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
- Create a .env file in the project root
- Add your Gemini API key and auto-send preference. 

```bash
echo "GEMINI_API_KEY=your_google_gemini_api_key" >> .env
echo "AUTO_SEND=False" >> .env  # set True to auto-send emails
```

5. **Add Gmail API Credentials**
- Download credentials.json from Google Cloud Console (Gmail API enabled)
- Place it in the project root directory

6. **Run the Agent**

- This will fetch emails, detect tone, generate replies, and either create drafts or send them
```bash
python main.py
```
---

## Usage

By default, NeuroMail will:
1. Fetch unread emails (first batch = 10, subsequent batches = 5)
2. Detect tone (empathetic, polite, formal)
3. Generate a reply using Google Gemini
4. Either save as draft (AUTO_SEND=False) or send directly (AUTO_SEND=True)

All replies maintain conversation threads using Gmail threadId

---

## Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes.
4. Push to your branch: `git push origin feature/your-feature`.
5. Submit a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## Authors

- Mahnoor Shahid

---

## Acknowledgments

- Google for Gmail API & Gemini
- HuggingFace for Transformers
- Open-source community 🚀

