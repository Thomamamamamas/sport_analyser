from PIL import Image,ImageTk
import tkinter
from utils import resource_path

def check_if_image_already_create(app, file_name, i):
    if i == 0:
        if file_name not in app.ligue_logo_file_name:
            print("Sauvegarde image ligue")
            img = Image.open(resource_path(file_name)).convert('RGBA')
            app.ligue_logo_file_name.append(file_name)
            app.ligue_logo.append(img)
        else:
            for n in range(0, len(app.ligue_logo_file_name)):
                if app.ligue_logo_file_name[n] ==  file_name:
                    tmp = n
                    break
            img = app.ligue_logo[tmp]
    elif i == 1:
        if file_name not in app.team_logo_file_name:
            print("Sauvegarde image team")
            img = Image.open(resource_path(file_name)).convert('RGBA')
            app.team_logo_file_name.append(file_name)
            app.team_logo.append(img)
        else:
            for n in range(0, len(app.team_logo_file_name)):
                if app.team_logo_file_name[n] ==  file_name:
                    tmp = n
                    break
            img = app.team_logo[tmp]
    return img
        

def get_image(image_url, app, n, i):
    tmp = 0
    if 'https://www.' not in image_url:
        image_url = 'https://www.' + image_url
    file_name = 'images/' + image_url.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
    img = check_if_image_already_create(app, file_name, i)
    if i == 0:    
        app.lta[n].logo_cv.append(tkinter.Canvas(app.lta[n].ligue_frame, width= 50, height= 50, bd=0, highlightthickness=0, relief='ridge'))
    else:
        app.lta[n].logo_cv.append(tkinter.Canvas(app.lta[n].team_name_frame, width= 40, height= 40, bd=0, highlightthickness=0, relief='ridge'))
    app.lta[n].logo_cv[i].configure(bg="white")
    app.lta[n].photo.append(ImageTk.PhotoImage(img))

def format_name(team_name):
    while len(team_name) < 100:
        team_name = team_name + ' '
    return team_name

def place_teams(app):
    print("place les équipes")
    for i in range(0, len(app.lta), 2):
        year1 = app.YEAR1
        for j in range(0, 2):
            place_team(app, i + j, year1)
            year1 = year1 - 1

def place_team(app, n, year1):
    if app.lta[n].prochain_match != None and app.lta[n].prochain_match != '':
        print("place l'équipe : %d" % (app.lta[n].team_id))
        app.lta[n].team_frame.grid(row = app.row_team_id, column = 0, sticky = 'nsew')
        if year1 == app.YEAR1:
            app.lta[n].ligue_frame.grid(row = 0, column = 0, sticky = 'nsew')
            app.lta[n].logo_cv[0].grid(row = 0, column = 0, sticky = 'nsew')
            app.lta[n].logo_cv[0].create_image(0 ,0, anchor="nw", image=app.lta[n].photo[0])
            app.lta[n].ligue_label.grid(row = 0, column = 1, sticky = 'nsew')
            app.lta[n].team_name_frame.grid(row = 0, column = 1, sticky = 'nsew')
            app.lta[n].logo_cv[1].grid(row = 0, column = 0, sticky = 'nsew')
            app.lta[n].logo_cv[1].create_image(0 ,0,anchor="nw",image=app.lta[n].photo[1])
            app.lta[n].team_label.grid(row = 0, column = 1, sticky = 'nsew')
        else:
            app.lta[n].ligue_frame.grid(row = 0, column = 0, sticky = 'nsew')
            app.lta[n].ligue_label.grid(row = 0, column = 0, sticky = 'nsew')
            app.lta[n].team_name_frame.grid(row = 0, column = 1, sticky = 'nsew')
            app.lta[n].team_label.grid(row = 0, column = 0, sticky = 'nsew')
        app.lta[n].taux_historique_label.grid(row = 0, column = 2, sticky = 'nsew')
        app.lta[n].taux_saison_label.grid(row = 0, column = 3, sticky = 'nsew')
        app.lta[n].serie_label.grid(row = 0, column = 4, sticky = 'nsew')
        app.lta[n].longest_serie_label.grid(row = 0, column = 5, sticky = 'nsew')
        app.lta[n].taux_2x_no_goal_label.grid(row = 0, column = 6, sticky = 'nsew')
        app.lta[n].taux_3x_no_goal_label.grid(row = 0, column = 7, sticky = 'nsew')
        app.lta[n].prochain_match_label.grid(row = 0, column = 8, sticky = 'nsew')
        app.lta[n].adversaire_label.grid(row = 0, column = 9, sticky = 'nsew')
        app.lta[n].adversaire_taux_historique_label.grid(row = 0, column = 10, sticky = 'nsew')
        app.lta[n].adversaire_taux_saison_label.grid(row = 0, column = 11, sticky = 'nsew')
        app.lta[n].cote_match_label.grid(row = 0, column = 12, sticky = 'nsew')
        app.lta[n].classement_label.grid(row = 0, column = 13, sticky = 'nsew')
        app.lta[n].tete_a_tete_label.grid(row = 0, column = 14, sticky = 'nsew')
        app.lta[n].serie_a_contre_b_label.grid(row = 0, column = 15, sticky = 'nsew')
        app.lta[n].taux_historique_a_contre_b_label.grid(row = 0, column = 16, sticky = 'nsew')
        app.lta[n].longest_serie_a_contre_b_label.grid(row = 0, column = 17, sticky = 'nsew')
        app.lta[n].match_joues_label.grid(row = 0, column = 18, sticky = 'nsew')
        app.lta[n].victoire_label.grid(row = 0, column = 19, sticky = 'nsew')
        app.lta[n].nul_label.grid(row = 0, column = 20, sticky = 'nsew')
        app.lta[n].defaite_label.grid(row = 0, column = 21, sticky = 'nsew')
        app.lta[n].moyenne_match_goals_label.grid(row = 0, column = 22, sticky = 'nsew')
        app.lta[n].moyenne_goals_label.grid(row = 0, column = 23, sticky = 'nsew')
        app.row_team_id = app.row_team_id + 1

def delete_all_teams_widget(app):
    for i in range(0, len(app.lta)):
        delete_team_widget(app, i)

def delete_team_widget(app, n):
    try:
        app.lta[n].team_frame.grid_forget()
        app.lta[n].ligue_frame.grid_forget()
        app.lta[n].team_name_frame.grid_forget()
        app.lta[n].taux_historique_label.grid_forget()
        app.lta[n].taux_saison_label.grid_forget()
        app.lta[n].serie_label.grid_forget()
        app.lta[n].longest_serie_label.grid_forget()
        app.lta[n].taux_2x_no_goal_label.grid_forget()
        app.lta[n].taux_3x_no_goal_label.grid_forget()
        app.lta[n].prochain_match_label.grid_forget()
        app.lta[n].adversaire_label.grid_forget()
        app.lta[n].adversaire_taux_historique_label.grid_forget()
        app.lta[n].adversaire_taux_saison_label.grid_forget()
        app.lta[n].cote_match_label.grid_forget()
        app.lta[n].classement_label.grid_forget()
        app.lta[n].tete_a_tete_label.grid_forget()
        app.lta[n].serie_a_contre_b_label.grid_forget()
        app.lta[n].taux_historique_a_contre_b_label.grid_forget()
        app.lta[n].longest_serie_a_contre_b_label.grid_forget()
        app.lta[n].match_joues_label.grid_forget()
        app.lta[n].victoire_label.grid_forget()
        app.lta[n].nul_label.grid_forget()
        app.lta[n].defaite_label.grid_forget()
        app.lta[n].moyenne_match_goals_label.grid_forget()
        app.lta[n].moyenne_goals_label.grid_forget()
    except:
        return