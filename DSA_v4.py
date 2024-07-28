# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:34:25 2024

@author: user
"""

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
def calculate_distance(port_order, cell_order):
    total_distance = 0
    for port in connections:
        port_index = port_order.index(port)
        for cell in connections[port]:
            cell_index = cell_order.index(cell)
            total_distance += abs(port_index - cell_index)
    return total_distance

# Simulated annealing algorithm for dual optimization
def simulated_annealing_dual(connections):
    # Initial state
    ports = list(connections.keys())
    cells = [cell for cells in connections.values() for cell in cells]
    random.shuffle(ports)
    random.shuffle(cells)
    
    # Current state and best state
    current_ports = ports[:]
    current_cells = cells[:]
    best_ports = ports[:]
    best_cells = cells[:]
    best_distance = calculate_distance(current_ports, current_cells)
    
    # Parameters for simulated annealing
    T = 1000.0
    T_min = 1.0
    alpha = 0.9
    
    while T > T_min:
        i = 0
        while i < 100:
            new_ports = current_ports[:]
            new_cells = current_cells[:]
            # Swap two ports
            a = random.randint(0, len(ports) - 1)
            b = random.randint(0, len(ports) - 1)
            new_ports[a], new_ports[b] = new_ports[b], new_ports[a]
            # Swap two cells
            c = random.randint(0, len(cells) - 1)
            d = random.randint(0, len(cells) - 1)
            new_cells[c], new_cells[d] = new_cells[d], new_cells[c]
            
            current_distance = calculate_distance(current_ports, current_cells)
            new_distance = calculate_distance(new_ports, new_cells)
            delta = new_distance - current_distance
            
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
                current_ports = new_ports[:]
                current_cells = new_cells[:]
                current_distance = new_distance
            
            if current_distance < best_distance:
                best_ports = current_ports[:]
                best_cells = current_cells[:]
                best_distance = current_distance
            
            i += 1
        T = T * alpha
    
    return best_ports, best_cells, best_distance

# Perform simulated annealing
best_ports, best_cells, best_distance = simulated_annealing_dual(connections)

# Save the result to a file
with open('result_tc1g1.txt', 'w') as f:
    f.write('Ports:\n')
    f.write(' '.join(best_ports) + '\n')
    f.write('Cells:\n')
    f.write(' '.join(best_cells) + '\n')

print("Optimization completed. Results saved to result_tc1g1.txt")

# Create a mapping of ports to their cells based on the optimized order
port_cell_mapping = {port: [] for port in best_ports}
cell_to_port = {cell: port for port, cells in connections.items() for cell in cells}

for cell in best_cells:
    port = cell_to_port[cell]
    port_cell_mapping[port].append(cell)

# Create the graph
G = nx.Graph()

# Add nodes
for port in best_ports:
    G.add_node(port, color='blue')
for cell in best_cells:
    G.add_node(cell, color='green')

# Add edges
for port, cells in port_cell_mapping.items():
    for cell in cells:
        G.add_edge(port, cell, color=port)

# Define colors for each port
port_colors = {port: plt.cm.tab10(i) for i, port in enumerate(best_ports)}
edge_colors = [port_colors[u] for u, v in G.edges()]

# Draw the graph with ports and cells in two separate columns
pos = {}
num_ports = len(best_ports)
num_cells = len(best_cells)
for i, port in enumerate(best_ports):
    pos[port] = (0, i * 2)  # Increase the distance between ports
for i, cell in enumerate(best_cells):
    pos[cell] = (1, i * 2)  # Increase the distance between cells

# Center-align the ports and cells columns
offset = (num_cells * 2 - num_ports * 2) / 2
for i, port in enumerate(best_ports):
    pos[port] = (0, i * 2 + offset)

plt.figure(figsize=(12, 8), dpi=300)  # Increase the resolution
nx.draw(G, pos, with_labels=True, node_color=['blue' if n in best_ports else 'green' for n in G.nodes()],
        node_size=500, font_size=8, font_color='white', edge_color=edge_colors)

# Save the graph
plt.savefig('optimized_connections.png')
plt.show()
