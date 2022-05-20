import tkinter
from database_utils import *
from team import delete_all_teams, add_single_team, add_ligue_teams, add_all_teams
from utils import *


def change_selected_value(app, type):
        app.sport_drop.pack_forget()
        app.pays_drop.pack_forget()
        app.ligue_drop.pack_forget()
        app.team_drop.pack_forget()
        app.add_team_button.pack_forget()
        app.add_ligue_button.pack_forget()
        app.add_all_teams_button.pack_forget()
        app.crawl_button.pack_forget()
        if type == 1:
            app.pays = list(set(database_fetchall(app.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (app.sport_selected.get()))))
            app.pays_selected = tkinter.StringVar()
            app.pays_selected.set(app.pays[0])
        if type == 2 or type == 1:
            app.ligues = database_fetchall(app.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (app.sport_selected.get(), app.pays_selected.get()))
            app.ligue_selected = tkinter.StringVar()
            app.ligue_selected.set(app.ligues[0])
            app.ligue_id = database_fetchone(app.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (app.sport_selected.get(), app.ligue_selected.get(), app.pays_selected.get()))          
        if type == 3 or type == 1 or type == 2:      
            app.teams = database_fetchall(app.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (app.sport_selected.get(), app.ligue_id))
            app.team_selected = tkinter.StringVar()
            app.team_selected.set(app.teams[0])
            app.team_id = database_fetchone(app.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (app.sport_selected.get(), app.team_selected.get(), app.ligue_id))

        app.sport_drop = tkinter.OptionMenu(app.frame_option, app.sport_selected, *app.sports, command= app.set_sport_selected)
        app.pays_drop = tkinter.OptionMenu(app.frame_option, app.pays_selected, *app.pays, command= app.set_pays_selected)
        app.ligue_drop = tkinter.OptionMenu(app.frame_option, app.ligue_selected, *app.ligues, command= app.set_ligue_selected)
        app.team_drop = tkinter.OptionMenu(app.frame_option, app.team_selected, *app.teams, command = app.set_team_selected)
        app.add_team_button = tkinter.Button(app.frame_option, text="AJOUTER TEAM", bg="white", fg='black', borderwidth=0, command= lambda:add_single_team(app, app.ligue_id, app.team_id))
        app.add_ligue_button = tkinter.Button(app.frame_option, text="AJOUTER LIGUE", bg="white", fg='black', borderwidth=0, command= lambda:add_ligue_teams(app, app.ligue_id))
        app.add_all_teams_button = tkinter.Button(app.frame_option, text="AJOUTER TOUTES LES EQUIPES", bg="white", fg='black', borderwidth=0, command= lambda:add_all_teams(app))
        app.crawl_button = tkinter.Button(app.frame_option, text="RÉCUPERE TOUTES LES DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: app.crawl_all_new_data())

        app.sport_drop.pack(side= 'left', anchor= 'nw', padx=0)
        app.pays_drop.pack(side= 'left', anchor= 'nw', padx=0)
        app.ligue_drop.pack(side= 'left', anchor= 'nw', padx=0)
        app.team_drop.pack(side= 'left', anchor= 'nw', padx=0)
        app.add_team_button.pack(side= 'left', anchor= 'nw', padx=0)
        app.add_ligue_button.pack(side= 'left', anchor= 'nw', padx=0)
        app.add_all_teams_button.pack(side= 'left', anchor= 'nw', padx=0)
        app.crawl_button.pack(side= 'right')


def place_option_menu(app):
    app.frame_option = tkinter.Frame(app)
    app.frame_option.configure(bg='white')
    app.frame_option.pack(pady = 20, fill=tkinter.X)

    app.sports = ['football']
    app.sport_selected = tkinter.StringVar()
    app.sport_selected.set(app.sports[0])
    app.sport_drop = tkinter.OptionMenu(app.frame_option, app.sport_selected, *app.sports, command= app.set_sport_selected)

    app.pays = list(set(database_fetchall(app.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (app.sport_selected.get()))))
    app.pays_selected = tkinter.StringVar()
    app.pays_selected.set(app.pays[0])
    app.pays_drop = tkinter.OptionMenu(app.frame_option, app.pays_selected, *app.pays, command= app.set_pays_selected)

    app.ligues = database_fetchall(app.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (app.sport_selected.get(), app.pays_selected.get()))
    app.ligue_selected = tkinter.StringVar()
    app.ligue_selected.set(app.ligues[0])
    app.ligue_drop = tkinter.OptionMenu(app.frame_option, app.ligue_selected, *app.ligues, command= app.set_ligue_selected)

    app.ligue_id = database_fetchone(app.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (app.sport_selected.get(), app.ligue_selected.get(), app.pays_selected.get()))

    app.teams = database_fetchall(app.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (app.sport_selected.get(), app.ligue_id))
    app.team_selected = tkinter.StringVar()
    app.team_selected.set(app.teams[0])
    app.team_drop = tkinter.OptionMenu(app.frame_option, app.team_selected, *app.teams, command = app.set_team_selected)

    app.team_id = database_fetchone(app.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (app.sport_selected.get(), app.team_selected.get(), app.ligue_id))

    app.add_team_button = tkinter.Button(app.frame_option, text="AJOUTER TEAM", bg="white", fg='black', borderwidth=0, command= lambda:add_single_team(app, app.ligue_id, app.team_id))
    app.add_ligue_button = tkinter.Button(app.frame_option, text="AJOUTER LIGUE", bg="white", fg='black', borderwidth=0, command= lambda:add_ligue_teams(app, app.ligue_id))
    app.add_all_teams_button = tkinter.Button(app.frame_option, text="AJOUTER TOUTES LES EQUIPES", bg="white", fg='black', borderwidth=0, command= lambda:add_all_teams(app))
    app.crawl_button = tkinter.Button(app.frame_option, text="RÉCUPERE TOUTES LES DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: app.crawl_all_new_data())

    app.sport_drop.pack(side= 'left', anchor= 'nw', padx=0)
    app.pays_drop.pack(side= 'left', anchor= 'nw', padx=0)
    app.ligue_drop.pack(side= 'left', anchor= 'nw', padx=0)
    app.team_drop.pack(side= 'left', anchor= 'nw', padx=0)
    app.add_team_button.pack(side= 'left', anchor= 'nw', padx=0)
    app.add_ligue_button.pack(side= 'left', anchor= 'nw', padx=0)
    app.add_all_teams_button.pack(side= 'left', anchor= 'nw', padx=0)
    app.crawl_button.pack(side= 'right')


def place_result_frame(app):
    app.canvas = tkinter.Canvas(app)
    app.scrollbary = tkinter.Scrollbar(app, orient="vertical", command=app.canvas.yview)
    app.scrollbarx = tkinter.Scrollbar(app.canvas, orient="horizontal", command=app.canvas.xview)
    app.scrollable_frame = tkinter.Frame(app.canvas)
    app.scrollable_frame.bind(
        "<Configure>",
        lambda e: app.canvas.configure(
            scrollregion=app.canvas.bbox("all")
        )
        )
    app.canvas.create_window((0, 0), window=app.scrollable_frame, anchor="nw")
    app.canvas.configure(yscrollcommand=app.scrollbary.set)
    app.canvas.configure(xscrollcommand=app.scrollbarx.set)
    app.scrollable_frame.configure(bg= 'white')
    app.canvas.configure(bg= 'white')
    
    app.canvas.pack(side="left", fill="both", expand=True)
    app.scrollbary.pack(side="right", fill="y")
    app.scrollbarx.pack(side="bottom", anchor="sw", fill="x")

def place_column_utils(app):
    app.championnat_label = tkinter.Label(app.frame_column[0], text="Championnat", font='Helvetica 18 bold',  fg='black', bg='white', borderwidth=2,  height = 5)
    app.equipe_label = tkinter.Label(app.frame_column[1], text= "Équipe", font='Helvetica 18 bold',  fg='black', bg='white', borderwidth=2, height = 5)
    app.taux_historique_button = tkinter.Button(app.frame_column[2], text= "Taux Historique", font='Helvetica 18 bold',fg='black', bg='white', borderwidth=2, command= lambda: app.sort_taux(1),height = 5)
    app.taux_saison_button = tkinter.Button(app.frame_column[3], text= "Taux Saison", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: app.sort_taux(2), height = 5)
    app.serie_button = tkinter.Button(app.frame_column[4], text="Série en cours", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: app.sort_taux(3), height = 5)
    app.longest_serie_button = tkinter.Button(app.frame_column[5], text="Record", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: app.sort_taux(4), height = 5)
    app.taux_2x_button = tkinter.Button(app.frame_column[6], text="Taux 2X", font='Helvetica 18 bold',  fg='black', bg='white',borderwidth=2, command= lambda: app.sort_taux(5), height = 5)
    app.taux_3x_button = tkinter.Button(app.frame_column[7], text="Taux 3X", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: app.sort_taux(6), height = 5)
    app.prochain_match_label = tkinter.Label(app.frame_column[8], text="Prochain match", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2,  height = 5)
    app.delete_button = tkinter.Button(app.frame_column[9], text="X", font='Helvetica 18 bold', fg='black', bg='white', width= 2, height = 5, command= lambda: delete_all_teams(app))

    app.championnat_label.pack()
    app.equipe_label.pack(padx= 50)
    app.taux_historique_button.pack()
    app.taux_saison_button.pack()
    app.serie_button.pack()
    app.longest_serie_button.pack()
    app.taux_2x_button.pack()
    app.taux_3x_button.pack()
    app.prochain_match_label.pack(padx= 50)
    app.delete_button.pack()