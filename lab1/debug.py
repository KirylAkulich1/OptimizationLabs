from scipy.optimize import linprog

import math
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

def zeros(length):
    return [0 for _ in range(length)]

def borders_and_branches_algorithm(c,lhs_ineq,rhs_ineq,bnd):
    def get_node_label_from_solution(opt_sol):
            ans = str(opt_sol.fun) if opt_sol.success else "NA"
            return str(opt_sol.x)+":"+ ans
    
    print("Left A:" + str(lhs_ineq))
    print("Right A:"+str(rhs_ineq))
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=bnd,
              method="revised simplex")
    
    parent_str = get_node_label_from_solution(opt)
    G.add_node(parent_str)
    #if opt_old is not None:
    #    G.add_edge(opt_old,str(opt.x)+" "+ str(opt.func))

    print(opt)
    if not opt.success:
        opt.fun =  float('inf')
        return opt

    x_values = opt.x
    print("============================" )
    min_solutions=[]
    for i,x in enumerate(x_values):
        if x.is_integer():
            continue
        ceil_lhs_ineq = lhs_ineq.copy()
        ceil_lhs_ineq_row = zeros(len(c))
        ceil_lhs_ineq_row[i] = -1
        ceil_lhs_ineq.append(ceil_lhs_ineq_row)
        ceil_rhs_ineq = rhs_ineq.copy()
        ceil_rhs_ineq.append((-1)* math.ceil(x))
        ceil_solution = borders_and_branches_algorithm(c,ceil_lhs_ineq, ceil_rhs_ineq,bnd)
        G.add_edge(parent_str, get_node_label_from_solution(ceil_solution))

        floor_lhs_ineq = lhs_ineq.copy()
        floor_lhs_ineq_row = zeros(len(c))
        floor_lhs_ineq_row[i] = 1
        floor_lhs_ineq.append(floor_lhs_ineq_row)
        floor_rhs_ineq = rhs_ineq.copy()
        floor_rhs_ineq.append(math.floor(x))
        floor_solution = borders_and_branches_algorithm(c,floor_lhs_ineq, floor_rhs_ineq,bnd)
        G.add_edge(parent_str, get_node_label_from_solution(floor_solution))

        if floor_solution.fun > ceil_solution.fun:
            min_solutions.append(ceil_solution)
        else:
            min_solutions.append(floor_solution)
    
    if len(min_solutions) == 0:
        return opt

    return min(min_solutions,key=lambda x: x.fun)


# function to optimaze params
obj  = [-1,-1]

# constraint matrix
lhs_ineq = [[ 2,  11], 
            [1,  1],  
            [ 4, -5]]

rhs_ineq = [ 38,  # правая сторона красного неравенства
            7,  # правая сторона синего неравенства
            5]

bnd = [(0, float("inf")),  # x1 x2 constraints 
       (0, float("inf"))] 
       
#print(borders_and_branches_algorithm(obj,lhs_ineq,rhs_ineq,bnd,None))

obj  = [-7,-9]

# constraint matrix
lhs_ineq = [[ -1,  3], 
            [7,  1]]

rhs_ineq = [ 6, # правая сторона красного неравенства
            35]

bnd = [(0, float("inf")),  # x1 x2 constraints 
       (0, float("inf"))] 

#print(borders_and_branches_algorithm(obj,lhs_ineq,rhs_ineq,bnd,None))


obj  = [2,3]

# constraint matrix
lhs_ineq = [[ 3,  5], 
            [3,  4],
            [0,1]]

rhs_ineq = [ 60, # правая сторона красного неравенства
            34,
            8]

bnd = [(0, float("inf")),  # x1 x2 constraints 
       (0, float("inf"))] 

#print(borders_and_branches_algorithm(obj,lhs_ineq,rhs_ineq,bnd,None))

G = nx.DiGraph()

obj  = [-2,-3]

# constraint matrix
lhs_ineq = [[ 3,  4], 
            [2,  5]]

rhs_ineq = [ 24, # правая сторона красного неравенства
            22]

bnd = [(0, float("inf")),  # x1 x2 constraints 
       (0, float("inf"))] 

from networkx.drawing.nx_agraph import graphviz_layout

print(borders_and_branches_algorithm(obj,lhs_ineq,rhs_ineq,bnd))

pos=graphviz_layout(G, prog='dot')

nx.draw(G, pos, with_labels=True, arrows=True)

plt.show()