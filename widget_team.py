from PIL import Image,ImageTk
import tkinter

def get_image(image_url, team, i):
    if 'https://www.' not in image_url:
        image_url = 'https://www.' + image_url
    file_name = 'images/' + image_url.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
    img = Image.open(file_name).convert('RGBA')
    if i == 0:
        team.logo_cv.append(tkinter.Canvas(team.ligue_frame, width= 50, height= 50, bd=0, highlightthickness=0, relief='ridge'))
    else:
            team.logo_cv.append(tkinter.Canvas(team.team_frame, width= 40, height= 40, bd=0, highlightthickness=0, relief='ridge'))
    team.logo_cv[i].configure(bg="white")
    team.photo.append(ImageTk.PhotoImage(img))

def place_teams(app):
    for i in range(0, len(app.team_added)):
        place_team(app.team_added[i])

def place_team(team):
    print("place team : %d de la ligue %d" % (team.team_id, team.ligue_id))
    team.ligue_frame.pack(pady = 0)
    team.logo_cv[0].pack(side='left')
    team.logo_cv[0].create_image(0 ,0, anchor="nw", image=team.photo[0])
    team.ligue_label.pack(anchor='center')
    team.team_frame.pack(pady = 0, fill='x')
    team.logo_cv[1].pack(side='left')
    team.logo_cv[1].create_image(0 ,0,anchor="nw",image=team.photo[1])
    team.team_label.pack(anchor='center')

    team.taux_historique_label.pack(pady = 0, fill='x')
    team.taux_saison_label.pack(pady = 0, fill='x')
    team.serie_label.pack(pady = 0, fill='x')
    team.longest_serie_label.pack(pady = 0, fill='x')
    team.taux_2x_no_goal_label.pack(pady = 0, fill='x')
    team.taux_3x_no_goal_label.pack(pady = 0, fill='x')
    team.prochain_match_label.pack(pady = 0, fill='x')
    team.empty_label.pack(pady = 0, fill='x')

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