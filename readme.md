# 🔐 Secure File Sharing System

A RESTful Python API for secure file sharing between Ops and Client users using FastAPI.

## 🚀 Features
- JWT Authentication
- Role-based Access
- Secure File Upload (.docx/.pptx/.xlsx)
- Encrypted Download URLs (client-only access)
- Email Verification with SMTP

## 📦 Tech Stack
- FastAPI + SQLAlchemy
- SQLite / PostgreSQL
- JWT + Passlib
- SMTP (Gmail) for Email Verification

## 🛠️ Run Locally
```bash
git clone ...
cd secure_file_sharing
pip install -r requirements.txt
uvicorn main:app --reload


