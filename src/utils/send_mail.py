import smtplib
import codecs
import email.message
from starlette.config import Config
from bs4 import BeautifulSoup

templateMail = codecs.open("./templates/email_template.html", "r", "utf-8")
# create config password mail
config = Config('.env')

MAIL_PASSWORD: str = config("MAIL_PASSWORD")
MAIL: str = config("MAIL")

# create message object instance
msg = email.message.Message()


async def mail_send(email: str) -> str:
    soup = BeautifulSoup(templateMail, 'html.parser')
    strhtm: str = soup.prettify()

    # setup the parameters of the message
    password = MAIL_PASSWORD
    msg['From'] = MAIL
    msg['To'] = email
    msg['Subject'] = "Cadastro Feito - Cbank"

    # add in the message body
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(payload=strhtm)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

# Login Credentials for sending the mail
    s.login(msg['From'], password)

    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode("utf-8"))

    s.quit()
    print("successfully sent email to %s:" % (msg['To']))
