import smtplib
import os
import datetime
from email.utils import formataddr
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS")

def send_email_password(user_email, token):
    try:
        msg = EmailMessage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = f"SFISAS {current_date}"
        msg["Subject"] = subject
        msg['From'] = formataddr(('SFISAS', MAIL_FROM_ADDRESS))
        msg['To'] = formataddr((user_email, user_email))

        reset_link = f"http://127.0.0.1:8000/auth/confirm-reset?token={token}"
        
        html_content = f"""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="    font-family: sans-serif; background-color: #fcfcfc; color: #333333; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
    <div style="width: 100%; max-width: 500px; background-color: white; border-radius: 20px; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); overflow: hidden; text-align: center;">
        <div style="padding: 30px; background-color: white;     padding-bottom: 0px;">
            <img src="https://media.licdn.com/dms/image/v2/C4D16AQELt7w9e9nxUw/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1654112997672?e=2147483647&v=beta&t=KVxj8dh0WES4CpgHdXm_LxdGIZjq0BkdJRpZN7fq1Hw" alt="Logo" style="width: 350px; " />
        </div>
        <div style="padding: 30px; background-color: #3286d1; color: white; font-size: 18px; line-height: 1.6; border-radius: 0 0 20px 20px;">
            <p style="margin: 0; margin-bottom: 15px;">Para continuar con el restablecimiento de su contraseña, por favor haga clic en el botón a continuación.</p>
            <p style="margin: 0; margin-bottom: 15px;">Si no solicitó este restablecimiento, puede ignorar este correo.</p>
            <div style="margin: 20px 0;">
                <a href="{reset_link}" style="border:2px solid white; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; transition: background-color 0.3s ease;">Confirmar</a>
            </div>
        </div>
    </div>
</body>
</html>
        """
        msg.set_content(html_content, subtype="html")

        with smtplib.SMTP_SSL(MAIL_HOST, int(MAIL_PORT)) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e
