import json
from matplotlib.pyplot import subplots_adjust
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from database_utils import *

def get_data_json(data):
    config_text = ''
    with open('config.json', 'r') as config_json:
        for line in config_json:
            config_text = config_text + line
        config_json.close()
    json_dict = json.loads(config_text)
    return json_dict[data]

def process_data(data):
    replace_values = ["'", '"', "'"]
    for i in range(0, len(replace_values)):
        data = data.replace(replace_values[i], '')
    return data

def wait_till_appear_class(driver, delay, path):
    try:
        res = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, path)))
    except TimeoutException:
            res = None
    return res

def get_correct_page(driver, pays, ligues, year1, year2, j):
    ligue_name = ''

    time.sleep(2)
    if j == 0:
        try:
            url = 'https://www.flashscore.fr/football/%s/%s/' % (pays, ligues)
            driver.get(url)
            ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
        except:
            url = 'https://www.flashscore.fr/football/%s/%s-%d-%d/' % (pays, ligues, year1, year2)
            driver.get(url)
            ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
    else:
        try:
            url = 'https://www.flashscore.fr/football/%s/%s-%d-%d/' % (pays, ligues, year1, year2)
            driver.get(url)
            ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
        except:
            try:
                url = 'https://www.flashscore.fr/football/%s/%s-%d' % (pays, ligues, year2)
                driver.get(url)
                ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
            except:
                url = 'https://www.flashscore.fr/football/%s/%s' % (pays, ligues)
                driver.get(url)
                ligue_name = driver.find_element_by_class_name('heading__name').get_attribute('innerHTML').replace("'", '')
    return ligue_name


def get_next_match_data(driver, db, pays, ligue_name):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    driver.get('https://www.flashscore.fr/football/%s/%s/calendrier/' % (pays, ligue_name))
    time.sleep(1)
    show_all_match(driver)
    if db:
        cursor = db.cursor(buffered=True)
        try:
            div = driver.find_element_by_class_name('sportName')
        except:
            return
        for n in range(2, 100):
            try:
                subdiv = div.find_element_by_xpath('div[%d]' % (n))
            except:
                break
            if 'event__round' not in subdiv.get_attribute('class') and 'event__header' not in subdiv.get_attribute('class'):
                team_1_name = subdiv.find_elements_by_class_name('event__participant')[0]
                team_1_name = re.sub(CLEANR, '', str(team_1_name.get_attribute("innerHTML")))
                team_2_name = subdiv.find_elements_by_class_name('event__participant')[1]
                team_2_name = re.sub(CLEANR, '', str(team_2_name.get_attribute("innerHTML")))
                match_time = subdiv.find_element_by_class_name('event__time')
                match_time = re.sub(CLEANR, '', str(match_time.get_attribute("innerHTML")))
                coming_match_time = database_fetchone(cursor, "SELECT MATCH_TO_COMING FROM teams WHERE TEAM_NAME = '%s'" % (process_data(team_1_name)))
                if coming_match_time != match_time:
                    print(team_1_name)
                    print(team_2_name)
                    cursor.execute("UPDATE teams SET MATCH_TO_COMING = '%s' WHERE TEAM_NAME = '%s'" % (match_time, process_data(team_1_name)))
                    print("UPDATE teams SET MATCH_TO_COMING = '%s' WHERE TEAM_NAME = '%s'" % (match_time, process_data(team_1_name)))
                    cursor.execute("UPDATE teams SET MATCH_TO_COMING = '%s' WHERE TEAM_NAME = '%s'" % (match_time, process_data(team_2_name)))
                    print("UPDATE teams SET MATCH_TO_COMING = '%s' WHERE TEAM_NAME = '%s'" % (match_time, process_data(team_2_name)))      
                else:
                    break
                db.commit()
                print("commit")
    else:
        print("Echec de la connection a la base de données")

def match_already_exist(cursor, team_1_name, team_2_name, journee):
    team1_matchs_id = database_fetchall(cursor, "SELECT ID FROM matchs WHERE TEAM_NAME = '%s' AND JOURNEE = '%s'" % (team_1_name, journee))
    team2_matchs_id = database_fetchall(cursor, "SELECT ID FROM matchs WHERE TEAM_NAME = '%s' AND JOURNEE = '%s'" % (team_2_name, journee))
    for i in range(0, len(team1_matchs_id)):
        for j in range(0, len(team2_matchs_id)):
            if team1_matchs_id[i] == team2_matchs_id[j]:
                return 1
    return 0


def show_all_match(driver):
    for i in range(0, 5):
        try:
            element_click = driver.find_element_by_class_name('event__more')
            driver.execute_script("arguments[0].click();", element_click)
            print('click')
            time.sleep(1)
        except:
            break

def get_match_id(cursor):
    data = 0

    cursor.execute("SELECT ID FROM matchs ORDER BY ID DESC LIMIT 1")
    try:
        data = cursor.fetchone()[0] + 1
        if data == None:
            data = 0
    except:
        data = 0
    return data


def get_detail_goal_first(driver, match_url):
    res = 0

    driver.get(match_url)
    time.sleep(1)
    div = wait_till_appear_class(driver, 5, 'smv__verticalSections')
    if div == None:
        return 0
    for i in range(1, 20):
        try:
            subdiv = div.find_element_by_xpath('div[%d]' % (i))
            try:
                if 'smv__participantRow' in subdiv.get_attribute('class'):
                    if subdiv.find_element_by_xpath('div/div[2]/div[1]').get_attribute('class') == 'smv__incidentAwayScore':
                        res = 0
                        break
                    elif subdiv.find_element_by_xpath('div/div[2]/div[1]').get_attribute('class') == 'smv__incidentHomeScore':
                        res = 1
                        break
                    elif subdiv.find_element_by_xpath('div/div[2]/div[2]').get_attribute('class') == 'smv__incidentAwayScore':
                        res = 0
                        break
                    elif subdiv.find_element_by_xpath('div/div[2]/div[2]').get_attribute('class') == 'smv__incidentHomeScore':
                        res = 1
                        break
                    elif subdiv.find_element_by_xpath('div[2]/div/div[2]/div').get_attribute('class') == 'smv__incidentAwayScore':
                        res = 0
                        break
                    elif subdiv.find_element_by_xpath('div[2]/div/div[2]/div]').get_attribute('class') == 'smv__incidentHomeScore':
                        res = 1
                        break     
            except:
                continue
        except:
            break
    return res

def get_who_goal_first(driver, match_url, subdiv, team1_score, team1_midterm_score, m):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    if m == 0:
        team2_score = subdiv.find_elements_by_class_name('event__score')[1]
        team2_score = int(re.sub(CLEANR, '', str(team2_score.get_attribute("innerHTML"))))
        try:
            team2_midterm_score = subdiv.find_elements_by_class_name('event__part--1')[1]
            team2_midterm_score = int(re.sub(CLEANR, '', str(team2_midterm_score.get_attribute("innerHTML"))).replace('(', '').replace(')', ''))
        except:
            team2_midterm_score = 0
        
    else:
        team2_score = subdiv.find_elements_by_class_name('event__score')[0]
        team2_score = int(re.sub(CLEANR, '', str(team2_score.get_attribute("innerHTML"))))
        try:
            team2_midterm_score = subdiv.find_elements_by_class_name('event__part--1')[0]
            team2_midterm_score = int(re.sub(CLEANR, '', str(team2_midterm_score.get_attribute("innerHTML"))).replace('(', '').replace(')', ''))
        except:
            team1_midterm_score = 0
    if team2_midterm_score == 0 and team1_midterm_score != 0:
        return 1
    elif team2_midterm_score != 0 and team1_midterm_score != 0:
        return get_detail_goal_first(driver, match_url)
    elif team2_midterm_score == 0 and team1_midterm_score == 0:
        if team2_score == 0 and team1_score != 0:
            return 1
        elif team2_score != 0 and team1_score != 0:
            return get_detail_goal_first(driver, match_url)
    return 0


def crawl_all_ligues(pays, ligues):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
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