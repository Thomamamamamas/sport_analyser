import tkinter
from PIL import Image
from multiprocessing import Process, Manager
from database_utils import *
from utils import *
from utils_taux import *
from utils_serie import *
from widget_team import get_image, delete_all_teams_widget
    
class Team_data():
    def __init__(self):
        #____________________________________________________________________TEAM_INFO______________________________________________________________________________________
        self.team_id = 0
        self.ligue_id = 0
        self.ligue_name = ''
        self.team_name = ''
        self.classement = ''
        self.a_classement = ''
        self.cotes = ''
        self.ligue_logo_url = ''
        self.team_logo_url = ''
        self.logo_cv = []
        self.photo = []
        self.BG = ''
        self.TEAM_BG = '#79CEFF'
        self.ADVERSAIRE_BG = '#FD8D23'
        #____________________________________________________________________TEAM_TAUX______________________________________________________________________________________
        self.taux_historique = 0
        self.taux_saison = 0
        self.serie = [0-0-0-0-0]
        self.longest_serie = 0
        self.actual_serie = 0
        self.taux_2x_no_goal = 0
        self.taux_3x_no_goal = 0
        self.prochain_match = ''
        #____________________________________________________________________ADVERSAIRE______________________________________________________________________________________
        self.adversaire = ''
        self.adversaire_team_id = 0
        self.adversaire_taux_historique = 0
        self.adversaire_taux_saison = 0
        self.tete_a_tete = []
        self.serie_a_contre_b = []
        self.taux_historique_a_contre_b = []
        self.longest_serie_a_contre_b = 0
        self.actual_serie_a_contre_b = 0
        #_______________________________________________________________________TEAM_TK______________________________________________________________________________________
        self.team_frame = None
        self.ligue_frame = None
        self.ligue_label = None
        self.team_name_frame = None
        self.team_label = None
        self.taux_historique_label = None
        self.taux_saison_label = None
        self.serie_label = None
        self.longest_serie_label = None
        self.taux_2x_no_goal_label = None
        self.taux_3x_no_goal_label = None
        self.prochain_match_label = None
        self.empty_label = None
        self.adversaire_label = None
        self.adversaire_taux_historique_label = None
        self.adversaire_taux_saison_label = None
        self.tete_a_tete_label = None
        self.serie_a_contre_b_label = None
        self.taux_historique_a_contre_b_label = None
        self.longest_serie_a_contre_b_label = None
        self.actual_serie_a_contre_b_label = None
        self.match_joues_label = None
        self.victoire_label = None
        self.nul_label = None
        self.defaite_label = None
        self.moyenne_match_goals_label = None
        self.moyenne_goals_label = None
        self.empty_large_label = None
        #____________________________________________________________________TEAM_OTHERS_STATS_____________________________________________________________________________________
        self.team_matchs_joues = 0
        self.team_victoire = 0
        self.team_nul = 0
        self.team_defaite = 0
        self.team_moyenne_match_goals = 0
        self.team_moyenne_goals = 0

        self.team_against_adversaire_matchs_joues = 0
        self.team_against_adversaire_victoire = 0   
        self.team_against_adversaire_nul = 0
        self.team_against_adversaire_defaite = 0
        self.team_against_adversaire_moyenne_match_goals = 0
        self.team_against_adversaire_moyenne_goals = 0
        
        self.t_home_day_sorted = []
        self.t_home_goal_first = []

        self.a_ext_day_sorted = []
        self.a_ext_goal_first = []

        self.t_vs_a_home_day_sorted = []
        self.t_vs_a_home_goal_first = []

        self.t_vs_a_match_id = []
        self.t_vs_a_day_sorted = []
        self.t_vs_a_winner = []
        self.t_vs_a_goal_first = []
        self.t_vs_a_total_domicile_match = 0
        self.t_vs_a_total_goal_first = 0

        self.t_match_id = []
        self.t_match_day = []
        self.t_match_res = []
        self.t_match_home = []
        self.t_match_goalfirst = []
        self.t_total_domicile_match = 0
        self.t_total_goal_first = 0
        self.t_saison_domicile_match = 0
        self.t_saison_goal_first = 0

        self.a_match_id = []
        self.a_match_home = []
        self.a_match_res = []
        self.a_match_day = []
        self.a_match_goalfirst = []
        self.a_total_exterieur_match = 0
        self.a_total_goal_first = 0
        self.a_saison_exterieur_match = 0
        self.a_saison_goal_first = 0

        self.o_match_id = []
        self.o_match_res = []

        self.team_victoire = 0
        self.team_nul = 0
        self.team_defaite = 0
        self.team_against_adversaire_victoire = 0
        self.team_against_adversaire__nul = 0
        self.team_against_adversaire_defaite = 0

def check_if_team_is_valid(app, n):
    if (app.lta[n].prochain_match == None or app.lta[n].prochain_match == '') or (len(app.lta[n].t_match_id[0]) == 0 and len(app.lta[n].t_match_id[1]) == 0):
        return 0
    return 1

def get_team_taux(app, n, year1):
    if year1 == app.YEAR1:
        app.lta[n].taux_historique = get_taux_historique(app, n)
        app.lta[n].taux_saison = get_taux_actual_saison(app, n, 0)
        app.lta[n].serie = get_actual_serie(app, n, year1)
        app.lta[n].actual_serie = calculate_actual_serie(app.lta[n].serie)
    else:
        app.lta[n].taux_saison = get_taux_actual_saison(app, n, 1)
    app.lta[n].longest_serie = get_longest_serie_without_goal(app, n, year1)
    app.lta[n].taux_2x_no_goal = get_taux_x_no_goal(app, n, year1, 2)
    app.lta[n].taux_3x_no_goal = get_taux_x_no_goal(app, n, year1, 3)
    if app.lta[n].actual_serie >= app.lta[n].longest_serie and app.lta[n].longest_serie > 0:
        app.lta[n].BG = '#66ff99'
        if year1 == app.YEAR1:
            app.lta[n + 1].BG = '#66ff99'

def get_team_adversaire(app, n, year1):
    if year1 == app.YEAR1:
        app.lta[n].adversaire_taux_historique = get_taux_historique_adversaire(app, n)
        app.lta[n].tete_a_tete = get_tete_a_tete(year1, app, n)
        app.lta[n].serie_a_contre_b = get_serie_a_contre_b(year1, app, n)
        app.lta[n].taux_historique_a_contre_b = taux_historique_a_contre_b(app, n)
        app.lta[n].actual_serie_a_contre_b = calculate_actual_serie(app.lta[n].serie_a_contre_b)
        app.lta[n].longest_serie_a_contre_b = get_longest_serie_without_goal_a_contre_b(app, n, year1)
        app.lta[n].adversaire_taux_saison = get_taux_actual_saison_adversaire(app, n, 0) 
    else:
        app.lta[n].adversaire_taux_saison = get_taux_actual_saison_adversaire(app, n, 1)
    
def get_team_others_stats(app, n, year1):
    if year1 == app.YEAR1:
        get_stats(app.cursor, app, n, 0)
    else:
        get_stats(app.cursor, app, n, 1)
    get_moyenne_goals(app, n)


def get_team_tk(app, n, year1):
    if app.lta[n].BG == '#66ff99':
        app.lta[n].TEAM_BG = '#66ff99'
        app.lta[n].ADVERSAIRE_BG = '#66ff99'
    app.lta[n].team_frame = tkinter.Frame(app.scrollable_frame, bg=app.lta[n].BG, highlightbackground="black", highlightthickness=2)
    app.lta[n].ligue_frame = tkinter.Frame(app.lta[n].team_frame, bg= app.lta[n].BG, height= app.height_column, width = app.large_column)
    app.lta[n].taux_saison_label = tkinter.Label(app.lta[n].team_frame, text= "%s\n%s (%s / %s)" % (app.lta[n].taux_saison, year1, app.lta[n].t_saison_goal_first, app.lta[n].t_saison_domicile_match ), font=app.font_style,  bg= app.lta[n].TEAM_BG, fg='black', height= 3, width = app.small_column)
    app.lta[n].adversaire_taux_saison_label = tkinter.Label(app.lta[n].team_frame, text= "%s\n%s (%s / %s)" % (app.lta[n].adversaire_taux_saison, year1, app.lta[n].a_saison_goal_first, app.lta[n].a_saison_exterieur_match ), font=app.font_style,  bg= app.lta[n].ADVERSAIRE_BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].match_joues_label =  tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].team_matchs_joues, app.lta[n].team_against_adversaire_matchs_joues), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].victoire_label =  tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].team_victoire, app.lta[n].team_against_adversaire_victoire), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].nul_label =  tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].team_nul, app.lta[n].team_against_adversaire_nul), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].defaite_label =  tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].team_defaite, app.lta[n].team_against_adversaire_defaite), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].moyenne_match_goals_label =  tkinter.Label(app.lta[n].team_frame, text="%s / %s" % (app.lta[n].team_moyenne_match_goals, app.lta[n].team_against_adversaire_moyenne_match_goals), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    app.lta[n].moyenne_goals_label =  tkinter.Label(app.lta[n].team_frame, text="%s / %s" % (app.lta[n].team_moyenne_goals, app.lta[n].team_against_adversaire_moyenne_goals), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
    if year1 == app.YEAR1:
        app.lta[n].team_name_frame = tkinter.Frame(app.lta[n].team_frame,bg= app.lta[n].TEAM_BG, height= app.height_column, width = app.large_column)
        app.lta[n].ligue_label = tkinter.Label(app.lta[n].ligue_frame, text= app.lta[n].ligue_name, font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width=app.medium_column)
        app.lta[n].team_label = tkinter.Label(app.lta[n].team_name_frame, text= app.lta[n].team_name, font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width=app.medium_column)
        app.lta[n].taux_2x_no_goal_label = tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].taux_2x_no_goal), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_3x_no_goal_label = tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].taux_3x_no_goal), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_historique_label = tkinter.Label(app.lta[n].team_frame, text= "%s\n2017 (%s / %s)" % (app.lta[n].taux_historique, app.lta[n].t_total_goal_first, app.lta[n].t_total_domicile_match), font=app.font_style,  bg= app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].serie_label = tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].serie), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].longest_serie_label = tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].actual_serie, app.lta[n].longest_serie), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].prochain_match_label = tkinter.Label(app.lta[n].team_frame, text= app.lta[n].prochain_match, font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.large_column)
        app.lta[n].adversaire_label = tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].adversaire), font=app.font_style,  bg= app.lta[n].ADVERSAIRE_BG, fg='black', height= app.height_column, width = app.large_column)
        app.lta[n].adversaire_taux_historique_label =  tkinter.Label(app.lta[n].team_frame, text= "%s\n2017 (%s / %s)" % (app.lta[n].adversaire_taux_historique, app.lta[n].a_total_goal_first, app.lta[n].a_total_exterieur_match ), font=app.font_style,  bg= app.lta[n].ADVERSAIRE_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].cote_match_label = tkinter.Label(app.lta[n].team_frame, text=app.lta[n].cotes, font=app.font_style, fg='black', bg=app.lta[n].BG, borderwidth=2,  height = app.height_column, width = app.small_column)
        app.lta[n].classement_label = tkinter.Label(app.lta[n].team_frame, text="%s / %s" % (app.lta[n].classement, app.lta[n].a_classement), font=app.font_style, fg='black', bg=app.lta[n].BG, borderwidth=2,  height = app.height_column, width = app.small_column)
        app.lta[n].tete_a_tete_label =  tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].tete_a_tete), font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.medium_column)
        app.lta[n].serie_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text= str(app.lta[n].serie_a_contre_b), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_historique_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text = "%s\n2017 (%s / %s)" % (app.lta[n].taux_historique_a_contre_b, app.lta[n].t_vs_a_total_goal_first, app.lta[n].t_vs_a_total_domicile_match), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].longest_serie_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text="%d / %d" % (app.lta[n].actual_serie_a_contre_b, app.lta[n].longest_serie_a_contre_b), font=app.font_style,  bg=app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        get_image(app.lta[n].ligue_logo_url, app, n, 0)  
        get_image(app.lta[n].team_logo_url, app, n, 1)
    else:
        app.lta[n].team_name_frame = tkinter.Frame(app.lta[n].team_frame,bg= app.lta[n].BG, height= app.height_column, width = app.large_column)
        app.lta[n].ligue_label = tkinter.Label(app.lta[n].ligue_frame, text=  " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width=app.large_column)
        app.lta[n].team_label = tkinter.Label(app.lta[n].team_name_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width=app.large_column)
        app.lta[n].taux_historique_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.medium_empty_column)
        app.lta[n].serie_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].longest_serie_label = tkinter.Label(app.lta[n].team_frame, text="%d" % (app.lta[n].longest_serie), font=app.font_style,  bg= app.lta[n].TEAM_BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_2x_no_goal_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_3x_no_goal_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].prochain_match_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.large_column)
        app.lta[n].adversaire_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.large_column)
        app.lta[n].adversaire_taux_historique_label =  tkinter.Label(app.lta[n].team_frame, text= "", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].cote_match_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style, fg='black', bg=app.lta[n].BG, borderwidth=2,  height = app.height_column, width = app.small_column)
        app.lta[n].classement_label = tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style, fg='black', bg=app.lta[n].BG, borderwidth=2,  height = app.height_column, width = app.small_column)
        app.lta[n].tete_a_tete_label =  tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.medium_column)
        app.lta[n].serie_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].taux_historique_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text= " ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].longest_serie_a_contre_b_label =  tkinter.Label(app.lta[n].team_frame, text=" ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.small_column)
        app.lta[n].empty_large_label =  tkinter.Label(app.lta[n].team_frame, text="                                                        ", font=app.font_style,  bg=app.lta[n].BG, fg='black', height= app.height_column, width = app.large_column)


def add_team(app, n, year1):
    if app.lta[n].BG != '#66ff99':
        app.lta[n].BG = "white"
    if app.lta[n].prochain_match != None or app.lta[n].prochain_match != '':
        get_all_match_team_a_contre_team_b(app, n)
        get_all_match_winner_team_a_contre_team_b(app, n)
        get_all_match_domicile_team_a_contre_team_b(app, n)
        get_all_match_domicile(app, n)
        get_all_match_exterieur(app, n)
        if check_if_team_is_valid(app, n) == 1:
            print("ajoute l'??quipe : %d" % (app.lta[n].team_id))
            reverse_sort_goal_by_day(app, n)
            get_team_taux(app, n, year1)
            get_team_adversaire(app, n, year1)
            get_team_others_stats(app, n, year1)
            get_team_tk(app, n, year1)

def delete_all_teams(app):
    delete_all_teams_widget(app)
    app.lta.clear()

def add_all_ligue_teams_image(ligue_logo, team_logo, ligue_logo_file_name, team_logo_file_name, team_logo_url, ligue_logo_url, ligue_id):
    for i in range(0, len(ligue_logo_url)):
        file_name = ligue_logo_url[i]
        if 'https://www.' not in file_name:
            file_name = 'https://www.' + file_name
        file_name = 'images/' + file_name.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
        if file_name not in ligue_logo_file_name:
                print("Sauvegarde image des ligues")
                img = Image.open(resource_path(file_name)).convert('RGBA')
                ligue_logo.append(img)
                ligue_logo_file_name.append(file_name)
    for i in range(0, len(team_logo_url)):
        file_name = team_logo_url[i]
        if 'https://www.' not in file_name:
            team_logo_url = 'https://www.' + file_name
        file_name = 'images/' + file_name.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
        if file_name not in team_logo_file_name:
            print("Sauvegarde image des ??quipes")
            img = Image.open(resource_path(file_name)).convert('RGBA')
            team_logo.append(img)
            team_logo_file_name.append(file_name)

ligue_logo = []
team_logo = []
ligue_logo_file_name = []
team_logo_file_name = []

def add_all_image(app):
    with Manager() as manager:
        ligue_logo = manager.list()  # <-- can be shared between processes.
        team_logo = manager.list()  # <-- can be shared between processes.
        ligue_logo_file_name = manager.list()  # <-- can be shared between processes.
        team_logo_file_name = manager.list()  # <-- can be shared between processes.
        processes = []
        for i in range(1 , 6):
            team_logo_url = []
            ligue_logo_url = []
            for j in range(1, len(app.lta)):
                if app.lta[j].ligue_id < i * 16 and app.lta[j].ligue_id <= (i - 1) * 16 and check_if_team_is_valid(app, i) == 1:
                    team_logo_url.append(app.lta[j].team_logo_url)
                    ligue_logo_url.append(app.lta[j].ligue_logo_url)
            p = Process(target=add_all_ligue_teams_image, args=(ligue_logo, team_logo, ligue_logo_file_name, team_logo_file_name, team_logo_url, ligue_logo_url, i))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
            p.terminate()
        tmp = []
        for i in range(0, len(team_logo)):
            if team_logo[i] not in app.team_logo:
                app.team_logo.append(team_logo[i])
        for i in range(0, len(team_logo_file_name)):
            if team_logo_file_name[i] not in app.team_logo_file_name:
                app.team_logo_file_name.append(team_logo_file_name[i])
        for i in range(0, len(ligue_logo)):
            if ligue_logo[i] not in app.ligue_logo :
                app.ligue_logo .append(ligue_logo[i])
        for i in range(0, len(ligue_logo_file_name)):
            if ligue_logo_file_name[i] not in app.ligue_logo_file_name :
                app.ligue_logo_file_name .append(ligue_logo_file_name[i])

        print(len(app.team_logo_file_name))
        print(len(app.team_logo))