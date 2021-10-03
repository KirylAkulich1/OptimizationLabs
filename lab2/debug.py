import numpy as np
from numpy.lib.index_tricks import index_exp
import math

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

        print(self._simplex_table)

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
        print(i)
        print(self._simplex_table[1:,i])
        print(self._simplex_table[1:,-1]/self._simplex_table[1:,i])
        for _i,v in enumerate(self._simplex_table[1:,-1]/self._simplex_table[1:,i]):
            if v > 0 and v!= np.inf and v < min_positive:
                indx = _i +1 
                min_positive = v

        return indx

    def solve(self):

        while True:
            row_inx= self._get_max_first_table_coeff()
            if row_inx == -1:
                print("STOP ITERATION!!!!")
                return
            
            line_indx = self._get_min_positive_solve(row_inx)

            if line_indx == -1:
                print("STOP ITERATION!!")
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
        if one_count == 1 and zeros_count ==( len(row) -1):
            return np.where(row == 1)[0][0] +1
        else:
            return  -1
    def _find_f(self,v):
        return  v- math.floor(v)
    def integer_solve(self):
        self.solve()
        basis_indexes = [i+1 for i in range(self._x_count)]
        while True:
            solutions = np.zeros(self._x_count)
            for basis_indx in basis_indexes:
                solution_indx = self._check_if_basis(basis_indx)
                if solution_indx != -1:
                    solutions[basis_indx - 1] = self._simplex_table[solution_indx,-1]
            print(solutions)
            f_list = list(map(lambda x: self._find_f(x),solutions))
            f_max = np.max(f_list)
            if f_max == 0:
                print("STOP ITERATION!!!!!!!!!")
                return
            f_max_indx = f_list.index(f_max) + 1
            self._simplex_table=np.insert(self._simplex_table,-1,np.zeros(self._simplex_table.shape[0]),1)
            row_to_insert = np.zeros(self._simplex_table.shape[1])
            row_to_insert[-1] = -1* f_max
            row_to_insert[-2] = 1
            for i in range(len(row_to_insert)-3):
                value = self._simplex_table[f_max_indx][i+1]
                row_to_insert[i + 1] = -self._find_f(value)
            self._simplex_table=np.insert(self._simplex_table,self._simplex_table.shape[0],row_to_insert,0) 
            print(self._simplex_table)  
            
            divided_line = self._simplex_table[0,:-2]/self._simplex_table[-1,:-2]
            min_for_new_value = min(divided_line)
            new_basis_indx = divided_line.index(min_for_new_value) + 1
            self._simplex_table[-1]/= min_for_new_value
            for row_indx  in range(self._simplex_table.shape[0] - 1):
                self._simplex_table[row_indx] = self._simplex_table[row_indx] - self._simplex_table[-1] * self._simplex_table[row_indx][new_basis_indx] 
            return


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

c=[4,5,6]
a=[[1,2,3],
[4,3,2],
[3,1,1]]

b=[35,45,40]

solver = SimplexTableSolver(c,a,b,3)
solver.integer_solve()