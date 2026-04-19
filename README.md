# Vunoh Global — AI Diaspora Assistant

An AI-powered platform that helps Kenyans living abroad initiate and track services back home — including money transfers, local service hiring, and document verification.

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Database:** SQLite (development)
- **AI:** Google Gemini API (gemini-2.5-flash)

## Features
- Customer request input via chat interface
- AI intent extraction using Gemini
- Risk scoring engine with custom rules
- Task creation and database persistence
- 3-format message generation (WhatsApp, Email, SMS)
- Employee team assignment
- Task dashboard with live status updates
- Seed data with 5 sample tasks

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/osena1804/vunoh_ai_assistant.git
cd vunoh_ai_assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_django_secret_key

### 4. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

### 5. Visit the app
- Chat interface: http://127.0.0.1:8000
- Dashboard: http://127.0.0.1:8000/dashboard
- Admin panel: http://127.0.0.1:8000/admin

## Decisions I Made and Why

### AI tools used
I used Claude throughout this project for planning, code generation, and debugging. Claude helped me design the folder structure, write the Django models, and debug errors like the SECRET_KEY issue and the .env Git tracking problem. Gemini was used as the runtime AI brain that processes customer requests.

### How I designed the system prompt
I designed the system prompt to be strict and output-focused only. The most important decision was telling Gemini to return ONLY a JSON object with no markdown, no explanation, and no code fences. This is because the first version of the prompt returned markdown-wrapped JSON which broke the parser. I added a strip function to handle cases where Gemini still adds fences, but the prompt itself now explicitly forbids them.

I included specific step templates for each intent (send_money, hire_service, verify_document, airport_transfer) so the steps are always relevant and not generic. I also forced the urgency field to always be set based on keywords in the message.

### One decision where I changed what the AI suggested
Claude initially suggested using OpenAI for the AI brain. I decided to use Google Gemini instead because it has a genuinely free tier that does not require a credit card, which is more practical for an internship project and for other developers who want to run this locally. I also switched the model from gemini-1.5-flash to gemini-2.5-flash after discovering the older model was deprecated.

### One thing that did not work as expected
The .env file kept getting committed even after I added it to .gitignore. I knew the basics of secret management, but I didn’t realize GitHub blocks pushes if a secret appears anywhere in the commit history. Once a secret is committed, Git keeps tracking it unless the history is rewritten.

In my case, the simplest fix was to delete the entire repository and start fresh, instead of trying to clean the history. This taught me two key lessons:

.gitignore only prevents new files from being tracked but doesn’t erase past commits.

Secret management isn’t just about ignoring files; it’s also about cleaning history when something sensitive slips in.

## Sample Data
The file `sample_data.json` contains 18 tasks exported from the database including the 5 seeded sample tasks covering all intents: send_money, verify_document, hire_service, and airport_transfer.

## Database Schema
Four tables:
- **Task** — core record with intent, entities, risk score, status, and team assignment
- **TaskStep** — ordered steps to fulfil each task
- **TaskMessage** — WhatsApp, Email, and SMS confirmations per task
- **StatusHistory** — audit trail of every status change