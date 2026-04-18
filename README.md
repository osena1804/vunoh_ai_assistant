# Vunoh Global AI Assistant

An AI-powered web application designed to help Kenyans living abroad manage important tasks back home with transparency and a clear audit trail.

## 🌟 The Problem
Diaspora customers often rely on informal channels like phone calls or WhatsApp, which are slow, unreliable, and leave no digital record. This project provides a structured, intelligent assistant to bridge that gap.

## 🛠️ Core Services
* **💸 Remittance Management:** Initiate and track transfers securely.
* **🧑‍💼 Service Marketplace:** Connect with verified cleaners, lawyers, or errand runners.
* **📑 Document Verification:** Validate land titles, IDs, and certificates through official channels.

## 🚀 Project Roadmap & Progress
- [x] **Day 1: Foundation & Data Architecture** - Setup Django project and `assistant` app.
    - Designed and migrated a 4-table normalized database (Tasks, Steps, Messages, Status History).
    - Configured Admin Dashboard for manual oversight.
- [ ] **Day 2: AI Intent Recognition**
    - Integrate Gemini API to extract intents and entities from user messages.
- [ ] **Day 3: Risk Scoring & Task Logic**
    - Implement automated risk assessment and task assignment.
- [ ] **Day 4: Multi-channel Communication**
    - Integration with WhatsApp/SMS/Email simulation.

## 💻 Tech Stack
* **Backend:** Python (Django)
* **Database:** SQLite (Development) / PostgreSQL (Production)
* **AI/NLP:** Google Gemini API
* **Tools:** Git, VS Code, Django Admin

## 🔒 Security & Standards
* Environment variables managed via `.env` to protect API credentials.
* Follows PEP 8 Python coding standards.