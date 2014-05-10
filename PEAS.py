#-------------------------------------------------------------------------------
# Name:        PEAS
# Purpose:
#
# Author:      k3rn3l
#
# Created:     27-04-2014
# Copyright:   (c) k3rn3l 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import email
import getpass, imaplib
import os
import sys
from time import sleep
import postfile
import tempfile
import json

detach_dir = tempfile.gettempdir()
os.chdir(detach_dir)
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

host = "www.virustotal.com"
selector = "https://www.virustotal.com/vtapi/v2/file/scan"
fields = [("apikey", "1dc9f9084c25ab7603cb6d8cff2cb3326837ca56503e0d6853d34c08f2365068")]

userName = raw_input('Enter your GMail username:')
passwd = getpass.getpass('Enter your password: ')

try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)

    while 1:
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


        # Iterating over all emails
        for msgId in data[0].split():
            typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
            if typ != 'OK':
                print 'Error fetching mail.'
                raise

            emailBody = messageParts[0][1]
            mail = email.message_from_string(emailBody)
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    # print part.as_string()
                    continue
                if part.get('Content-Disposition') is None:
                    # print part.as_string()
                    continue

                fileName = part.get_filename()
                fileName=str(fileName).replace('=?utf-8?Q?', '')
                fileName=str(fileName).replace('?=', '')
                print fileName


                if bool(fileName):
                    filePath = os.path.join(detach_dir, 'attachments', fileName)
                    if not os.path.isfile(filePath) :
                        print fileName
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()


        attachmentPath = os.path.join(detach_dir, 'attachments')
        allFiles = os.listdir(attachmentPath)

        scanIds = []


        for fileName in allFiles:
            filePath = os.path.join(detach_dir, 'attachments', fileName)
            file_to_send = open(filePath, "rb").read()
            files = [("file", fileName, file_to_send)]
            json1 = postfile.post_multipart(host, selector, fields, files)
            jsonData = json.loads(json1)
            scanIds.append(jsonData['md5']) #Check for error here
            print scanIds




        sleep(20)
    imapSession.close()
    imapSession.logout()
except :
    print 'Not able to download all attachments.'