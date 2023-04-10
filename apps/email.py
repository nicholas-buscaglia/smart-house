import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(subject, body, from_email, to_emails, cc_emails=[], bcc_emails=[], attachments=[]):
    """
    Sends an email using SMTP.

    :param subject: Email subject
    :param body: Email body
    :param from_email: Email sender address
    :param to_emails: List of email recipient addresses
    :param cc_emails: List of email recipient addresses to be carbon copied
    :param bcc_emails: List of email recipient addresses to be blind carbon copied
    :param attachments: List of file paths to attach to the email
    """
    # Get SMTP server credentials from environment variables
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT'))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    # Create the email message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = ','.join(to_emails)
    if cc_emails:
        message['Cc'] = ','.join(cc_emails)
    if bcc_emails:
        message['Bcc'] = ','.join(bcc_emails)

    # Attach the email body
    body_part = MIMEText(body, 'plain')
    message.attach(body_part)

    # Attach any files
    for attachment_path in attachments:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            message.attach(attachment)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_emails + cc_emails + bcc_emails, message.as_string())

    # Print a success message
    print("Email sent successfully.")

# Get the email details from the user
subject = input("Enter the email subject: ")
body = input("Enter the email body: ")
from_email = input("Enter your email address: ")
to_emails = input("Enter the recipient email addresses (comma-separated): ").split(',')
cc_emails = input("Enter the CC email addresses (comma-separated): ").split(',')
bcc_emails = input("Enter the BCC email addresses (comma-separated): ").split(',')
attachments = input("Enter the file paths to attach (comma-separated): ").split(',')

# Send the email
send_email(subject, body, from_email, to_emails, cc_emails=cc_emails, bcc_emails=bcc_emails, attachments=attachments)
