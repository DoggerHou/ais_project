import pandas as pd
from pulp import *
import numpy as np
from scipy.optimize import minimize
import math
import time


def X(file_path, max_capacity):
    df = pd.read_csv(file_path)
    l = len(df.index)

    # Transportation Costs
    A = -0.3975  # variable part of transportation cost
    b = 42.250  # fixed part of transportation cost

    #Objective Function
    def objective(R):
        result = 0
        for i in range(60):
            # TR Costs
            result += (A * (df.loc[i, 'DEMAND'] / R[i]) + b) * R[i]
            # Capital Costs
            result += (df.loc[i, 'DEMAND'] / (2 * R[i])) * df.loc[i, 'COST'] * 0.125
            # Storage Costs
            result += (df.loc[i, 'DEMAND'] / (2 * R[i])) * 12 * max_capacity / 2000
        return result

    # CONSTARAITS
    cons = []
    # Constraint 1: Maximum inventory
    def constraint1(R):
        loop = 0
        for i in range(60):
            loop += R[i]
        result = max_capacity - loop
        return result

    cons.append({'type': 'ineq', 'fun': constraint1})

    # Constraint 2: Order Size
    for i in range(l):
        # Minimum Order Quantity
        c2 = lambda R: (df.loc[i, 'DEMAND'] / R[i]) - 1
        cons.append({'type': 'ineq', 'fun': c2})
        # Maximum Order Quantity
        c3 = lambda R: 400 - (df.loc[i, 'DEMAND'] / R[i])
        cons.append({'type': 'ineq', 'fun': c3})

    # Initial value (guessing)
    # All SKU replenished 1 time
    R0 = [2 for i in range(l)]

    # Bounds
    # Bound vector
    b_vector = (1, 365)
    bnds = tuple([b_vector for i in range(l)])

    sol = minimize(objective, R0, method='SLSQP', bounds=bnds, constraints=cons, options={'maxiter': 500})

    # Solution values
    # Initial solution
    sol_init = sol.x
    # Take the ceiling of the solution to have an integer as number of replenishment
    sol_final = [math.ceil(i) for i in sol_init]

    names = list(df['SKU'])

    ans_df = pd.DataFrame({'SKU': names, 'total_cost': sol_final})

    return ans_df, sum(sol_final)