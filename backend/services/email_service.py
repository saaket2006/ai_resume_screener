import smtplib
import logging
from email.message import EmailMessage
from backend.config import settings

logger = logging.getLogger("resume_screener")

def send_password_reset_email(to_email: str, reset_link: str) -> bool:
    """
    Dispatches a secure password reset email to the specified recipient.
    
    Security Constraints:
    - Never logs raw reset tokens or reset URLs unless explicitly enabled in local dev/test mode.
    - Never prints or exposes SMTP credentials.
    - Returns False and logs a warning if SMTP credentials are not configured.
    """
    # Safe dev/test token logging: ONLY if DEBUG is True AND LOG_RESET_TOKENS is explicitly enabled
    if settings.DEBUG and settings.LOG_RESET_TOKENS:
        logger.info("[DEV MODE ONLY] Password reset link for %s: %s", to_email, reset_link)

    # If SMTP is not configured, do not pretend it was sent
    if not settings.EMAIL_USER or not settings.EMAIL_PASS:
        logger.warning(
            "Password reset email delivery skipped: EMAIL_USER or EMAIL_PASS is not configured."
        )
        return False

    try:
        msg = EmailMessage()
        msg["Subject"] = "Reset Your Nipun Password"
        msg["From"] = settings.EMAIL_USER
        msg["To"] = to_email

        # Plain-text version
        plain_text = f"""Hello,

We received a request to reset your password for your Nipun account.

Please use the following link to set a new password:
{reset_link}

This link is valid for {settings.PASSWORD_RESET_EXPIRY_MINUTES} minutes and can only be used once.

If you did not request this password reset, please ignore this email. Your password will remain unchanged.

Best regards,
The Nipun Team
"""
        msg.set_content(plain_text)

        # HTML version
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }}
        .card {{ max-width: 500px; margin: 0 auto; background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; margin-bottom: 24px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #10b981; letter-spacing: 0.5px; }}
        h2 {{ color: #ffffff; font-size: 20px; margin-top: 0; }}
        p {{ color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 16px 0; }}
        .button-wrapper {{ text-align: center; margin: 28px 0; }}
        .btn {{ display: inline-block; background-color: #10b981; color: #ffffff; text-decoration: none; font-weight: 600; padding: 12px 28px; border-radius: 8px; font-size: 14px; letter-spacing: 0.3px; }}
        .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 24px; border-top: 1px solid #334155; padding-top: 16px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="logo">Nipun</div>
        </div>
        <h2>Password Reset Request</h2>
        <p>Hello,</p>
        <p>We received a request to reset your password. Click the button below to set a new password for your account:</p>
        <div class="button-wrapper">
            <a href="{reset_link}" class="btn" target="_blank">Reset Password</a>
        </div>
        <p>This link is valid for <strong>{settings.PASSWORD_RESET_EXPIRY_MINUTES} minutes</strong> and can only be used once.</p>
        <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
        <div class="footer">
            &copy; 2026 Nipun Platform. All rights reserved.
        </div>
    </div>
</body>
</html>"""
        msg.add_alternative(html_content, subtype="html")

        # Dispatch via SMTP with explicit STARTTLS / EHLO sequence
        # Google App Passwords often contain decorative spaces (e.g. 'xxxx xxxx xxxx xxxx')
        email_password = settings.EMAIL_PASS.replace(" ", "").strip()

        if settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
                server.ehlo()
                server.login(settings.EMAIL_USER, email_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(settings.EMAIL_USER, email_password)
                server.send_message(msg)

        logger.info("Successfully dispatched password reset email to %s", to_email)
        return True

    except Exception as e:
        logger.error(
            "Failed to send password reset email to %s: %s (Target SMTP: %s:%s)",
            to_email,
            e,
            settings.SMTP_HOST,
            settings.SMTP_PORT,
        )
        return False
