# Network Path Optimizer

import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt


def create_network():
    G = nx.Graph()
    edges = [
        ("Device A", "Device B", 10),
        ("Device A", "Device C", 15),
        ("Device A", "Device F", 20),
        ("Device B", "Device D", 12),
        ("Device B", "Device E", 15),
        ("Device C", "Device D", 5),
        ("Device C", "Device G", 25),
        ("Device D", "Device E", 8),
        ("Device D", "Device H", 10),
        ("Device E", "Device F", 18),
        ("Device F", "Device G", 30),
        ("Device G", "Device H", 5)
    ]
    G.add_weighted_edges_from(edges)
    return G


# Dijkstra's Algorithm to find the shortest path
def dijkstra(graph, start, end):
    try:
        path = nx.dijkstra_path(graph, start, end)
        latency = nx.dijkstra_path_length(graph, start, end)
        return path, latency
    except nx.NetworkXNoPath:
        return None, None


# Function to visualize the network and the shortest path
def visualize_path():
    start = entry_start.get().strip()
    end = entry_end.get().strip()

    if not start or not end:
        messagebox.showerror("Error", "Please enter both start and end devices.")
        return

    path, latency = dijkstra(network_graph, start, end)

    if path is None:
        messagebox.showerror("Error", f"No path between {start} and {end}.")
        return

    # Create a new window for results
    result_window = tk.Toplevel(root)
    result_window.title("Result")
    result_window.geometry("500x250+600+300")
    result_window.configure(bg='lightgray')

    # Result header
    result_header = tk.Label(result_window, text="Shortest Path Result", font=("Helvetica", 16), bg='lightgray')
    result_header.pack(pady=10)

    # Show the result in a message
    result_message = f"Shortest path:\n{' -> '.join(path)}\nLatency: {latency} ms"
    result_label = tk.Label(result_window, text=result_message, font=("Helvetica", 14), bg='lightgray', justify='center')
    result_label.pack(pady=20)

    # Close button
    btn_close = tk.Button(result_window, text="Close", font=("Helvetica", 12), bg='#004d4d', fg='white', command=result_window.destroy)
    btn_close.pack(pady=10)

    # Visualize the graph
    plt.figure(figsize=(8, 6))
    nx.draw(network_graph, pos, with_labels=True, node_color='lightblue', node_size=4000)
    labels = nx.get_edge_attributes(network_graph, 'weight')
    nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=labels)

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(network_graph, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title(f"Resultant Graph - Shortest Path from {start} to {end}")
    plt.get_current_fig_manager().window.wm_geometry("+1200+100")
    plt.show()


# Function to draw the initial graph when the program starts
def draw_initial_graph():
    plt.figure(figsize=(8, 6))  # Create a new figure
    nx.draw(network_graph, pos, with_labels=True, node_color='lightblue', node_size=4000)
    labels = nx.get_edge_attributes(network_graph, 'weight')
    nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=labels)

    plt.title("Computer Network Topology")  # Set the desired title
    plt.get_current_fig_manager().window.wm_geometry("+0+100")  # Position the window
    plt.show()  # Display the figure


# Create the main application window
root = tk.Tk()
root.title("User Input - Computer Network Shortest Path Finder")
root.geometry("400x400+600+300")  # Set a smaller size for the main window

# Create a frame for the inputs with a border
input_frame = tk.Frame(root, padx=20, pady=20, bg='lightgray', relief='groove', bd=2)
input_frame.pack(expand=True, fill='both', padx=10, pady=10)

# Title Label
title_label = tk.Label(input_frame, text="Shortest Path Finder", font=("Helvetica", 20), bg='lightgray')
title_label.pack(pady=10)

label_font = ("Helvetica", 14)
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 14)

# Input fields for start and end devices
tk.Label(input_frame, text="Start Device:", font=label_font, bg='lightgray').pack(pady=5)
entry_start = tk.Entry(input_frame, font=entry_font, bg='white')
entry_start.pack(pady=5, ipadx=10, ipady=5)

tk.Label(input_frame, text="End Device:", font=label_font, bg='lightgray').pack(pady=5)
entry_end = tk.Entry(input_frame, font=entry_font, bg='white')
entry_end.pack(pady=5, ipadx=10, ipady=5)

# Button to visualize the path 
btn_find_path = tk.Button(input_frame, text="Find Shortest Path", font=button_font, bg='#004d4d', fg='white', relief='raised', command=visualize_path, width=20)
btn_find_path.pack(pady=30)  # Adjusted padding for better spacing

# Create the network graph
network_graph = create_network()

# Calculate positions only once
pos = nx.spring_layout(network_graph)

# Draw the initial graph layout when the program starts
draw_initial_graph()

# Run the application
root.mainloop()
