## Algorithm
Concept: The purpose is to read messages from satori channels via websockets,
count the number of messages within each interval, and display the results
in a bar-graph.

### Methodology:
1. Data driven design: Each channel is modelled as a data-structure, that
 contains the required information about each channel. This structure contains
 all the information required, from the 'backend' - websockets, to the
 front-end, which is the charts.  The data-structure drives the program
 structure.
 
..1.
