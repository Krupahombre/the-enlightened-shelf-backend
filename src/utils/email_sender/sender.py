import json
import logging
import os
import pathlib
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

from src.server.models.checkout import QRCodeDTO
from src.utils.qr_utils import generate_qr_code

logger = logging.getLogger("EmailSender")


class EmailSender:
    def __init__(self):
        self.logger = logging.getLogger("EmailSender")
        self.user = None
        self.password = None
        self.smtp_server = None
        self.smtp_port = None
        self.email_from = None

        self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        config_file_path = "project_config_hidden.ini"

        if os.path.exists(config_file_path):
            config.read(config_file_path)

            if "email" in config:
                email_config = config["email"]
                self.user = email_config.get("user", "")
                self.password = email_config.get("password", "")
                self.smtp_server = email_config.get("smtp_server", "")
                self.smtp_port = email_config.get("smtp_port", "")
                self.email_from = email_config.get("email_from", "")
        else:
            self.logger.warning(f"File not found: {config_file_path}")

    def prepare_html(self, qr_data: QRCodeDTO):
        with open(f"{pathlib.Path(__file__).parent.resolve()}/template.html", "r") as template:
            html_str = template.read()

            html_str = html_str.replace("{user_full_name}", f"{qr_data.user_full_name}")
            html_str = html_str.replace("{book_title}", f"{qr_data.book_title}")
            html_str = html_str.replace("{checkout_date}", f"{qr_data.checkout_date}")
            html_str = html_str.replace("{pickup_code}", f"{qr_data.pickup_code}")

            return html_str

    def send_email(self, email_to: str, qr_data: QRCodeDTO):
        service = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=ssl.create_default_context())
        try:
            message = MIMEMultipart("alternative")
            message["From"] = self.email_from
            message["Subject"] = "Book Checkout - The Enlightened Shelf"
            message.attach(MIMEText(self.prepare_html(qr_data), "html"))

            generate_qr_code(qr_data)

            with open("./qr_code_folder/qrcode.png", "rb") as attachment:
                part = MIMEApplication(attachment.read(), Name="qrcode.png")
                part['Content-Disposition'] = f'attachment; filename="qrcode.png"'
                message.attach(part)

            service.login(self.user, self.password)
            service.sendmail(message["From"], email_to, message.as_string())
        finally:
            service.quit()


email_sender = EmailSender()
