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

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = "user@gmail.com"
# Chose folder below
# EMAIL_FOLDER = "INBOX"
# EMAIL_FOLDER = '"[Gmail]/Sent Mail"' # note the double quoting
EMAIL_FOLDER = '"[Gmail]/All Mail"'
OUTPUT_DIRECTORY = '/tmp/mails'

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
        # Write filename as mail number, from, and subject line
        f = open('%s/%s--%s--%s.eml' %(OUTPUT_DIRECTORY, num, from_m, subject), 'wb')
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

