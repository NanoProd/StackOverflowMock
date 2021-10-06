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
<img src="https://user-images.githubusercontent.com/19224656/136255831-497b7c65-82b5-4863-90e2-c030d2bddf9d.png" width="75%">
</p>

## UML Class Diagram
Based on the MVC model chosen and the associated diagram shown in the previous section, a UML class diagram was created to represent all objects in the application, how they relate to eachother, and how they fit within the MVC development model. Note that the views in this diagram are not shown. This is because the views are in practice html templates that are rendered by the controllers. There are no classes associated with views in this application.

<p align="center">
<img src="https://user-images.githubusercontent.com/19224656/136256401-d5721490-e35f-4477-9059-13b30abda9a1.png" width="75%">
</p>


