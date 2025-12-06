import smtplib
import os
from email.mime.text import MIMEText

class SendMail:
    port = os.getenv("EMAIL_SMTP_PORT")
    server = os.getenv("EMAIL_SMTP_SERVER")
    login = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    sender = os.getenv("EMAIL_SENDER")

    def __init__(self, receiver, subject, body): 
        self.message = MIMEText(body, "plain")
        self.message["From"] = self.sender
        self.message["Subject"] = subject
        self.message["To"] = receiver
        
    def send(self):
        print("Sending mail to: "+ self.message["To"])
        with smtplib.SMTP_SSL(self.server, self.port) as server:
            server.login(self.login, self.password)
            server.sendmail(self.sender, self.message["To"], self.message.as_string())
