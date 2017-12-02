# ItemCatalog

## Overview: 
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Building Blocks:
1. Flask framework
2. Google OAuth for authentication and authorization
3. SQLAlchemy to communicate with database
4. Rest API Endpoints
5. HTML, CSS and Bootstrap for User Interface

## How to Run
1. Install Vagrant and VirtualBox
2. Clone or downlaod the ItemCatalog project (https://github.com/MounikaArkala/ItemCatalog.git)
3. Launch the Vagrant VM (vagrant up)
4. set up the database by using the commnad (python database_setup.py)
5. Run the application within the VM with the command(python project.py)
6. Access and test the application by visiting http://localhost:5656/ locally

## JSON Endpoints:
items under a category :  '/categories/<int:category_id>/menu/JSON'  

item information:         '/categories/<int:id>/menu/JSON'


