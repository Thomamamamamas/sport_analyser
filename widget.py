from os import uname
import tkinter
from tkinter import ttk
from database_utils import *
from utils import *
from widget_utils import Filtre_option, pack_column_utils, pack_filtre_menu, add_new_filtre_button

def change_selected_value(app, type):
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

def set_option_menu(app):
    app.frame_option = tkinter.Frame(app)
    app.frame_option.configure(bg='white')
    app.frame_option.pack(side='top')

    app.sports = ['football']
    app.sport_selected = tkinter.StringVar()
    app.sport_selected.set(app.sports[0])
    app.sport_drop = tkinter.OptionMenu(app.frame_option, app.sport_selected, *app.sports, command= app.set_sport_selected)

    app.pays = list(set(database_fetchall(app.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (app.sport_selected.get()))))
    app.pays_selected = tkinter.StringVar()
    app.pays_selected.set("bielorussie")
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

def set_result_frame(app):
    app.canvas = tkinter.Canvas(app)
    app.canvas_column = tkinter.Canvas(app, height = 100)
    app.scrollbary = tkinter.Scrollbar(app, orient="vertical", command=app.canvas.yview)
    app.scrollbarx = tkinter.Scrollbar(app, orient="horizontal", command= app.xview_scroll)
    app.scrollable_frame = tkinter.Frame(app.canvas)
    app.column_frame = tkinter.Frame(app.canvas_column, bg='white')
    app.scrollable_frame.bind(
        "<Configure>",
        lambda e: app.canvas.configure(
            scrollregion=app.canvas.bbox("all")
        )
        )
    app.column_frame.bind(
        "<Configure>",
        lambda e: app.canvas_column.configure(
            scrollregion=app.canvas_column.bbox("all")
        )
        )
    app.canvas_column.create_window((0, 0), window=app.column_frame, anchor="nw")
    app.column_frame.configure(bg= 'white')
    app.canvas_column.configure(xscrollcommand=app.scrollbarx.set)
    app.canvas_column.grid(row = 1, column = 0, sticky='nsew')
    app.canvas.create_window((0, 0), window=app.scrollable_frame, anchor="nw")
    app.canvas.configure(yscrollcommand=app.scrollbary.set)
    app.canvas.configure(xscrollcommand=app.scrollbarx.set)
    app.scrollable_frame.configure(bg= 'white')
    app.canvas.configure(bg= 'white', height=app.screen_height / 1.3, width=app.screen_width - 20)
    
    app.canvas.grid(row = 2, column = 0)
    app.scrollbary.grid(row = 2, column = 1, sticky='ns')
    app.scrollbarx.grid(row = 3, column = 0,sticky='nsew')


def set_column_utils(app):
    app.championnat_label = tkinter.Label(app.column_frame, text="Championnat", font='Helvetica 16 bold',  fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.equipe_label = tkinter.Label(app.column_frame, text= "Équipe", font='Helvetica 16 bold',  fg='black', bg='white', borderwidth=2, height = 5, width = app.large_column)
    app.taux_historique_label = tkinter.Label(app.column_frame, text= "Taux Historique", font='Helvetica 16 bold',fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.taux_saison_label = tkinter.Label(app.column_frame, text= "Taux Saison", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.serie_label = tkinter.Label(app.column_frame, text="Série en cours", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.longest_serie_label = tkinter.Label(app.column_frame, text="Record", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.taux_2x_label = tkinter.Label(app.column_frame, text="Taux 2X", font='Helvetica 16 bold',  fg='black', bg='white',borderwidth=2, height = 5, width = app.small_column)
    app.taux_3x_label = tkinter.Label(app.column_frame, text="Taux 3X", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.prochain_match_label = tkinter.Label(app.column_frame, text="Prochain match", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.adversaire_label = tkinter.Label(app.column_frame, text="Adversaire", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.adversaire_taux_historique_label = tkinter.Label(app.column_frame, text= "Adversaire taux Historique", font='Helvetica 16 bold',fg='black', bg='white', borderwidth=2,height = 5, width = app.large_column)
    app.adversaire_taux_saison_label = tkinter.Label(app.column_frame, text= "Advesaire Taux Saison", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2, height = 5, width = app.large_column)
    app.cote_match_label = tkinter.Label(app.column_frame, text="Cotes", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.classement_label = tkinter.Label(app.column_frame, text="Classement", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.tete_a_tete_label = tkinter.Label(app.column_frame, text="Tête-à-tête", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.serie_a_contre_b_label = tkinter.Label(app.column_frame, text="Série A contre B", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.taux_a_contre_b_label = tkinter.Label(app.column_frame, text="Taux A contre B", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.record_a_contre_b_label = tkinter.Label(app.column_frame, text="Record A/B", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.match_joues_label = tkinter.Label(app.column_frame, text="Match joués", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.victoire_label = tkinter.Label(app.column_frame, text="Victoire", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.nul_label = tkinter.Label(app.column_frame, text="Nuls", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.defaite_label = tkinter.Label(app.column_frame, text="Défaites", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.moyenne_match_label = tkinter.Label(app.column_frame, text="Moyenne but par Match", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.moyenne_but_marque_label = tkinter.Label(app.column_frame, text="Moyenne but marqués", font='Helvetica 16 bold', fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    pack_column_utils(app)

def set_filtre_menu(app):
    app.filtre_menu_frame = tkinter.Frame(app, bg='white', height = 100, width = 200)
    app.filtre_menu_frame.grid(row= 0, column= 0,  sticky='nsew')
    app.filtre_add_button = tkinter.Button(app.filtre_menu_frame, text="Ajouter filtre", bg='white', command = lambda: add_new_filtre_button(app))
    app.filtre_options.append(Filtre_option(app))
    pack_filtre_menu(app)