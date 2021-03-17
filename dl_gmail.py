#!/usr/bin/env python
#
# Adapted from https://gist.github.com/robulouski/7442321
# Very simple Python script to dump all emails in an IMAP folder to files.  
# This code is released into the public domain.
#

import sys
import imaplib
import getpass
import email
import os

IMAP_SERVER = 'imap.gmail.com'

# Set email here or pass it as first argument
EMAIL_ACCOUNT = ""
if not EMAIL_ACCOUNT:
    EMAIL_ACCOUNT = str(sys.argv[1])

# Chose folder below
# EMAIL_FOLDER = "INBOX"
# EMAIL_FOLDER = '"[Gmail]/Sent Mail"' # note the double quoting
EMAIL_FOLDER = '"[Gmail]/All Mail"'

# Download emails into current directory or set a custom path on cmdline
if len(sys.argv) > 2:
    OUTPUT_DIRECTORY = str(sys.argv[2])
else:
    OUTPUT_DIRECTORY = os.getcwd()

# Set password here or the script will get it from cmd line
PASSWORD = ""
if not PASSWORD:
    PASSWORD = getpass.getpass()


def process_mailbox(M):
    """
    Dump all emails in the folder to files in output directory.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print ("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)
        from_m = mail["From"]
        subject = mail["Subject"]
        if rv != 'OK':
            print("ERROR getting message", subject)
            return
        print("Writing message ", subject)
        # Write filename as mail number, from, and subject line; delete forward slash to
        # prevent interpreting subject as a file path
        f = open(f'{OUTPUT_DIRECTORY}/{num.decode("utf-8")}--{from_m}--{subject.replace("/","")}.eml', 'wb')
        f.write(data[0][1])
        f.close()

def main():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox: ", EMAIL_FOLDER)
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)
    M.logout()

if __name__ == "__main__":
    main()

