import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

# Set up OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.settings.basic']
redirect_uri = 'http://localhost:40133/'

# Set up email details
sender_email = 'aditya@techorigins.io'
email_subject = 'Test'
email_body = 'Dear {name},\n\nThis is a sample email to {company}. Thank you for your attention.\n\nSincerely,\nAditya'

def authenticate_application():
    # Set up the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file('/home/aditya/credentials.json', SCOPES, redirect_uri=redirect_uri)
    flow.run_local_server(port=0, authorization_prompt_uri='https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=client_id&redirect_uri=redirect_uri&scope=SCOPES')
    credentials = flow.credentials

    return credentials

def send_email(recipient_email, recipient_name, recipient_company, app_password):
    # Set up the email content
    message = MIMEMultipart()
    message['Subject'] = email_subject
    personalized_body = email_body.format(name=recipient_name, company=recipient_company)
    message.attach(MIMEText(personalized_body, 'plain'))

    # Connect to Gmail's SMTP server using the generated app password
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

def send_bulk_emails():
    # Authenticate the application
    credentials = authenticate_application()

    # Generate the app password
    app_password = input("Enter your app password: ")

    # Read recipient details from input.csv file
    with open('/home/aditya/input.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipient_email = row['Email']
            recipient_name = row['Name']
            recipient_company = row['Company']

            # Call send_email function for each recipient
            send_email(recipient_email, recipient_name, recipient_company,app_password)

# Call the send_bulk_emails function to send bulk emails
send_bulk_emails()
