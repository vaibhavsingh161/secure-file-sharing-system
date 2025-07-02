import aiosmtplib
from email.message import EmailMessage
from app.config import settings

async def send_verification_email(to_email: str, token: str):
    link = f"http://localhost:8000/client/verify-email?token={token}"
    
    message = EmailMessage()
    message["From"] = settings.SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = "Verify your account"
    message.set_content(f"Click the link to verify your email: {link}")
    
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_SERVER,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
    )
