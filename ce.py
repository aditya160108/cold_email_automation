import csv
import smtplib

def send_cold_email(name, email, company):
    # Customize your email content
    subject = "Your Subject Line"
    message = f"Dear {name},\n\nI hope this email finds you well. I am reaching out to offer our web development services to {company}.\n\nBest regards,\nYour Name"

    # SMTP server details
    smtp_server = "<server_details>"
    smtp_port = <port>
    smtp_username = "email_id"
    smtp_password = "password"

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Create the email
        email_message = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(smtp_username, email, email_message)

# Path to the CSV file containing name, email, and company details
csv_file_path = "path_on_disk"

# Read the CSV file and send emails
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row if it exists
    for row in reader:
        name, email, company = row
        send_cold_email(name, email, company)
        print(f"Email sent to {name} at {email} for {company}")
