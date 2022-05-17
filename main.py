import tkinter

from database_utils import *
from utils import *
from crawler_main import crawl_specific_ligue_matchs

class Team_data():
    def __init__(self, tk):
        self.team_id = 0
        self.ligue_id = 0
        self.ligue_name = ''
        self.team_name = ''
        self.ligue_label = None
        self.team_label = None
        self.taux_historique_label = None
        self.taux_saison_label = None
        self.serie_label = None
        self.taux_2x_no_goal_label = None
        self.taux_3x_no_goal_label = None
        self.prochain_match_label = None
        self.taux_historique = 0
        self.taux_saison = 0
        self.serie = [0-0-0-0-0]
        self.taux_2x_no_goal = 0
        self.taux_3x_no_goal = 0
        self.prochain_match = ''

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.ligue_name_url = ["bundesliga", "2-bundesliga", "premier-league","championship","bundesliga","pro-league","vysshaya-liga","serie-a","primera-division","primera-a","1-hnl","superliga","premiership","liga-pro","laliga","laliga2","meistriliiga","veikkausliiga","ligue-1","ligue-2","super-league","otp-bank-liga","premier-division","besta-deild-karla","ligat-ha-al","serie-a","serie-b","j1-league","eliteserien","primera-division", "ekstraklasa","liga-portugal","liga-portugal-2","1-liga","liga-1","premier-league","fortuna-liga","prva-liga","allsvenskan","super-league","super-lig","mls"]
        self.team_added = []
        self.sorted = 0
        self.sort_type = 0
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry('%sx%s' % (screen_width, screen_height))
        self.configure(bg='white')
        self.s_db = Db()
        self.db = connect_to_database(self.s_db)
        start = 0
       
        if self.db:
            if start == 0:
                self.cursor = self.db.cursor()
                self.place_option_menu()
                self.place_result_frame()
                self.place_column_utils()    
                start = 1
        else:
            mylabel = tkinter.Label(self, text="Erreur de connection à la base de données", fg="red")
            mylabel.pack()

    def crawl_new_data(self):
        self.cursor.close()
        self.db.close()
        crawl_specific_ligue_matchs(self.pays_selected.get(), self.ligue_name_url[self.ligue_id - 1], self.ligue_id)
        self.db = connect_to_database(self.s_db)
        self.cursor = self.db.cursor()

    def sort_taux(self, type):
        column_sort = []
        tmp = 0
        if len(self.team_added) >= 2:
            if type == 1:
                for i in range(0, len(self.team_added)):
                    column_sort.append(self.team_added[i].taux_historique)
            elif type == 2:
                for i in range(0, len(self.team_added)):
                    column_sort.append(self.team_added[i].taux_saison)
            elif type == 3:
                for i in range(0, len(self.team_added)):
                    for j in range(0, len(self.team_added[i].serie)):
                        tmp = self.team_added[i].serie[j] + tmp
                    column_sort.append(tmp)
            elif type == 4:
                for i in range(0, len(self.team_added)):
                    column_sort.append(self.team_added[i].taux_2x_no_goal)
            elif type == 5:
                for i in range(0, len(self.team_added)):
                    column_sort.append(self.team_added[i].taux_3x_no_goal)
            for j in range(1, len(column_sort)):
                tmp = column_sort[j]
                tmp2 = self.team_added[j]
                i = j - 1
                while i >= 0 and column_sort[i] > tmp:
                    column_sort[i + 1] = column_sort[i]
                    self.team_added[i + 1] = self.team_added[i]
                    i = i - 1
                column_sort[i + 1] = tmp
                self.team_added[i + 1] = tmp2
            if self.sorted == 1 and self.sort_type == type:
                self.sorted = 0
            else:
                self.team_added.reverse()
                self.sorted = 1
                self.sort_type = type
            for i in range(0, len(self.team_added)):
                self.team_added[i].ligue_label.pack_forget()
                self.team_added[i].team_label.pack_forget()
                self.team_added[i].taux_historique_label.pack_forget()
                self.team_added[i].taux_saison_label.pack_forget()
                self.team_added[i].serie_label.pack_forget()
                self.team_added[i].taux_2x_no_goal_label.pack_forget()
                self.team_added[i].taux_3x_no_goal_label.pack_forget()
                self.team_added[i].prochain_match_label.pack_forget()
            self.place_teams()
        
    def change_selected_value(self, type):
        self.sport_drop.pack_forget()
        self.pays_drop.pack_forget()
        self.ligue_drop.pack_forget()
        self.team_drop.pack_forget()
        self.add_button.pack_forget()
        self.crawl_button.pack_forget()
        if type == 1:
            self.pays = list(set(database_fetchall(self.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (self.sport_selected.get()))))
            self.pays_selected = tkinter.StringVar()
            self.pays_selected.set(self.pays[0])
        if type == 2 or type == 1:
            self.ligues = database_fetchall(self.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.pays_selected.get()))
            self.ligue_selected = tkinter.StringVar()
            self.ligue_selected.set(self.ligues[0])
            self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))          
        if type == 3 or type == 1 or type == 2:      
            self.teams = database_fetchall(self.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (self.sport_selected.get(), self.ligue_id))
            self.team_selected = tkinter.StringVar()
            self.team_selected.set(self.teams[0])
            self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

        self.sport_drop = tkinter.OptionMenu(self.frame_option, self.sport_selected, *self.sports, command= self.set_sport_selected)
        self.pays_drop = tkinter.OptionMenu(self.frame_option, self.pays_selected, *self.pays, command= self.set_pays_selected)
        self.ligue_drop = tkinter.OptionMenu(self.frame_option, self.ligue_selected, *self.ligues, command= self.set_ligue_selected)
        self.team_drop = tkinter.OptionMenu(self.frame_option, self.team_selected, *self.teams, command = self.set_team_selected)
        self.add_button = tkinter.Button(self.frame_option, text="AJOUTER", bg="white", fg='black', borderwidth=0, command= self.add_team)
        self.crawl_button = tkinter.Button(self.frame_option, text="RÉCUPERE DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: self.crawl_new_data())

        self.sport_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.pays_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.ligue_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.team_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.add_button.pack(side= 'left', anchor= 'nw', padx=0)
        self.crawl_button.pack(side= 'right')

    def set_sport_selected(self, selection):
        print(selection)
        self.sport_selected.set(selection)
        self.change_selected_value(1)
    
    def set_pays_selected(self, selection):
        print(selection)
        self.pays_selected.set(selection)
        self.change_selected_value(2)

    def set_ligue_selected(self, selection):
        print(selection)
        self.ligue_selected.set(selection)
        self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))          
        print(self.ligue_id)
        self.change_selected_value(3)

    def set_team_selected(self, selection):
        print(selection)
        self.team_selected.set(selection)
        self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

    def place_option_menu(self):
        self.frame_option = tkinter.Frame(self)
        self.frame_option.configure(bg='white')
        self.frame_option.pack(pady = 20, fill=tkinter.X)

        self.sports = ['football']
        self.sport_selected = tkinter.StringVar()
        self.sport_selected.set(self.sports[0])
        self.sport_drop = tkinter.OptionMenu(self.frame_option, self.sport_selected, *self.sports, command= self.set_sport_selected)

        self.pays = list(set(database_fetchall(self.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (self.sport_selected.get()))))
        self.pays_selected = tkinter.StringVar()
        self.pays_selected.set(self.pays[0])
        self.pays_drop = tkinter.OptionMenu(self.frame_option, self.pays_selected, *self.pays, command= self.set_pays_selected)

        self.ligues = database_fetchall(self.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.pays_selected.get()))
        self.ligue_selected = tkinter.StringVar()
        self.ligue_selected.set(self.ligues[0])
        self.ligue_drop = tkinter.OptionMenu(self.frame_option, self.ligue_selected, *self.ligues, command= self.set_ligue_selected)

        self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))

        self.teams = database_fetchall(self.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (self.sport_selected.get(), self.ligue_id))
        self.team_selected = tkinter.StringVar()
        self.team_selected.set(self.teams[0])
        self.team_drop = tkinter.OptionMenu(self.frame_option, self.team_selected, *self.teams, command = self.set_team_selected)

        self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

        self.add_button = tkinter.Button(self.frame_option, text="AJOUTER", bg="white", fg='black', borderwidth=0, command= self.add_team)
        self.crawl_button = tkinter.Button(self.frame_option, text="RÉCUPERE DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: self.crawl_new_data())

        self.sport_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.pays_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.ligue_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.team_drop.pack(side= 'left', anchor= 'nw', padx=0)
        self.add_button.pack(side= 'left', anchor= 'nw', padx=0)
        self.crawl_button.pack(side= 'right')

    def place_result_frame(self):
        self.canvas = tkinter.Canvas(self)
        self.scrollbary = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbarx = tkinter.Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tkinter.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
            )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbary.set)
        self.canvas.configure(xscrollcommand=self.scrollbarx.set)
        self.scrollable_frame.configure(bg= 'white')
        self.canvas.configure(bg= 'white')
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbary.pack(side="right", fill="y")
        self.scrollbarx.pack(side="bottom", anchor="sw", fill="x")

    def place_column_utils(self):
        self.frame_column = []
        for i in range(0, 8):
            self.frame_column.append(tkinter.Frame(self.scrollable_frame))
            self.frame_column[i].configure(bg='white')
            self.frame_column[i].pack(side="left")

        championnat_label = tkinter.Label(self.frame_column[0], text="Championnat", font='Helvetica 18 bold',  fg='black', bg='white', borderwidth=2,  height = 5)
        equipe_label = tkinter.Label(self.frame_column[1], text= "Équipe", font='Helvetica 18 bold',  fg='black', bg='white', borderwidth=2, height = 5)
        taux_historique_button = tkinter.Button(self.frame_column[2], text= "Taux Historique", font='Helvetica 18 bold',fg='black', bg='white', borderwidth=2, command= lambda: self.sort_taux(1),height = 5)
        taux_saison_button = tkinter.Button(self.frame_column[3], text= "Taux Saison", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: self.sort_taux(2), height = 5)
        serie_button = tkinter.Button(self.frame_column[4], text="Série en cours", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: self.sort_taux(3), height = 5)
        taux_2x_button = tkinter.Button(self.frame_column[5], text="Taux 2X", font='Helvetica 18 bold',  fg='black', bg='white',borderwidth=2, command= lambda: self.sort_taux(4), height = 5)
        taux_3x_button = tkinter.Button(self.frame_column[6], text="Taux 3X", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2, command= lambda: self.sort_taux(5), height = 5)
        prochain_match_label = tkinter.Label(self.frame_column[7], text="Prochain match", font='Helvetica 18 bold', fg='black', bg='white', borderwidth=2,  height = 5)
        delete_button = tkinter.Button(self.scrollable_frame, text="X", font='Helvetica 18 bold', fg='black', bg='white', width= 2, height = 5, command= lambda: self.delete_all_teams())

        championnat_label.pack()
        equipe_label.pack(padx= 50)
        taux_historique_button.pack()
        taux_saison_button.pack()
        serie_button.pack()
        taux_2x_button.pack()
        taux_3x_button.pack()
        prochain_match_label.pack(padx= 50)
        delete_button.pack()
        
    def delete_team(self, team):
        team.ligue_label.pack_forget()
        team.team_label.pack_forget()
        team.taux_historique_label.pack_forget()
        team.taux_saison_label.pack_forget()
        team.serie_label.pack_forget()
        team.taux_2x_no_goal_label.pack_forget()
        team.taux_3x_no_goal_label.pack_forget()
        team.prochain_match_label.pack_forget()
        self.team_added.remove(team)
        del team
        print(self.team_added)

    def delete_all_teams(self):
        for i in range(0, len(self.team_added)):
            self.team_added[i].ligue_label.pack_forget()
            self.team_added[i].team_label.pack_forget()
            self.team_added[i].taux_historique_label.pack_forget()
            self.team_added[i].taux_saison_label.pack_forget()
            self.team_added[i].serie_label.pack_forget()
            self.team_added[i].taux_2x_no_goal_label.pack_forget()
            self.team_added[i].taux_3x_no_goal_label.pack_forget()
            self.team_added[i].prochain_match_label.pack_forget()
        self.team_added.clear()
        print(self.team_added)

    def add_team(self):
        print("ajoute team : %d de la ligue : %d" % (self.team_id, self.ligue_id))
        new_team = Team_data(self)
        new_team.team_id = self.team_id
        new_team.ligue_id = self.ligue_id
        new_team.ligue_name = database_fetchone(self.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE ID = %d" %(self.sport_selected.get(), self.ligue_id))
        new_team.team_name = database_fetchone(self.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE ID = %d" %(self.sport_selected.get(), self.team_id))
        new_team.taux_historique = get_taux_historique(self.db, self.team_id)
        new_team.taux_saison = get_taux_actual_season(self.db, self.team_id, 2021, 2022)
        new_team.serie = get_actual_serie(self.db, self.team_id, 2021, 2022)
        new_team.taux_2x_no_goal = get_taux_x_no_goal(self.db, self.team_id, 2)
        new_team.taux_3x_no_goal = get_taux_x_no_goal(self.db, self.team_id, 3)
        self.prochain_match = database_fetchone(self.cursor, "SELECT MATCH_TO_COMING FROM %s.teams WHERE ID = %d" %(self.sport_selected.get(), self.team_id)) 

        new_team.ligue_label = tkinter.Label(self.frame_column[0], text= new_team.ligue_name, font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        new_team.team_label = tkinter.Label(self.frame_column[1], text= new_team.team_name, font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        new_team.taux_historique_label = tkinter.Label(self.frame_column[2], text= str(new_team.taux_historique), font='Helvetica 18 bold',  bg='white', height= 2)
        new_team.taux_saison_label = tkinter.Label(self.frame_column[3], text= str(new_team.taux_saison), font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        new_team.serie_label = tkinter.Label(self.frame_column[4], text= str(new_team.serie), font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        new_team.taux_2x_no_goal_label = tkinter.Label(self.frame_column[5], text= str(new_team.taux_2x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        new_team.taux_3x_no_goal_label = tkinter.Label(self.frame_column[6], text= str(new_team.taux_3x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        if new_team.prochain_match != None:
            new_team.prochain_match_label = tkinter.Label(self.frame_column[7], text= self.prochain_match, font='Helvetica 18 bold',  bg='white', fg='black', height= 2)
        self.team_added.append(new_team)
        print(self.team_added)
        self.place_team(new_team)

    def place_teams(self):
        for i in range(0, len(self.team_added)):
            self.place_team(self.team_added[i])

    def place_team(self, team):
        team.ligue_label.pack(pady= 20)
        team.team_label.pack(pady = 20)
        team.taux_historique_label.pack(pady = 20)
        team.taux_saison_label.pack(pady = 20)
        team.serie_label.pack(pady = 20)
        team.taux_2x_no_goal_label.pack(pady = 20)
        team.taux_3x_no_goal_label.pack(pady = 20)
        team.prochain_match_label.pack(pady = 20)

if __name__ == '__main__':
    app = App()
    app.mainloop()