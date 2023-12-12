# Project Proposal

Use this template to help get you started right away! Once the proposal is complete, please let your mentor know that this is ready to be reviewed.

## Get Started

|            | Description                                                                                                                                                                                                                                                                                                                                              | Fill in |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| Tech Stack | What tech stack will you use for your final project? It is recommended to use the following technologies in this project: Python/Flask, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful APIs, JavaScript, HTML, CSS. Depending on your idea, you might end up using WTForms and other technologies discussed in the course.  | Will use Python/Flask, SQLAlchemy, RESTful APIs, JS, , WTForms, HTML, CSS, Bootstrap.                             |         
| Type       | Will this be a website? A mobile app? Something else?   | It will be a webapp.                                                                                                                                                                                                                                                                                                 |         
| Goal       | What goal will your project be designed to achieve?    | Help service desks keep track of issues, steps taken to resolve the issue, time needed to resolve the issue. Also keep track of which support user is assinged to each issue, and client details.                                                                                                                                                                                                                                                                                                 |         
| Users      | What kind of users will visit your app? In other words, what is the demographic of your users?                                                                                                                                                                                                                                                           |     The webapp will be used by help desk personel and managers    |
| Data       | What data do you plan on using? How are you planning on collecting your data? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. You are welcome to create your own API and populate it with data. If you are using a Python/Flask stack, you are required to create your own API. |    It will be an API specific to the app. The data will be entered by the webapp users - help desk personel will enter details about each issue into tickets. Same for the steps to resolve the issue.  An external API would be used to send email notifications to the assigned support employee and the client.   |
| DB schema | What does your DB schema look like | The DB would have tables for tickets, issue status, type, and priority related to tickets. A separate ticket activity table for adding steps to resolve for each ticket. Also users table - for the service desk users, and contacts table for clients. |
| Issues | What type of issues might you run into with your API | A possible issue could be with the external API setup to send emails out of the app |
| Sensitive information | Is there any sensitive information you need to secure? | Users passwords and emails, along with clients emails. Will use Bcrypt for user passwords |
| Functionality | What functionality will the app have? | Must-have: Store tickets containing the issue, and resolution steps. Should-have: Email notifications, Could-have: List of configurations that could go wrong to be selected in each ticket. Will not have: Part of the app with documentation and/or KB articles|
| User flow | What will the user flow look like?	| The user will have to log in. Only admin users can create new users, and change settings. Users will be able to view a list, and create new tickets, as well add resolution steps for each ticket. |
| More than CRUD | What features make your side more than CRUD? | Maybe the email notification part that will happen in the background when a ticket is saved or updated |

# Breaking down your project

When planning your project, break down your project into smaller tasks, knowing that you may not know everything in advance and that these details might change later. Some common tasks might include:

- Determining the database schema
- Sourcing your data
- Determining user flow(s)
- Setting up the backend and database
- Setting up the frontend
- What functionality will your app include?
  - User login and sign up
  - Uploading a user profile picture

Here are a few examples to get you started with. During the proposal stage, you just need to create the tasks. Description and details can be edited at a later time. In addition, more tasks can be added in at a later time.

| Task Name                   | Description                                                                                                   | Example                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Design Database schema      | Determine the models and database schema required for your project.                                           | [Link](https://github.com/hatchways/sb-capstone-example/issues/1) |
| Source Your Data            | Determine where your data will come from. You may choose to use an existing API or create your own.           | [Link](https://github.com/hatchways/sb-capstone-example/issues/2) |
| User Flows                  | Determine user flow(s) - think about what you want a user’s experience to be like as they navigate your site. | [Link](https://github.com/hatchways/sb-capstone-example/issues/3) |
| Set up backend and database | Configure the environmental variables on your framework of choice for development and set up database.        | [Link](https://github.com/hatchways/sb-capstone-example/issues/4) |
| Set up frontend             | Set up frontend framework of choice and link it to the backend with a simple API call for example.            | [Link](https://github.com/hatchways/sb-capstone-example/issues/5) |
| User Authentication         | Fullstack feature - ability to authenticate (login and sign up) as a user                                     | [Link](https://github.com/hatchways/sb-capstone-example/issues/6) |

## Labeling

Labeling is a great way to separate out your tasks and to track progress. Here’s an [example](https://github.com/hatchways/sb-capstone-example/issues) of a list of issues that have labels associated.

| Label Type    | Description                                                                                                                                                                                                                                                                                                                     | Example                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Difficulty    | Estimating the difficulty level will be helpful to determine if the project is unique and ready to be showcased as part of your portfolio - having a mix of task difficultlies will be essential.                                                                                                                               | Easy, Medium, Hard           |
| Type          | If a frontend/backend task is large at scale (for example: more than 100 additional lines or changes), it might be a good idea to separate these tasks out into their own individual task. If a feature is smaller at scale (not more than 10 files changed), labeling it as fullstack would be suitable to review all at once. | Frontend, Backend, Fullstack |
| Stretch Goals | You can also label certain tasks as stretch goals - as a nice to have, but not mandatory for completing this project.                                                                                                                                                                                                           | Must Have, Stretch Goal      |
