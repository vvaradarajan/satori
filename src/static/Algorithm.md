## Design
*Concept*: The purpose is to read messages from satori channels via websockets,
count the number of messages within each interval, and display the results
in a bar-graph. There are two major parts of the design:  
1. Design a common data-structure, which is then distributed to the technology stack. This helps specify the functions of each portion of the stack. Here 'stack' is comprised of the technologies used (Python, Javascript, Google-charts etc.).  
2. Multithreading as required by this application. This application is divided into websockets processing, rest API processing and timer event processing. Each of these take place in individual threads.

![alt Text](http://45.55.0.197:88/images/TechStack.PNG)
### Methodology:
1. Data driven design: Each channel is modelled as a data-structure, that
 contains the required information about each channel. This structure contains
 all the information required, from the 'backend' - websockets, to the
 front-end, which is the charts.  The main purpose of this single data-structure is to co-ordinate the programming across the technology stack. In this application the structure is:  
  
	+ Channel Name -the key  
	+ Web-socket-info - Information required to connect to the websocket
	+ Class Name - The name of the program that controls the processing of the websocket message. Here it is a Python Class.  
	+ Chart Title - The title of the Chart on which the information is to be displayed. Here it is Google Chart on the UI
     
 The entire stack reads this data structure and performs accordingly. The data from this structure is distributed to the technology stack. The distribution is thru reading the stack directly (from Python) or thru a rest api (for Google Chart).
 
### Algorithm

The application is multi-threaded, with websockets processing, rest API processing and timer event processing being the three threads.  Each thread is essentially an 'infinite loop', and within this loop is a 'wait' for an event. The 'wait' time between events is assumed to be large enough for the threads to complete processing of the previous events. Therefore 'shared' memory is sufficient to pass information between these threads (as opposed to queueing the events).  
The threads and events are:
  
 - Websocket thread: Waits for data on websocket and reads websocket and processes to shared memory
 - Rest API webserver thread: Waits for a request from UI and processes the request accessing the information in the shared memorry.
 - Timer thread: Waits for an interval of time, and processes the shared memory data to time intervals (used by the UI to chart the data).


