import tkinter
from PIL import Image
from urllib.request import urlopen
import io
import base64
from database_utils import *
from utils import resource_path
from widget_team import delete_all_teams_widget

class Filtre_option():
    def __init__(self, app):
        self.filtre_dict = { 
                            "text_mode": [
                                "taux_historique", "taux_saison", "serie", "record", "taux_2x_no_goal", "taux_3x_no_goal", "prochain_match", 
                                "adversaire_taux_historique",  "adversaire_taux_saison", "classement", "serie_a_contre_b", "taux_a_contre_b", 
                                "serie_a_contre_b", "record_a_contre_b", "match_joues", "victoire", "nul", "defaite", 
                                "team_moyenne_match_goals", "team_moyenne_goals"],
                            "text_values": [
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus ancien au plus récent", "Du plus récent au plus ancien"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"] ,
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"],
                                ["Du plus grand au plus petit", "Du plus petit au plus grand"]]
                            }
        self.filtre_selected = tkinter.StringVar()
        self.filtre_selected.set(self.filtre_dict["text_mode"][0])
        self.value_selected = tkinter.StringVar()
        self.value_selected.set(self.filtre_dict["text_values"][0][0])
        self.filtre_drop = tkinter.OptionMenu(app.filtre_menu_frame, self.filtre_selected, *self.filtre_dict["text_mode"], command= lambda x :set_filtre_mode(x, app, self))
        self.value_drop = tkinter.OptionMenu(app.filtre_menu_frame, self.value_selected, *self.filtre_dict["text_values"][0], command= lambda x :set_filtre_value(x, app, self))
        self.delete_button = tkinter.Button(app.filtre_menu_frame, text="X", width = 1, height= 1, bg='white', command= lambda : delete_filtre(app, self))
        self.filtre = 0
        self.value = 0
    
    def get_filtre(self):
        for i in range(0, len(self.filtre_dict["text_mode"])):
            if self.filtre_dict["text_mode"][i] == self.filtre_selected.get():
                self.filtre = i
                break

    def get_value(self):
        for i in range(0, len(self.filtre_dict["text_values"][self.filtre])):
            if self.filtre_dict["text_values"][self.filtre][i] == self.value_selected.get():
                self.value = i
                break

def save_image(image_url, type):
    if 'https://www.' not in image_url:
            image_url = 'https://www.' + image_url
    file_name = 'images/' + image_url.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
    image_byt = urlopen(resource_path(image_url)).read()
    img_b64 = base64.encodebytes(image_byt)
    imgdata = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(imgdata))
    if type == 0:
        new_img = img.resize((40, 40))  # x, y
    elif type == 1:
        new_img = img.resize((30, 30))  # x, y
    file = open(file_name, "wb")
    new_img.save(file, format="PNG")
    file.close()

def save_all_images(db, sport):
    if db:
        cursor = db.cursor()
        ligues_id = database_fetchall(cursor, "SELECT ID FROM %s.ligues" % (sport))
        logo_url = database_fetchall(cursor, "SELECT LIGUE_LOGO FROM %s.ligues" % (sport))
        for i in range(0, len(ligues_id)):
            save_image(logo_url[i], 0)
            teams_id = database_fetchall(cursor, "SELECT ID FROM %s.teams WHERE LIGUE_ID = %d" % (sport, ligues_id[i] ))
            team_logo = database_fetchall(cursor, "SELECT TEAM_LOGO FROM %s.teams WHERE LIGUE_ID = %d" % (sport, ligues_id[i]))
            for j in range(0, len(teams_id)):
                save_image(team_logo[j], 1)

def pack_column_utils(app):
    app.championnat_label.grid(row = 0, column = 0,  sticky='nsew')
    app.equipe_label.grid(row = 0, column = 1,  sticky='nsew')
    app.taux_historique_label.grid(row = 0, column = 2,  sticky='nsew')
    app.taux_saison_label.grid(row = 0, column = 3,  sticky='nsew')
    app.serie_label.grid(row = 0, column = 4,  sticky='nsew')
    app.longest_serie_label.grid(row = 0, column = 5,  sticky='nsew')
    app.taux_2x_label.grid(row = 0, column = 6,  sticky='nsew')
    app.taux_3x_label.grid(row = 0, column = 7,  sticky='nsew')
    app.prochain_match_label.grid(row = 0, column = 8,  sticky='nsew')
    app.adversaire_label.grid(row = 0, column = 9,  sticky='nsew')
    app.adversaire_taux_historique_label.grid(row = 0, column = 10,  sticky='nsew')
    app.adversaire_taux_saison_label.grid(row = 0, column = 11,  sticky='nsew')
    app.cote_match_label.grid(row = 0, column = 12,  sticky='nsew')
    app.classement_label.grid(row = 0, column = 13,  sticky='nsew')
    app.tete_a_tete_label.grid(row = 0, column = 14,  sticky='nsew')
    app.serie_a_contre_b_label.grid(row = 0, column = 15,  sticky='nsew')
    app.taux_a_contre_b_label.grid(row = 0, column = 16,  sticky='nsew')
    app.record_a_contre_b_label.grid(row = 0, column = 17,  sticky='nsew')
    app.match_joues_label.grid(row = 0, column = 18,  sticky='nsew')
    app.victoire_label.grid(row = 0, column = 19,  sticky='nsew')
    app.nul_label.grid(row = 0, column = 20,  sticky='nsew')
    app.defaite_label.grid(row = 0, column = 21,  sticky='nsew')
    app.moyenne_match_label.grid(row = 0, column = 22,  sticky='nsew')
    app.moyenne_but_marque_label.grid(row = 0, column = 23,  sticky='nsew')

def add_new_filtre_button(app):
    if platform.system() == 'Windows':
        delete_all_teams_widget(app)
    filtre = Filtre_option(app)
    app.list_filtres.append(filtre.filtre)
    app.list_filtres_value.append(filtre.value)
    app.filtre_options.append(filtre)
    unpack_filtre_menu(app)
    pack_filtre_menu(app)
    app.sort_teams(app.list_filtres, app.list_filtres_value, 1)

def pack_filtre_menu(app):
    app.filtre_menu_frame.grid(row=0, column = 0, sticky='nsew')
    app.filtre_add_button.grid(row = 0, column = 0)
    r_id = 1
    c_id = 0
    for i in range(0, len(app.filtre_options)):
        app.filtre_options[i].filtre_drop.grid(row = r_id, column = c_id)
        app.filtre_options[i].value_drop.grid(row = r_id, column = c_id + 1)
        app.filtre_options[i].delete_button.grid(row = r_id, column = c_id + 2, padx=(0, 100))
        c_id = c_id + 3
        if c_id == 9:
            r_id = r_id + 1
            c_id = 0

def unpack_filtre_menu(app):
    app.filtre_menu_frame.grid_forget()
    for i in range(0, len(app.filtre_options), 1):
        app.filtre_options[i].filtre_drop.grid_forget()
        app.filtre_options[i].value_drop.grid_forget()
        app.filtre_options[i].delete_button.grid_forget()
        
def delete_filtre(app, filtre):
    if platform.system() == 'Windows':
        delete_all_teams_widget(app)
    for i in range(0, len(app.filtre_options)):
        if filtre == app.filtre_options[i]:
            app.list_filtres.pop(i)
            app.list_filtres_value.pop(i)
            app.filtre_options.remove(filtre)
            filtre.filtre_drop.grid_forget()
            filtre.value_drop.grid_forget()
            filtre.delete_button.grid_forget()
            filtre.filtre_drop = None
            filtre.value_drop = None
            filtre.delete_button = None
            del filtre
            app.sort_teams(app.list_filtres, app.list_filtres_value, 1)
            break

def set_filtre_mode(selection, app, filtre):
    if platform.system() == 'Windows':
        delete_all_teams_widget(app)
    filtre.filtre_selected.set(selection)
    filtre.filtre_drop.grid_forget()
    filtre.filtre_drop = None
    filtre.filtre_drop = tkinter.OptionMenu(app.filtre_menu_frame, filtre.filtre_selected, *filtre.filtre_dict["text_mode"], command= lambda x:set_filtre_mode(x, app, filtre))
    filtre.get_filtre()
    filtre.value_selected.set(filtre.filtre_dict["text_values"][filtre.filtre][0])
    filtre.value = 0
    app.update_filtre_list(filtre)
    filtre.value_drop.grid_forget()
    filtre.value_drop =  None
    filtre.value_drop = tkinter.OptionMenu(app.filtre_menu_frame, filtre.value_selected, *filtre.filtre_dict["text_values"][filtre.filtre], command= lambda x :set_filtre_value(x, app, filtre))
    for i in range(0, len(app.filtre_options)):
        print(app.filtre_options[i].filtre_selected.get())
        if filtre == app.filtre_options[i]:
            app.filtre_options[i] = filtre
            break
    unpack_filtre_menu(app)
    pack_filtre_menu(app)
    app.sort_teams(app.list_filtres, app.list_filtres_value, 1)

def set_filtre_value(selection, app, filtre):
    if platform.system() == 'Windows':
        delete_all_teams_widget(app)
    filtre.value_selected.set(selection)
    filtre.get_value()
    app.update_filtre_list(filtre)
    filtre.value_drop.grid_forget()
    filtre.value_drop =  None
    filtre.value_drop = tkinter.OptionMenu(app.filtre_menu_frame, filtre.value_selected, *filtre.filtre_dict["text_values"][filtre.value], command= lambda x :set_filtre_value(x, app, filtre))
    for i in range(0, len(app.filtre_options)):
        if filtre == app.filtre_options[i]:
            app.filtre_options[i] = filtre
            break
    unpack_filtre_menu(app)
    pack_filtre_menu(app)
    app.sort_teams(app.list_filtres, app.list_filtres_value, 1)