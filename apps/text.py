import os
from twilio.rest import Client


def send_text_message(from_number, to_number, message):
    """
    Sends a text message using Twilio API.

    :param from_number: Twilio phone number to send message from
    :param to_number: Phone number to send message to
    :param message: Message to send
    """
    # Get Twilio account credentials from environment variables
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    # Send the text message
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

    # Print the message SID
    print("Message SID:", message.sid)

# Get the phone numbers and message from the user
from_number = input("Enter your Twilio phone number: ")
to_number = input("Enter the recipient's phone number: ")
message = input("Enter the message to send: ")

# Send the text message
send_text_message(from_number, to_number, message)
