import pandas as pd
from scipy.optimize import minimize
import math


def X(file_path, max_capacity):
    df = pd.read_csv(file_path)
    l = len(df.index)

    # Транспортные затраты
    A = -0.3975  # переменная часть транспортных затрат
    b = 42.250  # фиксированная часть транспортных затрат

    #Функция вычисления затрат
    def objective(R):
        result = 0
        for i in range(60):
            # транс. затр
            result += (A * (df.loc[i, 'DEMAND'] / R[i]) + b) * R[i]
            # кап. затр
            result += (df.loc[i, 'DEMAND'] / (2 * R[i])) * df.loc[i, 'COST'] * 0.125
            # хран. затр
            result += (df.loc[i, 'DEMAND'] / (2 * R[i])) * 12 * max_capacity / 2000
        return result

    #Ограничения
    cons = []
    # Ограничение 1: Вместимость склада
    def constraint1(R):
        loop = 0
        for i in range(60):
            loop += R[i]
        result = max_capacity - loop
        return result

    cons.append({'type': 'ineq', 'fun': constraint1})

    # Ограничение 2: Размер заказа
    for i in range(l):
        # Минимум для заказа
        c2 = lambda R: (df.loc[i, 'DEMAND'] / R[i]) - 1
        cons.append({'type': 'ineq', 'fun': c2})
        # Максимум для заказа
        c3 = lambda R: 400 - (df.loc[i, 'DEMAND'] / R[i])
        cons.append({'type': 'ineq', 'fun': c3})

    # начальная точка (преположение)
    # Все позиции пополняются на 2
    R0 = [2 for i in range(l)]

    # Границы
    b_vector = (1, 365)
    bnds = tuple([b_vector for i in range(l)])

    # Минимизация
    sol = minimize(objective, R0, method='SLSQP', bounds=bnds, constraints=cons, options={'maxiter': 500})

    # Решение
    sol_init = sol.x
    sol_final = [math.ceil(i) for i in sol_init]

    names = list(df['SKU'])
    ans_df = pd.DataFrame({'SKU': names, 'total_cost': sol_final})
    return ans_df, float(round(objective(sol_final), 1))