import smtplib
import os
from email.mime.text import MIMEText

class sendMail:
    port = os.getenv("EMAIL_SMTP_PORT")
    smtp_server = os.getenv("EMAIL_SMTP_SERVER")
    login = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    sender_email = os.getenv("EMAIL_SENDER")

    def __init__(self, receiver, subject, body): 
        self.message = MIMEText(body, "plain")
        self.message["From"] = "Vertretungsplan Mailer Jenaplanschule Weimar"
        self.message["Subject"] = subject
        self.message["To"] = receiver
        
    def send(self):
        print("Sending mail to: "+ self.message["To"])
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.login(self.login, self.password)
            server.sendmail(self.sender_email, self.message["To"], self.message.as_string())
