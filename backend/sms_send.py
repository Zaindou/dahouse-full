from twilio.rest import Client
from config import Config

account_sid = Config.TWILIO_ACCOUNT_SID
auth_token = Config.TWILIO_AUTH_TOKEN
phone_number = Config.TWILIO_PHONE_NUMBER

client = Client(account_sid, auth_token)


def send_sms(number, message):
    message = client.messages.create(
        to=f"+57{number}", from_=f"{phone_number}", body=message
    )
    return message.sid
