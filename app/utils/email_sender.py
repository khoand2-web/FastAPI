# app/utils/email_sender.py
from typing import List


def send_email(recipients: List[str], subject: str, body: str) -> None:
    """
    Send email to recipients. Skeleton implementation.

    Args:
        recipients: list of recipient emails.
        subject: email subject.
        body: email body.
    """
    # Integration with SMTP or external provider (sendgrid, SES) goes here.
    pass
