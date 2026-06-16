import smtplib
import re
from email.message import EmailMessage
from getpass import getpass
import os


# -----------------------------
# Email Validation
# -----------------------------
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


# -----------------------------
# Create Email
# -----------------------------
def create_email(sender, recipients, subject, body, attachment=None):
    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    # Add attachment if provided
    if attachment:
        try:
            with open(attachment, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(attachment)

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name
            )

        except Exception as e:
            print(f"Attachment Error: {e}")

    return msg


# -----------------------------
# Send Email
# -----------------------------
def send_email():
    print("\n===== EMAIL SENDER APP =====\n")

    sender = input("Sender Email: ").strip()

    recipients_input = input(
        "Recipient Email(s) (comma separated): "
    ).strip()

    recipients = [email.strip() for email in recipients_input.split(",")]

    subject = input("Subject: ").strip()

    print("\nEnter Message:")
    body = input("> ")

    attachment = input(
        "Attachment Path (Leave blank if none): "
    ).strip()

    if attachment == "":
        attachment = None

    # Validation
    if not sender or not subject or not body:
        print("Error: Required fields cannot be empty.")
        return

    if not validate_email(sender):
        print("Invalid sender email.")
        return

    for email in recipients:
        if not validate_email(email):
            print(f"Invalid recipient email: {email}")
            return

    password = getpass("\nEnter Email Password/App Password: ")

    try:
        msg = create_email(
            sender,
            recipients,
            subject,
            body,
            attachment
        )

        # Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(sender, password)

            server.send_message(msg)

        print("\nEmail sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Login failed. Check email or password.")

    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")


# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":
    send_email()
