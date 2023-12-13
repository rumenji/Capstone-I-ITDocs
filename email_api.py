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
def send_mail(ticket):
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