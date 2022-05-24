import tkinter
import io
import base64
from PIL import Image
from urllib.request import urlopen
from database_utils import *
from utils import *
    
class Team_data():
    def __init__(self):
        self.team_id = 0
        self.ligue_id = 0
        self.ligue_name = ''
        self.team_name = ''
        self.ligue_logo_url = ''
        self.team_logo_url = ''
        self.logo_cv = []
        self.photo = []
        self.ligue_frame = None
        self.ligue_label = None
        self.team_frame = None
        self.team_label = None
        self.taux_historique_label = None
        self.taux_saison_label = None
        self.serie_label = None
        self.longest_serie_label = None
        self.taux_2x_no_goal_label = None
        self.taux_3x_no_goal_label = None
        self.prochain_match_label = None
        self.empty_label = None
        self.taux_historique = 0
        self.taux_saison = 0
        self.serie = [0-0-0-0-0]
        self.longest_serie = 0
        self.actual_serie = 0
        self.taux_2x_no_goal = 0
        self.taux_3x_no_goal = 0
        self.prochain_match = '' 

def get_image(image_url, team, i):
    if 'https://www.' not in image_url:
        image_url = 'https://www.' + image_url
    image_byt = urlopen(image_url).read()
    img_b64 = base64.encodebytes(image_byt)
    buffer = io.BytesIO()
    imgdata = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(imgdata))
    if i == 0:
        new_img = img.resize((40, 40))  # x, y
    elif i == 1:
        new_img = img.resize((30, 30))  # x, y
    new_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    if i == 0:
        team.logo_cv.append(tkinter.Canvas(team.ligue_frame, width= 50, height= 50, bd=0, highlightthickness=0, relief='ridge'))
    else:
            team.logo_cv.append(tkinter.Canvas(team.team_frame, width= 50, height= 50, bd=0, highlightthickness=0, relief='ridge'))
    team.logo_cv[i].configure(bg= 'white')
    team.photo.append(tkinter.PhotoImage(data=img_b64))

def add_all_teams(app):
    ligues = database_fetchall(app.cursor, "SELECT ID FROM %s.ligues" % (app.sport_selected.get()))
    for i in range(0, len(ligues)):
        ligue_teams = database_fetchall(app.cursor, "SELECT ID FROM %s.teams WHERE LIGUE_ID = %d" % (app.sport_selected.get(), ligues[i]))
        for j in range(0, len(ligue_teams)):
            app.team_id = ligue_teams[j]
            add_team(app, ligues[i], app.team_id)
    app.sort_taux(7)

def add_ligue_teams(app, ligue_id):
    ligue_teams = database_fetchall(app.cursor, "SELECT ID FROM %s.teams WHERE LIGUE_ID = %d" % (app.sport_selected.get(), ligue_id))
    for j in range(0, len(ligue_teams)):
        app.team_id = ligue_teams[j]
        add_team(app, ligue_id, app.team_id)
    app.sort_taux(7)

def add_single_team(app, ligue_id, team_id):
    team = add_team(app, ligue_id, team_id)
    place_team(team)

def add_team(app, ligue_id, team_id):
    print("ajoute team : %d de la ligue : %d" % (team_id, ligue_id))
    year1 = 2021
    year2 = 2022
    new_team = Team_data()
    new_team.team_id = team_id
    new_team.ligue_id = ligue_id
    new_team.ligue_name = database_fetchone(app.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE ID = %d" %(app.sport_selected.get(), new_team.ligue_id))
    new_team.team_name = database_fetchone(app.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE ID = %d" %(app.sport_selected.get(), new_team.team_id))
    new_team.ligue_logo_url = database_fetchone(app.cursor, "SELECT LIGUE_LOGO FROM %s.ligues WHERE ID = %d" %(app.sport_selected.get(), new_team.ligue_id))
    new_team.team_logo_url = database_fetchone(app.cursor, "SELECT TEAM_LOGO FROM %s.teams WHERE ID = %d" %(app.sport_selected.get(), new_team.team_id))
    s_dg = Day_goal()
    s_dg.domicile_match = database_fetchall(app.cursor, "SELECT GOAL_FIRST FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
    s_dg.domicile_journee = database_fetchall(app.cursor, "SELECT JOURNEE FROM matchs WHERE TEAM_ID = %d AND DOMICILE = 1 AND YEAR1 = %d AND YEAR2 = %d" % (team_id, year1, year2))
    
    new_team.taux_historique = get_taux_historique(app.db, app.team_id)
    new_team.taux_saison = get_taux_actual_season(app.db, app.team_id, 2021, 2022)
    if new_team.taux_saison == 0:
        return
    get_domicile_journee(s_dg, new_team.ligue_id)
    reverse_sort_goal_by_day(s_dg)
    new_team.serie = get_actual_serie(s_dg)
    new_team.longest_serie = get_longest_serie_without_goal(app.cursor, s_dg, year1, year2, new_team.ligue_id, new_team.team_id)
    new_team.actual_serie = calculate_actual_serie(new_team.serie)
    new_team.taux_2x_no_goal = get_taux_x_no_goal(app.cursor, s_dg, year1, year2, new_team.ligue_id, new_team.team_id, 2)
    new_team.taux_3x_no_goal = get_taux_x_no_goal(app.cursor, s_dg, year1, year2, new_team.ligue_id, new_team.team_id, 3)
    new_team.prochain_match = database_fetchone(app.cursor, "SELECT MATCH_TO_COMING FROM %s.teams WHERE ID = %d" %(app.sport_selected.get(), new_team.team_id)) 

    new_team.ligue_frame = tkinter.Frame(app.frame_column[0], bg='white', height= 3)
    new_team.ligue_label = tkinter.Label(new_team.ligue_frame, text= new_team.ligue_name, font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.team_frame = tkinter.Frame(app.frame_column[1],bg='white', height= 3)
    new_team.team_label = tkinter.Label(new_team.team_frame, text= new_team.team_name, font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.taux_historique_label = tkinter.Label(app.frame_column[2], text= str(new_team.taux_historique), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.taux_saison_label = tkinter.Label(app.frame_column[3], text= str(new_team.taux_saison), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.serie_label = tkinter.Label(app.frame_column[4], text= str(new_team.serie), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.longest_serie_label = tkinter.Label(app.frame_column[5], text="%d/%d" % (new_team.actual_serie, new_team.longest_serie), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.taux_2x_no_goal_label = tkinter.Label(app.frame_column[6], text= str(new_team.taux_2x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.taux_3x_no_goal_label = tkinter.Label(app.frame_column[7], text= str(new_team.taux_3x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    if new_team.prochain_match != None:
        new_team.prochain_match_label = tkinter.Label(app.frame_column[8], text= new_team.prochain_match, font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    else:
        new_team.prochain_match_label = tkinter.Label(app.frame_column[8], text= " ", font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    new_team.empty_label = tkinter.Label(app.frame_column[9], text= " ", font='Helvetica 18 bold',  bg='white', fg='black', height= 3)
    get_image(new_team.ligue_logo_url, new_team, 0)  
    get_image(new_team.team_logo_url, new_team, 1)
    app.team_added.append(new_team)
    return new_team

def place_teams(app):
    for i in range(0, len(app.team_added)):
        place_team(app.team_added[i])

def place_team(team):
    print("place team : %d de la ligue %d" % (team.team_id, team.ligue_id))
    team.ligue_frame.pack(pady = 0)
     
    team.logo_cv[0].pack(side='left')
    team.logo_cv[0].create_image(0 ,0, anchor="nw", image=team.photo[0])
    team.ligue_label.pack(side='left')
    team.team_frame.pack(pady = 0)
    
    team.logo_cv[1].pack(side='left')
    team.logo_cv[1].create_image(0 ,0,anchor="nw",image=team.photo[1])
    team.team_label.pack(side='left')
    team.taux_historique_label.pack(pady = 0)
    team.taux_saison_label.pack(pady = 0)
    team.serie_label.pack(pady = 0)
    team.longest_serie_label.pack(pady = 0)
    team.taux_2x_no_goal_label.pack(pady = 0)
    team.taux_3x_no_goal_label.pack(pady = 0)
    team.prochain_match_label.pack(pady = 0)
    team.empty_label.pack(pady = 0)

def delete_team(app, team):
    delete_team_widget(team)
    app.team_added.remove(team)
    del team

def delete_all_teams(app):
    delete_all_teams_widget(app)
    app.team_added.clear()

def delete_all_teams_widget(app):
    app.championnat_label.pack_forget()
    app.equipe_label.pack_forget()
    app.taux_historique_button.pack_forget()
    app.taux_saison_button.pack_forget()
    app.serie_button.pack_forget()
    app.longest_serie_button.pack_forget()
    app.taux_2x_button.pack_forget()
    app.taux_3x_button.pack_forget()
    app.prochain_match_label.pack_forget()
    app.delete_button.pack_forget()
    for i in range(0, 10):
        app.frame_column[i].pack_forget()
    for i in range(0, len(app.team_added)):
        delete_team_widget(app.team_added[i])
    for i in range(0, 10):
        app.frame_column[i].pack(side="left")
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

def delete_team_widget(team):
    team.ligue_frame.pack_forget()
    team.team_frame.pack_forget()
    team.taux_historique_label.pack_forget()
    team.taux_saison_label.pack_forget()
    team.serie_label.pack_forget()
    team.longest_serie_label.pack_forget()
    team.taux_2x_no_goal_label.pack_forget()
    team.taux_3x_no_goal_label.pack_forget()
    team.prochain_match_label.pack_forget()
    team.empty_label.pack_forget()