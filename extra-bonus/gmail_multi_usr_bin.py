#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created by Ranger (Feb 2024) Version 1.0.0
# Modified by David Keane (Dec 31st 2024) Version 2.0.1

# Title: Gmail Email Client v1.0 for Python and CLI

# More details are available in the 'how_to_use.md' file in the extra-bonus folder. 
# There are a few steps to get this script working with the Gmail Bin feature.

# Version: 2.0.1
# Description: A simple email client that allows you to check, read, and send emails from your Gmail account.

# About:
# This version allows you to select from multiple Gmail accounts using dotenv and colorama.
# Features: Fetch new emails, fetch older emails, read emails, send emails, and switch between multiple accounts.
#
# Usage: Run the script and follow the prompts to select an account and choose an action from the menu.
#
# Dependencies: colorama, python-dotenv
# Installation: pip install colorama python-dotenv
#
# Gmail Email Credentials - Google Less Secure App Passwords
#
# Note: Make sure to enable "Less Secure Apps" in your Gmail settings to send emails.
# Go here to get yours @ https://myaccount.google.com/apppasswords
#
# Extra-bonus scripts: usr-bin.sh and Gmail Multi-User Bin Script.
# 
# The Gmail Email Client has an extra-bonus feature called Gmail Bin that allows you to run the script from anywhere in the terminal.
#
# There are two versions of the Gmail Bin feature:
# 
# 0. gmail_multi.py
# 
# The gmail_multi.py is the main script that allows you to select from multiple Gmail accounts and perform actions like checking new emails, reading emails, and sending emails.
# This script is the main Gmail Email Client that you can run from the terminal.
# You can run the script by typing python gmail_multi.py in the terminal.
# 
# 1. gmail_multi_usr_bin.py
# The Gmail version in the extra-bonus/gmail_multi_usr_bin.py file is a standalone script that can be run from the command line with the password as an argument.
# This Gmail Bin version works by entering the prompt gmail in the terminal and the Gmail script will run from anywhere inside your files and drives.
# More details are available in the gmail_multi_usr_bin.py file and the how_to_use.md file in the extra-bonus folder.
#
# 2. usr-bin.sh
# The usr-bin.sh script is a bash script that creates a symbolic link to the Gmail script in the /usr/local/bin directory.
# This allows you to run the Gmail script from anywhere in the terminal by simply typing gmail.
# More details are available in the usr-bin.sh file and the how_to_use.md file in the extra-bonus folder.
# 
# 3. gmail_ping_test.py
# The gmail_ping_test.py script is a simple script that pings the Gmail server to check the connection status.
# This script can be run from the command line to test the connection to the Gmail server.
# More details are available in the how_to_use.md file in the extra-bonus folder.
#
# To use the Gmail Bin version, follow these steps:
#
# Note: Make sure to enable "Less Secure Apps" in your Gmail settings to send emails.
# Go here to get yours @ https://myaccount.google.com/apppasswords
#
# A: Two options to rename the file:
#       1st Option. The file has to save the file without the .py extension. For example, rn gmail_multi_usr_bin.py to gmail
#       2nd Option. The file has to be renamed to gmail (without the .py extension). For example, mv gmail_multi_usr_bin.py gmail
#
# B: The file has to be made executable using the chmod +x command. For example, chmod +x gmail
# C: The file has to be moved to the /usr/local/bin directory. For example, sudo mv gmail /usr/local/bin
#
# D: You will need to refresh the terminal or run source ~/.bashrc to use the gmail command from anywhere.
#
# Congrats! The file now can be run from the terminal by typing gmail. For example, gmail

# Import required libraries
import os
import smtplib
import imaplib
import email
import sys
import logging
from time import sleep
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gmail Email Credentials - Google Less Secure App Passwords
# Go here to get yours @ https://myaccount.google.com/apppasswords

EMAIL_ACCOUNTS = { # directly added to the dict.
    '1': {
        'user': 'Bob',   # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'add-password-here'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    },
    '2': {
        'user': 'Man', # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'add-password-here'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    },
    '3': {
        'user': 'Linky', # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'add-password-here'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    }
}
def print_ascii_gmail2():
    print(r"""
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
............:############+......................................-#############-...........
............:##############+..................................-###############-...........
............:################=..............................:#################-...........
............:##################-..........................:###################-...........
............:####################:.......................*####################-...........
............:######################:...................*############-*########-...........
............:#########.-#############................*############=..*########-...........
............:#########...-#############............*############+....*########-...........
............:#########.....=############*........+############+......*########=...........
............:#########.......=############+....=############*........*########=...........
..........:::#########.........+############+-############*..........*########=.:.........
.......::::::#########...........*#######################:...........*########=:::::......
.....::::::::#########............:*###################:.............*########=:::::::....
........=::::#########...............################:...............*########=::::-......
...........--#########....::..:.:.::..:############-.:...::.:::.:.::.*########=-:.........
..............=#######.:::::::::::::::::-########=::::::::::::::::::.*######*:............
.................:%###::::::::::::::::::::=####+:::::::::::::::::::::####*................
....................:+::::::::::::::::::::::=+:::::::::::::::::::::::#=...................
........................:-::::::::::::::::::::::::::::::::::::::::-.......................
............................=::::::::::::::::::::::::::::::::::-..........................
...............................:-::::::::::::::::::::::::::-:.............................
""")

# Display settings
DISPLAY_SETTINGS = {
    'max_subject_length': 50,
    'max_preview_length': 100,
    'email_separator': '\n' + '-' * 80 + '\n',
    'body_width': 70
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_account():
    print_ascii_gmail2()
    print(Fore.YELLOW + "\nSelect an account:")
    print("1. Ranger Smyth")
    print("2. David Keane")
    print("3. Proxy Busterburg")
    print("0. Exit" + Style.RESET_ALL)
    while True:
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
        if choice == '0':
            print(Fore.GREEN + "\nExiting the program. Goodbye!\n" + Style.RESET_ALL)
            sys.exit()
        elif choice in EMAIL_ACCOUNTS:
            global EMAIL_USER, EMAIL_PASS
            EMAIL_USER = EMAIL_ACCOUNTS[choice]['user']
            EMAIL_PASS = EMAIL_ACCOUNTS[choice]['pass']
            return
        else:
            print(Fore.RED + "\nInvalid choice. Please enter a number from the menu.\n" + Style.RESET_ALL)

def show_menu():
    print(Fore.YELLOW + "\nMenu:")
    print("1. Check new emails")
    print("2. Check older emails")
    print("3. Send an email")
    print("4. Back to account selection")
    print("0. Exit" + Style.RESET_ALL)

def fetch_emails(unseen=True):
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993
    print_ascii_gmail2()
    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as mail:
            mail.login(EMAIL_USER, EMAIL_PASS)
            mail.select("inbox")

            status, messages = mail.search(None, 'UNSEEN' if unseen else 'ALL')
            email_ids = messages[0].split()

            if not email_ids:
                print("No emails found.")
                return

            email_summary = []
            for message in email_ids[-20:]:  # Fetching the last 20 emails
                try:
                    status, msg_data = mail.fetch(message, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject = decode_email_header(msg["Subject"])
                            from_ = decode_email_header(msg.get("From"))
                            body = get_email_body(msg)
                            email_summary.append((from_, subject, body))
                    logging.info(f"Successfully processed email: {subject}")
                except Exception as e:
                    logging.error(f"Error processing email: {str(e)}")
                    continue

            display_email_summaries(email_summary)

    except Exception as e:
        logging.error(f"Error in fetch_emails: {str(e)}")

def decode_email_header(header):
    try:
        decoded, encoding = decode_header(header)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(encoding or 'utf-8', errors='replace')
        return decoded
    except Exception as e:
        logging.error(f"Error decoding email header: {str(e)}")
        return "Unable to decode header"

def get_email_body(msg):
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return decode_email_body(part.get_payload(decode=True))
        else:
            return decode_email_body(msg.get_payload(decode=True))
    except Exception as e:
        logging.error(f"Error getting email body: {str(e)}")
        return "Unable to retrieve email body"

def decode_email_body(body):
    try:
        if isinstance(body, bytes):
            return body.decode('utf-8', errors='replace')
        return body
    except Exception as e:
        logging.error(f"Error decoding email body: {str(e)}")
        return "Unable to decode email body"

def display_email_summaries(email_summary):
    clear_screen()
    print_ascii_gmail2()
    print(Fore.CYAN + "\n===== INBOX =====" + Style.RESET_ALL)
    for i, (from_, subject, body) in enumerate(email_summary, 1):
        truncated_subject = subject[:DISPLAY_SETTINGS['max_subject_length']] + '...' if len(subject) > DISPLAY_SETTINGS['max_subject_length'] else subject
        email_preview = ' '.join(body.split()[:10])
        truncated_preview = email_preview[:DISPLAY_SETTINGS['max_preview_length']] + '...' if len(email_preview) > DISPLAY_SETTINGS['max_preview_length'] else email_preview
        print(f"{Fore.GREEN}{i}. From: {from_}{Style.RESET_ALL}")
        print(f"   Subject: {truncated_subject}")
        print(f"   Preview: {truncated_preview}")
        print(DISPLAY_SETTINGS['email_separator'])

    while True:
        email_choice = input("Enter the number of the email you want to read (or 'back' to return to menu): ")
        if email_choice.lower() == 'back':
            return
        try:
            choice = int(email_choice) - 1
            if 0 <= choice < len(email_summary):
                display_full_email(email_summary[choice])
                break
            else:
                print(Fore.RED + "Invalid choice. Please enter a valid email number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number or type 'back'." + Style.RESET_ALL)

def display_full_email(email_details):
    clear_screen()
    print_ascii_gmail2()
    from_, subject, body = email_details
    print(Fore.CYAN + "\n===== EMAIL DETAILS =====" + Style.RESET_ALL)
    print(f"{Fore.GREEN}From: {from_}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Subject: {subject}{Style.RESET_ALL}")
    print(Fore.GREEN + "\nBody:" + Style.RESET_ALL)
    
    # Wrap the body text
    wrapped_body = '\n'.join([body[i:i+DISPLAY_SETTINGS['body_width']] for i in range(0, len(body), DISPLAY_SETTINGS['body_width'])])
    print(wrapped_body)
    
    print("\n" + DISPLAY_SETTINGS['email_separator'])
    
    if input("Do you want to forward this email? (yes/no): ").lower() in ['yes', 'y']:
        to_email = input("Enter the recipient's email address: ")
        send_email(subject=subject, message_body=body, to_email=to_email)

def send_email(to_email=None, subject=None, message_body=None):
    print(Fore.GREEN + "\nSending email...\n" + Style.RESET_ALL)
    while True:
        if not to_email:
            to_email = input("Enter the recipient's email address (or 'menu' to return to main menu): ")
            if to_email.lower() == 'menu':
                return
        if not subject:
            subject = input("Enter your subject (or 'menu' to return to main menu): ")
            if subject.lower() == 'menu':
                return
        if not message_body:
            message_body = input("Enter your message (or 'menu' to return to main menu): ")
            if message_body.lower() == 'menu':
                return
        break

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(Fore.GREEN + "Email sent successfully." + Style.RESET_ALL)
    except smtplib.SMTPException as e:
        print(Fore.RED + f"Failed to send email: {e}" + Style.RESET_ALL)

def main():
    try:
        while True:
            clear_screen()
            select_account()
            while True:
                show_menu()
                choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
                if choice == '0':
                    print(Fore.GREEN + "\nExiting the program. Goodbye!\n" + Style.RESET_ALL)
                    sys.exit()
                elif choice == '1':
                    fetch_emails(unseen=True)
                elif choice == '2':
                    fetch_emails(unseen=False)
                elif choice == '3':
                    send_email()
                elif choice == '4':
                    break
                else:
                    print(Fore.RED + "\nInvalid choice. Please enter a number from the menu.\n" + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nProgram interrupted. Exiting gracefully." + Style.RESET_ALL)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        print(Fore.RED + f"\nAn unexpected error occurred. Please check the log file for details." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
    clear_screen()
    print_ascii_gmail2()