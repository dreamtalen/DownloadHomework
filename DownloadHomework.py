# -*- coding: UTF-8 -*-
import pickle
import poplib  
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr 

def decode_str(s):
    if not s:
        return None
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def get_mails(keyword):
    with open('config.pk', 'r') as f:
        host, username, password = pickle.load(f)
      
    server = poplib.POP3(host)
    server.user(username)
    server.pass_(password)
    
    messages = [server.retr(i) for i in range(len(server.list()[1]), len(server.list()[1]) - 20, -1)]  
    messages = ['\r\n'.join(mssg[1]) for mssg in messages]  
    messages = [Parser().parsestr(mssg) for mssg in messages]  
    print("===="*10)
    messages = messages[::-1]
    for message in messages:  
        subject = message.get('Subject')
        subject = decode_str(subject)
        if subject and keyword in subject:
            value = message.get('From')
            if value:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
            print("Sender: %s" % value)
            print("Title:%s" % subject)
            for part in message.walk():  
                fileName = part.get_filename()  
                fileName = decode_str(fileName)
                if fileName:  
                    with open(fileName, 'wb') as fEx:
                        data = part.get_payload(decode=True) 
                        fEx.write(data)  
                        print("%s Downloaded" % fileName)
                        print("----"*10)
    server.quit()  

if __name__ == '__main__':
    keyword = input("Keyword:")
    get_mails(keyword)
