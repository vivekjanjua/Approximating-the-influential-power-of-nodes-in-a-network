import networkx as nx
import math

def h_operator(h_list):
	size = len(h_list)
	max_value = 0
	for i in range(size):
		if h_list[i] > max_value:
			max_value = h_list[i]
			
	list_count = []
	for i in range(max_value+1):
		list_count.append(0)
		
	for i in range(size):
		list_count[h_list[i]] = list_count[h_list[i]] + 1
		
	frequency = 0
	for i in range(max_value+1):
		index = max_value-i
		frequency = frequency + list_count[index]
		if frequency >= index:
			return index
			
			
			
f = open("dataset.txt","r")
temp = f.read().split('\n')


for xx in temp:
	
	file_name = xx + ".txt"
	g = nx.read_edgelist(file_name,create_using = nx.Graph(),nodetype = int)
	G = g.copy()
	G.remove_edges_from(nx.selfloop_edges(G))
	#G.remove_edges_from(nx.parallel_edges(G))
	g = G.copy()
	
	core = nx.core_number(g)
	clique = {}
	degree = {}
	Cc = {}
	h1_index = {}
	list = []
	
	
	file_ = xx + "+data.txt"
	ff = open(file_,"a")
	
	ff.write("Nd\t\t\tDg\t\t\tCq\t\t\tCc\t\t\tH1\t\t\tSn")
	
	for i in g.nodes():
		clique[i] = nx.node_clique_number(g,nodes=i)
		degree[i] = g.degree(i)
		print("\n")
		print(degree[i])
		if degree[i] == 1:
			Cc[i] = 1
		else:
			Cc[i] = round(nx.clustering(g,i),2)
		for each in g.neighbors(i):
			list.append(g.degree(each))
		print(list)
		h1_index[i] = h_operator(list)
		del list[:]
		ff.write("\n")
		ff.write(str(i))
		ff.write("\t\t\t")
		ff.write(str(degree[i]))
		ff.write("\t\t\t")
		ff.write(str(clique[i]))
		ff.write("\t\t\t")
		ff.write(str(Cc[i]))
		ff.write("\t\t\t")
		ff.write(str(h1_index[i]))
		ff.write("\t\t\t")
		ff.write(str(core[i]))
	
	ff.close()
	
f.close()
	
	
	