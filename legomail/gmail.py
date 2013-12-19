# Gmail Function module for
# Raspberry Pi
#
# Author : Kris Wang
# email  : kris2808@gmail.com
# Date   : 8/12/2013
#
import email, getpass, imaplib, os

def save_voicemsg(att_path):

    user = '' # the user gmail address that receive message
    pwd = '' # the user gmail password
    sender = '' # the mail address that you send message from
    getmsg = False

    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("inbox") # here you a can choose a mail box like INBOX instead

    resp, items =  m.search(None, 'UNSEEN', 'FROM', sender)
    items = items[0].split() # get the mails' id

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail,
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content

        #Check if any attachments
        if mail.get_content_maintype() != 'multipart':
            continue

        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment
            if part.get('Content-Disposition') is None:
                continue
            
            # check if wav file(wait for implement)
            
            getmsg = True
            filename = part.get_filename()

            if os.path.isfile(att_path) :
                #remove the old msg
                os.remove(att_path)
                
            # finally write the content
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

            # delete the mail that attached is saved
            m.store(emailid, '+FLAGS', '\\Deleted')

    m.expunge()
    m.close()
    m.logout()
    return getmsg