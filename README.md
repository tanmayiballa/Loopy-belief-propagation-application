# tballa-svujjin-a2

# Part 2 :  Understanding Markov Random Fields - Implementing Loopy Belief Propagation

## Statement : 

Given that political rancor has gotten so bad in Bloomingville that the mayor has decided to do something about it. The town consists of n^2 houses, arranged in an n × n grid. The mayor has decided that every home will be assigned to a political affiliation — either Republicrat (R) or Democran (D). To keep the peace, they will install a fence between any two adjacent houses that have differing political affiliations. This, of course, will cost money: a fence costs $1000 to build between any two houses. In the worst case, if all neighbors disagreed with one another, then it would cost 2000 × (n^2 − n) dollars to build fences between every pair of
neighboring houses (since an n × n grid graph has 2(n^2 − n) edges). But it turns out that many homes have not yet decided their affiliation, and others could be bribed to change their affiliation. The council has two files called r bribes.txt and d bribes.txt that contain this information based on a survey of the town’s residents. 

We have to write a program called label city.py that implements loopy belief propagation to find the cheapest way for the city council to assign political parties to the homes.  

## Approach Explanation :

To implement the loopy belief propagation :

- The read_bribes function reads the Republicrat and Democran bribes files and returns the bribes as numpy arrays.

- The get_neighbors function returns the indices of the neighboring nodes for a node in the grid

- The fence_cost function calculates the cost of putting a fence between two neighboring nodes based on their labels. If the nodes have the same label, the cost is 0. Otherwise, the cost is a large value of 1000.

- The bribe_cost function calculates the cost of bribing a node based on its label and the bribes paid by Republicrats and Democrans

- In the loopy_belief_propagation function, we first initialized the message and belief numpy arrays to all ones, representing an equal belief in both possible labels("Republicrat" or "Democran"). We then initialize the grid numpy array to the label with the highest belief value.

- We iterated over the message and belief 50 times. For each node j, we calculated the msgs by taking the product of the messages from all its neighbors'k scaled by the appropriate costs(fence cost and the bribe cost).

- We then normalized the belief which ensures that we are always considering the differennce between the two label options.

- We updated the grid with the label with the highest belief value. Tried flipping the label of each node in the grid array and calculated the total cost of the resulting labeling. If the cost is lower than the cost of the current grid labeling, we update the grid array with the new labeling.

- We print the final labeling of the nodes, as well as the total cost of the labeling, which is the sum of the fence cost and bribe cost for each node. 


### References Used :


https://www.youtube.com/watch?v=C5j_8oguUik <br/>
http://nghiaho.com/?page_id=1366 <br/>
https://www.cs.cmu.edu/~epxing/Class/10708-14/scribe_notes/scribe_note_lecture13.pdf <br/>

