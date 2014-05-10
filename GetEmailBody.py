#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      k3rn3l
#
# Created:     10-05-2014
# Copyright:   (c) k3rn3l 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import email
import getpass, imaplib
import os
import sys
from time import sleep

import tempfile
import json

userName = raw_input('Enter your GMail username:')
passwd = getpass.getpass('Enter your password: ')

try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)


##        imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
##        typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print 'Not able to sign in!'
        raise

    imapSession.select('[Gmail]/All Mail')
    typ, data = imapSession.search(None, 'UNSEEN')
    print typ
    print data
    if typ != 'OK':
        print 'Error searching Inbox.'
        raise
    typ, messageParts = imapSession.fetch(116, '(RFC822)')

    emailBody = messageParts[0][1]
    mail = email.message_from_string(emailBody)
    for part in mail.walk():
        if part.get_content_type() == 'text/plain':
            print part.get_payload()
        else:
            part.get_content_type()


    imapSession.close()
    imapSession.logout()
except :
    print "Error"
##
##        # Iterating over all emails
##        for msgId in data[0].split():
##            typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
##            if typ != 'OK':
##                print 'Error fetching mail.'
##                raise
##
##            emailBody = messageParts[0][1]
##            mail = email.message_from_string(emailBody)
##            for part in mail.walk():
##                if part.get_content_maintype() == 'multipart':
##                    print part.as_string()
##                    continue
##                if part.get('Content-Disposition') is None:
##                    print part.as_string()
##                    continue
