"""
Email service for sending emails via Gmail SMTP.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

# Global SMTP client
smtp_client = None


def initialize_email():
    """
    Initialize SMTP client for Gmail.
    This should be called once during Django application startup.
    """
    global smtp_client

    if smtp_client is not None:
        # Email client already initialized
        return smtp_client

    smtp_client = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_client.starttls()
    smtp_client.login(settings.EMAIL_HOST_USER, settings.GOOGLE_APP_PASSWORD)

    return smtp_client


def get_smtp_client():
    """
    Get the SMTP client instance.
    Returns the global smtp_client, initializing if necessary.
    """
    global smtp_client
    if smtp_client is None:
        smtp_client = initialize_email()
    return smtp_client


def send_email(to, subject, body, html_body=None):
    """
    Send an email using Gmail SMTP.
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content (plain text)
        html_body (str, optional): HTML version of email body
    """
    client = get_smtp_client()

    msg = MIMEMultipart('alternative')
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to
    msg['Subject'] = subject

    # Add plain text version
    msg.attach(MIMEText(body, 'plain'))

    # Add HTML version if provided
    if html_body:
        msg.attach(MIMEText(html_body, 'html'))

    client.send_message(msg)
