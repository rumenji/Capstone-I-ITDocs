# Project Proposal

This project is about creating a web application that allows help desk users to keep track of issues by creating tickets, and activity logs for each ticket.
The app also has metrics that will be displayed on the dashboard homepage.

## Goal

- A web application that allows help desk users to create support tickets and log activities. 
- The app will provide statistics about the issues and time logged. 
- The app will keep track of the clients.
- There will be two user types - admin and standard, with the admin being able to set the app for the standard users.

## User Profile

There'll be two users type:
- Admin
  - Admin can create, update, and delete setting types, like ticket priority, status, and type; configurations status, and configurations.
  - Admin can create, update, and delete users.
- Regular users
  - Regular users can create, update, and log activites for tickets.
  - Regular users can view tickets created by other users.
  - Regular users can view the dashboard.

## Data / API Information

The data will be logged by the help desk users.
Admins will have to set up the app for the users beforehand.
External API will be used to send email notifications to clients, and a copy to the assigned employee.

## Methodologies

### Tech Stack

- Python
- Flask
- JavaScript
- jQuery
- CSS
- Bootstrap
- Flask-SQLAlchemy
- WTF-Forms
- Bcrypt
- Bokeh

### Database Schema

[Entity Relationship Diagram](InitialProjectRequirements/DatabaseDiagram.jpeg)

- DB design assumptions:

  - A user can create many tickets.
  - A user can be assigned to many tickets.
  - A ticket can have many ticket activities.
  - A ticket can have only one status, priority, or type.
  - A ticket can have only one contact/client, or configuration /the device the issue refers to/.

### Security

  - User passwords will be hashed using bcrypt library.
  - User passwords will be validated using the bcrypt library.

- Sensitive information that needs to be protected:

  - User passwords
  - User email addresses
  - User email addresses

## Features


MUST-HAVE

| Feature | Estimated Time | Actual Time |
| ------- | -------------- | ----------- |
| Create tickets for logged issues       |  10 hrs          | 13 hrs       |
| Send email notifications at ticket creation | 2 hrs | 1 hr |
| Add ticket activities to each ticket | 5 hrs | 3.5 hrs |
| Add time spent to each activity and a total for the ticket | 2 hrs | 1.75 hrs |
| Two user types - admin and standard | 2 hrs | 1.5 hrs |
| Settings menu for admins | 10 hrs | 11 hrs |
| Dashboard with metrics | 10 hours | 14 hrs |


SHOULD-HAVE

| Feature | Estimated Time | Actual Time |
| ------- | -------------- | ----------- |
| Allow resending notificaiton for email failure| 1 hr | 1 hr |


COULD-HAVE

| Feature | Estimated Time | Actual Time |
| ------- | -------------- | ----------- |
| Part with support and KB articles to attach to tickets     | 10 hrs          |        |
| Part with more in-depth documentation for the support matter - like IT equipment, etc. | 15 hrs | |

MORE THAN CRUD FEATURES

| Feature | Estimated Time | Actual Time |
| ------- | -------------- | ----------- |
| Dashboard with metrics/statistics about tickets per date/range/assignee | 10 hours | 14 hrs |

### Tasks

Reference to the project board and issues:

[Project Board][https://github.com/rumenji/Capstone1Personal/projects?query=is%3Aopen](https://github.com/rumenji/Capstone1Personal/projects?query=is%3Aopen)
[List of Issues][https://github.com/rumenji/Capstone1Personal/issues](https://github.com/rumenji/Capstone1Personal/issues)

**New issue checklist:**

1. Enter Task title & Task Code
2. Enter Task description: enter requirement of the task and what needs to be done to complete the task.
3. Label the issue
4. Add story points label
5. Assign the task


**Story Points reference:**

| Story Points | Description                                                                                                                                                                                                              |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1            | Very simple / trivial task, you can do it in (max) 1 hour                                                                                                                                                                |
| 2            | Simple / decent / not too difficult task, you can do it (max) a day                                                                                                                                                      |
| 3            | Difficult task, you’re not immediately sure of how to solve it, needs some further research, but you know the underlying concept on how to solve it.                                                                     |
| 5            | Difficult complex task, requires extensive research, a lot of features combined into one ticket. This will not be a story / task, this will be something more of an Epic ticket.  **Needs to be broken into smaller tasks.** |

## User Flow Diagram


[User Flow Diagram](InitialProjectRequirements/Cap1UserFlow.png)



## Challenges & Risk Mitigation


| Challenges     | Risk Mitigation Plan / Strategy |
| -------------- | ------------------------------- |
| API down       | Alert users that the email is not successfully sent, and allow them to resend |
| Securing user passwords       | Hashing the passwords with Bcrypt |

## Out of Scope


- Will not have detailed permissions settings and levels of access.
- Will not have reporting other than the Dashboard statistics.
- Will not have support and KB articles available within the app.
