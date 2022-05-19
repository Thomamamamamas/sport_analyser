from curses import nocbreak
import mysql
from database_utils import *

class Day_goal():
    def __init__(self):
        self.domicile_journee = []
        self.domicile_match = []


def get_taux_historique(db, team_id):
    try:
        cursor = db.cursor()
        domicile_match = database_fetchall(cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1" % (team_id))
        total_match = len(domicile_match)
        total_goal_first = 0

        for i in range(0, total_match):
            if domicile_match[i] == 1:
                total_goal_first = total_goal_first + 1
        return round((total_goal_first / total_match) * 100, 2)
    except:
        return 0

def get_taux_actual_season(db, team_id, year1, year2):
    try:
        cursor = db.cursor()
        domicile_match = database_fetchall(cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
        total_match = len(domicile_match)
        total_goal_first = 0

        for i in range(0, total_match):
            if domicile_match[i] == 1:
                total_goal_first = total_goal_first + 1
        return round((total_goal_first / total_match) * 100, 2)
    except:
        return 0

def reverse_sort_goal_by_day(s_dg):
    for j in range(1, len(s_dg.domicile_match)):
        tmp = s_dg.domicile_journee[j]
        tmp2 = s_dg.domicile_match[j]
        i = j - 1
        while i >= 0 and s_dg.domicile_journee[i] > tmp:
            s_dg.domicile_journee[i + 1] = s_dg.domicile_journee[i]
            s_dg.domicile_match[i + 1] = s_dg.domicile_match[i]
            i = i - 1
        s_dg.domicile_journee[i + 1] = tmp
        s_dg.domicile_match[i + 1] = tmp2
    s_dg.domicile_journee.reverse()
    s_dg.domicile_match.reverse()
    
def get_domicile_journee(s_dg):
    for i in range(0, len(s_dg.domicile_journee)):
        if s_dg.domicile_journee[i] != '' and s_dg.domicile_journee[i] != None:
            s_dg.domicile_journee[i] = s_dg.domicile_journee[i].replace("Journée ", '')
            s_dg.domicile_journee[i] = s_dg.domicile_journee[i].replace("1/8 de finale", '97')
            s_dg.domicile_journee[i] = s_dg.domicile_journee[i].replace("Quarts de finale", '')
            s_dg.domicile_journee[i] = s_dg.domicile_journee[i].replace("Demi-finales", '99')
            s_dg.domicile_journee[i] = s_dg.domicile_journee[i].replace("Finale", '100')
            if s_dg.domicile_journee[i] != '':
                s_dg.domicile_journee[i] = int(s_dg.domicile_journee[i])
            else:
                s_dg.domicile_journee[i] = 0
        else:
            s_dg.domicile_journee[i] = 0
    
def get_actual_serie(db, team_id, year1, year2):
    try:
        s_dg = Day_goal()
        cursor = db.cursor()
        s_dg.domicile_match = database_fetchall(cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
        s_dg.domicile_journee = database_fetchall(cursor, "SELECT JOURNEE FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
        s_dg.domicile_journee =  s_dg.domicile_journee + database_fetchall(cursor, "SELECT JOURNEE FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1 - 1, year2 - 1))
        s_dg.domicile_journee =  s_dg.domicile_journee + database_fetchall(cursor, "SELECT JOURNEE FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1 - 2, year2 - 2))
        get_domicile_journee(s_dg)
        reverse_sort_goal_by_day(s_dg)
        actual_serie = []
        for i in range(0, 5):
            if i == len(s_dg.domicile_match):
                break
            if s_dg.domicile_match[i] != 0:
                actual_serie.append(1)
            else:
                actual_serie.append(0)
        actual_serie.reverse()
        return actual_serie
    except:
        actual_serie.reverse()
        return actual_serie

def get_longest_serie_without_goal(db, team_id, year1, year2):
    s_dg = Day_goal()
    cursor = db.cursor()
    res = 0
    tmp = 0
    for i in range(0, 5):
        s_dg.domicile_match = database_fetchall(cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
        s_dg.domicile_journee = database_fetchall(cursor, "SELECT JOURNEE FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
        if s_dg.domicile_journee == None:
            return get_longest_serie_without_goal(db, team_id, year1 - 1, year2 - 1)
        get_domicile_journee(s_dg)
        for j in range(0, len(s_dg.domicile_journee)):
            if j == len(s_dg.domicile_match):
                break
            if s_dg.domicile_match[j] == 0:
                tmp = tmp + 1
            else:
                if tmp > res:
                    res = tmp
                tmp = 0
        year1 = year1 - 1
        year2 = year2 - 1
        s_dg.domicile_match.clear()
        s_dg.domicile_journee.clear()
    return res

def calculate_actual_serie(actual_serie):
    res = 0

    for i in range(len(actual_serie) - 1, -1, -1):
        if actual_serie[i] == 0:
            res = res + 1
        else:
            break
    return res

def get_taux_x_no_goal(db, team_id, x):
    try:
        cursor = db.cursor()
        domicile_match = database_fetchall(cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1" % (team_id))
        total_match = len(domicile_match)
        total_goal_first = 0
        tmp = 0

        for i in range(0, total_match):
            if domicile_match[i] == 1:
                tmp = tmp + 1
                if tmp == x:
                    total_goal_first = total_goal_first + 1
            else:
                tmp = 0
        return round((total_goal_first / total_match) * 100, 2)
    except:
        return 0