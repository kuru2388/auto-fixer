import os
import re
import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Import our custom modules from Phases 2, 3, and 4
from vision import test_ui_and_get_dom
from ai import generate_code_fix
from github_agent import push_and_create_pr

# Load environment variables
load_dotenv()

# Initialize Slack App
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")

def get_linear_ticket(ticket_id):
    """Fetches ticket details from Linear API using GraphQL"""
    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json"
    }
    query = """
    query Issue($id: String!) {
      issue(id: $id) {
        identifier
        title
        description
      }
    }
    """
    response = requests.post(url, json={"query": query, "variables": {"id": ticket_id}}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']['issue']:
            return data['data']['issue']
    return None

# Listen for messages like "!fix AUT-5"
@app.message(re.compile(r"^!fix ([A-Za-z]+-\d+)"))
def handle_fix_command(message, say, context):
    ticket_id = context['matches'][0].upper()
    user = message['user']
    
    say(f"🤖 Hey <@{user}>! Agent activated. Processing ticket *{ticket_id}*...")
    
    # Step 1: Fetch from Linear
    ticket = get_linear_ticket(ticket_id)
    if not ticket:
        say(f"❌ Could not find ticket {ticket_id} in Linear.")
        return
    
    title = ticket.get('title')
    desc = ticket.get('description', 'No description provided')
    say(f"✅ *Ticket Acquired:* {title}\n_Step 1/3: Running Playwright UI inspection..._")
    
    # Step 2: Playwright QA Inspection
    dom_html, error_msg = test_ui_and_get_dom("http://localhost:3000")
    if not dom_html:
        say(f"⚠️ UI check passed with no errors. No fix needed!")
        return
        
    say(f"🔍 _Step 2/3: Bug isolated! Sending DOM to Gemini AI for diagnosis..._")
    
    # Step 3: Gemini AI Diagnosis
    diagnosis = generate_code_fix(title, error_msg, dom_html)
    say(f"🧠 *AI Diagnosis Complete!*\n```{diagnosis[:300]}...```\n_Step 3/3: Pushing code fix & opening Pull Request..._")
    
    # Step 4: GitHub Automation & PR
    pr_url = push_and_create_pr(ticket_id, diagnosis)
    
    if pr_url:
        say(f"🚀 *Mission Accomplished!* Auto-fix Pull Request successfully created:\n{pr_url}")
    else:
        say(f"⚠️ Diagnosis complete, but automatic GitHub push failed. Check terminal logs.")

if __name__ == "__main__":
    print("🚀 Auto-Fixer Autonomous Agent is fully online and listening in Slack...")
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()