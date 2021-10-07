# Stackoverflow mock
This web application features a question and answer forum where users can seek help and advice from professionals and enthusiasts around the world. It is a clone of the popular stackoverflow website that we created for our SOEN-341 course at Concordia University.

The main objective of this application is to create a medium which makes it easy for people to obtain reliable and trustworthy information to help them understand any STEM related problems they may be facing. 

Users can post questions and answer other people's questions to gain points and increase their reputation in the forum. The more people upvote your answer to a question, the more points you gain!
# Tech Stack
- Javascript
- Python
- Flask 
- HTML/CSS

# Members
- Tim Freiman, GH: VimFreeman
- Philippe Carvajal, GH: PhilCarPi
- Aleksandr Vinokhodov, GH:daxsis
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
8. to find ip of the db container 
 - `docker ps`  find the name of the db container, it will be like `project_db_1` 
 - `docker instpect project_db_1 | grep "IPAddress"` you will see something 
```
"SecondaryIPAddresses": null,
"IPAddress": "",
    "IPAddress": "172.21.0.2",
```
 - use `172.21.0.2` you found in the output for connecting to the db container in your pgadmin dashboard.
9. all the changes will be loaded into the container because we have mounted volumes.
10. happy codding






