<h2>Retail Network API service</h2>

<h3>Main idea</h3>

Retail Network API service

It is necessary to implement a network model for selling electronics.
The network should be a hierarchical structure of 3 levels:

Factory;
Retail network;
Individual entrepreneur.
Each link in the network refers to only one equipment supplier (not necessarily the previous one in the hierarchy). It is important to note that the hierarchy level is determined not by the name of the link, but by its relationship to other elements of the network, i.e. The plant is always at level 0, and if the retail network relates directly to the plant, bypassing other links, its level is 1.

Each link in the network must have the following elements:
Name;
Contacts:
Email;
A country;
City;
Street;
House number;
Products:
Name;
Model;
Date of product launch on the market;
Supplier (the previous network object in the hierarchy);
Debt to the supplier in monetary terms, accurate to the nearest kopeck;
Creation time (filled in automatically upon creation).


<h3>What does this project do.</h3>

this project realise a service for handling selling network with API interface.
pls find additional information in file <h4>comments.pdf (comments.docx)</h4> 


This app was writen by kirill.s (aka Mr.K) in 2023.


<h3>How to prepare.</h3>
this project use next components:
- python as a base platform
- postgresql database - EXTERNAL


<h3>How to install.</h3>
- clone project to own disk in new directory
- activate virtual environment (python -m venv venv)
- install all needs packages (pip install -r requirements.txt)
- see next step for configure

<h3>How to configure.</h3>
Please pay your attention to configure .env file.
You can find example in root of your project directory (.env.example)
please fill all parameters with your data and save the changed file as .env

after that you need create empty database.
you may use command
>psql -U postgres;
>CREATE DATABASE <database_name>

or 
> createdb -U postgres <database_name>

alternatively you can use pgadmin or other interface app.

Use next commands for tables creation
>python manage.py migrate


Next step helps you create superuser user. With this user login you will be able to create and change timing for periodic tasks
>python manage.py createsuperuser

or
> python manage.py create_su
 
Congratulation, we are ready to start!

<h3>Ноw it works.</h3>

Start the server with
>python manage.py runserver

you will find API documentation for front-end connecting  
http://YOUR_HOST/swagger/ or 
http://YOUR_HOST/redoc/
use it with any browser what you like


Easy way for a work start in localhost:
- create new user: 
- http://localhost:8000/users/
POST {
        "email": "your@e.mail",
        "password": "your_password",
        "last_name": "Any",
        "telegram_username": "your_telegram_name"
    }
NOTE: your_telegram_name must be created in telegram app settings 
- take a token via 
- http://localhost:8000/users/token/ 
POST {
        "email": "your@e.mail",
        "password": "your_password"
    }
- add access token as Bearer for your next requests


- create a new Node

http://127.0.0.1:8000/nodes/create/
POST{
    "name": "Korean Retail",
    "node_type": 2,
    "contacts": 6, 
    "products": [3],
    "supplier_link": 5
}

-  view all nodes

http://127.0.0.1:8000/nodes/all/
GET

- view one node detail

http://127.0.0.1:8000/nodes/detail/<id>
DELETE

-etc  





if you want to test this app with little database which already have some data you be able to tap 
> python manage.py loaddata all_apps_full.json

Testing

To run the tests, ensure that you have pytest installed in your virtual environment. If you don't have it, you can install it using: pip install pytest pytest-django
Next, navigate to the root directory of your project and execute: <b>pytest</b>


For create docker image use:
build docker image
>docker build -t retail-app .

for run container execute (pay attention now it works on port 8001):
>docker run retail-app


if you want to use docker-compose run the following commands:
>docker-compose build;
docker-compose up



That's all
<h4>Have a nice day! See you! </h4>
with best wishes, kirill.s
