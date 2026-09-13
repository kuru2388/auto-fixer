import os
from google import genai
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Initialize the new Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_code_fix(ticket_title, error_message, dom_html):
    """
    Sends the bug context and the raw HTML to Gemini for diagnosis.
    """
    print("🧠 Sending data to Gemini for diagnosis...")
    
    prompt = f"""
    You are an elite Next.js developer debugging a web application.
    
    Bug Ticket Title: {ticket_title}
    Automated QA Error: {error_message}
    
    Here is the raw HTML DOM of the page where the error occurred:
    {dom_html[:80000]} 
    
    The Playwright automation failed to click the 'Pay Now' button. This is usually caused by an invisible overlay (like a div with a high z-index) blocking the UI.
    
    Please analyze the HTML, locate the exact CSS classes (like Tailwind) causing this issue, and explain how to fix it in 2-3 short sentences.
    """
    
    try:
        # Using the requested 3.6-flash model and Chat API to clear the warning
        chat = client.chats.create(model='gemini-3.6-flash')
        response = chat.send_message(prompt)
        return response.text
        
    except Exception as e:
        return f"AI Error: {str(e)}"

# Quick test block to run this file on its own
if __name__ == "__main__":
    print("Testing AI Brain (Gemini 3.6 Edition)...")
    
    # Fake data to test the API connection
    test_title = "Pay button blocked"
    test_error = "Page.click: Timeout 3000ms exceeded."
    test_html = '<div class="absolute inset-0 z-50"></div> <button>Pay Now</button>'
    
    answer = generate_code_fix(test_title, test_error, test_html)
    
    print("\n--- AI Diagnosis ---")
    print(answer)