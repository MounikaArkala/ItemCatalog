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
2. Clone or downlaod the ItemCatalog project
3. Launch the Vagrant VM (vagrant up)
4. Run the application within the VM with the command(project project.py)
5. Access and test the application by visiting http://localhost:5656/ locally

## JSON Endpoints:
items under a category :  '/categories/<int:category_id>/menu/JSON'


