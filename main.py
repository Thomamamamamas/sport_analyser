import tkinter

from database_utils import *
from utils import *
from crawler_main import crawl_specific_ligue_matchs
from team import delete_all_teams_widget, place_teams, delete_all_teams_widget
from widget import *


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        BIG_FRAME = 100
        MEDIUM_FRAME = 75
        SMALL_FRAME = 50
        self.title = "Sport Analyser"
        self.ligue_name_url = ["bundesliga", "2-bundesliga", "premier-league","championship","bundesliga","pro-league","vysshaya-liga","serie-a","primera-division","primera-a","1-hnl","superliga","premiership","liga-pro","laliga","laliga2","meistriliiga","veikkausliiga","ligue-1","ligue-2","super-league","otp-bank-liga","premier-division","besta-deild-karla","ligat-ha-al","serie-a","serie-b","j1-league","eliteserien","primera-division", "ekstraklasa","liga-portugal","liga-portugal-2","1-liga","liga-1","premier-league","fortuna-liga","prva-liga","allsvenskan","super-league","super-lig","mls"]
        self.pays_name_url = ["allemagne","allemagne","angleterre","angleterre","autriche","belgique","bielorussie","bresil","chili","colombie","croatie","danemark","ecosse","equateur", "espagne","espagne","estonie","finlande","france","france","grece","hongrie","irlande","islande","israel","italie","italie","japon","norvege", "paraguay","pologne","portugal","portugal","republique-tcheque","roumanie","russie","slovaquie","slovenie", "suede", "suisse","turquie","usa"]
        self.frame_column = []
        self.team_added = []
        self.sorted = 0
        self.sort_type = 0
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry('%sx%s' % (screen_width, screen_height))
        self.configure(bg='white')
        self.s_db = Db()
        self.db = connect_to_database(self.s_db)
        self.has_crawled_all_data = 0
        start = 0
       
        if self.db:
            if start == 0:
                self.ligue_id = 0
                self.team_id = 0
                self.cursor = self.db.cursor()
                place_option_menu(self)
                place_result_frame(self)
                for i in range(0, 10):                
                    self.frame_column.append(tkinter.Frame(self.scrollable_frame))
                    self.frame_column[i].configure(bg='white')
                    self.frame_column[i].pack(side="left")
                place_column_utils(self) 
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

    def crawl_all_new_data(self):
        ligues = database_fetchall(self.cursor, "SELECT ID FROM %s.ligues" % (self.sport_selected.get()))
        self.cursor.close()
        self.db.close()
        for i in range(0, len(ligues)):
            crawl_specific_ligue_matchs(self.pays_name_url[ligues[i] - 1], self.ligue_name_url[ligues[i] - 1], ligues[i])  
        self.db = connect_to_database(self.s_db)
        self.cursor = self.db.cursor()
        self.has_crawled_all_data = 1

    def set_sport_selected(self, selection):
        print(selection)
        self.sport_selected.set(selection)
        change_selected_value(self, 1)

    def set_pays_selected(self, selection):
        print(selection)
        self.pays_selected.set(selection)
        change_selected_value(self, 2)

    def set_ligue_selected(self, selection):
        print(selection)
        self.ligue_selected.set(selection)
        self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))          
        print(self.ligue_id)
        change_selected_value(self, 3)

    def set_team_selected(self, selection):
        print(selection)
        self.team_selected.set(selection)
        self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

    def get_column_to_sort(self, type):
        column_sort = []
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
                column_sort.append(self.team_added[i].actual_serie)
        elif type == 5:
            for i in range(0, len(self.team_added)):
                column_sort.append(self.team_added[i].taux_2x_no_goal)
        elif type == 6:
            for i in range(0, len(self.team_added)):
                column_sort.append(self.team_added[i].taux_3x_no_goal)
        elif type == 7:
            for i in range(0, len(self.team_added)):
                column_sort.append(self.team_added[i].taux_historique)
        return column_sort          

    def quick_sort(self, column_sort, team_added):
        less = []
        equal = []
        greater = []
        less_team = []
        equal_team = []
        greater_team = []
        if len(column_sort) > 1:
            pivot = column_sort[0]
            for i in range(0, len(column_sort)):
                if column_sort[i] < pivot:
                    less.append(column_sort[i])
                    less_team.append(team_added[i])
                elif column_sort[i] == pivot:
                    equal.append(column_sort[i])
                    equal_team.append(team_added[i])
                elif column_sort[i] > pivot:
                    greater.append(column_sort[i])
                    greater_team.append(team_added[i])
            return self.quick_sort(less, less_team) + equal_team + self.quick_sort(greater, greater_team) 
        else: 
            return team_added
            
    def sort_taux(self, type):
        tmp = 0
        
        if len(self.team_added) >= 2:
            column_sort = self.get_column_to_sort(type)
            self.team_added = self.quick_sort(column_sort, self.team_added)
            if self.sorted == 1 and self.sort_type == type:
                self.sorted = 0
            else:
                self.team_added.reverse()
                self.sorted = 1
                if type != 7:
                    self.sort_type = type
                else:
                    self.sort_type = 1
            delete_all_teams_widget(self)
            place_teams(self)

if __name__ == '__main__':
    app = App()
    app.mainloop()