import os
import smtplib

from dataclasses import dataclass
from typing import Optional, List

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE


@dataclass
class EmailAccount:
    email_address: str
    password: str


@dataclass
class EmailContent:
    send_to: List[str]
    subject: str
    body: str
    cc_list: Optional[List[str]] = None
    files_paths: Optional[List[str]] = None


def send_gmail(account: EmailAccount, content: EmailContent):
    """Send gmail using given from address and attach attachments"""
    msg = MIMEMultipart()
    msg["From"] = account.email_address
    msg["To"] = COMMASPACE.join(content.send_to)
    msg["Cc"] = COMMASPACE.join(content.cc_list) if content.cc_list is not None else ""
    msg["Subject"] = content.subject
    msg.attach(MIMEText(content.body, 'html'))
    if content.files_paths is not None:
        for f in content.files_paths:
            with open(f, "rb") as fil:
                attach_file = MIMEApplication(fil.read())
            attach_file.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(f)
            )
            msg.attach(attach_file)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(account.email_address, account.password)
    MsgText = msg.as_string()
    to_addr = content.send_to
    if content.cc_list is not None:
        to_addr += content.cc_list
    server.sendmail(account.email_address, to_addr, MsgText)
    server.quit()


def example_email():
    account = EmailAccount(
        email_address="",
        password="",  # Gmail App Password
    )
    content = EmailContent(
        send_to=[""],  # Must be a list type
        subject="This is a test",
        body="Success",
    )
    send_gmail(account, content)
