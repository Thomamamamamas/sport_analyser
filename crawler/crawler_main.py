import re
import time
import platform
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database_utils import *
from crawler_utils_1 import get_os_chromedriver_path, resource_path, get_who_goal_first, get_match_id, process_data, get_next_match_data, get_classement_correct_page, get_correct_page, match_already_exist, show_all_match, wait_till_appear_class
from crawler_utils_2 import get_data_json

def crawl_specific_ligue_matchs(pays, ligue_name, ligue_id):
    print("Récupère les dernieres données de :")
    print(pays)
    print(ligue_name)
    print(ligue_id)
    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
        subdriver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
        caldriver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    elif platform.system() == 'Windows':
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        subdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        caldriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    year1 = 2021
    year2 = 2022

    get_next_match_data(caldriver, db, pays, ligue_name, ligue_id)
    crawl_classement(db, pays, ligue_name, ligue_id, year1, year2)
    for j in range(0, 5):
        get_correct_page(driver, pays, ligue_name, year1, year2, j)
        show_all_match(driver)
        if crawl_specific_match(driver, subdriver, s_db, db, ligue_id, year1, year2) == 0:
            break
        year1 = year1 - 1
        year2 = year2 - 1
    db.commit()
    db.close()
    db = connect_to_database(s_db)
    driver.quit()
    subdriver.quit()

def crawl_classement(db, pays, ligue_name, ligue_id, year1, year2):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    elif platform.system() == 'Windows':
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    if db:
        cursor = db.cursor()
        get_classement_correct_page(driver, pays, ligue_name, year1, year2, 0)
        element_click =  wait_till_appear_class(driver, 3, 'tournamentStage')
        if element_click != None:
            try:
                driver.execute_script("arguments[0].click();", element_click)
            except:
                element_click.click()
        cursor.execute("UPDATE teams SET CLASSEMENT = '' WHERE LIGUE_ID = %d" % (ligue_id))
        time.sleep(2)
        try:
            div = wait_till_appear_class(driver, 3, 'ui-table__body')
        except:
            return
        for i in range(0, 100):
            try:
                subdiv = div.find_elements_by_class_name('ui-table__row')[i]
            except:
                break
            classement = subdiv.find_element_by_class_name('tableCellRank')
            classement = re.sub(CLEANR, '', str(classement.get_attribute("innerHTML"))).replace('.', '')
            team_name = subdiv.find_element_by_class_name('tableCellParticipant__name')
            team_name = re.sub(CLEANR, '', str(team_name.get_attribute("innerHTML")))
            cursor.execute("UPDATE teams SET CLASSEMENT = '%s' WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (classement, process_data(team_name), ligue_id))
            print("UPDATE teams SET CLASSEMENT = '%s' WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (classement, process_data(team_name), ligue_id))
        return 0
    else:
        print("Echec de la connection a la base de données")
        return 1



def crawl_specific_match(driver, subdriver, s_db, db, ligue_id, year1, year2):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    journee = ''

    if db == None:
        db = connect_to_database(s_db)
    if db:
        cursor = db.cursor(buffered=True)
        div = driver.find_element_by_class_name('sportName')
        for n in range(2, 400):
            try:
                subdiv = div.find_element_by_xpath('div[%d]' % (n))
            except:
                break
            if 'event__round' not in subdiv.get_attribute('class') and 'event__header' not in subdiv.get_attribute('class'):
                match_id = get_match_id(cursor)
                team_1_name = subdiv.find_elements_by_class_name('event__participant')[0]
                team_1_name = re.sub(CLEANR, '', str(team_1_name.get_attribute("innerHTML")))
                team_2_name = subdiv.find_elements_by_class_name('event__participant')[1]
                team_2_name = re.sub(CLEANR, '', str(team_2_name.get_attribute("innerHTML")))
                for m in range(0, 2):
                    team_name = subdiv.find_elements_by_class_name('event__participant')[m]
                    if ligue_id == 42 or ligue_id == 18 or ligue_id == 35 or ligue_id == 26 or ligue_id == 27 or ligue_id == 13 or ligue_id == 25 or ligue_id == 29 or ligue_id == 36:
                        journee = subdiv.find_element_by_class_name('event__time')
                        journee  = re.sub(CLEANR, '', str(journee.get_attribute("innerHTML")))
                    if 'event__participant--home' in team_name.get_attribute('class'):
                        domicile = 1
                    else:
                        domicile = 0
                    team_name = re.sub(CLEANR, '', str(team_name.get_attribute("innerHTML")))
                    team_score = subdiv.find_elements_by_class_name('event__score')[m]
                    try:
                        team_score = int(re.sub(CLEANR, '', str(team_score.get_attribute("innerHTML"))))
                    except:
                        try:
                            team_score = re.sub(CLEANR, '', str(team_score.get_attribute("innerHTML")))
                        except:
                            team_score = 0
                    try:
                        team_midterm_score = subdiv.find_elements_by_class_name('event__part--1')[m]
                        team_midterm_score = int(re.sub(CLEANR, '', str(team_midterm_score.get_attribute("innerHTML"))).replace('(', '').replace(')', ''))
                    except:
                        team_midterm_score = 0
                    team_id =  database_fetchone(cursor, "SELECT ID FROM teams WHERE TEAM_NAME = '%s'" % (process_data(team_name)))
                    if match_already_exist(cursor, ligue_id, process_data(team_1_name), process_data(team_2_name), process_data(journee), year1, year2) == 1:
                        print("Match dèjà enregistré")
                        return 0
                    match_url = 'https://www.flashscore.fr/match/' + subdiv.get_attribute('id').split('_', 2)[2] + '/#/resume-du-match/resume-du-match'
                    if domicile == 1:
                        t_goal_first = get_who_goal_first(subdriver, match_url, subdiv, team_score, team_midterm_score, m)
                    else:
                        t_goal_first = 0
                    try:
                        cursor.execute("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE, TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, t_goal_first))
                        print("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, t_goal_first))
                    except:
                        print("N'insère rien")
                        continue
            else:
                if ligue_id != 42 and ligue_id != 18 and ligue_id != 35 and ligue_id != 26 and ligue_id != 27 and ligue_id != 13 and ligue_id != 25 and ligue_id != 29 and ligue_id != 36:
                    journee = subdiv.get_attribute('innerHTML')   
        db.commit()
        print("commit")
        return 0
    else:
        print("Echec de la connection a la base de données")
        return 1

def crawl_cotes():
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    elif platform.system() == 'Windows':
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    if db:
        cursor = db.cursor(buffered=True)
        team = database_fetchall(cursor, "SELECT TEAM_NAME FROM teams WHERE MATCH_TO_COMING != ''")
        adversaire = database_fetchall(cursor, "SELECT ADVERSAIRE_B FROM teams WHERE MATCH_TO_COMING != ''")
        driver.get("https://www.flashscore.fr/football/")
        element_click_div = wait_till_appear_class(driver, 3, 'filters__group')
        element_click = element_click_div.find_element_by_xpath('div[3]/div')
        driver.execute_script("arguments[0].click();", element_click)
        time.sleep(2)
        cursor.execute("UPDATE teams SET COTE_MATCH = ''")
        for i in range(0, 31):
            if i != 0 :
                try:
                    calendar_click = driver.find_element_by_class_name('calendar__navigation--tomorrow')
                    driver.execute_script("arguments[0].click();", calendar_click)
                    time.sleep(2)
                except:
                    break
            try:
                div = driver.find_element_by_class_name('sportName')  
            except:
                break
            for n in range(2, 300):
                try:
                    subdiv = div.find_element_by_xpath('div[%d]' % (n))
                except:
                    break
                if 'event__round' not in subdiv.get_attribute('class') and 'event__header' not in subdiv.get_attribute('class'):
                    actual_team = subdiv.find_element_by_class_name('event__participant--home')
                    actual_team = re.sub(CLEANR, '', str(actual_team.get_attribute("innerHTML")))
                    if process_data(actual_team) in team:
                        print(actual_team, end='')
                        actual_adversaire = subdiv.find_element_by_class_name('event__participant--away')
                        actual_adversaire = re.sub(CLEANR, '', str(actual_adversaire.get_attribute("innerHTML")))
                        if process_data(actual_adversaire) in adversaire:
                            print(' / ' + actual_adversaire)
                            element_cote1 = subdiv.find_element_by_class_name('event__odd--odd1')
                            try:
                                cote1 = element_cote1.find_element_by_xpath('span')
                                cote1 = re.sub(CLEANR, '', str(cote1.get_attribute("innerHTML")))
                            except:
                                cote1 = ''
                            if cote1 != '':
                                element_cote2 = subdiv.find_element_by_class_name('event__odd--odd3')
                                try:
                                    cote2 = element_cote2.find_element_by_xpath('span')
                                    cote2 = re.sub(CLEANR, '', str(cote2.get_attribute("innerHTML")))
                                except:
                                    cote2 = ''
                                if cote1 != '' and cote2 != '':
                                    cote = str(cote1) + '/' + str(cote2)
                                    cursor.execute("UPDATE teams SET COTE_MATCH = '%s' WHERE TEAM_NAME = '%s' AND ADVERSAIRE_B = '%s'" % (cote, process_data(actual_team), process_data(actual_adversaire)))
                                    print("UPDATE teams SET COTE_MATCH = %s WHERE TEAM_NAME = %s AND ADVERSAIRE_B = %s" % (cote, process_data(actual_team), process_data(actual_adversaire)))
                db.commit()
        db.commit()
        cursor.close()
        db.close()
        driver.quit()
        print("fin de la récupération des cotes")
    else:
        print("Echec de la connection a la base de données")
        return 1


def __main__():
    ligue_name_url = get_data_json("ligues")
    pays_name_url = get_data_json("pays")
    s_db = Db()
    db = connect_to_database(s_db)
    cursor = db.cursor()
    ligues = database_fetchall(cursor, "SELECT ID FROM %s.ligues" % ('football'))
    for i in range(0, len(ligues)):
        crawl_specific_ligue_matchs(pays_name_url[ligues[i] - 1], ligue_name_url[ligues[i] - 1], ligues[i])
    crawl_cotes()  
    

if __name__ == '__main__':
    __main__()