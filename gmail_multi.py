#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gmail Email Client v3.1
A powerful CLI email client for managing multiple Gmail accounts.

Version: 3.1.0
Created by: Ranger (Feb 2024)
Modified by: David Keane (Jan 2026)

Features:
- Multiple Gmail account support
- Check new/old emails
- Read and forward emails
- Send emails from CLI
- Search emails
- Connection testing

Dependencies: colorama, psutil (auto-installed if missing)

Setup:
1. Get App Password: https://myaccount.google.com/apppasswords
2. Add your credentials to EMAIL_ACCOUNTS dict below
3. Run: gmail --help
"""

# =============================================================================
# AUTO-INSTALL MISSING PACKAGES
# =============================================================================
import subprocess
import sys

def check_and_install_packages():
    """Check for required packages and offer to install if missing."""
    required_packages = {
        'colorama': 'colorama',
        'psutil': 'psutil',
    }

    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing required packages: {', '.join(missing)}")
        print(f"These packages are needed for the Gmail client to work.\n")

        response = input(f"Install missing packages now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            for package in missing:
                print(f"Installing {package}...")
                try:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', package, '--quiet'
                    ])
                    print(f"✓ {package} installed successfully")
                except subprocess.CalledProcessError:
                    # Try with --user flag
                    try:
                        subprocess.check_call([
                            sys.executable, '-m', 'pip', 'install', package, '--user', '--quiet'
                        ])
                        print(f"✓ {package} installed successfully (user)")
                    except subprocess.CalledProcessError:
                        print(f"✗ Failed to install {package}")
                        print(f"  Try manually: pip install {package}")
                        sys.exit(1)
            print("\n✓ All packages installed! Restarting...\n")
            # Re-run the script
            import os
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("\nTo install manually, run:")
            print(f"  pip install {' '.join(missing)}")
            sys.exit(1)

# Check packages before importing
check_and_install_packages()

# =============================================================================
# IMPORTS
# =============================================================================
import os
import smtplib
import imaplib
import email
import logging
import platform
import socket
import re
import argparse
import psutil
import getpass

from time import sleep
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# =============================================================================
# SUDO AUTHENTICATION (Local Security Feature)
# =============================================================================

def needs_sudo():
    """Check if the current command needs sudo access."""
    # Read-only commands that don't need sudo
    read_only_args = ['--help', '-h', '--bunny', '--accounts']
    for arg in sys.argv[1:]:
        if arg in read_only_args:
            return False
    return True

def request_sudo_password():
    """Request sudo password for security before accessing email accounts."""
    if platform.system().lower() == 'windows':
        return  # Skip on Windows

    if os.geteuid() == 0:  # Already running as root
        return

    print()
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  🔐 Local Security Authentication{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}This script requires authentication to access email accounts.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}This prevents unauthorized access to your emails.{Style.RESET_ALL}")
    print()

    try:
        password = getpass.getpass(f"{Fore.GREEN}Enter sudo password: {Style.RESET_ALL}")
        cmd = ['sudo', '-S', 'echo', 'authenticated']
        result = subprocess.run(cmd, input=f"{password}\n", text=True, capture_output=True)
        if result.returncode != 0:
            print(f"\n{Fore.RED}✗ Invalid sudo password. Access denied.{Style.RESET_ALL}")
            sys.exit(1)
        print(f"\n{Fore.GREEN}✓ Authentication successful!{Style.RESET_ALL}\n")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}✗ Authentication cancelled.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}✗ Authentication failed: {e}{Style.RESET_ALL}")
        sys.exit(1)

# Request sudo for sensitive operations
if needs_sudo() and len(sys.argv) > 1:
    request_sudo_password()

# Email Credentials
# You can add more email accounts here by following the same format
# Replace the example credentials with your actual email credentials

EMAIL_ACCOUNTS = { # directly added to the dict.
    '1': {
        'user': 'rangersmyth.74@gmail.com',   # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'rhvyqknrnatoxetv'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    },
    '2': {
        'user': 'david.keane.1974@gmail.com', # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'vpalbyubhfheoesl'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    },
    '3': {
        'user': 'proxybusterburg@gmail.com', # Example - REPLACE WITH YOUR ACTUAL CREDENTIALS
        'pass': 'hgotecaahndqinnf'      # Example - REPLACE WITH YOUR ACTUAL PASSWORD
    }
}

# Gmail Email Credentials - Google Less Secure App Passwords
# Go here to get yours @ https://myaccount.google.com/apppasswords

# Email ASCII Art

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
    pass  # This line is crucial to actually display the ascii art

# This is the banner for the bot
def banner():
    Banner = r"""
            ____  ___    _   __________________       _____ __  _____  __________  __
           / __ \/   |  / | / / ____/ ____/ __ \     / ___//  |/  /\ \/ /_  __/ / / /
          / /_/ / /| | /  |/ / / __/ __/ / /_/ /_____\__ \/ /|_/ /  \  / / / / /_/ /
         / _, _/ ___ |/ /|  / /_/ / /___/ _, _/_____/__/ / /  / /   / / / / / __  /
        /_/ |_/_/  |_/_/ |_/\____/_____/_/ |_|     /____/_/  /_/   /_/ /_/ /_/ /_/
"""
    print(Banner)  # This line is crucial to actually display the banner

def bunny():
    print(r"""
            % 💀

           /\ /|
          |||| |
           \ | \
       _ _ /  ()()
     /    \   =>*<=
   /|      \   /
   \|     /__| |
     \_____) \__)


I hope this helps!% 💀
    """)


# Display settings for email previews
# You can adjust these settings to change the appearance of the email previews

DISPLAY_SETTINGS = {
    'max_subject_length': 50,
    'max_preview_length': 100,
    'email_separator': '\n' + '-' * 80 + '\n',
    'body_width': 70
}

# --- Colors --- # 
# This is the color scheme for the script
# You can customize the colors by changing the values here

GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
NC = '\033[0m'

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print welcome banner
# Welcome message only shown in interactive mode (handled in main)

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
            print(Fore.BLUE + "\nExiting. See you next time!\n" + Style.RESET_ALL)
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
            if not messages or not messages[0]:
                print("No emails found.")
                return
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
                bunny()
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number or type 'back'." + Style.RESET_ALL)
            bunny()

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
        bunny()
    except smtplib.SMTPException as e:
        print(Fore.RED + f"Failed to send email: {e}" + Style.RESET_ALL)
        bunny()

def test_connection():
    """Test connection to Gmail servers."""
    print(Fore.CYAN + "\n===== CONNECTION TEST =====" + Style.RESET_ALL)

    # Test IMAP
    print(f"\n{Fore.YELLOW}Testing IMAP (imap.gmail.com:993)...{Style.RESET_ALL}")
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com", 993) as mail:
            print(f"{Fore.GREEN}✓ IMAP connection successful{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ IMAP connection failed: {e}{Style.RESET_ALL}")

    # Test SMTP
    print(f"\n{Fore.YELLOW}Testing SMTP (smtp.gmail.com:587)...{Style.RESET_ALL}")
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print(f"{Fore.GREEN}✓ SMTP connection successful{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ SMTP connection failed: {e}{Style.RESET_ALL}")

    # Test DNS
    print(f"\n{Fore.YELLOW}Testing DNS resolution...{Style.RESET_ALL}")
    try:
        ip = socket.gethostbyname('gmail.com')
        print(f"{Fore.GREEN}✓ DNS resolution successful (gmail.com -> {ip}){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ DNS resolution failed: {e}{Style.RESET_ALL}")

    print()

def list_accounts():
    """List all configured email accounts."""
    print(Fore.CYAN + "\n===== CONFIGURED ACCOUNTS =====" + Style.RESET_ALL)
    for key, account in EMAIL_ACCOUNTS.items():
        user = account['user']
        # Mask the password
        masked_pass = account['pass'][:4] + '*' * 8 + account['pass'][-4:]
        print(f"{Fore.GREEN}{key}. {user}{Style.RESET_ALL}")
        print(f"   App Password: {masked_pass}")
    print()

def quick_check(account_num, unseen_only=True):
    """Quick check emails for a specific account."""
    global EMAIL_USER, EMAIL_PASS

    if account_num not in EMAIL_ACCOUNTS:
        print(f"{Fore.RED}Invalid account number. Use --accounts to see available accounts.{Style.RESET_ALL}")
        return

    EMAIL_USER = EMAIL_ACCOUNTS[account_num]['user']
    EMAIL_PASS = EMAIL_ACCOUNTS[account_num]['pass']

    print(f"{Fore.CYAN}Checking {'new' if unseen_only else 'all'} emails for {EMAIL_USER}...{Style.RESET_ALL}\n")
    fetch_emails(unseen=unseen_only)

def quick_send(account_num, to_email, subject, body):
    """Quick send email from CLI."""
    global EMAIL_USER, EMAIL_PASS

    if account_num not in EMAIL_ACCOUNTS:
        print(f"{Fore.RED}Invalid account number. Use --accounts to see available accounts.{Style.RESET_ALL}")
        return

    EMAIL_USER = EMAIL_ACCOUNTS[account_num]['user']
    EMAIL_PASS = EMAIL_ACCOUNTS[account_num]['pass']

    print(f"{Fore.CYAN}Sending email from {EMAIL_USER}...{Style.RESET_ALL}\n")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(Fore.GREEN + "✓ Email sent successfully!" + Style.RESET_ALL)
    except smtplib.SMTPException as e:
        print(Fore.RED + f"✗ Failed to send email: {e}" + Style.RESET_ALL)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gmail Email Client v3.0 - A powerful CLI email client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
================================================================================
                           GMAIL EMAIL CLIENT v3.0
================================================================================

QUICK START:
  gmail                                Launch interactive menu
  gmail --accounts                     List configured accounts
  gmail --check 1                      Check new emails (account 1)
  gmail --check-all 1                  Check all emails (account 1)
  gmail --test                         Test Gmail server connection

--------------------------------------------------------------------------------
ACCOUNT MANAGEMENT:
--------------------------------------------------------------------------------
  --accounts              List all configured Gmail accounts
                          Shows email addresses and masked app passwords

  --test                  Test connection to Gmail IMAP/SMTP servers
                          Useful for troubleshooting connection issues

--------------------------------------------------------------------------------
CHECK EMAILS:
--------------------------------------------------------------------------------
  --check ACCOUNT         Check NEW (unread) emails only
                          Example: gmail --check 1

  --check-all ACCOUNT     Check ALL emails (including read)
                          Example: gmail --check-all 2

--------------------------------------------------------------------------------
SEND EMAILS:
--------------------------------------------------------------------------------
  --send ACCOUNT          Send email (interactive prompts)
                          Example: gmail --send 1

  --quick-send            Send email with all parameters
                          Example: gmail --quick-send 1 "to@email.com" "Subject" "Body"

--------------------------------------------------------------------------------
CONFIGURED ACCOUNTS:
--------------------------------------------------------------------------------
  1. Ranger Smyth     (rangersmyth.74@gmail.com)
  2. David Keane      (david.keane.1974@gmail.com)
  3. Proxy Busterburg (proxybusterburg@gmail.com)

--------------------------------------------------------------------------------
INTERACTIVE MENU (when run without arguments):
--------------------------------------------------------------------------------
  1. Check new emails      - Fetch only unread emails
  2. Check older emails    - Fetch all emails
  3. Send an email         - Compose and send email
  4. Back to accounts      - Switch to different account
  0. Exit                  - Exit the program

--------------------------------------------------------------------------------
SETUP INSTRUCTIONS:
--------------------------------------------------------------------------------
  1. Go to: https://myaccount.google.com/apppasswords
  2. Generate an App Password for "Mail"
  3. Add credentials to EMAIL_ACCOUNTS in this script
  4. Run: gmail --test (to verify connection)

--------------------------------------------------------------------------------
TIPS:
--------------------------------------------------------------------------------
  * Use App Passwords, NOT your regular Gmail password
  * Run --test first to verify your connection works
  * Use --check for quick inbox preview
  * The script auto-installs missing packages (colorama, psutil)

================================================================================
        """
    )

    # Account & Connection
    conn_group = parser.add_argument_group('Account & Connection')
    conn_group.add_argument('--accounts', action='store_true',
                           help="List all configured Gmail accounts")
    conn_group.add_argument('--test', action='store_true',
                           help="Test connection to Gmail servers")

    # Check Emails
    check_group = parser.add_argument_group('Check Emails')
    check_group.add_argument('--check', metavar='ACCOUNT',
                            help="Check NEW emails for account (1, 2, or 3)")
    check_group.add_argument('--check-all', metavar='ACCOUNT',
                            help="Check ALL emails for account")

    # Send Emails
    send_group = parser.add_argument_group('Send Emails')
    send_group.add_argument('--send', metavar='ACCOUNT',
                           help="Send email interactively")
    send_group.add_argument('--quick-send', nargs=4,
                           metavar=('ACCOUNT', 'TO', 'SUBJECT', 'BODY'),
                           help="Send email with all parameters")

    # Easter Eggs
    easter_group = parser.add_argument_group('Easter Eggs')
    easter_group.add_argument('--bunny', action='store_true',
                             help="🐰 A surprise awaits...")

    return parser.parse_args()

def main():
    try:
        while True:
            clear_screen()
            select_account()
            while True:
                show_menu()
                choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
                if choice == '0':
                    print(Fore.BLUE + "\nExiting. See you next time!\n" + Style.RESET_ALL)
                    bunny()
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
                    bunny()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nProgram interrupted. Exiting gracefully." + Style.RESET_ALL)
        bunny()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        print(Fore.RED + f"\nAn unexpected error occurred. Please check the log file for details." + Style.RESET_ALL)
        bunny()

def rainbow_bunny():
    """Display a rainbow-colored bunny!"""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    bunny_art = r"""
           /\ /|
          |||| |
           \ | \
       _ _ /  ()()
     /    \   =>*<=
   /|      \   /
   \|     /__| |
     \_____) \__)
    """
    print()
    lines = bunny_art.split('\n')
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(f"{color}{line}{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}🐰 Bunny says: 'You've got mail... probably!' 🐰{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   Easter egg found! You're awesome!{Style.RESET_ALL}\n")

def cli_main():
    """Main entry point with CLI argument handling."""
    args = parse_args()

    # Handle CLI arguments
    if args.bunny:
        rainbow_bunny()
    elif args.accounts:
        list_accounts()
    elif args.test:
        test_connection()
    elif args.check:
        quick_check(args.check, unseen_only=True)
    elif args.check_all:
        quick_check(args.check_all, unseen_only=False)
    elif args.send:
        global EMAIL_USER, EMAIL_PASS
        if args.send in EMAIL_ACCOUNTS:
            EMAIL_USER = EMAIL_ACCOUNTS[args.send]['user']
            EMAIL_PASS = EMAIL_ACCOUNTS[args.send]['pass']
            print(f"{Fore.CYAN}Sending from: {EMAIL_USER}{Style.RESET_ALL}\n")
            send_email()
        else:
            print(f"{Fore.RED}Invalid account. Use --accounts to see available accounts.{Style.RESET_ALL}")
    elif args.quick_send:
        account, to_email, subject, body = args.quick_send
        quick_send(account, to_email, subject, body)
    else:
        # No CLI args - launch interactive menu
        main()

if __name__ == "__main__":
    cli_main()
    
