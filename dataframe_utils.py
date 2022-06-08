import pandas as pd

def get_team_prochain_match_df(prochain_match):
    try:
        prochain_match = str(prochain_match).split(' ', 2)[0]
        prochain_match = str(prochain_match[:len(prochain_match) - 1])
        prochain_match = str(prochain_match).split('.', 2)[1] + '.' + str(prochain_match).split('.', 2)[0]
        prochain_match = float(prochain_match)
        return prochain_match
    except:
        return 100

def add_team_to_dataframe(app, team):
    dict_team = {
        "id": team.team_id, "taux_saison": team.taux_saison, "match_joues": team.team_matchs_joues, "victoire": team.team_victoire, "nul": team.team_nul, 
    "defaite": team.team_defaite, "team_moyenne_match_goals": team.team_moyenne_match_goals, "moyenne_goals": team.team_moyenne_goals, 
    "taux_2x_no_goal": team.taux_2x_no_goal, "taux_3x_no_goal": team.taux_3x_no_goal, "adversaire_taux_saison": team.adversaire_taux_saison,
    "taux_historique": team.taux_historique, "prochain_match": get_team_prochain_match_df(team.prochain_match), 
    "adversaire_taux_historique": team.adversaire_taux_historique, "classement": team.classement, "serie_a_contre_b": team.serie_a_contre_b
    }
    app.df = app.df.append(dict_team, ignore_index=True)

def get_dataframe_sort_values(values):
    sort_values = []
    for i in range(0, len(values)):
        if values[i] == 1:
            sort_values.append("taux_saison")
        elif values[i] == 2:
            sort_values.append("match_joues")
        elif values[i] == 3:
            sort_values.append("victoire")
        elif values[i] == 4:
            sort_values.append("nul")
        elif values[i] == 5:
            sort_values.append("defaite")
        elif values[i] == 6:
            sort_values.append("team_moyenne_goals")
        elif values[i] == 7:
            sort_values.append("moyenne_goals")
        elif values[i] == 8:
            sort_values.append("taux_2x_no_goal")
        elif values[i] == 9:
            sort_values.append("taux_3x_no_goals")
        elif values[i] == 10:
            sort_values.append("adversaire_taux_saison")
        elif values[i] == 11:
            sort_values.append("taux_historique")
        elif values[i] == 12:
            sort_values.append("prochain_match")
        elif values[i] == 13:
            sort_values.append("adversaire_taux_historique")
        elif values[i] == 14:
            sort_values.append("classement")
        elif values[i] == 15:
            sort_values.append("serie_a_contre_b")
    return sort_values


def get_dataframe_ascending_values(ascendings):
    sort_ascending = []
    for i in range(0, len(ascendings)):
        if ascendings[i] == 1:
            sort_ascending.append(True)
        else:
            sort_ascending.append(False)
    return sort_ascending


def sort_dataframe(app, values, ascendings):
    sort_values = get_dataframe_sort_values(values)
    sort_ascending = get_dataframe_ascending_values(ascendings)
    app.df = app.df.sort_values(sort_values, ascending=sort_ascending)
    app.df = app.df.reset_index(drop=True)
