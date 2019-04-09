import os

import pyzmail

smtp_params = {
    'smtp_host': os.getenv('SMTP_HOST'),
    'smtp_port': os.getenv('SMTP_PORT'),
    'smtp_login': os.getenv('SMTP_LOGIN'),
    'smtp_password': os.getenv('SMTP_PASSWORD')
}

SENDER_EMAIL = 'info@chuzzapp.com'


def send_mail(subject, receiver_mail, content):
    payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
        SENDER_EMAIL,
        [receiver_mail],
        subject,
        'utf-8',
        ('', 'utf-8'),
        html=(content, 'utf-8'))

    pyzmail.send_mail2(payload, mail_from, rcpt_to, **smtp_params)
