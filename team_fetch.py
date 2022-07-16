from database_utils import *
from team import Team_data

def get_all_team_id(app):
    db_data = database_fetchall(app.cursor, "SELECT ID FROM football.teams WHERE MATCH_TO_COMING != ''")
    for i in range(0, len(db_data)):
        for j in range(0, 2):
            new_team = Team_data()
            new_team.team_id = db_data[i]
            app.lta.append(new_team)

def get_all_team_name(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_NAME FROM football.teams WHERE ID = %s" % (app.lta[i].team_id))
        for j in range(0, 2):
            app.lta[i + j].team_name = db_data

def get_all_prochain_match(app):
    tmp_team_added = []
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT MATCH_TO_COMING FROM football.teams WHERE ID = %d" %(app.lta[i].team_id))
        if db_data != '' and db_data != None and db_data != ' ':
            for j in range(0, 2):
                app.lta[i + j].prochain_match = db_data
                tmp_team_added.append(app.lta[i + j])
    app.lta.clear()
    app.lta = tmp_team_added

def get_all_ligues_id(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_ID FROM football.teams WHERE ID = %s" % (app.lta[i].team_id))
        for j in range(0, 2):
            app.lta[i + j].ligue_id = db_data

def get_all_ligue_name(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_NAME FROM football.ligues WHERE ID = %s" % (app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].ligue_name = db_data

def get_all_cotes(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT COTE_MATCH FROM football.teams WHERE ID = %d" %(app.lta[i].team_id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].cotes = db_data

def get_all_classement(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d" %(app.lta[i].team_id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].classement = db_data

def get_all_ligue_logo_url(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_LOGO FROM football.ligues WHERE ID = %d" %(app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].ligue_logo_url = db_data

def get_all_team_logo_url(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_LOGO FROM football.teams WHERE ID = %d" %(app.lta[i].team_id))
        for j in range(0, 2):
            app.lta[i + j].team_logo_url = db_data

def get_all_adversaire(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ADVERSAIRE_B FROM football.teams WHERE ID = %d" % ( app.lta[i].team_id))
        for j in range(0, 2):
            app.lta[i + j].adversaire = db_data

def get_all_adversaire_team_id(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ID FROM football.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (app.lta[i].adversaire, app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].adversaire_team_id = db_data

def get_all_adversaire_classement(app):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d" %(app.lta[i].adversaire_team_id))
        for j in range(0, 2):
            if db_data != None and db_data != '':
                app.lta[i + j].a_classement = db_data
            else:
                app.lta[i + j].a_classement = 0

def get_all_match_team(app):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].t_match_id.append([])
            app.lta[i].t_match_res.append([])
            app.lta[i].t_match_day.append([])
            app.lta[i].t_match_home.append([])
            app.lta[i].t_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d" % (app.lta[i].team_id, year1))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].t_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].t_match_id[a].append(db_data[z][0])
                app.lta[i].t_match_res[a].append(db_data[z][7])
                app.lta[i].t_match_day[a].append(db_data[z][4])
                app.lta[i].t_match_home[a].append(db_data[z][9])
                app.lta[i].t_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1
            
def get_all_match_adversaire(app):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].a_match_id.append([])
            app.lta[i].a_match_res.append([])
            app.lta[i].a_match_day.append([])
            app.lta[i].a_match_home.append([])
            app.lta[i].a_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d" % (app.lta[i].adversaire_team_id, year1))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].a_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].a_match_id[a].append(db_data[z][0])
                app.lta[i].a_match_res[a].append(db_data[z][7])
                app.lta[i].a_match_day[a].append(db_data[z][4])
                app.lta[i].a_match_home[a].append(db_data[z][9])
                app.lta[i].a_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1

def get_other_match_result(app):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].o_match_id.append([])
            app.lta[i].o_match_res.append([])
            format_match_id = ','.join(['%s'] * len(app.lta[i].t_match_id[a],))
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE ID IN (%s) AND YEAR1 = %d" % (format_match_id, tuple(app.lta[i].t_match_id[a]), year1))
            for z in range(0, len(db_data), 1):
                app.lta[i].o_match_id[a].append(db_data[z][0])
                app.lta[i].o_match_res[a].append(db_data[z][7])
            db_data.clear()
            year1 = year1 - 1


#_____________________________________________________________________________________LIGUE__________________________________________________________________________________________________________________________________________

def get_ligue_team_id(app, id):
    db_data = database_fetchall(app.cursor, "SELECT ID FROM football.teams WHERE LIGUE_ID = %s AND MATCH_TO_COMING != ''" % (id))
    for i in range(0, len(db_data)):
        for j in range(0, 2):
            new_team = Team_data()
            new_team.team_id = db_data[i]
            app.lta.append(new_team)

def get_ligue_team_name(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_NAME FROM football.teams WHERE ID = %s AND LIGUE_ID = %s" % (app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].team_name = db_data

def get_ligue_prochain_match(app, id):
    tmp_team_added = []
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT MATCH_TO_COMING FROM football.teams WHERE ID = %d AND LIGUE_ID = %s" %(app.lta[i].team_id, id))
        if db_data != '' and db_data != None and db_data != ' ':
            for j in range(0, 2):
                app.lta[i + j].prochain_match = db_data
                tmp_team_added.append(app.lta[i + j])
    app.lta.clear()
    app.lta = tmp_team_added

def get_ligue_ligues_id(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_ID FROM football.teams WHERE ID = %s AND LIGUE_ID = %s" % (app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].ligue_id = db_data

def get_ligue_ligue_name(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_NAME FROM football.ligues WHERE ID = %s AND ID = %s" % (app.lta[i].ligue_id, id))
        for j in range(0, 2):
            app.lta[i + j].ligue_name = db_data

def get_ligue_cotes(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT COTE_MATCH FROM football.teams WHERE ID = %d AND LIGUE_ID = %s" %(app.lta[i].team_id, id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].cotes = db_data

def get_ligue_classement(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d AND LIGUE_ID = %s" %(app.lta[i].team_id, id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].classement = db_data

def get_ligue_ligue_logo_url(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_LOGO FROM football.ligues WHERE ID = %d AND ID = %s" %(app.lta[i].ligue_id, id))
        for j in range(0, 2):
            app.lta[i + j].ligue_logo_url = db_data

def get_ligue_team_logo_url(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_LOGO FROM football.teams WHERE ID = %d" %(app.lta[i].team_id))
        for j in range(0, 2):
            app.lta[i + j].team_logo_url = db_data

def get_ligue_adversaire(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ADVERSAIRE_B FROM football.teams WHERE ID = %d AND LIGUE_ID = %s" % ( app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].adversaire = db_data

def get_ligue_adversaire_team_id(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ID FROM football.teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %s" % (app.lta[i].adversaire, id))
        for j in range(0, 2):
            app.lta[i + j].adversaire_team_id = db_data

def get_ligue_adversaire_classement(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d AND LIGUE_ID = %s" %(app.lta[i].adversaire_team_id, id))
        for j in range(0, 2):
            if db_data != None and db_data != '':
                app.lta[i + j].a_classement = db_data
            else:
                app.lta[i + j].a_classement = 0

def get_ligue_match_team(app, id):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].t_match_id.append([])
            app.lta[i].t_match_res.append([])
            app.lta[i].t_match_day.append([])
            app.lta[i].t_match_home.append([])
            app.lta[i].t_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d AND LIGUE_ID = %s" % (app.lta[i].team_id, year1, id))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].t_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].t_match_id[a].append(db_data[z][0])
                app.lta[i].t_match_res[a].append(db_data[z][7])
                app.lta[i].t_match_day[a].append(db_data[z][4])
                app.lta[i].t_match_home[a].append(db_data[z][9])
                app.lta[i].t_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1
            
def get_ligue_match_adversaire(app, id):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].a_match_id.append([])
            app.lta[i].a_match_res.append([])
            app.lta[i].a_match_day.append([])
            app.lta[i].a_match_home.append([])
            app.lta[i].a_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d AND LIGUE_ID = %s" % (app.lta[i].adversaire_team_id, year1, id))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].a_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].a_match_id[a].append(db_data[z][0])
                app.lta[i].a_match_res[a].append(db_data[z][7])
                app.lta[i].a_match_day[a].append(db_data[z][4])
                app.lta[i].a_match_home[a].append(db_data[z][9])
                app.lta[i].a_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1

#______________________________________________________________________________________TEAM__________________________________________________________________________________________________________________________________________

def get_team_team_id(app, id):
    db_data = database_fetchall(app.cursor, "SELECT ID FROM football.teams WHERE ID = %s AND MATCH_TO_COMING != ''" % (id))
    for i in range(0, len(db_data)):
        for j in range(0, 2):
            new_team = Team_data()
            new_team.team_id = db_data[i]
            app.lta.append(new_team)

def get_team_team_name(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_NAME FROM football.teams WHERE ID = %s AND ID = %s" % (app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].team_name = db_data

def get_team_prochain_match(app, id):
    tmp_team_added = []
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT MATCH_TO_COMING FROM football.teams WHERE ID = %d AND ID = %s" %(app.lta[i].team_id, id))
        if db_data != '' and db_data != None and db_data != ' ':
            for j in range(0, 2):
                app.lta[i + j].prochain_match = db_data
                tmp_team_added.append(app.lta[i + j])
    app.lta.clear()
    app.lta = tmp_team_added

def get_team_ligues_id(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_ID FROM football.teams WHERE ID = %s AND ID = %s" % (app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].ligue_id = db_data

def get_team_ligue_name(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_NAME FROM football.ligues WHERE ID = %s" % (app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].ligue_name = db_data

def get_team_cotes(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT COTE_MATCH FROM football.teams WHERE ID = %d AND ID = %s" %(app.lta[i].team_id, id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].cotes = db_data

def get_team_classement(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d AND ID = %s" %(app.lta[i].team_id, id))
        if db_data == None:
            db_data = ''
        for j in range(0, 2):
            app.lta[i + j].classement = db_data

def get_team_ligue_logo_url(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT LIGUE_LOGO FROM football.ligues WHERE ID = %d" %(app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].ligue_logo_url = db_data

def get_team_team_logo_url(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT TEAM_LOGO FROM football.teams WHERE ID = %d AND ID = %s" %(app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].team_logo_url = db_data

def get_team_adversaire(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ADVERSAIRE_B FROM football.teams WHERE ID = %d AND ID = %s" % ( app.lta[i].team_id, id))
        for j in range(0, 2):
            app.lta[i + j].adversaire = db_data

def get_team_adversaire_team_id(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT ID FROM football.teams WHERE TEAM_NAME = '%s' AND ID = %s AND LIGUE_ID = $d" % (app.lta[i].adversaire, id, app.lta[i].ligue_id))
        for j in range(0, 2):
            app.lta[i + j].adversaire_team_id = db_data

def get_team_adversaire_classement(app, id):
    for i in range(0, len(app.lta), 2):
        db_data = database_fetchone(app.cursor, "SELECT CLASSEMENT FROM football.teams WHERE ID = %d AND ID = %s" %(app.lta[i].adversaire_team_id, id))
        for j in range(0, 2):
            if db_data != None and db_data != '':
                app.lta[i + j].a_classement = db_data
            else:
                app.lta[i + j].a_classement = 0

def get_team_match_team(app, id):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].t_match_id.append([])
            app.lta[i].t_match_res.append([])
            app.lta[i].t_match_day.append([])
            app.lta[i].t_match_home.append([])
            app.lta[i].t_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d AND TEAM_ID = %s" % (app.lta[i].team_id, year1, id))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].t_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].t_match_id[a].append(db_data[z][0])
                app.lta[i].t_match_res[a].append(db_data[z][7])
                app.lta[i].t_match_day[a].append(db_data[z][4])
                app.lta[i].t_match_home[a].append(db_data[z][9])
                app.lta[i].t_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1
            
def get_team_match_adversaire(app, id):
    for i in range(0, len(app.lta), 1):
        year1 = app.YEAR1
        for a in range(0, 5):
            app.lta[i].a_match_id.append([])
            app.lta[i].a_match_res.append([])
            app.lta[i].a_match_day.append([])
            app.lta[i].a_match_home.append([])
            app.lta[i].a_match_goalfirst.append([])
            db_data = database_fetchall_everything(app.cursor, "SELECT * FROM matchs WHERE TEAM_ID = %d AND YEAR1 = %d AND TEAM_ID = %s" % (app.lta[i].adversaire_team_id, year1, id))
            for z in range(0, len(db_data), 1):
                if db_data[z][4] in app.lta[i].a_match_day[a] and db_data[z][4] != 'Finale':
                    break
                app.lta[i].a_match_id[a].append(db_data[z][0])
                app.lta[i].a_match_res[a].append(db_data[z][7])
                app.lta[i].a_match_day[a].append(db_data[z][4])
                app.lta[i].a_match_home[a].append(db_data[z][9])
                app.lta[i].a_match_goalfirst[a].append(db_data[z][10])
            db_data.clear()
            year1 = year1 - 1