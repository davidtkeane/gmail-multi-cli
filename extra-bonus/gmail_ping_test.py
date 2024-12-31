#!/usr/bin/env python3

# Created by Ranger (Dec 2024)
# Title: Gmail Ping Test 

# Version: 1.0
# Usage = Please move this file into the folder with the .env file and run the following command: mv gmail_ping.py ../.env && cd ../ && python gmail_ping.py
# python gmail_ping.py

# What this script does:
# This script checks by sending a ping to the SMTP - IMAP Email Servers to check for a connection.
# This script checks by sending a ping to the Email SMTP - IMAP login Servers to check for a connection.

# Change your name from Bob below in the script. Not below, but below on Line 39 and 40.
        # Get credentials from environment variables (BEST PRACTICE)
        # EMAIL_USER = os.getenv("EMAIL_USER_Bob")
        # EMAIL_PASS = os.getenv("EMAIL_PASS_Bob")

# Importing the required libraries
import smtplib
import imaplib
import os
import socket
import email

from dotenv import load_dotenv

load_dotenv()

os.system('cls' if os.name == 'nt' else 'clear')

# Print welcome banner
print("\nMade By David\nVersion 1.0.0\n")

# Set a timeout for socket operations (e.g., 10 seconds)
socket.setdefaulttimeout(10)  # Timeout after 10 seconds

# Get credentials from environment variables (BEST PRACTICE)
EMAIL_USER = os.getenv("EMAIL_USER_Bob")
EMAIL_PASS = os.getenv("EMAIL_PASS_Bob")

def test_smtp_gmail():
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_gmail:
            smtp_gmail.ehlo()
            if smtp_gmail.noop()[0] == 250:
                print("Gmail SMTP server is responding.")
            else:
                print("Failed to connect to Gmail SMTP server.")
    except Exception as e:
        print(f"Error testing SMTP: {e}")

def test_imap_gmail():
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as imap_gmail:
            imap_gmail.noop()  # Check initial connection
            if imap_gmail.noop()[0] == 'OK':
                print("Gmail IMAP server is responding.")
            else:
                print("Failed to connect to Gmail IMAP server.")
    except Exception as e:
        print(f"Error testing IMAP: {e}")

def test_smtp_login():
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            print("Gmail SMTP login successful.")
    except Exception as e:  # Catch all SMTP exceptions
        print(f"Gmail SMTP login failed: {e}")

def test_imap_login():
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as mail:
            mail.login(EMAIL_USER, EMAIL_PASS)
            print("Gmail IMAP login successful.")
    except Exception as e:  # Catch all IMAP exceptions
        print(f"Gmail IMAP login failed: {e}")

if __name__ == "__main__":
    test_smtp_gmail()
    test_imap_gmail()

    # Run login tests only if credentials are available
    if EMAIL_USER and EMAIL_PASS:
        test_smtp_login()
        test_imap_login()
    else:
        print("Login tests skipped (credentials not found).")



