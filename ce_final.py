import os
import httplib2, csv, json, base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient import errors, discovery
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials



SCOPES = ['https://www.googleapis.com/auth/gmail.send']

CLIENT_SECRET_FILE = '/home/aditya/client_secret_164302493153-noevam53obuvr2c2rdes6lubb9oo7kbk.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Gmail API Python Send Email'
sender_email = ""
email_subject = "Testing3"
service = None 

def authenticate():
    home_dir = os.path.expanduser('~')
    json_path = os.path.join(home_dir, 'client_secret_12.json')
    flow = InstalledAppFlow.from_client_secrets_file(json_path, SCOPES)
    flow.user_agent = APPLICATION_NAME
    creds = flow.run_local_server(port=0)
    global service
    service = build('gmail', 'v1', credentials=creds)

def SendMessage(to, email_subject, recipient_name, recipient_company, email_body):
    message1 = CreateMessage(sender_email, to, email_subject, email_body)
    SendMessageInternal(service, "me", message1, recipient_name, to, recipient_company)

def SendMessageInternal(service, user_id, email_body, recipient_name, to, recipient_company):
    try:
        message = service.users().messages().send(userId=user_id, body=email_body).execute()
        print(f"Sending mail with subject {email_subject}")
        print(f"Email sent to {recipient_name} at {to} for {recipient_company}")
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessage(sender_email, to, email_subject, email_body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = sender_email
    msg['To'] = to
    msg.attach(MIMEText(email_body, 'plain'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def send_bulk_emails():
    with open('/home/aditya/input.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            to = row['Email']
            recipient_name = row['Name']
            recipient_company = row['Company']
            email_body = f"Dear {recipient_name},\n\nThis is a sample email to {recipient_company}. This email is powered by GCP. Thank you for your attention.\n\nSincerely,\n\nAditya Chandra"
            SendMessage(to, email_subject, recipient_name, recipient_company, email_body)

authenticate()
send_bulk_emails()