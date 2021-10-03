import numpy as np
from numpy.lib.index_tricks import index_exp


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

c = [5,4]
a= [
    [6,4],
    [1,2],
    [-1,1],
    [0,1]
    ]
b = [24,6,1,2]

solver = SimplexTableSolver(c,a,b,2)
solver.solve()
