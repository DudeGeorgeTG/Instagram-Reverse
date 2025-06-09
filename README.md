📸 Instagram Headers Generator (Reverse Engineered)
A Python script that simulates browser-like HTTP headers and cookies to mimic authentic Instagram requests — ideal for automation, scraping, or research use cases.

✨ Features
✅ Automatically generates realistic Instagram headers
✅ Parses CSRF token, device ID, app ID, and rollout hash
✅ Dynamically constructs Instagram's required cookies
✅ Random User-Agent and X-Mid values per session
✅ Built with simplicity and readability in mind

📦 Requirements
Install the dependencies using pip:

bash
Copy
Edit
pip install requests user_agent
🧠 How It Works
Generate a User-Agent
Mimics a real browser using the user_agent library.

Fetch Initial Cookie (_js_datr)
Sent by Instagram when visiting the email signup page.

Scrape Tokens from Homepage
Parses out the following values from the homepage HTML:

csrf_token

device_id

appID

rollout_hash

Generate Headers & Cookies
Combines the scraped values into fully-formed HTTP headers including:

X-CSRFToken

X-IG-App-ID

X-Web-Device-ID

X-Instagram-AJAX

Cookie (with CSRF, device ID, etc.)

🧪 Usage
🔹 As a script
bash
Copy
Edit
python instagram_headers.py
🔹 As a module
python
Copy
Edit
from instagram_headers import get_headers

headers = get_headers()
print(headers)
📤 Example Output
text
Copy
Edit
X-Mid: 2xk0z5gwn1q3h7z9o3byx9uv5qz0uv5b
X-CSRFToken: uL9vOkRtjv8kFz0PvqJ1zKFxQW9VhKZs
X-IG-App-ID: 936619743392459
X-Web-Device-ID: 36d8e1a4-2c7d-4a63-9187-f26366de5ac3
X-Instagram-AJAX: 1007682309
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
Cookie: csrftoken=...; datr=...; mid=...; ig_did=...
📁 Project Structure
bash
Copy
Edit
📂 instagram_headers/
├── instagram_headers.py    # Main script to generate headers
└── README.md               # Documentation
⚠️ Disclaimer
This tool is for educational and research purposes only.
Automated interaction with Instagram may violate their Terms of Service. Use responsibly and at your own risk.

📝 License
MIT License — use freely, with attribution.
