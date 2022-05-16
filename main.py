from cProfile import label
from pkgutil import get_data
from tkinter import *
import tkinter.ttk

from pytz import NonExistentTimeError
from crawler_utils import get_data_json
from database_utils import *
from utils import *
from crawler_main import crawl_specific_ligue_matchs

class Team_data():
    def __init__(self, tk):
        self.frame_team = Frame(tk.scrollable_frame)
        self.frame_team.configure(bg='white')
        self.team_id = 0
        self.ligue_id = 0
        self.ligue_name = ''
        self.team_name = ''
        self.delete_button = None
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

class App(Tk):
    def __init__(self):
        super().__init__()
        self.team_added = []
        self.sorted = 0
        self.sort_type = 0
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.large_case_size = int(self.winfo_width() / 10)
        self.normal_case_size = int(self.winfo_width() / 12)
        self.geometry('%sx%s' % (screen_width, screen_height))
        self.configure(bg='white')
        self.s_db = Db()
        self.db = connect_to_database(self.s_db)
        start = 0
       
        if self.db:
            if start == 0:
                self.cursor = self.db.cursor()
                self.ligue_name_url = get_data_json('ligues')
                self.place_option_menu()
                self.place_column_utils()
                self.place_result_frame()
                start = 1
        else:
            mylabel = Label(self, text="Erreur de connection à la base de données", fg="red")
            mylabel.pack()


    def crawl_new_data(self):
        self.cursor.close()
        self.db.close()
        crawl_specific_ligue_matchs(self.pays_selected.get(), self.ligue_name_url[self.ligue_id - 1], self.ligue_id)
        self.db = connect_to_database(self.s_db)
        self.cursor = self.db.cursor()

    def delete_team(self, team):
        team.frame_team.pack_forget()
        self.team_added.remove(team)
        del team
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

        new_team.delete_button = Button(new_team.frame_team, text= 'X', font= 'Helvetica 12 bold',  bg= 'white', fg= 'black', command= lambda: self.delete_team(new_team), width= 1, height = 3)
        new_team.ligue_label = Label(new_team.frame_team, text= new_team.ligue_name, font='Helvetica 18 bold',  bg='white', fg='black', width= self.normal_case_size, height = 3)
        new_team.team_label = Label(new_team.frame_team, text= new_team.team_name, font='Helvetica 18 bold',  bg='white', fg='black', width= self.large_case_size, height = 3)
        new_team.taux_historique_label = Label(new_team.frame_team, text= str(new_team.taux_historique), font='Helvetica 18 bold',  bg='white', fg='black', width= self.large_case_size, height = 3)
        new_team.taux_saison_label = Label(new_team.frame_team, text= str(new_team.taux_saison), font='Helvetica 18 bold',  bg='white', fg='black', width=self.normal_case_size, height = 3)
        new_team.serie_label = Label(new_team.frame_team, text= str(new_team.serie), font='Helvetica 18 bold',  bg='white', fg='black', width= self.large_case_size, height = 3)
        new_team.taux_2x_no_goal_label = Label(new_team.frame_team, text= str(new_team.taux_2x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', width= self.normal_case_size, height = 3)
        new_team.taux_3x_no_goal_label = Label(new_team.frame_team, text= str(new_team.taux_3x_no_goal), font='Helvetica 18 bold',  bg='white', fg='black', width= self.large_case_size, height = 3)
        if new_team.prochain_match != None:
            new_team.prochain_match_label = Label(new_team.frame_team, text= self.prochain_match, font='Helvetica 18 bold',  bg='white', fg='black', width= self.large_case_size, height = 1)
        self.team_added.append(new_team)
        print(self.team_added)
        self.place_team(new_team)

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
                print("second")
                self.sorted = 0
            else:
                print("first")
                self.team_added.reverse()
                self.sorted = 1
                self.sort_type = type
            for i in range(0, len(self.team_added)):
                print("delete")
                self.team_added[i].frame_team.pack_forget()
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
            self.pays_selected = StringVar()
            self.pays_selected.set(self.pays[0])
        if type == 2 or type == 1:
            self.ligues = database_fetchall(self.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.pays_selected.get()))
            self.ligue_selected = StringVar()
            self.ligue_selected.set(self.ligues[0])
            self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))          
        if type == 3 or type == 1 or type == 2:      
            self.teams = database_fetchall(self.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (self.sport_selected.get(), self.ligue_id))
            self.team_selected = StringVar()
            self.team_selected.set(self.teams[0])
            self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

        self.sport_drop = OptionMenu(self.frame_option, self.sport_selected, *self.sports, command= self.set_sport_selected)
        self.pays_drop = OptionMenu(self.frame_option, self.pays_selected, *self.pays, command= self.set_pays_selected)
        self.ligue_drop = OptionMenu(self.frame_option, self.ligue_selected, *self.ligues, command= self.set_ligue_selected)
        self.team_drop = OptionMenu(self.frame_option, self.team_selected, *self.teams, command = self.set_team_selected)
        self.add_button = Button(self.frame_option, text="AJOUTER", bg="white", fg='black', borderwidth=0, command= self.add_team)
        self.crawl_button = Button(self.frame_option, text="RÉCUPERE DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: self.crawl_new_data())

        self.sport_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.pays_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.ligue_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.team_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.add_button.pack(side=LEFT, anchor=NW, padx=0)
        self.crawl_button.pack(side=RIGHT)

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
        self.frame_option = Frame(self)
        self.frame_option.configure(bg='white')
        self.frame_option.pack(pady = 20, fill=X)

        self.sports = ['football']
        self.sport_selected = StringVar()
        self.sport_selected.set(self.sports[0])
        self.sport_drop = OptionMenu(self.frame_option, self.sport_selected, *self.sports, command= self.set_sport_selected)

        self.pays = list(set(database_fetchall(self.cursor, "SELECT LIGUE_PAYS FROM %s.ligues" % (self.sport_selected.get()))))
        self.pays_selected = StringVar()
        self.pays_selected.set(self.pays[0])
        self.pays_drop = OptionMenu(self.frame_option, self.pays_selected, *self.pays, command= self.set_pays_selected)

        self.ligues = database_fetchall(self.cursor, "SELECT LIGUE_NAME FROM %s.ligues WHERE LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.pays_selected.get()))
        self.ligue_selected = StringVar()
        self.ligue_selected.set(self.ligues[0])
        self.ligue_drop = OptionMenu(self.frame_option, self.ligue_selected, *self.ligues, command= self.set_ligue_selected)

        self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))

        self.teams = database_fetchall(self.cursor, "SELECT TEAM_NAME FROM %s.teams WHERE LIGUE_ID = %d" %  (self.sport_selected.get(), self.ligue_id))
        self.team_selected = StringVar()
        self.team_selected.set(self.teams[0])
        self.team_drop = OptionMenu(self.frame_option, self.team_selected, *self.teams, command = self.set_team_selected)

        self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

        self.add_button = Button(self.frame_option, text="AJOUTER", bg="white", fg='black', borderwidth=0, command= self.add_team)
        self.crawl_button = Button(self.frame_option, text="RÉCUPERE DONNÉES", bg="white", fg='black', borderwidth=0, command= lambda: self.crawl_new_data())

        self.sport_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.pays_drop.pack(side=LEFT, anchor=NW, padx=0,)
        self.ligue_drop.pack(side=LEFT, anchor=NW, padx=0, )
        self.team_drop.pack(side=LEFT, anchor=NW, padx=0)
        self.add_button.pack(side=LEFT, anchor=NW, padx=0)
        self.crawl_button.pack(side=RIGHT, anchor=NW)


    def place_column_utils(self):
        frame_column = Frame(self)
        frame_column.configure(bg='white')
        frame_column.pack(pady = 10, fill=X)
        

        empty_label = Label(frame_column, text = "  ", bg="white")
        championnat_label = Label(frame_column, text="Championnat", font='Helvetica 18 bold',  bg='white', fg='black', borderwidth=2, relief="solid", width= self.large_case_size, height = 5)
        equipe_label = Label(frame_column, text= "Équipe", font='Helvetica 18 bold',  bg='white', fg='black', borderwidth=2, relief="solid", width= self.large_case_size, height = 5)
        taux_historique_button = Button(frame_column, text= "Taux Historique", font='Helvetica 18 bold', bg='white', fg='black', borderwidth=2, command= lambda: self.sort_taux(1), width= self.normal_case_size, height = 5)
        taux_saison_button = Button(frame_column, text= "Taux Saison", font='Helvetica 18 bold', bg='white', fg='black', borderwidth=2, command= lambda: self.sort_taux(2), width= self.normal_case_size, height = 5)
        serie_button = Button(frame_column, text="Série en cours", font='Helvetica 18 bold',  bg='white', fg='black', borderwidth=2, relief="solid",command= lambda: self.sort_taux(3), width= self.normal_case_size, height = 5)
        taux_2x_button = Button(frame_column, text="Taux 2X", font='Helvetica 18 bold',  bg='white', fg='black', borderwidth=2, command= lambda: self.sort_taux(4), width= self.normal_case_size, height = 5)
        taux_3x_button = Button(frame_column, text="Taux 3X", font='Helvetica 18 bold',  bg='white', fg='black', borderwidth=2, command= lambda: self.sort_taux(5), width= self.normal_case_size, height = 5)
        prochain_match_label = Label(frame_column, text="Prochain match", font='Helvetica 18 bold', bg='white', fg='black', borderwidth=2, relief="solid", width= self.normal_case_size, height = 5)
        
        empty_label.grid(column = 0, row= 0)
        championnat_label.grid(column= 1, row= 0)
        equipe_label.grid(column= 2, row=0)
        taux_historique_button.grid(column= 3, row= 0)
        taux_saison_button.grid(column= 4, row= 0)
        serie_button.grid(column= 5, row= 0)
        taux_2x_button.grid(column= 6, row= 0)
        taux_3x_button.grid(column= 7, row= 0)
        prochain_match_label.grid(column= 8, row= 0)

    def place_result_frame(self):
        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
            )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def place_teams(self):
        for i in range(0, len(self.team_added)):
            self.place_team(self.team_added[i])

    def place_team(self, team):
        team.frame_team.pack(pady=0, fill=X)
        team.delete_button.grid(column = 0, row= 0)
        team.ligue_label.grid(column = 1, row= 0)
        team.team_label.grid(column = 2, row= 0)
        team.taux_historique_label.grid(column = 3, row= 0)
        team.taux_saison_label.grid(column = 4, row= 0)
        team.serie_label.grid(column = 5, row= 0)
        team.taux_2x_no_goal_label.grid(column = 6, row= 0)
        team.taux_3x_no_goal_label.grid(column = 7, row= 0)
        team.prochain_match_label.grid(column = 8, row= 0)

if __name__ == '__main__':
    app = App()
    app.mainloop()