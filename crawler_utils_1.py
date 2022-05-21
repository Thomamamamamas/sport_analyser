import time
import re
import os
import sys
import platform
from configparser import ConfigParser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from database_utils import *

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

def get_os_chromedriver_path():
    config = ConfigParser()
    config.read("example.ini")
    if platform.system() == 'Darwin':
        return config.get("chromedriver_mac", "path")
    elif platform.system() == 'Windows':
        return config.get("chromedriver_windows", "path")

def chromedriver_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

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
    teams_name = []
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
                if team_1_name in teams_name or team_2_name in teams_name:
                    print("Date du prochain match deja enregistrer")
                    return
                teams_name.append(team_1_name)
                teams_name.append(team_2_name)
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
                    print("Date du prochain match deja enregistrer")
                    break
                db.commit()
                print("commit")
    else:
        print("Echec de la connection a la base de données")

def match_already_exist(cursor, team_1_name, team_2_name, journee, year1, year2):
    team1_matchs_id = database_fetchall(cursor, "SELECT ID FROM matchs WHERE TEAM_NAME = '%s' AND JOURNEE = '%s' AND YEAR1 = %d AND YEAR2 = %d" % (team_1_name, journee, year1, year2))
    team2_matchs_id = database_fetchall(cursor, "SELECT ID FROM matchs WHERE TEAM_NAME = '%s' AND JOURNEE = '%s' AND YEAR1 = %d AND YEAR2 = %d" % (team_2_name, journee, year1, year2))
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