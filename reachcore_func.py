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
			for each1 in g.neighbors(each):
				node_var,var,z,list_hop = reachcore(each1,core,step,0,g,lst,list_hop)
				if var > core:
					corr = var
					node = node_var
					break
			if node == each:
				return each,core,step,list_hop	
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