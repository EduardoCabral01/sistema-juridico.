import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

async def enviar_email_prazo(destinatario: str, descricao: str, data_limite: str):
    remetente = os.getenv('MAIL_USERNAME')
    senha = os.getenv('MAIL_PASSWORD')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = '⚠️ Prazo se aproximando — Sistema Jurídico'
    msg['From'] = remetente
    msg['To'] = destinatario

    html = f"""
    <h2>⚖️ Sistema Jurídico</h2>
    <p>Olá! Você tem um prazo se aproximando:</p>
    <table style="border-collapse:collapse; width:100%;">
        <tr style="background:#1a1a2e; color:white;">
            <th style="padding:10px;">Descrição</th>
            <th style="padding:10px;">Data limite</th>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid #ddd;">{descricao}</td>
            <td style="padding:10px; border:1px solid #ddd;">{data_limite}</td>
        </tr>
    </table>
    <br>
    <p>Acesse o sistema para mais detalhes.</p>
    """

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(remetente, senha)
        s.send_message(msg)