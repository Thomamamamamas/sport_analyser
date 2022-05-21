import re


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from database_utils import *
from crawler_utils_1 import get_os_chromedriver_path, chromedriver_path, get_who_goal_first, get_match_id, process_data, get_next_match_data, get_correct_page, match_already_exist, show_all_match



def crawl_specific_ligue_matchs(pays, ligue_name, ligue_id):
    print("Récupère les dernieres données de :")
    print(pays)
    print(ligue_name)
    print(ligue_id)
    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chromedriver_path(CHROME_DRIVER_PATH), options=chrome_options)
    subdriver = webdriver.Chrome(chromedriver_path(CHROME_DRIVER_PATH), options=chrome_options)
    caldriver = webdriver.Chrome(chromedriver_path(CHROME_DRIVER_PATH), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    year1 = 2021
    year2 = 2022

    get_next_match_data(caldriver, db, pays, ligue_name, ligue_id)
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
                    if ligue_id == 42 or ligue_id == 35:
                        journee = subdiv.find_element_by_class_name('event__time')
                        journee  = re.sub(CLEANR, '', str(journee.get_attribute("innerHTML")))
                    if 'event__participant--home' in team_name.get_attribute('class'):
                        domicile = 1
                    else:
                        domicile = 0
                    team_name = re.sub(CLEANR, '', str(team_name.get_attribute("innerHTML")))
                    team_score = subdiv.find_elements_by_class_name('event__score')[m]
                    team_score = int(re.sub(CLEANR, '', str(team_score.get_attribute("innerHTML"))))
                    try:
                        team_midterm_score = subdiv.find_elements_by_class_name('event__part--1')[m]
                        team_midterm_score = int(re.sub(CLEANR, '', str(team_midterm_score.get_attribute("innerHTML"))).replace('(', '').replace(')', ''))
                    except:
                        team_midterm_score = 0
                    team_id =  database_fetchone(cursor, "SELECT ID FROM teams WHERE TEAM_NAME = '%s'" % (process_data(team_name)))
                    if match_already_exist(cursor, process_data(team_1_name), process_data(team_2_name), process_data(journee), year1, year2) == 1:
                        print("Match dèjà enregistré")
                        return 0
                    match_url = 'https://www.flashscore.fr/match/' + subdiv.get_attribute('id').split('_', 2)[2] + '/#/resume-du-match/resume-du-match'
                    if domicile == 1:
                        goal_first = get_who_goal_first(subdriver, match_url, subdiv, team_score, team_midterm_score, m)
                    else:
                        goal_first = 0
                    try:
                        cursor.execute("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE, TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, goal_first))
                        print("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, goal_first))
                    except:
                        print("N'insère rien")
                        continue
            else:
                if ligue_id != 42 and ligue_id != 35:
                    journee = subdiv.get_attribute('innerHTML')   
        db.commit()
        print("commit")
        return 1
    else:
        print("Echec de la connection a la base de données")
        return 0