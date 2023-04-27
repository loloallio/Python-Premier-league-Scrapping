# Python-Premier League Web-Scrapping
> A python web-scrapping projects wich uses the pandas, regex, time, selenium and webdriver libraries to create five differents datasets

## Table of Contents
* [General Info](#general-information)
* [Python libraries](#Python-libraries)
* [Data Sets](#Data-Sets)
* [Usage](#usage)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)


## General Information
- The project is based on the official premier league website "www.premierleague.com". 
- First, it gathers every link from its results section and finally iterates every link extracting the required information.
- 5 different data sets are created in a csv format. Matches, Goals, Fouls, Cards and Subs. 


## Python libraries
- Re (Regex)
- Pandas
- Selenium (By, Keys, Service, WebDriverWait, expected_conditions)
- Time
- Web Driver (ChromeDriverManager)


## Data Sets
- All data sets are related through the Match_ID
- Matches (Match, date, referee, stadium, Attendance, HOME, Fulltime_Score, Visit, Halftime_score, Kickoff, MOTM)
- Goals (ID_Goal, ID_Match, Time, Team, Player, Own_Goal, Penalty, Assistant)
- Fouls (ID_Foul, Time, Player, Team, ID_Match)
- Cards (ID_Foul, ID_Match, Time, Player, Team, Type)
- Subs (ID_Sub, ID_Match, Time, Team, In_player, Out_player)


## Usage
First, run the "Premier League.py" to gather all the links.
Finally, run the "Premier League2.py" to create the data sets


## Room for Improvement
I believe the scrapping can be done faster by finding a way to omit the usage of the time.sleep() method in order to wait for the loading stages of the web page.



## Contact
Created by Lorenzo Allio. I'm a Data science university student looking for its first data scientist jr position. Feel free to contact me www.linkedin.com/in/lorenzo-allio/

