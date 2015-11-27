# coding: utf-8
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_forgot_password_template():
    title = "یکسطر - بازیابی کلمه عبور"
    text_body = "سلام! \n برای بازیابی کلمه عبور متن زیر را در نوار آدرس مرورگر خود درج نموده و کلید اینتر را بزنید \n {0} "
    html_body = """
    سلام! <br />
    برای بازیابی کلمه عبور خود روی لینک زیر کلیک کنید <br /><br />
    {0} """
    return (title, text_body, html_body)

def get_reset_password_template():
    title = "یکسطر - کلمه عبور جدید"
    text_body = "سلام! \n بنا به درخواست شما کلمه عبور حساب کاربریتان در یکسطر بازنشانی شده است. کلمه عبور جدید شما عبارت است از: \n {0} "
    html_body = """
    سلام! <br />
    بنا به درخواست شما کلمه عبور حساب کاربریتان در یکسطر بازنشانی شده است. کلمه عبور جدید شما عبارت است از <br /><br />
    {0} """
    return (title, text_body, html_body)
    
def sendmail(recipient, title, text_body, html_body):
    # Define to/from
    sender = 'noreply@yeksatr.com'

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = recipient

    msg.attach(part1)
    msg.attach(part2)

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

    # Perform operations via server
    server.login(sender, '098321NOREPLy_!@')
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
