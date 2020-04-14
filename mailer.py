import smtplib
from datetime import date
from credentials import CREDENTIALS

u = CREDENTIALS.get("PROPERTIES_USER")
p = CREDENTIALS.get("PROPERTIES_PASSWORD")
mailing_list = CREDENTIALS.get("MAILING_LIST")


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(u, p)
        message = f'Subject: {subject} \n\n {msg}'

        for mail in mailing_list:
            server.sendmail(u, mail, message)
        server.quit()

        print("Success")
    except Exception as e:
        with open("error_log.txt", "a+") as f:
            f.write(str(e) + "\n")



if __name__ == "__main__":
    with open("current_data.txt", "r") as f:
        msg = f.read()

    subject = f'Boligpriser {str(date.today())}'
    with open("error_log.txt", "a+") as f:
        f.write(subject + "\n")
        f.write(msg + "\n")
    send_email(subject, msg)





