import sys
import json
import os
from database_utils import *

def get_data_json(data):
    config_text = ''
    with open(resource_path('config/config.json'), 'r') as config_json:
        for line in config_json:
            config_text = config_text + line
        config_json.close()
    json_dict = json.loads(config_text)
    return json_dict[data]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        while '/' in relative_path:
            relative_path = relative_path.split('/', 2)[1]
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def reverse_sort_goal_by_day(app, n):
    for m in range(0, 5):
        for j in range(1, len(app.lta[n].t_home_day_sorted[m])):
            try:
                tmp = app.lta[n].t_home_day_sorted[m][j]
                tmp2 = app.lta[n].t_home_goal_first[m][j]
                i = j - 1
                while i >= 0 and app.lta[n].t_home_day_sorted[m][i] > tmp:
                    app.lta[n].t_home_day_sorted[m][i + 1] = app.lta[n].t_home_day_sorted[m][i]
                    app.lta[n].t_home_goal_first[m][i + 1] = app.lta[n].t_home_goal_first[m][i]
                    i = i - 1
                app.lta[n].t_home_day_sorted[m][i + 1] = tmp
                app.lta[n].t_home_goal_first[m][i + 1] = tmp2
            except:
                break
        app.lta[n].t_home_day_sorted[m].reverse()
        app.lta[n].t_home_goal_first[m].reverse()
    for m in range(0, 5):
        for j in range(1, len(app.lta[n].a_ext_day_sorted[m])):
            try:
                tmp = app.lta[n].a_ext_day_sorted[m][j]
                tmp2 = app.lta[n].a_ext_goal_first[m][j]
                i = j - 1
                while i >= 0 and app.lta[n].a_ext_day_sorted[m][i] > tmp:
                    app.lta[n].a_ext_day_sorted[m][i + 1] = app.lta[n].a_ext_day_sorted[m][i]
                    app.lta[n].a_ext_goal_first[m][i + 1] = app.lta[n].a_ext_goal_first[m][i]
                    i = i - 1
                app.lta[n].a_ext_day_sorted[m][i + 1] = tmp
                app.lta[n].a_ext_goal_first[m][i + 1] = tmp2
            except:
                break
        app.lta[n].a_ext_day_sorted[m].reverse()
        app.lta[n].a_ext_goal_first[m].reverse()
    
def process_journee(app, base_journee, ligue_id):
    if base_journee != '' and base_journee != None:
        try:
            journee = str(base_journee).split(' ', 2)[0]
            journee = str(journee[:len(journee) - 1])
            journee = str(journee).split('.', 2)[1] + '.' + str(journee).split('.', 2)[0]
            journee = float(journee)
            if ((ligue_id in app.ligue_end_january) and journee >= 1 and journee <= 2)\
            or ((ligue_id in app.ligue_end_july) and journee >= 8)\
            or (ligue_id not in app.ligue_end_december) and journee >= 7:
                journee = journee - 12
        except:
            journee = 0
    else:
        journee = 0
    return journee


def get_all_match_winner_team_a_contre_team_b(app, n):
    for m in range(0, 5):
        app.lta[n].t_vs_a_winner.append([])
        for i in range(0, len(app.lta[n].t_match_id[m])):
            for j in range(0, len(app.lta[n].a_match_id[m])):
                if app.lta[n].a_match_id[m][j] == app.lta[n].t_match_id[m][i]:
                    if app.lta[n].t_match_res[m][i] > app.lta[n].a_match_res[m][j]:
                        app.lta[n].t_vs_a_winner[m].append(1)
                    elif app.lta[n].t_match_res[m][i] < app.lta[n].a_match_res[m][j]:
                        app.lta[n].t_vs_a_winner[m].append(-1)
                    else:
                        app.lta[n].t_vs_a_winner[m].append(0)

def get_all_match_team_a_contre_team_b(app, n):
    for m in range(0, 5):
        app.lta[n].t_vs_a_match_id.append([])
        app.lta[n].t_vs_a_day_sorted.append([])
        app.lta[n].t_vs_a_goal_first.append([])
        for i in range(0, len(app.lta[n].t_match_id[m])):
            for j in range(0, len(app.lta[n].a_match_id[m])):
                if app.lta[n].a_match_id[m][j] == app.lta[n].t_match_id[m][i] and process_journee(app, app.lta[n].t_match_day[m][i], app.lta[n].ligue_id) not in app.lta[n].t_vs_a_day_sorted[m]:
                    app.lta[n].t_vs_a_match_id[m].append(app.lta[n].t_match_id[m][i])
                    app.lta[n].t_vs_a_day_sorted[m].append(process_journee(app, app.lta[n].t_match_day[m][i], app.lta[n].ligue_id))
                    app.lta[n].t_vs_a_goal_first[m].append(app.lta[n].t_match_goalfirst[m][i])

def get_all_match_domicile(app, n):
    for i in range(0, 5):
        app.lta[n].t_home_day_sorted.append([])
        app.lta[n].t_home_goal_first.append([])
        for j in range(0, len(app.lta[n].t_match_home[i])):
            if app.lta[n].t_match_home[i][j] == 1 and process_journee(app, app.lta[n].t_match_day[i][j], app.lta[n].ligue_id) not in app.lta[n].t_home_day_sorted[i]:
                app.lta[n].t_home_day_sorted[i].append(process_journee(app, app.lta[n].t_match_day[i][j], app.lta[n].ligue_id))
                app.lta[n].t_home_goal_first[i].append(app.lta[n].t_match_goalfirst[i][j])

def get_all_match_exterieur(app, n):
    for i in range(0, 5):
        app.lta[n].a_ext_day_sorted.append([])
        app.lta[n].a_ext_goal_first.append([])
        for j in range(0, len(app.lta[n].a_match_home[i])):
            if app.lta[n].a_match_home[i][j] == 0 and process_journee(app, app.lta[n].a_match_day[i][j], app.lta[n].ligue_id) not in app.lta[n].a_ext_day_sorted[i]:
                app.lta[n].a_ext_day_sorted[i].append(process_journee(app, app.lta[n].a_match_day[i][j], app.lta[n].ligue_id))
                app.lta[n].a_ext_goal_first[i].append(app.lta[n].a_match_goalfirst[i][j])

def get_all_match_domicile_team_a_contre_team_b(app, n):
    for m in range(0, 5):
        app.lta[n].t_vs_a_home_day_sorted.append([])
        app.lta[n].t_vs_a_home_goal_first.append([])
        for i in range(0, len(app.lta[n].t_match_id[m])):
            if app.lta[n].t_match_home[m][i] == 1:
                for j in range(0, len(app.lta[n].a_match_id[m])):
                    if app.lta[n].a_match_id[m][j] == app.lta[n].t_match_id[m][i] and process_journee(app, app.lta[n].t_match_day[m][i], app.lta[n].ligue_id) not in  app.lta[n].t_vs_a_home_day_sorted[m]:
                        app.lta[n].t_vs_a_home_day_sorted[m].append(process_journee(app, app.lta[n].t_match_day[m][i], app.lta[n].ligue_id))
                        app.lta[n].t_vs_a_home_goal_first[m].append(app.lta[n].t_match_goalfirst[m][i])

def get_stats(cursor, app, n, m):
    total_team_score = 0
    total_adversaire_score = 0
    a_match_res = 0
    for i in range(0, len(app.lta[n].t_match_id[m])):
        match_is_against_b = 0
        for j in range(0, len(app.lta[n].a_match_id[m])):
            if app.lta[n].a_match_id[m][j] == app.lta[n].t_match_id[m][i]:
                match_is_against_b = 1
                app.lta[n].team_against_adversaire_matchs_joues = app.lta[n].team_against_adversaire_matchs_joues + 1
                if app.lta[n].t_match_res[m][i] > app.lta[n].a_match_res[m][j]:
                    app.lta[n].team_against_adversaire_victoire = app.lta[n].team_against_adversaire_victoire + 1
                elif app.lta[n].t_match_res[m][i] < app.lta[n].a_match_res[m][j]:
                    app.lta[n].adversaire_victoire = app.lta[n].team_against_adversaire_victoire + 1
                elif app.lta[n].t_match_res[m][i] == app.lta[n].a_match_res[m][j]:
                    app.lta[n].team_against_adversaire_nul = app.lta[n].team_against_adversaire_nul + 1
                a_match_res == app.lta[n].a_match_res[m][j]
                total_adversaire_score = total_adversaire_score + app.lta[n].a_match_res[m][j]
        if match_is_against_b == 0:
            a_match_res = database_fetchone(cursor, "SELECT GOAL FROM matchs WHERE ID = %d AND TEAM_ID != %d" % (app.lta[n].t_match_id[m][i], app.lta[n].team_id))
        if app.lta[n].t_match_res[m][i] > a_match_res:
                app.lta[n].team_victoire = app.lta[n].team_victoire + 1
        elif app.lta[n].t_match_res[m][i] < a_match_res:
                app.lta[n].team_defaite = app.lta[n].team_defaite + 1
        elif app.lta[n].t_match_res[m][i] == a_match_res:
                app.lta[n].team_nul = app.lta[n].team_nul + 1
        total_team_score =  total_team_score + app.lta[n].t_match_res[m][i]
    app.lta[n].team_matchs_joues = len(app.lta[n].t_match_id[m])
    if len(app.lta[n].t_match_id[m]) != 0:
        app.lta[n].team_moyenne_match_goals  = round(total_team_score / len(app.lta[n].t_match_id[m]), 2)
    if app.lta[n].team_against_adversaire_matchs_joues != 0:
        app.lta[n].team_against_adversaire_moyenne_match_goals  = round(total_adversaire_score / app.lta[n].team_against_adversaire_matchs_joues, 2)

def get_moyenne_goals(app, n):
    total_match = 0
    total_match_against_adversaire = 0
    res = 0 
    res_against_adversaire = 0
    for m in range(0, 5):
        for i in range(0, len(app.lta[n].t_match_id[m])):
            res = app.lta[n].t_match_res[m][i] + res 
            total_match = total_match + 1
            for j in range(0, len(app.lta[n].a_match_id[m])):
                if app.lta[n].a_match_id[m][j] == app.lta[n].t_match_id[m][i]:
                    res_against_adversaire = res_against_adversaire + app.lta[n].t_match_res[m][i]
                    total_match_against_adversaire = total_match_against_adversaire + 1
    if total_match != 0:
        app.lta[n].team_moyenne_goals = round(res / total_match, 2)
    if total_match_against_adversaire != 0 :
        app.lta[n].team_against_adversaire_moyenne_goals = round(res_against_adversaire / total_match_against_adversaire, 2)