import time
import re
import json
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from database_utils import *
from crawler_utils_1 import get_os_chromedriver_path, resource_path, get_who_goal_first, get_next_match_data, get_match_id, process_data, get_correct_page, show_all_match

def get_data_json(data):
    config_text = ''
    with open(resource_path('config/config.json'), 'r') as config_json:
        for line in config_json:
            config_text = config_text + line
        config_json.close()
    json_dict = json.loads(config_text)
    return json_dict[data]


def crawl_all_ligues(pays, ligues):
    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    cursor = db.cursor(buffered=True)

    drop_table(db, s_db, 'matchs')
    drop_table(db, s_db, 'teams')
    drop_table(db, s_db, 'ligues')
    configure_table(db, s_db, 'ligues', get_data_json('ligues_column'))
    for i in range(0, len(pays)):
        try:
            print('crawl la ligue : %s' % (pays[i]))
            url = 'https://www.flashscore.fr/football/%s/%s/' % (pays[i], ligues[i])
            driver.get(url)
            time.sleep(2)
            ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
            ligue_logo = driver.find_element_by_class_name('heading__logo').get_attribute('style').split('"', 2)[1].replace("'", '')
            ligue_logo = 'flashscore.fr' + ligue_logo
            cursor.execute("INSERT INTO ligues(LIGUE_NAME, LIGUE_LOGO, LIGUE_PAYS) VALUES ('%s', '%s', '%s')" % (process_data(ligue_name), process_data(ligue_logo), process_data(pays[i])))
            time.sleep(1)
        except:
            continue
    db.commit()
    cursor.close()
    db.close()
    driver.quit()

def crawl_all_teams(years_limit, pays, ligues):
    CHROME_DRIVER_PATH = get_os_chromedriver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    cursor = db.cursor(buffered=True)
    team_logo = ''
    team_name = ''
    ligue_name = ''
    ligue_id = 0

    drop_table(db, s_db, 'matchs')
    configure_table(db, s_db, 'teams', get_data_json('teams_column'))
    truncate_table(db, s_db, 'teams')
    for i in range(0, len(pays)):
        year1 = 2021
        year2 = 2022
        ligue_name = get_correct_page(driver, pays[i], ligues[i], year1, year2, 0)
        for j in range(0, years_limit):
            print('crawl les équipe de la ligue : %s année %s-%s' % (pays[i], year1, year2))
            if j > 0:
                get_correct_page(driver, pays[i], ligues[i], year1, year2, j)
            show_all_match(driver)
            get_ligue_teams(driver, db, cursor, ligue_name, pays[i])
            year1 = year1 - 1
            year2 = year2 - 1
            time.sleep(2)
    db.commit()
    cursor.close()
    db.close()
    driver.quit()

def get_ligue_teams(driver, db, cursor, ligue_name, pays):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    for n in range(2, 20):
        try:
            div = driver.find_elements_by_class_name('event__match')[n]
        except:
            break
        if 'event__round' not in div.get_attribute('class') and 'event__header' not in div.get_attribute('class'):
            for m in range(0, 2):
                team_logo = div.find_elements_by_class_name('event__logo')[m].get_attribute('src').replace("'", '')
                team_name = div.find_elements_by_class_name('event__participant')[m]
                team_name = re.sub(CLEANR, '', str(team_name.get_attribute("innerHTML")))
                ligue_id = database_fetchone(cursor, "SELECT ID FROM ligues WHERE LIGUE_NAME = '%s' AND LIGUE_PAYS = '%s'" % (process_data(ligue_name), process_data(pays)))
                tmp = database_fetchone(cursor, "SELECT TEAM_NAME FROM teams WHERE TEAM_NAME = '%s' AND LIGUE_ID = %d" % (process_data(team_name), ligue_id))
                print(team_name)
                if tmp == 0:
                    print(ligue_id)
                    print(team_name)
                    cursor.execute("INSERT INTO teams(TEAM_NAME, LIGUE_ID, TEAM_LOGO) VALUES ('%s', %d, '%s')" % (process_data(team_name), ligue_id, process_data(team_logo)))
                    print("INSERT INTO teams(TEAM_NAME, LIGUE_ID, TEAM_LOGO) VALUES ('%s', %d, '%s')" % (process_data(team_name), ligue_id, process_data(team_logo)))
                    db.commit()
    db.commit()
    print("commit")
    return


def crawl_all_ligues_matchs(years_limit):
    pays = get_data_json("pays")
    ligues = get_data_json("ligues")
    config = ConfigParser()
    config.read("example.ini")
    CHROME_DRIVER_PATH = config.get("chromedriver_mac", "path")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    subdriver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
    s_db = Db()
    db = connect_to_database(s_db)
    cursor = db.cursor(buffered=True)

    drop_table(db, s_db, 'matchs')
    configure_table(db, s_db, 'matchs', get_data_json('matchs_column'))
    ligues_id = database_fetchall(cursor, "SELECT ID FROM ligues")
    for i in range(0, len(ligues_id)):
        crawl_ligue(driver, subdriver, db, s_db, pays[i], ligues[i], ligues_id[i], years_limit)
        db.commit()
        cursor.close()
        db.close()
        db = connect_to_database(s_db)
    driver.quit()
    subdriver.quit()

def crawl_ligue(driver, subdriver, db, s_db, pays, ligues, ligue_id, years_limit):
    year1 = 2021
    year2 = 2022
    for j in range(0, years_limit):
        ligue_name = get_correct_page(driver, pays, ligues, year1, year2, j)
        show_all_match(driver)
        crawl_ligue_matchs(driver, subdriver, s_db, db, ligue_id, year1, year2)
        year1 = year1 - 1
        year2 = year2 - 1
    

def crawl_ligue_matchs(driver, subdriver, s_db, db, ligue_id, year1, year2):
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
                try:
                    match_id = get_match_id(cursor)
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
                        team_score = int(re.sub(CLEANR, '', str(team_score.get_attribute("innerHTML"))))
                        try:
                            team_midterm_score = subdiv.find_elements_by_class_name('event__part--1')[m]
                            team_midterm_score = int(re.sub(CLEANR, '', str(team_midterm_score.get_attribute("innerHTML"))).replace('(', '').replace(')', ''))
                        except:
                            team_midterm_score = 0
                        team_id =  database_fetchone(cursor, "SELECT ID FROM teams WHERE TEAM_NAME = '%s'" % (process_data(team_name)))
                        match_url = 'https://www.flashscore.fr/match/' + subdiv.get_attribute('id').split('_', 2)[2] + '/#/resume-du-match/resume-du-match'
                        t_goal_first = get_who_goal_first(subdriver, match_url, subdiv, team_score, team_midterm_score, m)
                        cursor.execute("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE, TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, t_goal_first))
                        print("INSERT INTO matchs(ID, LIGUE_ID, YEAR1, YEAR2, JOURNEE TEAM_ID, TEAM_NAME, GOAL, GOAL_MIDTERM, DOMICILE, GOAL_FIRST) VALUES (%d, %d , %d, %d, '%s', %d, '%s', %d, %d, %d, %d)" % (match_id, ligue_id, year1, year2, process_data(journee), team_id, process_data(team_name), team_score, team_midterm_score, domicile, t_goal_first))
                except:
                    print("ne peux pas ajouter le resultat")
            else:
                if ligue_id != 42 and ligue_id != 18 and ligue_id != 35 and ligue_id != 26 and ligue_id != 27 and ligue_id != 13 and ligue_id != 25 and ligue_id != 29 and ligue_id != 36:
                    journee = subdiv.get_attribute('innerHTML')   
        db.commit()
        print("commit")
    else:
        print("Echec de la connection a la base de données")


def crawl_all_ligue_next_match(db):
    if db:
        pays = get_data_json("pays")
        ligue_name = get_data_json("ligues")
        config = ConfigParser()
        config.read("example.ini")
        CHROME_DRIVER_PATH = config.get("chromedriver_mac", "path")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        caldriver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH), options=chrome_options)
        for i in range(0, len(pays)):
            get_next_match_data(caldriver, db, pays[i], ligue_name[i])

def __main__():
    s_db = Db()
    db = connect_to_database(s_db)
    pays = 'finlande'
    ligues = 'veikkausliiga'
    ligue_id = 18
    years_limit = 5
    config = ConfigParser()
    config.read("example.ini")
    CHROME_DRIVER_PATH = config.get("chromedriver_mac", "path")
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))
    subdriver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))
    crawl_ligue(driver, subdriver, db, s_db, pays, ligues, ligue_id, years_limit)

if __name__ == '__main__':
    __main__()