from pickle import TRUE
import tkinter
from datetime import date
from database_utils import *
from utils import *
from crawler_main import crawl_specific_ligue_matchs, crawl_cotes
from crawler_utils_2 import get_data_json
from team import  add_team
from team_fetch import  *
from widget import *
from widget_team import place_team
from dataframe_utils import *

class App(tkinter.Tk):
    def __init__(self):
        #app_utils
        self.YEAR1 = date.today().year - 1
        self.YEAR2 = date.today().year
        start = 0
        #widget_utils
        super().__init__()
        self.title = "Sport Analyser"
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry('%sx%s' % (self.screen_width, self.screen_height))
        self.configure(bg='white')
        self.large_column = 22
        self.medium_column = 17
        self.small_column = 12
        self.height_column = 1
        self.filtre_options = []
        #crawler_utils
        self.ligue_name_url = get_data_json("ligues")
        self.pays_name_url = get_data_json("pays")
        #team_utils
        self.lta = []
        self.ligue_logo_file_name = []
        self.team_logo_file_name = []
        self.ligue_logo = []
        self.team_logo = []
        self.sorted = 0
        self.sort_type = 0
        self.row_team_id = 0
        self.df = pd.DataFrame()
        self.id_team_sorted = []
        #database_utils
        self.s_db = Db()
        self.db = connect_to_database(self.s_db)
         
        if self.db:
            if start == 0:
                self.ligue_id = 0
                self.team_id = 0
                self.cursor = self.db.cursor(buffered=True)
                set_filtre_menu(self)
                set_result_frame(self)
                set_column_utils(self) 
                self.add_all_teams_to_app()
                start = 1
        else:
            mylabel = tkinter.Label(self, text="Erreur de connection à la base de données", fg="red")
            mylabel.pack()

    def add_all_teams_to_app(self):
        year1 = self.YEAR1
        get_all_team_id(self)
        get_all_prochain_match(self)
        get_all_team_name(self)
        get_all_ligues_id(self)
        get_all_ligue_name(self)
        get_all_cotes(self)
        get_all_classement(self)
        get_all_ligue_logo_url(self)
        get_all_team_logo_url(self)
        get_all_adversaire(self)
        get_all_adversaire_team_id(self)
        get_all_match_team(self)
        get_all_match_adversaire(self)
        for i in range(0, len(self.lta), 2):
            year1 = self.YEAR1
            if self.lta[i].team_id == 423:
            #if self.lta[i].ligue_id == 7:
                for j in range(0, 2):
                    add_team(self, i + j, year1)
                    add_team_to_dataframe(self, self.lta[i])
                    year1 = year1 - 1
        self.sort_teams([1], [0])

    def xview_scroll(self, *args):
        self.canvas.xview(*args)
        self.canvas_column.xview(*args)

    def set_sport_selected(self, selection):
        self.sport_selected.set(selection)
        change_selected_value(self, 1)

    def set_pays_selected(self, selection):
        self.pays_selected.set(selection)
        change_selected_value(self, 2)

    def set_ligue_selected(self, selection):
        self.ligue_selected.set(selection)
        self.ligue_id = database_fetchone(self.cursor, "SELECT ID FROM %s.ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (self.sport_selected.get(), self.ligue_selected.get(), self.pays_selected.get()))          
        change_selected_value(self, 3)

    def set_team_selected(self, selection):
        self.team_selected.set(selection)
        self.team_id = database_fetchone(self.cursor, "SELECT ID FROM %s.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (self.sport_selected.get(), self.team_selected.get(), self.ligue_id))

    def sort_teams(self, values, ascendings):
        self.row_team_id = 0
        self.id_team_sorted.clear()
        tmp_lta = []
        
        sort_dataframe(self, values, ascendings)
        for i in range(0, len(self.df)):
            if int(self.df.loc[i, 'id']) not in self.id_team_sorted:
                self.id_team_sorted.append(int(self.df.loc[i, 'id']))
                for j in range(0, len(self.lta)):
                    if self.lta[j].team_id == int(self.df.loc[i, 'id']):
                        tmp_lta.append(self.lta[j])
        self.lta.clear()
        self.lta = tmp_lta
        for i in range(0, len(self.lta), 2):
            year1 = self.YEAR1
            if self.lta[i].team_id == 423:
            #if self.lta[i].ligue_id == 7:
                for j in range(0, 2):
                    place_team(self, j + i, year1)
                    year1 = year1 - 1

if __name__ == '__main__':
    app = App()
    app.mainloop()