import networkx as nx
import time
import math
	
def coreness(var,gsize):
	f = open(var,"r")
	temp = f.read().split('\n')
	list = []
	for i in range(gsize + 1):
		list.append(0)
	for x in temp:
		xx = x.split('\t\t\t\t\t')
		list[int(xx[0])]=int(xx[2])
	return list

def reachcore(each,core,step,move,g,lst,list_hop):
	list_hop[each]=1
	node = each
	noddd = each
	corr = core
	corrr = core
	
	for each1 in g.neighbors(each):
		var = lst[each1]
		if move == 1:
			list_hop[each1]=1
		if var > corr:
			corr = var
			node = each1
			
		if var <= corrr:
			noddd = each1
			corrr = var
			
	if node == each:
		if move == 1:
			x = each
			count = 0 
			d = g.degree(each)
			for each1 in g.neighbors(each):
				node_var,var,z,list_hop = reachcore(each1,core,step,0,g,lst,list_hop)
				if var > core:
					corr = var
					node = node_var
					break
				if var == core && g.degree(node_var) > d:
					d = g.degree(node_var)
					node_ = node_var
			if node == each:
				step = step + 2
				return reachcore(node_,corr,step,1,g,lst,list_hop)	
			else:
				step = step + 2
				return reachcore(node,corr,step,1,g,lst,list_hop)
		else:
			return noddd,corrr,step,list_hop
		
	else:
		if move == 1:
			step = step + 1
			return reachcore(node,corr,step,1,g,lst,list_hop)
		else:
			return node,corr,step,list_hop


f = open("networks.txt","r")
temp = f.read().split('\n')

for xx in temp:
	
	var = xx + ".txt"
	g = nx.read_edgelist(var,create_using = nx.Graph(),nodetype = int)
	
	max_node=0
	for i in list(g.nodes()):
		#print(i)
		if i > max_node:
			max_node = i
	gsize = max_node
	
	G = g.copy()
	G.remove_edges_from(nx.selfloop_edges(G))
	g = G.copy()
	
	core = nx.core_number(g)
	list_actual = []
	for x in range(gsize+1):
		list_actual.append(0)
	for key in core:
		list_actual[key] = core[key]
	
	varr = xx + "+deg_cc.txt"
	list4 = []	
	list4 = coreness(varr,gsize)

	list_act = []
	list_path = []
	
	for i in range(gsize+1):
		list_act.append(list_actual[i])
		
	list_actual.sort(reverse=True)


	print(nx.info(g))
	file_name = xx + "++-.txt"
	
	list_hop = []
	for z in range(gsize+1):
		list_hop.append(0)
	ff = open(file_name, "a")
	ff.write("S_Node\t\t\tF_Node\t\t\tC_Node\t\t\tAc_Core\t\t\tPath\t\t\tScs/Uns(1/0)\n")	
	ff.close()
	count = 0
	countt = 0
	
	path = 0
	for each in g.nodes():
		if list_act[each] == 1:
			for z in range(gsize+1):
				list_hop[z] = 0
			count = count + 1
			step = 0
			list_hop[each]=1
			node,coreness,step,list_hop = reachcore(each,list4[each],step,1,g,list4,list_hop)
			
			list_path.append(step)
			path = path + step
			
			
			ff = open(file_name, "a")
			
			ff.write(str(each))
			ff.write("\t\t\t\t")
			ff.write(str(node))
			ff.write("\t\t\t\t")
			ff.write(str(coreness))
			ff.write("\t\t\t\t")
			ff.write(str(list_actual[0]))
			ff.write("\t\t\t\t")
			ff.write(str(step))
			ff.write("\t\t\t\t")
			
			if list_act[node] != list_actual[0]:
				varr = 0
			else:
				varr = 1
				countt = countt + 1 
			ff.write(str(varr))
			ff.write("\n")
			ff.close()
			print(each,node,coreness,list_actual[0],step,varr)
			
	ff = open(file_name, "a")
	ff.write("Number of Attempts: ")
	ff.write(str(count))
	ff.write("\nNumber of Successful Attempts: ")
	ff.write(str(countt))
	countt = (float(countt)/count)*100
	ff.write("\nPercentage of Success: ")
	ff.write(str(countt))
	ff.write("%")
	ff.write("\nAverage Path Length: ")
	path = float(path)/count
	ff.write(str(path))
	
	std = 0
	for i in range(count):
		std = std + (list_path[i] - path)*(list_path[i] - path)
	std = float(std)/count
	std = math.sqrt(std)
	ff.write("\nStandard Deviation: ")
	ff.write(str(std))

	del list_path[:]
	
f.close()



