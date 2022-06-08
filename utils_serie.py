from utils import *

def get_actual_serie(app, n, year1):
    actual_serie = []
    for j in range(0, 5):
        if len(actual_serie) == 5:
            break
        for i in range(0, len(app.lta[n].t_home_goal_first[j])):
            if i == len(app.lta[n].t_home_goal_first[j]) or len(actual_serie) == 5:
                break
            if app.lta[n].t_home_goal_first[j][i] != 0:
                actual_serie.append(1)
            else:
                actual_serie.append(0)  
        year1 = year1 - 1
    actual_serie.reverse()
    return actual_serie

def get_longest_serie_without_goal(app, n, year1):
    res = 0
    tmp = 0
    for i in range(0, 5):
        for j in range(0, len(app.lta[n].t_home_day_sorted[i])):
            if j == len(app.lta[n].t_home_goal_first[i]):
                break
            if app.lta[n].t_home_goal_first[i][j] == 0:
                tmp = tmp + 1
            else:
                if tmp > res:
                    res = tmp
                tmp = 0
        year1 = year1 - 1
    if tmp > res:
        res = tmp
    return res

def calculate_actual_serie(actual_serie):
    res = 0

    for i in range(len(actual_serie) - 1, -1, -1):
        if actual_serie[i] == 0:
            res = res + 1
        else:
            break
    return res

def get_tete_a_tete(year1, app, n):
    res = []
    for j in range(0, 5):
        if len(res) == 5:
            break
        for i in range(0, len(app.lta[n].t_vs_a_winner[j])):
            if len(res) == 5:
                break
            elif app.lta[n].t_vs_a_winner[j][i] == -1:
                res.append("D")
            elif app.lta[n].t_vs_a_winner[j][i] == 1:
                res.append("V")
            else:
                res.append("N")
        year1 = year1 - 1
    res.reverse()
    return res

def get_serie_a_contre_b(year1, app, n):
    actual_serie = []
    for j in range(0, 5):
        if len(actual_serie) == 5:
            break
        for i in range(0, len(app.lta[n].t_vs_a_home_goal_first[j])):
            if len(actual_serie) == 5:
                break
            if i == len(app.lta[n].t_vs_a_home_goal_first[j]):
                break
            if app.lta[n].t_vs_a_home_goal_first[j][i] != 0:
                actual_serie.append(1)
            else:
                actual_serie.append(0)
        year1 = year1 - 1 
    actual_serie.reverse()
    return actual_serie

def get_longest_serie_without_goal_a_contre_b(app, n, year1):
    res = 0
    tmp = 0
    for i in range(0, 5):
        for j in range(0, len(app.lta[n].t_vs_a_home_goal_first[i])):
            if j == len(app.lta[n].t_vs_a_home_goal_first[i]):
                break
            if app.lta[n].t_vs_a_home_goal_first[i][j] == 0:
                tmp = tmp + 1
            else:
                if tmp > res:
                    res = tmp
                tmp = 0
        year1 = year1 - 1
    return res