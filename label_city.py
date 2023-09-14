# Title : Understanding Markov Random Fields-Loopy Belief Propagation

import numpy as np
import sys

#Function to read the bribe files
def read_bribes(republicrat_bribes_file, democran_bribes_file):
    # Load the republicrat and democran bribes files into numpy arrays
    republicrat_bribes = np.loadtxt(republicrat_bribes_file, dtype=int)
    democran_bribes = np.loadtxt(democran_bribes_file, dtype=int)
    return republicrat_bribes, democran_bribes

#Function to get the neighbors of a given node on the grid
def get_neighbors(node_id, n):
    neighbors = []
    if node_id % n > 0:
        neighbors.append(node_id - 1) # left
    if node_id % n < n - 1:
        neighbors.append(node_id + 1) # right
    if node_id // n > 0:
        neighbors.append(node_id - n) # up
    if node_id // n < n - 1:
        neighbors.append(node_id + n) # down
    return neighbors

#Function to compute the fence cost between two adjacent nodes
def fence_cost(x, y, labels):
    #If the labels of two adjacent nodes are different, return a high cost
    if labels[x] != labels[y]:
        return 1000
    #Otherwise, return a cost of 0
    else:
        return 0

#Function to compute the bribe cost for a given node
def bribe_cost(x, labels, republicrat_bribes, democran_bribes, n):
    if labels[x] == 0:
        return democran_bribes[x // n, x % n]
    else:
        return republicrat_bribes[x // n, x % n]

#Main function for the loopy belief propagation algorithm
def loopy_belief_propagation(n, republicrat_bribes_file, democran_bribes_file):

    #Read the Republicrat and Democran republic bribe values
    republicrat_bribes, democran_bribes = read_bribes(republicrat_bribes_file, democran_bribes_file)
    
    # Initialize the message and belief arrays
    message = np.ones((n*n, 2))
    message[:, 1] = 0
    belief = np.zeros((n*n, 2))

    #Initialize the grid with the label with the highest belief value
    grid = np.zeros((n*n,), dtype=int)
    for i in range(n*n):
        grid[i] = np.argmax(message[i, :])

    # Run the loopy belief propagation algorithm
    for i in range(50):
        for j in range(n*n):
            msgs = np.ones((2,)) # initialize messages to 1

            #Compute the messages from all the neighboring nodes
            neighbors = get_neighbors(j, n)
            for k in neighbors:
                fence_cost_kj = fence_cost(j, k, grid)
                bribe_cost_k = bribe_cost(k, grid, republicrat_bribes, democran_bribes, n)
                msgs[0] *= np.exp(-fence_cost_kj / 2) * np.exp(-bribe_cost_k) * np.prod(message[k, :])
                msgs[1] *= np.exp(-fence_cost_kj / 2) * np.exp(-bribe_cost_k) * np.prod(message[k, ::-1])

            #Comute the belief values for the current node    
            belief[j, :] = msgs * np.array([1, -1])
            message[j, :] = belief[j, :] / (np.sum(belief[j, :]) + 1e-8)
        
        # Update the grid with the label with the highest belief value
        grid = np.argmax(message, axis=1)

    # Try all possible flips of each node's label
    for i in range(n*n):
        temp_grid = np.copy(grid)
        temp_grid[i] = 1 - temp_grid[i]
        temp_cost = np.sum([fence_cost(x, y, temp_grid) for x in range(n*n) for y in [x+1, x+n] if (y // n == x // n or y % n == x % n) and y < n*n]) + np.sum([bribe_cost(x, temp_grid, republicrat_bribes, democran_bribes, n ) for x in range(n*n)])
        if temp_cost < np.sum([fence_cost(x, y, grid) for x in range(n*n) for y in [x+1, x+n] if (y // n == x // n or y % n == x % n) and y < n*n]) + np.sum([bribe_cost(x, grid, republicrat_bribes, democran_bribes, n ) for x in range(n*n)]):
            grid = temp_grid

    # Print the final label assignment and total cost

    label = grid
    label_str = np.where(label==0, 'D', 'R').reshape(n, n) # convert 1's to 'd' and 0's to 'r'
    print("Computing optimal labeling:")
    for row in label_str:
        print(' '.join(row))
    total_cost = np.sum([fence_cost(x, y, label) for x in range(n*n) for y in [x+1, x+n] if (y // n == x // n or y % n == x % n) and y < n*n]) + np.sum([bribe_cost(x, label,  republicrat_bribes, democran_bribes, n) for x in range(n*n)])
    print(f"Total cost = ${total_cost}")



if __name__ == '__main__':
    # Read the command-line arguments
    if(len(sys.argv) < 4):
        raise Exception("error: please give an input image name as a parameter, like this: \n"
                         "python3 label_city.py sample_r_bribes.txt sample_d_bribes.txt")
    
    n = int(sys.argv[1])
    republicrat_bribes_file = sys.argv[2]
    democran_bribes_file = sys.argv[3]
    loopy_belief_propagation(n, republicrat_bribes_file, democran_bribes_file)

