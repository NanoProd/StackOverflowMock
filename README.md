# Stackoverflow mock
This web application features a question and answer forum where users can seek help and advice from professionals and enthusiasts around the world. It is a clone of the popular stackoverflow website that we created for our SOEN-341 course at Concordia University.

The main objective of this application is to create a medium which makes it easy for people to obtain reliable and trustworthy information to help them understand any STEM related problems they may be facing.

Three core features are to be implemented:
- Asking and answering questions
- Voting on answers
- Accepting the best answer

Users can post questions and answer other people's questions to gain points and increase their reputation in the forum. The more people upvote your answer to a question, the more points you gain!
# Tech Stack
- Javascript
- Python
- Flask 
- HTML/CSS
- Docker
- GitHub Actions (CI)

# Members
- Tim Freiman, GH: VimFreeman
- Philippe Carvajal, GH: PhilCarPi
- Aleksandr Vinokhodov, GH:daxsis **(Team Lead)**
- Joshua-James Nantel-Ouimet, GH: NanoProd
- Samaninder Singh, GH:SamSDK
- Lorne Geniele, GH: hotplate5

# Project Setup
1. `git clone` repository
2. copy environment file that you need, `cp .env.dev-sample .env.dev`
3. modify `.env.dev` with your variables
4. `cd services/web && python3.9 -m venv env` to create python virutal environment for that project, so that all dependecnies in development will be installed inside of this folder
5. `docker-compose up -d --build` will build `web` docker image fron `python3.9`
 - if you are don't running m1 silicon you can modify `services/web/Dockerfile` to `FROM python:3.9.5--slim-buster`
6. check that your application asnwers on `localhost:5000`
7. pgadmin is located on `localhost:5050` with credentials:
 - login: dev@concordia.ca
 - pass: root
 - use `postgres` as a hostname, `5432` as port with user `flask` password `flask` in your pgadmin dashboard when creating new connection the first time.
8. all the changes will be loaded into the container because we have mounted volumes.
9. happy codding

# Wireframe
## User Profile Page
<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137045617-75b56fc4-9082-471d-bee7-38b50e45a850.png" width="75%">
</p>

## Questions Forum Page
<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137045669-59873f59-2102-4056-ac27-db468de89b7e.png" width="75%">
</p>

## New Question Page
<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137046586-37c5ff0b-7f59-4274-ba2f-6492c01f4080.png">
</p>

## Question Page (with Answers)
<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137551694-be85e6c4-749e-4c84-ab0b-d448078d0494.png">
<img src="https://user-images.githubusercontent.com/19224656/137551716-9808a299-a08d-4813-9b8c-b5a9076fe3bd.png">
</p>

# Software Architecture
Development Note:<br>
All diagrams are located in the Google drive in the [Software Architecture Diagrams](https://app.diagrams.net/#G11lHgVPedABSrHVzqaIad7T8gBx-x8ebw) file. As development progresses, these diagrams can be modified and re-exported into this file. Access to this file is restricted to DT members only.

## Use Case Diagram
To better understand the behavior of users interacting with the application, a use case diagram was created. This diagram captures all actors (currently the user) and actions avaibale to these actors. This model informs design desicions disscussed in the following sections.

<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/136254205-1a231967-c4e9-485a-9170-29bcb5c51511.png" width="75%">
</p>

## MVC Model
To standardize code organization and make the software modular and therefore extensible, a development model was chosen. Model-View-Controller allows for a relatively straigh forward way of organizing code in a web application. Models capture the "business logic" and therfore the data structures used to store information within the application, Views encompass the graphical user interface provided to the user as a web page, and Controllers serve as the interface between the business logic and the user facing code.
<br>
A diagram of the high level architecture of the application is shown below.

<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137186968-7610cd7a-7394-483f-9aef-8555f6311808.png" width="75%">
</p>

## UML Class Diagram
Based on the MVC model chosen and the associated diagram shown in the previous section, a UML class diagram was created to represent all objects in the application, how they relate to eachother, and how they fit within the MVC development model. Note that the views in this diagram are not shown. This is because the views are in practice html templates that are rendered by the controllers. There are no classes associated with views in this application.

<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/136256401-d5721490-e35f-4477-9059-13b30abda9a1.png" width="75%">
</p>

## Entity Relationship Diagram
The application's database is organized as shown in the diagram below. All models are present in the DB as individual tables as is an additional table dedicated to password storage.

<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/137570754-2bb1069f-7011-4ead-b4e8-14c528ccda42.png" width="75%">
</p>