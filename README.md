# 🤖 Auto-Fixer: Autonomous Developer Agent

> An end-to-end autonomous engineering agent that bridges bug reports to verified Pull Requests through local environment code surgery, Playwright UI inspection, Gemini AI diagnostics, and seamless two-way Slack/Linear integration.

---

## 🎥 Demo Video
Watch our 2-minute submission demo video here:
[![Auto-Fixer Demo Video](https://img.shields.io/badge/Watch-Demo%20Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/naWmdTNIq_k)

---

## 🚀 What We Built
Auto-Fixer eliminates the friction of routine bug fixing and triage. When a bug report lands in Linear, our autonomous agent steps in to:
1. **Inspect the UI** locally using Playwright to isolate the bug and capture a failure state screenshot.
2. **Diagnose the Code** using Google Gemini AI to analyze the DOM, error logs, and issue description.
3. **Enforce Safety** via a Slack Interactive Block Kit workflow, pausing for human review before any code is modified.
4. **Execute Code Surgery** by automatically creating a Git branch, editing the local repository files, verifying the fix with post-repair snapshots, and pushing a GitHub Pull Request.
5. **Close the Loop** by posting a direct, two-way update comment back to the original Linear ticket.

---

## 🔌 External Apps & APIs Used
* **Linear API (GraphQL)**: Used for real-time ticket ingestion and automated two-way status commenting.
* **Slack Bolt (Socket Mode)**: Powers the developer interface, command listening (`!fix`), and interactive human-in-the-loop approval cards.
* **Google Gemini AI (via Google AI Studio)**: Analyzes runtime errors and DOM structure to formulate precise code fixes.
* **Playwright**: Drives local headless/headed browser sessions to audit `localhost:3000` and capture visual evidence (`before_bug.png`, `after_fix.png`).
* **GitHub API / Git Automation**: Handles clean branch creation, file staging, committing, and Pull Request generation.

---

## 🛡️ How We Tested Reliability
Building an autonomous agent that touches code requires strict safety guardrails. We ensured high reliability through:
* **Human-in-the-Loop Checkpoint**: The agent never pushes code or opens PRs blindly. It halts execution and presents an interactive Slack card requiring explicit human approval (`✅ Approve Fix & PR`).
* **Visual Regression Proofing**: Playwright captures automated snapshots before and after code modification to visually verify that the fix resolves the UI bug.
* **Fail-Safe Path Resolution**: Built-in fallback handlers ensure repository file paths map correctly even if component structures vary, preventing runtime crash exceptions during local execution.

---

## ⚙️ How to Run (Setup Instructions)

### Prerequisites
* Python 3.10+
* Node.js & npm (running your local frontend app, e.g., Next.js on `http://localhost:3000`)
* Git installed and configured locally
* A Slack App with Socket Mode enabled & a Linear API Workspace

### 1. Clone the Repository
```bash
git clone https://github.com/kuru2388/auto-fixer.git
cd auto-fixer
```

### 2. Create and Activate a Python Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add the following keys:

```env
# Slack App Level Token (Starts with xapp-)
SLACK_APP_TOKEN=

# Slack Bot Token (Starts with xoxb-)
SLACK_BOT_TOKEN=

# Linear API Key (Starts with lin_api_)
LINEAR_API_KEY=

# GitHub Fine-Grained Token
GITHUB_TOKEN=

# Google Gemini API Key
GEMINI_API_KEY=
```

### 5. Run the Agent
With your virtual environment activated:
```bash
python main.py
```
