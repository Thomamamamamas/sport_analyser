import tkinter
from PIL import Image
from urllib.request import urlopen
import io
import base64
from database_utils import *

class Filtre_option():
    def __init__(self, app):
        self.filtre_dict = { "mode": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 
                            "text_mode": [
                                "taux_saison", "match_joues", "victoire", "nul", "defaite", "team_moyenne_match_goals", "moyenne_goals", 
                                "taux_2x_no_goal", "taux_3x_no_goal", "adversaire_taux_saison", "taux_historique", "prochain_match", 
                                "adversaire_taux_historique", "classement", "serie_a_contre_b"],
                            "text_values": [
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus récent au plus ancien", "Du plus ancien au plus récent"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"],
                                ["Du plus petit au plus grand", "Du plus grand au plus petit"]]
                            }
        self.filtre_selected = tkinter.StringVar()
        self.filtre_selected.set(self.filtre_dict["text_mode"][0])
        self.value_selected = tkinter.StringVar()
        self.value_selected.set(self.filtre_dict["text_values"][0][0])
        self.filtre_drop = tkinter.OptionMenu(app.filtre_menu_frame, self.filtre_selected, *self.filtre_dict["text_mode"], command= lambda:set_filtre_mode(self))
        self.value_drop = tkinter.OptionMenu(app.filtre_menu_frame, self.value_selected, *self.filtre_dict["text_values"][0], command= lambda:set_filtre_value(self))
        self.mode = 0
        self.value = 0

def save_image(image_url, type):
    if 'https://www.' not in image_url:
            image_url = 'https://www.' + image_url
    file_name = 'images/' + image_url.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
    image_byt = urlopen(image_url).read()
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
    filtre = Filtre_option(app)
    app.filtre_options.append(filtre)


def pack_filtre_menu(app):
    app.filtre_add_button.grid(row = 0, column = 0)
    for i in range(0, len(app.filtre_options)):
        app.filtre_options[i].filtre_drop.grid(row = 1, column = 0)
        app.filtre_options[i].value_drop.grid(row = 1, column = 1)

def set_filtre_mode(filtre):
    print("pute")

def set_filtre_value(filtre):
    print("pute")