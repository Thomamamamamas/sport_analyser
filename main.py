from pickle import TRUE
import tkinter
from datetime import date
from database_utils import *
from utils import *
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
        self.small_column = 16
        self.large_button_column = 15
        self.small_button_column = 9
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
        self.list_filtres = []
        self.list_filtres_value = []
        #database_utils
        self.s_db = Db()
        self.db = connect_to_database(self.s_db)
        #touche
        self.bind_all("<MouseWheel>", self.on_mousewheel)
        if self.db:
            self.ligue_id = 0
            self.team_id = 0
            self.cursor = self.db.cursor(buffered=True)
            set_filtre_menu(self)
            set_result_frame(self)
            set_column_utils(self) 
        else:
            mylabel = tkinter.Label(self, text="Erreur de connection à la base de données", fg="red")
            mylabel.pack()

    def add_all_teams_to_app(self):
        app.unbind('<Map>')
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
        tmp_lta = []
        for i in range(0, len(self.lta), 2):
            tmp = 0
            for j in range(0, 5):
                tmp = len(self.lta[i].t_match_id[j]) + tmp
            if tmp != 0:
                tmp_lta.append(self.lta[i])
                tmp_lta.append(self.lta[i + 1])
        self.lta.clear()
        self.lta = tmp_lta
        for i in range(0, len(self.lta), 2):
            year1 = self.YEAR1
            #if self.lta[i].team_id == 163:
            #if self.lta[i].ligue_id == 7:
            for j in range(0, 2):
                add_team(self, i + j, year1)
                add_team_to_dataframe(self, self.lta[i])
                year1 = year1 - 1
        self.sort_teams([0], [0])

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll, "units")
        else:
            self.canvas.yview_scroll(scroll, "units")

    def xview_scroll(self, *args):
        self.canvas.xview(*args)
        self.canvas_column.xview(*args)

    def update_filtre_list(self, filtre):
        for i in range(0, len(self.filtre_options)):
            if filtre == self.filtre_options[i]:
                self.list_filtres[i] = filtre.filtre
                self.list_filtres_value[i] = filtre.value
                break
        print(self.list_filtres)
        print(self.list_filtres_value)

    def sort_teams(self, values, ascendings):
        if len(self.lta) >= 2:
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
            #if self.lta[i].team_id == 163:
            #if self.lta[i].ligue_id == 7:
            for j in range(0, 2):
                place_team(self, j + i, year1)
                year1 = year1 - 1

if __name__ == '__main__':
    app = App()
    app.after(100, app.add_all_teams_to_app)
    app.mainloop()
    