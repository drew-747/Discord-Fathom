import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

class UserManager:
    def __init__(self):
        self.db_path = 'users.db'
        self.init_db()

    def init_db(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (discord_id TEXT PRIMARY KEY,
                     email TEXT UNIQUE,
                     name TEXT)''')
        conn.commit()
        conn.close()

    def register_user(self, discord_id: str, email: str, name: str):
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (discord_id, email, name) VALUES (?, ?, ?)',
                     (discord_id, email, name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user_email(self, discord_id: str):
        """Get user's email by Discord ID"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT email FROM users WHERE discord_id = ?', (discord_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def send_email(self, to_email: str, subject: str, content: str):
        """Send email to user"""
        if not all([SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD]):
            print("Email configuration missing")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USERNAME
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(content, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 