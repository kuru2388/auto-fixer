from playwright.sync_api import sync_playwright

def test_ui_and_get_dom(url="http://localhost:3000"):
    """
    Simulates a human trying to click the 'Pay Now' button.
    When the z-50 bug blocks the click, it captures the page HTML.
    """
    print(f"🕵️ Starting UI investigation on {url}...")
    
    with sync_playwright() as p:
        # Launch Chromium in the background
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url)
            # Wait for the page to fully load
            page.wait_for_load_state("networkidle")
            
            print("🖱️ Attempting to click the 'Pay Now' button...")
            # We give it a strict 3-second timeout. If the overlay blocks it, this will throw an error!
            page.click("text=Pay Now", timeout=3000)
            
            print("❌ Click succeeded! (Wait, the bug is missing...)")
            return None, "No bug detected. Click went through."
            
        except Exception as e:
            print("✅ Bug detected! Click was intercepted. Capturing DOM...")
            # Grab the full HTML of the page so OpenAI can read it later
            html_content = page.content()
            error_message = str(e)
            return html_content, error_message
            
        finally:
            browser.close()

# Quick test block to run this file on its own
if __name__ == "__main__":
    html, error = test_ui_and_get_dom()
    if html:
        print(f"\n--- Results ---")
        print(f"Error caught: {error.splitlines()[0]}") # Print just the first line of the error
        print(f"HTML characters extracted: {len(html)}")