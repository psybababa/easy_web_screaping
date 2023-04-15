import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add some nodes
G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")

# Add some edges
G.add_edge("A", "B", weight=0.5)
G.add_edge("A", "C", weight=0.25)
G.add_edge("B", "D", weight=0.75)
G.add_edge("C", "D", weight=0.5)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, width=[d["weight"]*4 for (u,v,d) in G.edges(data=True)])
nx.draw_networkx_labels(G, pos)
plt.axis("off")
plt.show()