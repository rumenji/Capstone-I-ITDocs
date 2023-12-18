import os
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

"""
Run:
"""

api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

SENDER_EMAIL = 'rumen.j.ivanov@gmail.com'
def send_mail_ticket(ticket):
    assignee = ticket.user
    contact = ticket.contact
    ticket_title = ticket.title
    ticket_notes = ticket.notes
    
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
                                            "Name": f"{assignee.first_name} {assignee.last_name}"
                                    }
                            ],
                            "Subject": f"Ticket # {ticket.id} has been successfully created",
                            "TextPart": "Greetings from IT Docs!",
                            "HTMLPart": f"Ticket number {ticket.id} for {ticket_title} has been successfully created: {ticket_notes}"
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code

def send_mail_activity(ticket_activity):
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