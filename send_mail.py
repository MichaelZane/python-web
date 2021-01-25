import smtplib
from email.mime.text import MIMEText

def send_mail(email, name, phone, select_game, time_played, comments):

    smtp_server ='smtp.mailtrap.io'
    port = 2525
    login = '3bd9f4b09820e7'
    password = '0d074f1b22418d'
    message=f"<h3>New feedback</h3><ul><li>Email: {email}</li><li>Name: {name}</li><li>Phone: {phone}</li><li>Select Game: {select_game}</li><li>Time Played: {time_played}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'from@example.com'
    receiver_email = 'to@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Social Game Poker Club '
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email

    with smtplib.SMTP(smtp_server, port) as server:

        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())