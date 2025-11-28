import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def SendMail(ImgFileName):
    # **Hardcoded Email Credentials (Less Secure)**
    sender_email = ""
    receiver_email = ""
    email_password = ""


    msg = MIMEMultipart()
    msg['Subject'] = '🚨 Crash Alert 🚨'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    text = MIMEText("🚗💥 Vehicle Crash Detected! Immediate assistance required.")
    msg.attach(text)

    try:
        # Open image safely
        with open(ImgFileName, 'rb') as img_file:
            image = MIMEImage(img_file.read(), name=os.path.basename(ImgFileName))
            msg.attach(image)

        # Connect to Gmail SMTP Server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("🚀 Crash alert email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
