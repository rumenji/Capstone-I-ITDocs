# CapstoneTicketingApp

This project is about creating a web application that allows help desk users to keep track of issues by creating tickets, and activity logs for each ticket.
The app also has metrics that will be displayed on the dashboard homepage.


[App Screenshot Tickets](/Documentation/Tickets_list.png)
[App Screenshot Dashboard](/Documentation/Dashboard.png)


## Get Started

### Prerequisites

[Requirements](/requirements.txt)

  - Python 3.12
  - Pip
  - Virtualenv
  - Flask 3.0.0
  - Flask-SQLAlchemy 3.1.1
  - Flask-Bcrypt 1.0.1
  - Flask-WTF 1.2.1
  - Flask-Uploads 0.2.1
  - mailjet-rest 1.3.4

### Installation


  1. Clone the repository: `git clone`
  2. Create a virtual environment : `python3 -m venv venv`
  3. Activate the virtual environment: `source venv/bin/activate`
  4. Install dependencies: `pip3 install -r requirements.txt`
  5. Run app

### Main Features

- Create tickets for logged issues
- Send email notifications at ticket creation and following activities
/ability to resend notifications on failure/
- Add ticket activities to each ticket
- Add time spent to each activity - a total for the ticket is displayed
- Two user types - admin and standard
- Settings menu for admins - create entries for:
1. Users
2. Contacts
3. Locations
4. Ticket types, priorities, statuses
5. Configuration statuses and configurations
- Standard users can add tickets and activites, as well as add contacts.
- Dashboard with metrics - provides statistics for:
1. Tickets logged today, MTD, YTD, open tickets
2. Line chart for tickets per month YTD
3. Pie chart for tickets per status - open/closed YTD
4. Bar chart for tickets per assignee, and per status YTD

### Project Proposal

- [Project propsal](/Documentation/project_proposal_mentor.md)

### Project Management

- [Project Board](https://github.com/rumenji/Capstone1Personal/projects?query=is%3Aopen) 
- [List of Issues](https://github.com/rumenji/Capstone1Personal/issues)

### Live Demo

- [Live Demo](https://itdocs.onrender.com)
Demo username: admin
Demo password: Testtest!

### Author

Rumen Ivanov
[LinkedIn](https://www.linkedin.com/in/rumen-ivanov-it/)
