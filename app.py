from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Portfolio Data
PORTFOLIO_DATA = {
    "name": "Nived VC",
    "tagline": "Python Developer | Web Scraping & Automation Specialist",
    "summary": "Senior Python Developer with 3 years of experience specializing in web scraping, large-scale data extraction, anti-bot bypassing, and automation. Proven expertise in building scalable crawlers, reverse-engineering complex websites, and optimizing data pipelines.",
    "contact": {
        "email": "vcnived@gmail.com",
        "phone": "+9400501368",
        "location": "Kochi, Kerala",
        "linkedin": "https://linkedin.com/in/nived-vc",
        "github": "https://github.com/nivedvc"
    },
    "skills": {
        "Languages & Libraries": ["Python", "Pandas", "Playwright", "Requests", "curl_cffi", "lxml", "Flask"],
        "Web Scraping & Automation": ["Web Scraping", "Anti-Bot Bypassing", "CAPTCHA Handling", "Reverse Engineering", "XPath", "Regex"],
        "Tools & Platforms": ["Git", "GitLab CI/CD", "Jira", "PyCharm", "Sentry", "Graylog"],
        "Data & Storage": ["SQL", "CSV", "JSON", "XLSX", "ETL Pipelines", "Elasticsearch", "Redis"]
    },
    "experience": [
        {
            "company": "HCLTech",
            "role": "Senior Python Developer",
            "period": "Oct 2025 – Present",
            "highlights": [
                "Develop high-quality Python automation and scraping solutions for media metadata.",
                "Build structured datasets for identifying illegal content distribution.",
                "Handle complex anti-bot ecosystems including CAPTCHA and browser fingerprinting.",
                "Implement advanced bypass strategies using browser automation and proxy rotation.",
                "Design modular, class-based scraping frameworks for scalability."
            ]
        },
        {
            "company": "Turbolab Technologies",
            "role": "Python Developer",
            "period": "Apr 2023 – Sep 2025",
            "highlights": [
                "Maintained 60+ web crawlers for large-scale data extraction.",
                "Built reusable parser modules to standardize scraping workflows.",
                "Improved spider efficiency by converting browser-based crawlers to request-based systems.",
                "Collaborated on configuration-driven scraping frameworks."
            ]
        },
        {
            "company": "SFO Technologies",
            "role": "Process Engineer",
            "period": "Apr 2019 – Nov 2022",
            "highlights": [
                "Conducted FMEA analysis to identify production risks.",
                "Led Kaizen initiatives to improve manufacturing efficiency.",
                "Designed visual work instructions for shop-floor productivity."
            ]
        }
    ],
    "projects": [
        {
            "title": "Job Search Web App",
            "tech": "Flask | Python | SQLite",
            "description": "Built a Flask web application that aggregates job listings based on keywords. Implemented scraping with proxy handling and anti-bot bypass.",
            "link": "https://github.com/nivedvc/job_search_project"
        }
    ],
    "education": [
        {
            "degree": "BTech — Mechanical Engineering",
            "institution": "Cochin University of Science and Technology",
            "year": "2018 - CGPA 7.85"
        },
        {
            "degree": "Plus Two — Computer Science",
            "institution": "GHSS Kuthuparamba",
            "year": "2014 - 90%"
        }
    ],
    "certifications": [
        "GenAI Course — Convai (2025)",
        "Python Certification — HackerRank",
        "Best Employee Award — SFO Technologies (2021)"
    ]
}

# System Prompt for AI Assistant
SYSTEM_PROMPT = """You are an AI assistant for Nived's portfolio website. 
Answer questions about his skills, experience, and projects.

About Nived:
- Python developer with 2+ years experience
- Expertise in web scraping
- Antibot bypass techniques (CAPTCHA, browser fingerprinting)
- Automation using Python (Playwright, Requests, Pandas)
- Data processing and ETL pipelines
- Cloud experience with AWS

If users ask unrelated questions, politely redirect them to topics about Nived's work. 
Keep responses concise and professional."""

@app.route('/')
def index():
    return render_template('index.html', data=PORTFOLIO_DATA)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            config={
                'system_instruction': SYSTEM_PROMPT,
            },
            contents=[user_message]
        )
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"response": "I'm sorry, I'm having trouble connecting right now. Please try again later."}), 500

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # In a real app, you might send an email or save to a database here.
    # For now, we'll just flash a success message.
    flash(f"Thank you, {name}! Your message has been received.", "success")
    return redirect(url_for('index', _anchor='contact'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Using 5001 to avoid potential conflicts
