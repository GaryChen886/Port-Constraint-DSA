import random
import math
import matplotlib.pyplot as plt
import networkx as nx

# Define the connection data
connections = {
    'Port_1': ['Cell_23', 'Cell_108', 'Cell_200', 'Cell_263', 'Cell_518', 'Cell_538', 'Cell_566', 'Cell_577', 'Cell_578'],
    'Port_2': ['Cell_48', 'Cell_50', 'Cell_60', 'Cell_65', 'Cell_66', 'Cell_73', 'Cell_138', 'Cell_211', 'Cell_341', 'Cell_387', 'Cell_436', 'Cell_438', 'Cell_540', 'Cell_605'],
    'Port_3': ['Cell_29', 'Cell_39', 'Cell_65', 'Cell_73', 'Cell_138', 'Cell_271', 'Cell_306', 'Cell_350', 'Cell_367', 'Cell_371', 'Cell_377', 'Cell_481', 'Cell_525', 'Cell_583'],
    'Port_4': ['Cell_44', 'Cell_138', 'Cell_207', 'Cell_263', 'Cell_271', 'Cell_293', 'Cell_429', 'Cell_519', 'Cell_525', 'Cell_528', 'Cell_578', 'Cell_587', 'Cell_596', 'Cell_605'],
    'Port_5': ['Cell_27', 'Cell_66', 'Cell_73', 'Cell_335', 'Cell_359', 'Cell_431', 'Cell_518', 'Cell_578']
}

# Calculate the "distance" between ports and cells
def calculate_distance(mapping):
    total_distance = 0
    for port, cells in connections.items():
        for cell in cells:
            port_index = list(connections.keys()).index(port)
            cell_index = mapping.index(cell)
            total_distance += abs(port_index - cell_index)
    return total_distance

# Simulated annealing algorithm
def simulated_annealing(connections):
    # Initial state
    cells = [cell for cells in connections.values() for cell in cells]
    random.shuffle(cells)
    
    # Current state and best state
    current_state = cells[:]
    best_state = cells[:]
    best_distance = calculate_distance(current_state)
    
    # Parameters for simulated annealing
    T = 1000.0
    T_min = 1.0
    alpha = 0.9
    
    while T > T_min:
        i = 0
        while i < 100:
            new_state = current_state[:]
            # Swap two cells
            a = random.randint(0, len(cells) - 1)
            b = random.randint(0, len(cells) - 1)
            new_state[a], new_state[b] = new_state[b], new_state[a]
            
            current_distance = calculate_distance(current_state)
            new_distance = calculate_distance(new_state)
            delta = new_distance - current_distance
            
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
                current_state = new_state[:]
                current_distance = new_distance
            
            if current_distance < best_distance:
                best_state = current_state[:]
                best_distance = current_distance
            
            i += 1
        T = T * alpha
    
    return best_state, best_distance

# Perform simulated annealing
best_state, best_distance = simulated_annealing(connections)

# Save the result to a file
with open('result_tc1g1.txt', 'w') as f:
    ports = list(connections.keys())
    f.write('Ports:\n')
    f.write(' '.join(ports) + '\n')
    f.write('Cells:\n')
    f.write(' '.join(best_state) + '\n')

print("Optimization completed. Results saved to result_tc1g1.txt")

# Create a mapping of ports to their cells based on the optimized order
port_cell_mapping = {port: [] for port in connections.keys()}
cell_to_port = {cell: port for port, cells in connections.items() for cell in cells}

for cell in best_state:
    port = cell_to_port[cell]
    port_cell_mapping[port].append(cell)

# Create the graph
G = nx.Graph()

# Add nodes
for port in port_cell_mapping.keys():
    G.add_node(port, color='blue')
for cell in best_state:
    G.add_node(cell, color='green')

# Add edges
for port, cells in port_cell_mapping.items():
    for cell in cells:
        G.add_edge(port, cell, color=port)

# Define colors for each port
colors = ['red', 'blue', 'green', 'purple', 'orange']
edge_colors = [colors[list(port_cell_mapping.keys()).index(u)] for u, v in G.edges()]

# Draw the graph with ports and cells in two separate columns
pos = {}
for i, port in enumerate(port_cell_mapping.keys()):
    pos[port] = (0, i)
for i, cell in enumerate(best_state):
    pos[cell] = (1, i)

plt.figure(figsize=(12, 8), dpi=300)  # Increase the resolution
nx.draw(G, pos, with_labels=True, node_color=['blue' if n in port_cell_mapping else 'green' for n in G.nodes()],
        node_size=500, font_size=8, font_color='white', edge_color=edge_colors)

# Save the graph
plt.savefig('optimized_connections.png')
plt.show()
