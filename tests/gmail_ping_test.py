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
import smtplib # Import the smtplib library for SMTP operations 
import imaplib # Import the imaplib library for IMAP operations
import os      # Import the os library for interacting with the operating system
import socket  # Import the socket library for socket operations
import email   # Import the email library for email operations

from dotenv import load_dotenv # Import the load_dotenv function from the dotenv library to load environment variables

load_dotenv() # Load environment variables from a .env file into the script's environment

os.system('cls' if os.name == 'nt' else 'clear') # Clear the terminal screen

# Print welcome banner
print("\nMade By David\nVersion 1.0.0\n")

# Set a timeout for socket operations (e.g., 10 seconds)
socket.setdefaulttimeout(10)  # Timeout after 10 seconds

# Get credentials from environment variables (BEST PRACTICE)
EMAIL_USER = os.getenv("EMAIL_USER_Bob") # Change Bob to your name
EMAIL_PASS = os.getenv("EMAIL_PASS_Bob") # Change Bob to your name

def test_smtp_gmail(): # Test SMTP connection to Gmail server
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_gmail: # Connect to Gmail SMTP server
            smtp_gmail.ehlo() # Identify yourself to the server
            if smtp_gmail.noop()[0] == 250: # Check if the connection is successful
                print("Gmail SMTP server is responding.") # Print success message
            else:
                print("Failed to connect to Gmail SMTP server.")
    except Exception as e: # Catch all SMTP exceptions
        print(f"Error testing SMTP: {e}") # Print the error message

def test_imap_gmail(): # Test IMAP connection to Gmail server
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as imap_gmail: # Connect to Gmail IMAP server
            imap_gmail.noop()  # Check initial connection
            if imap_gmail.noop()[0] == 'OK': # Check if the connection is successful
                print("Gmail IMAP server is responding.") # Print success message
            else:
                print("Failed to connect to Gmail IMAP server.")
    except Exception as e: # Catch all IMAP exceptions
        print(f"Error testing IMAP: {e}") # Print the error message

def test_smtp_login(): # Test SMTP login to Gmail server
    try: # Connect to Gmail SMTP server and attempt to login 
        with smtplib.SMTP('smtp.gmail.com', 587) as server: # Connect to Gmail SMTP server
            server.starttls() # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(EMAIL_USER, EMAIL_PASS) # Attempt to login to Gmail SMTP server
            print("Gmail SMTP login successful.") # Print success message if login is successful
    except Exception as e:  # Catch all SMTP exceptions
        print(f"Gmail SMTP login failed: {e}") # Print the error message if login fails

def test_imap_login(): # Test IMAP login to Gmail server
    try: # Connect to Gmail IMAP server and attempt to login
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as mail: # Connect to Gmail IMAP server
            mail.login(EMAIL_USER, EMAIL_PASS) # Attempt to login to Gmail IMAP server
            print("Gmail IMAP login successful.") # Print success message if login is successful
    except Exception as e:  # Catch all IMAP exceptions
        print(f"Gmail IMAP login failed: {e}") # Print the error message if login fails

if __name__ == "__main__": # Run the tests
    test_smtp_gmail() # Test SMTP connection to Gmail server
    test_imap_gmail() # Test IMAP connection to Gmail server

    # Run login tests only if credentials are available
    if EMAIL_USER and EMAIL_PASS: # Check if credentials are available
        test_smtp_login() # Test SMTP login to Gmail server
        test_imap_login() # Test IMAP login to Gmail server
    else: # Skip login tests if credentials are not available
        print("Login tests skipped (credentials not found).") # Print a message indicating that login tests were skipped



