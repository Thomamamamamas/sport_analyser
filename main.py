from pickle import TRUE
from PIL import Image
import tkinter
from multiprocessing import Process, Manager
from datetime import date
from database_utils import *
from utils import *
from team import  add_all_image, add_team, get_team_tk, check_if_team_is_valid
from team_fetch import  *
from widget import *
from widget_team import delete_all_teams_widget, place_team
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
        self.number_of_widget = 0
        if platform.system() == 'Darwin':
            self.font_style = 'Helvetica 16 bold'
            self.large_column = 23
            self.medium_column = 18
            self.medium_empty_column = 12
            self.small_column = 12
            self.limit_of_widget = 5500
        elif platform.system() == 'Windows':
            self.font_style = 'Helvetica 14 bold'
            self.large_column = 23
            self.medium_column = 19
            self.medium_empty_column = 12
            self.small_column = 12
            self.limit_of_widget = 3000
        self.large_button_column = 15
        self.small_button_column = 9
        self.height_column = 1
        self.filtre_options = []
        #crawler_utils
        self.ligue_name_url = get_data_json("ligues")
        self.pays_name_url = get_data_json("pays")
        #team_utils
        self.lta = []
        self.tmp_lta = []
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
        self.ligue_end_january = get_data_json("ligue_end_january")
        self.ligue_end_july = get_data_json("ligue_end_july")
        self.ligue_end_december = get_data_json("ligue_end_december")
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

    def debug_mode(self, mode, id):
        self.unbind('<Map>')
        year1 = self.YEAR1
        if mode == "ligue": 
            get_ligue_team_id(self, id)
            get_ligue_prochain_match(self, id)
            get_ligue_team_name(self, id)
            get_ligue_ligues_id(self, id)
            get_ligue_ligue_name(self, id)
            get_ligue_cotes(self, id)
            get_ligue_classement(self, id)
            get_ligue_ligue_logo_url(self, id)
            get_ligue_team_logo_url(self, id)
            get_ligue_adversaire(self, id)
            get_ligue_adversaire_team_id(self, id)
            get_ligue_adversaire_classement(self, id)
            get_ligue_match_team(self, id)
            get_ligue_match_adversaire(self, id)
        elif mode == "team":
            get_team_team_id(self, id)
            get_team_prochain_match(self, id)
            get_team_team_name(self, id)
            get_team_ligues_id(self, id)
            get_team_ligue_name(self, id)
            get_team_cotes(self, id)
            get_team_classement(self, id)
            get_team_ligue_logo_url(self, id)
            get_team_team_logo_url(self, id)
            get_team_adversaire(self, id)
            get_team_adversaire_team_id(self, id)
            get_team_adversaire_classement(self, id)
            get_team_match_team(self, id)
            get_team_match_adversaire(self, id)
            get_other_match_result(self, id)
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
            if check_if_team_is_valid(app, i) == 1:
                year1 = self.YEAR1
                for j in range(0, 2):
                    add_team(self, i + j, year1)
                    add_team_to_dataframe(self, self.lta[i])
                    year1 = year1 - 1
        self.sort_teams(self.list_filtres, self.list_filtres_value, 0)

    def add_all_teams_to_app(self):
        self.unbind('<Map>')
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
        get_all_adversaire_classement(self)
        get_all_match_team(self)
        get_all_match_adversaire(self)
        for i in range(0, len(self.lta), 2):
            tmp = 0
            for j in range(0, 5):
                tmp = len(self.lta[i].t_match_id[j]) + tmp
            if tmp != 0:
                self.tmp_lta.append(self.lta[i])
                self.tmp_lta.append(self.lta[i + 1])
        self.lta.clear()
        self.lta = self.tmp_lta
        print("Ajoute les images ...")
        for i in range(0, len(self.lta), 2):
            if check_if_team_is_valid(app, i) == 1:
                year1 = self.YEAR1
                for j in range(0, 2):
                    add_team(self, i + j, year1)
                    add_team_to_dataframe(self, self.lta[i])
                    year1 = year1 - 1
        self.sort_teams(self.list_filtres, self.list_filtres_value, 0)

 

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll, "units")
            self.canvas_column.xview_scroll(scroll, "units")
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

    def sort_teams(self, values, ascendings, is_sort):
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
            if self.number_of_widget >= 10 and is_sort == 1:
                delete_all_teams_widget(self)
            self.lta.clear()
            for i in range(0, len(tmp_lta)):
                self.lta.append(tmp_lta[i])
            tmp_lta.clear()
        for i in range(0, len(self.lta), 2):
            if check_if_team_is_valid(app, i) == 1:
                year1 = self.YEAR1
                for j in range(0, 2):
                    if is_sort == 1:
                        get_team_tk(self, i + j, year1)
                    place_team(self, j + i, year1)
                    year1 = year1 - 1
                

def get_arg():
    dict = {"debug": False, "debug_mode": 'ligue', "mode_value": 7}
    for i in range(1, len(sys.argv)):
        if "DEBUG=" in sys.argv[i]:
            if "True" in sys.argv[i]:
                dict["debug"] = True
            else:
                dict["debug"] = False
        if "DEBUG_MODE=" in sys.argv[i]:
            if "ligue" in sys.argv[i]:
                dict["debug_mode"] = "ligue"
            elif "team" in sys.argv[i]:
                dict["debug_mode"] = "team"
        if "MODE_VALUE=" in sys.argv[i]:
            dict["mode_value"] = sys.argv[i].split('=', 1)[1]
    return dict

if __name__ == '__main__':
    arg_dict = get_arg()
    app = App()
    if arg_dict["debug"] == True:
        print("DEBUG MODE :")
        app.after(100, app.debug_mode(arg_dict["debug_mode"], arg_dict["mode_value"]))
    else:
        app.after(100, app.add_all_teams_to_app)
    app.mainloop()
    