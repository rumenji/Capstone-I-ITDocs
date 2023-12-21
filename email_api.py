import os
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

"""
Import the external API /MailJet/ library for sending emails.
Imports API credentials from the .env file
Sends emails for new tickets and ticket activity updates
"""

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')

def send_mail_ticket(ticket):
    # Send new ticket notifications. Checks if there is an assignee to the ticket - then adds their email as BCC
    assignee = ticket.user
    contact = ticket.contact
    ticket_title = ticket.title
    ticket_notes = ticket.notes
    if ticket.user:
        bcc = f'"Bcc": [{{"Email": "{assignee.email}","Name": "{assignee.first_name} {assignee.last_name}"}}],'
        print(bcc)
    else:
        bcc = ''

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": f"{SENDER_EMAIL}",
                                    "Name": "IT Docs"
                            },
                            "To": [
                                    {
                                            "Email": f"{contact.email}",
                                            "Name": f"{contact.first_name} {contact.last_name}"
                                    }
                            ],
                            f"{bcc}"
                            "Subject": f"Ticket # {ticket.id} has been successfully created",
                            "TextPart": "Greetings from IT Docs!",
                            "HTMLPart": f"Ticket number {ticket.id} for {ticket_title} has been successfully created: {ticket_notes}"
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


def send_mail_activity(ticket_activity):
    # Sends ticket activity notification updates
    assignee = ticket_activity.user
    contact = ticket_activity.ticket.contact
    ticket_notes = ticket_activity.notes
    
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": f"{SENDER_EMAIL}",
                                    "Name": "IT Docs"
                            },
                            "To": [
                                    {
                                            "Email": f"{contact.email}",
                                            "Name": f"{contact.first_name} {contact.last_name}"
                                    }
                            ],
                            "Bcc": [
                                    {
                                            "Email": f"{assignee.email}",
                                            "Name": f"{assignee.full_name}"
                                    }
                            ],
                            "Subject": f"Ticket # {ticket_activity.ticket.id} has been updated",
                            "TextPart": "New activity on your support ticket",
                            "HTMLPart": f"Ticket number {ticket_activity.ticket.id} for {ticket_activity.ticket.title} has been updated: {ticket_notes}"
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code