import keys
from twilio.rest import Client
account_sid = keys.account_sid
auth_token = keys.auth_token

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_= keys.twilio_number,
    body = "OTP is 111111",
    to=keys.my_number
)

print(message.sid)