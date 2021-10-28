import numpy as np
from numpy.core.fromnumeric import sort
from numpy.lib.index_tricks import index_exp
import math
import first
import copy 

class SimplexTableSolver:

    def __init__(self,c,a,b,x_count) -> None:
        self._c= np.array(c)
        self._a = np.array(a)
        self._b = np.array(b)
        self._x_count = x_count

        # initialize simplex table
        self._simplex_table = np.zeros(shape =(np.shape(a)[0] + 1,np.shape(a)[1] + 2 + np.shape(a)[0]))
        self._simplex_table[0][0] = 1
        self._simplex_table[0,1 : x_count + 1] = -1*self._c
        self._simplex_table[1:,1 : x_count + 1]= self._a
        self._simplex_table[1:,x_count+1:-1] =np.eye(np.shape(a)[0])
        self._simplex_table[1:,-1] = self._b

    def _get_max_first_table_coeff(self):
        indx = -1
        min_negative = 0
        for i,v in enumerate(self._simplex_table[0,1:self._x_count+1]):
            if v < 0 and v < min_negative:
                min_negative = v
                indx = i + 1
        return indx
    
    def _get_min_positive_solve(self, i):
        indx = -1
        min_positive = np.inf
        for _i,v in enumerate(self._simplex_table[1:,-1]/self._simplex_table[1:,i]):
            if v > 0 and v!= np.inf and v < min_positive:
                indx = _i +1 
                min_positive = v

        return indx

    def solve(self):

        while True:
            row_inx= self._get_max_first_table_coeff()
            if row_inx == -1:
                return
            
            line_indx = self._get_min_positive_solve(row_inx)

            if line_indx == -1:
                return
            self._simplex_table[line_indx] /= self._simplex_table[line_indx][row_inx]
            for table_line_indx in range(self._simplex_table.shape[0]):
                if table_line_indx == line_indx:
                    continue
                self._simplex_table[table_line_indx] = self._simplex_table[table_line_indx] - self._simplex_table[table_line_indx,row_inx]* self._simplex_table[line_indx]
            
            print(self._simplex_table)
    def _check_if_basis(self,i):
        row = self._simplex_table[1:,i]
        one_count = np.sum(row == 1.0)
        zeros_count = np.sum(row== 0.0)
        if one_count == 1 and zeros_count == ( len(row) -1):
            return np.where(row == 1)[0][0] + 1
        else:
            return  -1
    def _find_f(self,v):
        return  v - math.floor(v)
    def integer_solve(self):
        self.solve()
        self._simplex_table[0, 1 :-2] = -self._simplex_table[0, 1 :-2]
        i=0
        while True:
            solutions = list()
            for basis_indx in range(1,self._simplex_table.shape[1]-1):
                solution_indx = self._check_if_basis(basis_indx)
                if solution_indx != -1:
                    solutions.append( (solution_indx, self._simplex_table[solution_indx,-1]))
            print("solutions")
            solutions.sort(key=lambda x: x[0])
            print(solutions)
            f_list = list(map(lambda x: (x[0],self._find_f(x[1])),solutions))
            print("Ostatki")
            print(f_list)
            f_max = np.max([x[1] for x in f_list])
            if f_max <  0.00000000001:
                print("STOP ITERATION!!!!!!!!!")
                print(self._simplex_table)
                print(solutions)
                return
            f_max_indx = first.first(f_list, key= lambda x: x[1] == f_max)[0]
            print(f"Max ostatok: {f_max},{f_max_indx}")
            self._simplex_table = np.insert(self._simplex_table,-1,np.zeros(self._simplex_table.shape[0]),1)
            row_to_insert = np.zeros(self._simplex_table.shape[1])
            row_to_insert[-1] = -1* f_max
            row_to_insert[-2] = 1
            for i in range(1,len(row_to_insert)-2):
                value = self._simplex_table[f_max_indx,i]
                row_to_insert[i] = -self._find_f(value)
            self._simplex_table=np.insert(self._simplex_table,self._simplex_table.shape[0],row_to_insert,0) 
            print("Table with insert values")
            print(self._simplex_table)
            divided_line = list()
            for x,y in zip(self._simplex_table[0, 1 :-2],self._simplex_table[-1, 1 :-2]):
                if y == 0:
                    divided_line.append(np.inf)
                else:
                    divided_line.append(x/y)
            
            min_for_new_value = np.min(divided_line)
            new_basis_indx = divided_line.index(min_for_new_value) + 1 
            value_to_divide = float(self._simplex_table[-1,new_basis_indx])
            self._simplex_table[-1]/= value_to_divide
            for row_indx  in range(self._simplex_table.shape[0] - 1):
                self._simplex_table[row_indx] = self._simplex_table[row_indx] - self._simplex_table[-1] * self._simplex_table[row_indx][new_basis_indx] 
            print("Next iteration table")
            print(self._simplex_table)
            print('\n')
'''


c = [5,4]
a= [
    [6,4],
    [1,2],
    [-1,1],
    [0,1]
    ]
b = [24,6,1,2]

#solver = SimplexTableSolver(c,a,b,2)
#solver.solve()


c = [7,10]
a= [
    [-1,3],
    [7,1]
    ]
b = [6,35]

#solver = SimplexTableSolver(c,a,b,2)
#solver.solve()



c = [1,1]
a= [[2,11],
[1,1],
[4,-5]]

b=[38,7,5]

solver = SimplexTableSolver(c,a,b,2)
solver.integer_solve()

с = [7,9]

a=[[-1,3],[7,1]]
b = [6,35]

#solver = SimplexTableSolver(c,a,b,2)
#solver.integer_solve()

c= [-2,-3]

a=[[3,5],[3,4],[0,1]]

b=[60,34,8]

#solver = SimplexTableSolver(c,a,b,2)
#solver.integer_solve()


c=[2,3]
a=[[3,4],[2,5]]

b = [24,22]

#solver = SimplexTableSolver(c,a,b,2)
#solver.integer_solve()



c=[3,2,0,0]

a=[[2,1,1,0],[1,4,0,1]]
b=[6,5]

#solver = SimplexTableSolver(c,a,b,4)
#solver.integer_solve()

'''
'''
c= [5,6]
a=[[1,1],[4,7]]
b=[5,28]

solver = SimplexTableSolver(c,a,b,2)
solver.integer_solve()
'''

'''
c=[4,5,6]
a=[[1,2,3],
[4,3,2],
[3,1,1]]

b=[35,45,40]

solver = SimplexTableSolver(c,a,b,3)
solver.integer_solve()
'''
'''
c=[7,-9]
a=[[2,1],
[0,3],
[4,5]]

b=[9,7,5]

solver = SimplexTableSolver(c,a,b,2)
solver.integer_solve()


'''

c = [1,1]
a= [[2,11],
[1,1],
[4,-5]]

b=[38,7,5]

solver = SimplexTableSolver(c,a,b,2)
solver.integer_solve()