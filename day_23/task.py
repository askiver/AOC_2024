import networkx as nx
from pathlib import Path

G = nx.parse_edgelist(Path("input.txt").read_text().splitlines(), delimiter="-")

# Task 1
cliques = [clique for clique in nx.enumerate_all_cliques(G)]
triangle_comps = [comps for comps in cliques if any(node.startswith("t") for node in comps) and len(comps) == 3]
print(len(triangle_comps))

# Task 2
biggest_clique = cliques[-1]
print(sorted(biggest_clique))