from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import Clickmatch as CMTCH
import pandas as pd


# Creation of CSVMatches
ColumnsMatch = ['Match', 'date', 'referee', 'stadium', 'Attendance', 'HOME', 'Fulltime_Score', 'Visit',
                'Halftime_score',
                'Kickoff', 'MOTM']
DF_Match_ORIGIN = pd.DataFrame(columns=ColumnsMatch)
DF_Match_ORIGIN.to_csv('MATCHES.csv', index=False, header=True)

# Creation of CSVGoals
ColumnsGoals = ['ID_Goal', 'ID_Match', 'Time', 'Team', 'Player', 'Own_Goal', 'Penalty', 'Assistant']
DF_GOAL_ORIGIN = pd.DataFrame(columns=ColumnsGoals)
DF_GOAL_ORIGIN.to_csv('GOALS.csv', index=False, header=True)

# Creation of CSVFouls
ColumnsFouls = ['ID_Foul', 'Time', 'Player', 'Team', 'ID_Match']
DF_FOUL_ORIGIN = pd.DataFrame(columns=ColumnsFouls)
DF_FOUL_ORIGIN.to_csv('FOULS.csv', index=False, header=True)

# Creation of CSVCards
ColumnsCards = ['ID_Foul', 'ID_Match', 'Time', 'Player', 'Team', 'Type']
DF_CARDS_ORIGIN = pd.DataFrame(columns=ColumnsCards)
DF_CARDS_ORIGIN.to_csv('CARDS.csv', index=False, header=True)

# Creation of CSVSubstitutions
ColumnsSubs = ['ID_Sub', 'ID_Match', 'Time', 'Team', 'In_player', 'Out_player']
DF_SUBS_ORIGIN = pd.DataFrame(columns=ColumnsSubs)
DF_SUBS_ORIGIN.to_csv('SUBS.csv', index=False, header=True)

with open('links.txt', 'r', encoding='utf-8') as links:
    for i in links:
        DataMatch = []
        DataGoal = []
        DataFoul = []
        DataCards = []
        DataSubs = []
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        driver.get(f'https://{i.rstrip()}')
        time.sleep(1)
        cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body[@class='_3UeHq9yHsrBMeynzByHRY0']/div[@class='tcf-cmp "
                                        "_1Qu7MokjMuBXLOM2oKVLhZ _3_H6MsAd1grAO7T3v2WdhQ']/div["
                                        "@class='_2Mguj83Bz7C9Eq14DJizIM']/div["
                                        "@class='_90RzEeyM6H7IvIh291DTv']/div["
                                        "@class='_1QkG3L-zAijqYlFASTvCtT']/div["
                                        "@class='_24Il51SkQ29P1pCkJOUO-7']/button[@class='_2hTJ5th4dIYlveipSEMYHH "
                                        "BfdVlAo_cgSVjDUegen0F js-accept-all-close']")))
        driver.execute_script("arguments[0].click();", cookies)
        time.sleep(1)

        pgdown = driver.find_element(By.XPATH, "/html/body/footer[@class='mainFooter']/div["
                                               "@class='footerCorporate']/div[@class='wrapper col-12']/ul/li[4]/a")

        pgdown.send_keys(Keys.END)
        pgdown.send_keys(Keys.PAGE_UP)
        pgdown.send_keys(Keys.END)
        time.sleep(1)
        pgsour = driver.page_source.split('\n')

        Match_ID = (i[28:].strip())
        DataMatch.append(Match_ID)
        counter1 = 0
        for j in pgsour:
            if 'matchDate renderMatchDateContainer' in j:
                DataMatch.append(CMTCH.get_date(j))
            elif 'icn whistle-w' in j:
                DataMatch.append(CMTCH.get_referee(j))
            elif 'icn stadium-w' in j:
                DataMatch.append(CMTCH.get_stadium(j))
            elif 'attendance hide-m' in j:
                DataMatch.append(CMTCH.get_attendance(j))
            elif '<div class="kickoff">Kick Off: <strong class="renderKOContainer"' in j:
                DataMatch.append(CMTCH.get_kickoff(j))
            elif '<span class="long">' in j:
                if 'Half Time' not in j:
                    DataMatch.append(CMTCH.get_teams(j))
                else:
                    counter1 += 1
            elif counter1 == 1:
                DataMatch.append(CMTCH.get_score(j))
                counter1 = 0
            elif 'score fullTime' in j:
                DataMatch.append(CMTCH.get_score(j))
            elif '<div class="js-content">' in j:
                try:
                    DataMatch.append(CMTCH.get_motm(j))
                except:
                    DataMatch.append("")
            elif 'commentaryContainer' in j:

                # Adds info to Goals
                Teams2 = CMTCH.get_teams2(j)
                DataGoal.append(CMTCH.get_goal(j, Match_ID, Teams2))
                DFGoal = pd.DataFrame(DataGoal[0], columns=ColumnsGoals)
                DFGoal.to_csv('GOALS.csv', index=False, header=False, mode='a')

                # Adds info to Cards
                DataCards.append(
                    CMTCH.all_cards(CMTCH.get_yellow_cards(j), CMTCH.get_red_card(j), Match_ID))
                DfCards = pd.DataFrame(DataCards[0], columns=ColumnsCards)
                DfCards.to_csv('CARDS.csv', index=False, header=False, mode='a')

                # Adds info to Fouls
                DataFoul.append((CMTCH.get_fouls(j, Match_ID)))
                DfFouls = pd.DataFrame(DataFoul[0], columns=ColumnsFouls)
                DfFouls.to_csv('FOULS.csv', index=False, header=False, mode='a')

                # Adds info to Subs
                DataSubs.append((CMTCH.get_substitutions(j, Match_ID)))
                DfSubs = pd.DataFrame(DataSubs[0], columns=ColumnsSubs)
                DfSubs.to_csv('SUBS.csv', index=False, header=False, mode='a')

        # Adds info to CSV-MATCHES
        try:
            TemporaryDF = pd.DataFrame([DataMatch], columns=ColumnsMatch)
            TemporaryDF.to_csv('MATCHES.csv', index=False, header=False, mode='a')
        except:
            DataMatch.insert(4, '')
            TemporaryDF = pd.DataFrame([DataMatch], columns=ColumnsMatch)
            TemporaryDF.to_csv('MATCHES.csv', index=False, header=False, mode='a')
