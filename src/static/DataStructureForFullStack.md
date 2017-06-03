# Unified Data-structure for Full-stack Programming
## Introduction
Full stack development describes an end to end solution for a computer programming problem. The stack is all the technologies that are layered to implement the solution. For web-based programming the stack from the 'front-end to back-end' includes the following:
Javascript/Javascript frameworks - Web-server/frameworks - application layer/s - databases.
The idea here is to define the function of these layers with regards to specific computer programming problem, using a unified data structure. This unified data-structure is to help provide:

1. A comprehensive view of the solution.
2. Ability for segments of the data-structure to support/define each part of the Full-stack.
3. Create naming conventions, facilitating co-ordination between layers of the stack.
4. Facilitate growth/enhancements of the system, by allowing a 'full-stack' view of required changes.

## Details

Consider a specific Full-stack example:
Build a game to enhance the user's memory. The game consists of pairs of identical pictured cards all to be shown 'face-down' (i.e. to see the picture the cards have to be turned over).  The user 'clicks' on a card to turn-it over exposing the picture  for n seconds, and flips back. If the user then clicks on another card with the same picture, then both cards remain open. The user is to find all the matching pairs with the fewest number of clicks, shortest time etc.

### Central Data-structure (brainstorming):###
**'Static data:'**
1. A library of pictures.
2. A graphical representation of picture.
3. Number of cards to placed on one screen
4. Number of seconds a card should remain 'open' when clicked.  

**'Dynamic data:'**
1. Number of clicks by specific user.
2. Time taken by user between clicks.
3. Memory Evaluation chart (a kind of space map between time and accuracy)

### Central Data-structure - Version 1: ###

1. Name of folder containing pictures
2. Size of each card
3. Specification of N X M as the number of cards on the screen
4. Seconds a card should remain open
5. Memory evaluation chart type.
6. Counters for clicks and time.

### Design (as a JSON): ###
{"Title":"Memory Game"  
, "PictureFolder":"images"  
,"N":3,"M":3, W:100,H:100 #picture display details  
,"openSeconds": 2  
,"UserNM":"xxx"  
,"NoOfClicks":0  
,"TimeElapsed":0  
}

Consumption of the Data-Structure by Full-stack components:  

| Data Item     | Consumer     |
| :------------- | :------------- |
| Title       | Javascript-UI      |
|PictureFolder  | Python|
|N,M,W,H | Javascript-UI|
|openSeconds  | Javascript-UI|
|UserNM  | UI,Python|
|NoOfClicks  | Python|
|TimeElapsed  | Python|
