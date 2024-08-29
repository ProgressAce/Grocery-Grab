# Grocery List API

A back-end API for managing shared grocery lists for households. The API allows users to create, update, and share grocery lists with their household members, ensuring a collaborative approach to managing household needs.

## Features
* User Authentication & Authorization: Secured login and registration using Flask-Login. Users can register, confirm their email, reset passwords, and log in securely.
* Household Management: Users can create or join households, enabling shared grocery lists among members. Household admins can manage membership.
* Shared Grocery Lists: Real-time updates to grocery lists that are accessible to all household members. Items can be added, updated, marked as bought, or deleted.
* Email Notifications: Users receive email notifications for actions like account registration and password resets using Flask-Mail and MailHog for local development.

Technologies Used

* Python: Main programming language for backend logic.
* Flask: Web framework used to create the API.
* Flask-Login: Manages user session and authentication.
* Flask-Mail: Sends email notifications to users.
* MongoEngine: ODM (Object Document Mapper) for MongoDB, used for data modeling.
* MongoDB: NoSQL database for storing user and household data.
* MailHog: To capture emails in the development environment.

### Setup

    Clone the repository:

    bash

git clone https://github.com/yourusername/grocery-list-api.git
cd grocery-list-api

### Install dependencies:

bash

pip install -r requirements.txt

Configuration:

    Create a .env file based on .env.example with your environment variables (like SECRET_KEY, MAIL_SERVER, etc.).
    Configure the application settings in config.py.

Run the application:

bash

    python app.py

    Access the API: The API will be available at http://127.0.0.1:5000.

## Testing

Run tests using pytest to ensure all functionalities work as expected:

bash

pytest

### Next Steps

    Integrate a production-ready WSGI server like Gunicorn.
    Expand API features based on user feedback and additional requirements.
    Improve security by aligning more closely with OWASP guidelines.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
### License

This project is licensed under the MIT License.
