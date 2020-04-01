#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Sudoku puzzle generator and solver
Robert Noakes 2020
"""

import numpy as np

class Solver():
    """
    Class that solves a sudoku puzzle
    """

    def __init__(self, puzzle):
        """
        Initialises the Solver class with the puzzle to solve

        Parameters
        ----------
        puzzle : TYPE Class instance or 9x9 2D array
            Sudoku puzzzle to be solved

        Returns
        -------
        None.

        """
        self.puzzle = puzzle
    
    def __repr__(self):
        """
        Makes the class instance call a readable format
        """
        return " {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n".format(
            self.puzzle[0], self.puzzle[1], self.puzzle[2], self.puzzle[3], 
            self.puzzle[4], self.puzzle[5], self.puzzle[6], self.puzzle[7], 
            self.puzzle[8])
    
    def __str__(self):
        """
        Return a string to print of the puzzle in a readable form.
        """
        return " {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n".format(
            self.puzzle[0], self.puzzle[1], self.puzzle[2], self.puzzle[3], 
            self.puzzle[4], self.puzzle[5], self.puzzle[6], self.puzzle[7], 
            self.puzzle[8])
    
    def __getitem__(self, index):
        """
        Parameters
        ----------
        index : TYPE list/tuple [i,j]
            Allows elements from the class instance to be indexed

        Returns
        -------
        Element of the puzzle
        """
        i, j = index
        return self.puzzle[i][j]
    
    def __setitem__(self, index):
        """
        Parameters
        ----------
        index : TYPE list/tuple [i,j]
            Allows elements from the class instance to be set

        Returns
        -------
        Element of the puzzle
        """
        i, j = index
        return self.puzzle[i][j]
        
    def num_count(self, row, elem):
        """
        Counts the number of a given integer in a row

        Parameters
        ----------
        row : TYPE int
            Row of the puzzle to test
        elem : TYPE int 0-9
            Number to count the instanced of

        Returns
        -------
        count : TYPE int
            Number of "elem" in "row"

        """
        count = 0 
        for i in row:
            if i == elem:
                count += 1
        return count
    
    def rule(self, grid, row, test):
        """
        Boolean implementation of Sudoku logic
        
        Parameters
        ----------
        grid : TYPE 2D array
            The grid to test, either the puzzle, puzzle transpose or box list 
        row : TYPE int
            Row in puzzle to check
        test : TYPE int
            Number to check in the row

        Returns
        -------
        bool
            Boolean of whether test is allowed in row

        """
        if self.num_count(grid[row], test) == 0:
            return True
        else:
            return False
    
    def row_rule(self, i, test):
        """
        Sudoku row rule
        
        Parameters
        ----------
        i : TYPE int
            Row to test.
        test : TYPE int
            Number to test in row

        Returns
        -------
        TYPE Boolean
            True if test is allowed in i

        """
        return self.rule(self.puzzle, i, test)

    def column_rule(self, j, test):
        """
        Sudoku column rule
        
        Parameters
        ----------
        j : TYPE int
            Column to test
        test : TYPE int
            Number to test in column

        Returns
        -------
        TYPE Boolean
            True if test is allowed in j
            

        """
        return self.rule([list(a) for a in list(zip(*self.puzzle))], j, test)
    
    def box_rule(self, q, r, test):
        """
        Converts Sudoku boxes into rows for testing

        Parameters
        ----------
        q : TYPE = int
            Row to test
        r : TYPE 
            Column to test
        test : TYPE
            Number to test in location

        Returns
        -------
        TYPE Boolean
            True if test is allowd in position i, j in the puzzle

        """
        tl = [self.puzzle[i][j] for i in range(0,3) for j in range(0,3)]
        tm = [self.puzzle[i][j] for i in range(0,3) for j in range(3,6)]
        tr = [self.puzzle[i][j] for i in range(0,3) for j in range(6,9)]
        ml = [self.puzzle[i][j] for i in range(3,6) for j in range(0,3)]
        mm = [self.puzzle[i][j] for i in range(3,6) for j in range(3,6)]
        mr = [self.puzzle[i][j] for i in range(3,6) for j in range(6,9)]
        bl = [self.puzzle[i][j] for i in range(6,9) for j in range(0,3)]
        bm = [self.puzzle[i][j] for i in range(6,9) for j in range(3,6)]
        br = [self.puzzle[i][j] for i in range(6,9) for j in range(6,9)]
        return self.rule([tl, tm, tr, ml, mm, mr, bl, bm, br], self.which_box(q, r), test)

    def which_box(self, i, j):
        """
        Function outputting which box row to test

        Parameters
        ----------
        i : TYPE int
            Row to test
        j : TYPE
            Column to test

        Returns
        -------
        TYPE int
            Row in the box list to test

        """
        if i < 3:
            if j < 3:
                return 0
            if j < 6:
                return 1
            if j < 9:
                return 2
        if i < 6:
            if j < 3:
                return 3
            if j < 6:
                return 4
            if j < 9:
                return 5
        if i < 9:
            if j < 3:
                return 6
            if j < 6:
                return 7
            if j < 9:
                return 8

    def elem_checker(self, i, j, test):
        """
        Function uses all rules to check if an element is possible in a position

        Parameters
        ----------
        i : TYPE int
            Row to test
        j : TYPE int
            Column to teset
        test : TYPE int
            Number to test in position [i, j]

        Returns
        -------
        bool
            True if element is allowed in chosen position

        """
        if self.row_rule(i, test) == True:
            if self.column_rule(j, test) == True:
                if self.box_rule(i, j, test) == True:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check(self):
        """
        Function used in Generator to check if a partially generated
        puzzle still has a solution

        Returns
        -------
        TYPE Boolean
            True if a given partial puzzle has a solution

        """
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0: 
                    for n in range(1, 10):
                        if self.elem_checker(i, j, n):
                            self.puzzle[i][j] = n
                            if not any(0 in row for row in self.puzzle):
                                self.bool = True
                                break
                            self.check()
                            self.puzzle[i][j] = 0
                    return self.bool

    def solve(self):
        """
        Solves and prints the solution to the sudoku puzzle

        Raises
        ------
        SystemExit
            Stops the process when a solution is found

        Returns
        -------
        None.

        """
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    for n in range(1, 10):
                        if self.elem_checker(i, j, n):
                            self.puzzle[i][j] = n
                            if not any(0 in row for row in self.puzzle):
                                print(self)
                                print("")
                                raise SystemExit("Solved!")
                            self.solve()
                            self.puzzle[i][j] = 0
                    return
                
class Generator(Solver):
    """
    Class that generates a random sudoku puzzle
    """
    
    def __init__(self):
        """
        Initialises the class with an initial 9x9 2D array of zeros 

        Returns
        -------
        None.

        """
        self.puzzle = [[0,0,0,0,0,0,0,0,0] for x in range(9)]
        self.bool = False
        
    def make(self, num):
        """
        Generates a sudoku puzzle to solve

        Parameters
        ----------
        num : TYPE int
            The number of filled in elements in the generated puzzle

        Returns
        -------
        TYPE Instance
            Sudoku puzzle to solve

        """
        for i in range(9):
            for j in range(9):
                while any(0 in row for row in self.puzzle):
                    x = np.random.randint(1,10)
                    if self.elem_checker(i, j, x):
                        self.puzzle[i][j] = x
                    if not self.check():
                        self.puzzle[i][j] = 0
                for q in range(81-num):
                    r, c = np.random.randint(0,9), np.random.randint(0,9)
                    while self.puzzle[r][c] == 0:
                        r, c = np.random.randint(0,9), np.random.randint(0,9)
                    self.puzzle[r][c] = 0
                return self.puzzle