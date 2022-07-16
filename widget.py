import tkinter
from database_utils import *
from utils import *
from widget_utils import Filtre_option, pack_column_utils, pack_filtre_menu, add_new_filtre_button, set_filtre_mode, set_filtre_value

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
    app.championnat_label = tkinter.Label(app.column_frame, text="Championnat", font=app.font_style,  fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.equipe_label = tkinter.Label(app.column_frame, text= "Équipe (A)", font=app.font_style,  fg='black', bg='white', borderwidth=2, height = 5, width = app.large_column)
    app.taux_historique_label = tkinter.Label(app.column_frame, text= "Taux\nHistorique (A)\n(à domicile)", font=app.font_style,fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.taux_saison_label = tkinter.Label(app.column_frame, text= "Taux\nSaison (A)\n(à domicile)", font=app.font_style, fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.serie_label = tkinter.Label(app.column_frame, text="Série\nen cours", font=app.font_style, fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.longest_serie_label = tkinter.Label(app.column_frame, text="Record", font=app.font_style, fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.taux_2x_label = tkinter.Label(app.column_frame, text="Taux\n2X", font=app.font_style,  fg='black', bg='white',borderwidth=2, height = 5, width = app.small_column)
    app.taux_3x_label = tkinter.Label(app.column_frame, text="Taux\n3X", font=app.font_style, fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.prochain_match_label = tkinter.Label(app.column_frame, text="Prochain match", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.adversaire_label = tkinter.Label(app.column_frame, text="Adversaire (B)", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.large_column)
    app.adversaire_taux_historique_label = tkinter.Label(app.column_frame, text= "Taux Historique\nB (à l'extérieur)", font=app.font_style,fg='black', bg='white', borderwidth=2,height = 5, width = app.small_column)
    app.adversaire_taux_saison_label = tkinter.Label(app.column_frame, text= "Taux Saison B\n(à l'extérieur)", font=app.font_style, fg='black', bg='white', borderwidth=2, height = 5, width = app.small_column)
    app.cote_match_label = tkinter.Label(app.column_frame, text="Cotes", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.classement_label = tkinter.Label(app.column_frame, text="Classement", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.tete_a_tete_label = tkinter.Label(app.column_frame, text="Tête-à-tête\n(matchs)", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.medium_column)
    app.serie_a_contre_b_label = tkinter.Label(app.column_frame, text="Série\nA contre B", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.taux_a_contre_b_label = tkinter.Label(app.column_frame, text="Taux\nA contre B\n(à domicile)", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.record_a_contre_b_label = tkinter.Label(app.column_frame, text="Record A/B", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.match_joues_label = tkinter.Label(app.column_frame, text="Match joués", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.victoire_label = tkinter.Label(app.column_frame, text="Victoire", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.nul_label = tkinter.Label(app.column_frame, text="Nuls", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.defaite_label = tkinter.Label(app.column_frame, text="Défaites", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.moyenne_match_label = tkinter.Label(app.column_frame, text="Moyenne\nbuts par Match", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    app.moyenne_but_marque_label = tkinter.Label(app.column_frame, text="Moyenne\nbuts marqués", font=app.font_style, fg='black', bg='white', borderwidth=2,  height = 5, width = app.small_column)
    pack_column_utils(app)

def get_filtres_json(data):
    config_text = ''
    with open(home_path('config/filtre.json'), 'r') as config_json:
        for line in config_json:
            config_text = config_text + line
        config_json.close()
    json_dict = json.loads(config_text)
    return json_dict[data]

def set_filtre_menu(app):
    app.filtre_menu_frame = tkinter.Frame(app, bg='white', height = 200, width = 200)
    app.filtre_menu_frame.grid(row= 0, column= 0,  sticky='nsew')
    app.filtre_add_button = tkinter.Button(app.filtre_menu_frame, text="Ajouter filtre", bg='white', command = lambda: add_new_filtre_button(app))
    
    tmp_filtres = get_filtres_json("filtres")
    tmp_values = get_filtres_json("values")
    for i in range(0, len(tmp_filtres)):
        get_saved_filtre(app, tmp_filtres, tmp_values, i)
        
    pack_filtre_menu(app)


def get_saved_filtre(app, tmp_filtres, tmp_values, i):
    filtre = Filtre_option(app)
    filtre.filtre = tmp_filtres[i]
    filtre.value = tmp_values[i]
    filtre.filtre_selected.set(filtre.filtre_dict["text_mode"][filtre.filtre])
    filtre.value_selected.set(filtre.filtre_dict["text_values"][filtre.filtre][filtre.value])
    filtre.filtre_drop = tkinter.OptionMenu(app.filtre_menu_frame, filtre.filtre_selected, *filtre.filtre_dict["text_mode"], command= lambda x:set_filtre_mode(x, app, filtre))
    filtre.value_drop = tkinter.OptionMenu(app.filtre_menu_frame, filtre.value_selected, *filtre.filtre_dict["text_values"][filtre.filtre], command= lambda x :set_filtre_value(x, app, filtre))
    app.list_filtres.append(filtre.filtre)
    app.list_filtres_value.append(filtre.value)
    app.filtre_options.append(filtre)
