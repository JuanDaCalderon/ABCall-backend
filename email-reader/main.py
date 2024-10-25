from os import environ
from imap_tools import MailBox, AND
import sys
import imap_tools
import requests
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv('.env.incidentes.email')
loaded = load_dotenv(env_file)

username = environ.get("EMAIL") if environ.get(
    "EMAIL") is not None and environ.get("EMAIL") != "" else "miso.proyfinal.g1@gmail.com"
password = environ.get("PASSWORD") if environ.get(
    "PASSWORD") is not None and environ.get("PASSWORD") != "" else "kiwt syiq cdxq ybrb"
server_mail = environ.get("SERVER") if environ.get(
    "SERVER") is not None and environ.get("SERVER") != "" else "imap.gmail.com"
trigger_string = environ.get("TRIGGER") if environ.get(
    "TRIGGER") is not None and environ.get("TRIGGER") != "" else "[INCIDENTE]"
crear_incidente_url = environ.get("CREAR_INCIDENTE_ENDPOINT") if environ.get(
    "CREAR_INCIDENTE_ENDPOINT") is not None and environ.get("CREAR_INCIDENTE_ENDPOINT") != "" else 'http://localhost:8000/incidente/email'

print('********************************************************************************************************')
print('username->', username, '   '
      'password->', password, '   '
      'server_mail->', server_mail, '   '
      'trigger_string->', trigger_string, '   '
      'crear_incidente_url->', crear_incidente_url)
print('********************************************************************************************************')

mailbox = MailBox(server_mail)
mailbox.login(username, password, 'INBOX')
done = False
while not done:
    try:
        response = mailbox.idle.wait(timeout=5)
        uids = []
        requestBody = {}
        for msg in mailbox.fetch(AND(seen=False), mark_seen=False):
            subject = msg.subject
            body = msg.text or msg.html
            from_ = msg.from_
            if trigger_string.lower() in subject.lower():
                uids.append(msg.uid)
                correo = from_.strip()
                data = body.strip().replace("\r\n", "").split(',')
                requestBody = {
                    "correo": correo,
                    "prioridad": "media",
                    "estado": "abierto",
                    "canal": "email",
                    "tipo": "incidente"
                }
                for property in data:
                    prop = property.replace("[", "").replace("]", "")
                    key = prop.split(':')[0]
                    value = prop.split(':')[1]
                    requestBody[key] = value
                response = requests.post(crear_incidente_url, json=requestBody)
                print(requestBody, '-------', response.json())
        mailbox.flag(uids, imap_tools.MailMessageFlags.SEEN, True)
    except KeyboardInterrupt:
        done = True
    except:
        done = True

mailbox.logout()
sys.exit()
