import smtplib
from email.message import EmailMessage

# ------------------------ SENDING EMAIL ------------------------
def send_email():
    sender = "Sender's Email Id"
    receiver = "Reciever's Email Id"
    password = "Gmail's App Password" 

    subject = "Retail Sales Report"
    body = "Please find attached the latest Retail Sales Report."

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    with open("report/retail_sales_report.pdf", "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="retail_sales_report.pdf")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()