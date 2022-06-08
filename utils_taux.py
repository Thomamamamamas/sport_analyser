from utils import *
from database_utils import *

def get_taux_historique(app, n):
    total_match = 0
    total_goal_first = 0
    for i in range(0, 5):
        total_match = total_match + len(app.lta[n].t_home_goal_first[i])
        for j in range(0, len(app.lta[n].t_home_goal_first[i])):
            if app.lta[n].t_home_goal_first[i][j] == 1:
                total_goal_first = total_goal_first + 1
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0.0

def get_taux_actual_saison(app, n, year):
    total_match = 0
    total_goal_first = 0
    total_match = len(app.lta[n].t_home_goal_first[year])
    for i in range(0, total_match):
        if app.lta[n].t_home_goal_first[year][i] == 1:
            total_goal_first = total_goal_first + 1
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0.0

def get_taux_historique_adversaire(app, n):
    total_match = 0
    total_goal_first = 0
    for i in range(0, 5):
        total_match = total_match + len(app.lta[n].a_ext_goal_first[i])
        for j in range(0, len(app.lta[n].a_ext_goal_first[i])):
            if app.lta[n].a_ext_goal_first[i][j] == 1:
                total_goal_first = total_goal_first + 1
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0.0

def get_taux_actual_saison_adversaire(app, n, year):
    total_match = 0
    total_goal_first = 0
    total_match = len(app.lta[n].a_ext_goal_first[year])
    for i in range(0, total_match):
        if app.lta[n].a_ext_goal_first[year][i] == 0:
            total_goal_first = total_goal_first + 1
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0.0

def get_taux_x_no_goal(app, n, year1, x):
    total_match = 0
    total_goal_first = 0
    tmp = 0
    for j in range(0, 5):
        tmp_total_match = len(app.lta[n].t_home_goal_first[j])
        total_match = tmp_total_match + total_match
        for i in range(0, tmp_total_match):
            if app.lta[n].t_home_goal_first[j][i] == 0:
                tmp = tmp + 1
                if tmp == x :
                    total_goal_first = total_goal_first + 1
            else:
                tmp = 0
        year1 = year1 - 1
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0

def taux_historique_a_contre_b(app, n):
    total_goal_first = 0
    total_match = 0
    
    for i in range(0, 5):
        try:
            total_match = total_match + len(app.lta[n].t_home_day_sorted[i])
            for j in range(0, len(app.lta[n].t_home_day_sorted[i])):
                if app.lta[n].t_home_goal_first[i][j] == 1:
                    total_goal_first = total_goal_first + 1
        except:
            continue
    if total_match != 0:
        return round((total_goal_first / total_match) * 100, 2)
    else:
        return 0.0
