# Requirements and Analysis

After taking with the client they discussed the following need. 

*Client:* "I want to be able to track my spending, manage my expenses and create a budget to help me keep my savings and spending under control.

*Project Manager (PM):* So, will this be for your own purposes or do you want this to work for many people?

*Client:* Just for me, but I do want the information secure so that people cannot see my savings or spending. 

*PM:* Did you want a secure log in or are you ok with anyone who has access to you computer to have access?

*Client:* I live in a share house so I need it password protected so my flatmate who uses my laptop sometime cannot access it

---- 
There are many other questions that can be asked during a meeting with the client when getting requirements for developing a piece of software. It is not always about a building a stand alone application. It could be you (the PM or developer) talking to the business team about a new feature or you in a meeting with a major client to extend an existing application.

## Gathering Requirements

When gathering requirements, it is important to understand what the client needs and how they want to use the software. This can be done through meetings with stakeholders, interviews, surveys, and other methods of communication.

When trying to gather functional and non-functional requirements from stakeholders, you should ask the following types of questions:


1. **What are the key features of the system?**
	* What functionality do users expect?
	* How will the system interact with other systems or data sources?
2. **How will users interact with the system?**
	* What interfaces (e.g., web, mobile, desktop) will be used?
	* What types of input and output will be required?
3. **What data will be collected, stored, and processed?**
	* Types of data (e.g., user information, transactional data)
	* Data formats (e.g., CSV, JSON, XML)
4. **How will the system handle different scenarios?**
	* What happens in case of errors or exceptions?
	* How will the system handle multiple users or concurrent access?
5. **What are the business rules and logic?**
	* Are there any specific calculations or algorithms required?

## Non-Functional Requirements:

1. **Performance requirements**
	* Response time for different actions (e.g., login, data retrieval)
	* Throughput for high-volume transactions
2. **Security requirements**
	* Authentication and authorization mechanisms
	* Data encryption and access control
3. **Availability and reliability requirements**
	* Uptime targets (e.g., 99.9%)
	* Recovery time objectives (RTOs) in case of failures
4. **Scalability and maintainability requirements**
	* How will the system grow with increased usage or data?
	* What are the plans for future development and enhancements?
5. **User experience and accessibility requirements**
	* Are there any specific user interface or usability requirements?

## Additional Questions:

1. **What are the business goals and objectives?**
	* How will the software contribute to these goals?
2. **Who is the target audience?**
	* What are their needs, preferences, and pain points?
3. **Are there any regulatory or compliance requirements?**
	* e.g., GDPR, HIPAA, PCI-DSS
4. **What is the budget and timeline for development?**
	* Are there any constraints or dependencies on other projects?

## Why Ask Questions?

Asking questions helps you:

1. Clarify stakeholder expectations
2. Identify potential risks or roadblocks
3. Gather necessary information for feasibility studies and estimates
4. Develop a shared understanding of the project requirements

Remember to take detailed notes, ask follow-up questions, and document all discussions to ensure that you have a thorough understanding of the functional and non-functional requirements.


## Functional Requirements:

1. **User Authentication**: The system should allow a user to register and log in using their email and password.
2. **Expense Tracking**: The user should be able to add, edit, and delete expenses, including:
	* Date and amount
	* Category (e.g., food, transportation, entertainment)
	* Description
3. **Category Management**: The system should allow the user to create and manage categories for their expenses.
4. **Budgeting**: The user should be able to set a budget for each category and track their spending against it.
5. **Reporting**: The system should provide reports on:
	* Total expenses by category
	* Expenses by date
	* Budget vs. actual spending
6. **Data Export**: The user should be able to export their expense data in CSV or PDF format.

## Non-Functional Requirements:

1. **Security**: The system should ensure that user data is secure and protected from unauthorised access.
2. **User Experience**: The system should provide a user-friendly interface for adding, editing, and deleting expenses.
3. **Scalability**: The system should be able to handle a single user with many expenses and accounts without performance issues.
4. **Data Integrity**: The system should ensure that expense data is accurate and consistent.

## Technical Requirements:

1. **Backend**: The system should use Python as the backend language, with Flask or Django as the web framework.
2. **Frontend**: The system should use JavaScript as the frontend language, with React or Angular as the framework.
3. **Database**: The system should use a relational database management system (RDBMS) like MySQL or PostgreSQL to store user data and expense information.
4. **API Integration**: The system should allow integration with external APIs for payment gateway services.

## User Stories:

1. As a registered user, I want to be able to add new expenses so that I can track my spending.
2. As a registered user, I want to be able to edit existing expenses so that I can correct errors or update information.
3. As a registered user, I want to be able to delete expenses so that I can remove unnecessary entries.
4. As a registered user, I want to be able to view my expense reports so that I can see my spending patterns and make informed decisions.

## Acceptance Criteria:

1. The system should allow a user to add new expenses with the required information (date, amount, category, description).
2. The system should display a list of all added expenses, including their date, amount, category, and description.
3. The system should allow a user to edit existing expenses by updating their date, amount, category, or description.
4. The system should allow a user to delete existing expenses.
5. The system should generate reports on total expenses by category, expenses by date, and budget vs. actual spending.

You can see how these requirements are structured using project tracking software at the following link: [Project](https://github.com/orgs/KillarneyHeightsHS/projects/2)

[< Prev: README](../README.md) | [Next: Design >](./design.md)