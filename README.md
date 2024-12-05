# Volunteers-platform
## Connecting Volunteers with Those in Need in the Naryn Region, Kyrgyzstan
# Overview
The Volunteers Platform bridges volunteer organizations and individuals in need within the Naryn region. 
* Organizations can register to access and manage aid requests.
* People in need can submit forms with details about their situation and required assistance.
This platform, powered by Django REST Framework (DRF), ensures efficient and scalable data handling.

# Features
* __User Registration__: RESTful APIs for volunteer organizations to sign up and log in.
* __Request Submission__: Endpoints for individuals to submit forms detailing their needs.
* __Request Management__: APIs for organizations to view, filter, and respond to requests.
* __Secure Authentication__: Token-based authentication for secure access to resources.
  
# Installation
## Prerequisites
* Python 3.8+
* Django 4.x
* Django REST Framework
* PostgreSQL or SQLite
  
## Steps
1) __Clone the repository:__
bash
Copy code
git clone https://github.com/Turarova/Volunteers-platform.git
2) __Navigate to the project directory:__
bash
Copy code
cd Volunteers-platform
3) __Install dependencies:__
bash
Copy code
pip install -r req.txt
4) __Apply migrations:__
bash
Copy code
python manage.py migrate
5) __Run the server:__
bash
Copy code
python manage.py runserver
# Technologies Used
* __Backend Framework:__ Django with Django REST Framework (DRF)
* __Database:__ PostgreSQL (configurable in settings.py)
  
# Future Plans
* Adding multilingual support.
* Implementing a notification system for urgent requests.
* Enhancing analytics for volunteer organizations.
  
# Contributing
We welcome contributions! Please open an issue or submit a pull request.
