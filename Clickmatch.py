import re


def get_date(line1):
    datepatt = re.findall(r'\w+\s\d+\s\w*\s\d*(?=</div>)', line1)
    return " ".join(datepatt)


def get_kickoff(line14):
    kickpatt = re.findall(
        r"<div class=\"kickoff\">Kick Off: <strong class=\"renderKOContainer\" data-kickoff=\"\d*\">(.*?)</strong></div>",
        line14)
    return " ".join(kickpatt)


def get_referee(line2):
    refpatt = re.findall(r'(?<=\"icn whistle-w\"></div>)\w*\s\w*', line2)
    return " ".join(refpatt)


def get_stadium(line3):
    stdpatt = re.findall(r'</div>([\w\s\'\,.]*)', line3)
    return " ".join(stdpatt).strip()


def get_attendance(line4):
    attendancePattern = re.findall(r'[\d,]+', line4)
    return " ".join(attendancePattern).replace(',', '')


def get_teams(line5):
    teampatt = re.findall(r'(?<=long\">)[\w*\s*]*', line5)
    return " ".join(teampatt)


def get_teams2(line51):
    teampatt2 = re.findall(r'<h6>Full-time</h6> <p>Match ends, (.*?)[\s\d]*,\s(.*?)[\s\d]*\.</p>', line51)[0]
    return teampatt2


def get_score(line6):
    scopatt = re.findall(r'[\d-]', line6)
    return " ".join(scopatt)


def get_motm(line7):
    MOTMPattern = " ".join(re.findall(
        r'<h4 class="kotm-player__first-name">(.*?)</h4> <h3 class="kotm-player__second-name">(.*?)</h3>', line7)[0])
    return MOTMPattern


# Goles y assistencias en otros csv
def get_goal(line8, ID_MATCH, tins):
    GoalsRet = []
    goles = re.findall(r"<p>[\w\s]*Goal[!]*\s.*?</p>", line8)[::-1]
    timeeve = re.findall(
        r"<time>([\d+\s]*)'</time>  </div> <div class=\"cardContent\"> <div class=\"innerContent\"> <h6>[\w\s!]*</h6> <p>[\w\s]*Goal",
        line8)
    tiempito = len(timeeve)
    for h in goles:
        # (Own Goal) by (\w* \w*)\,|\.\s(.*)\s\((\w* \w*)\)incluir equipo en el gol
        playergoal = re.findall(r"(Own Goal) by ([\w\-\s]*),\s*(.*?)\.|\.\s(.*)\s\((.*?)\)", h)[0]
        playergoalte = check_owngoal(playergoal, tins)
        playerassist = re.findall(r"Assisted by ([A-Z\w]*\s*[A-Z\w\-]*\s*[A-Z][\w]*)[\w\s]*\.", h)
        tiempito -= 1
        penalty = re.findall(r"\spenalty*", h)
        GoalsRet.append(
            [f'{ID_MATCH}-{tiempito}', ID_MATCH, time_convert(timeeve[tiempito]), "".join(playergoalte[2] + playergoalte[4]),
             "".join(playergoalte[1] + playergoalte[3]).strip(), "".join(playergoalte[0]), " ".join(penalty).strip(),
             " ".join(playerassist)])
    return GoalsRet


def check_owngoal(playq, tims):
    newgoal = []
    if playq[0] == 'Own Goal':
        if playq[2] == tims[0]:
            newgoal.append([playq[0], playq[1], tims[1], "", ""])
        else:
            newgoal.append([playq[0], playq[1], tims[0], "", ""])
    else:
        newgoal.append(["", "", "", playq[3], playq[4]])
    return newgoal[0]


# FOULS in other CSV
def get_fouls(line9, MatchID):
    Fouls = re.findall(
        r"<time>([\d+\s]*)'</time>  </div> <div class=\"cardContent\"> <div class=\"innerContent\"> <h6>[\w\s!]*</h6> <p>[\w\s]*Foul by ([A-Z\w\-\s]*\s[A-Z]\w*)\s\(([A-Z]\w*\s*[A-Z]*\w*)\)",
        line9)
    Fouls_2 = [Time_Eval_foul(i, MatchID) for i in Fouls]
    counter = 0
    for foul in Fouls_2:
        foul.insert(0, f'{MatchID}-F-{counter}')
        counter += 1
    return Fouls_2


def get_yellow_cards(line10):
    YellowCard = re.findall(
        r"<time>([\d+\s]*)'</time>  </div> <div class=\"cardContent\"> <div class=\"innerContent\"> <h6>Yellow Card!</h6> <p>([A-Z\w\-\s]*\s[A-Z]\w*)\s\(([A-Z]\w*\s*[A-Z]*\w*)\)",
        line10)
    return [Time_Eval_foul(i, "Yellow") for i in YellowCard]


def get_red_card(line11):
    Reds = []
    RedCard = re.findall(
        r"<time>([\d+\s]*)'</time>  </div> <div class=\"cardContent\"> <div class=\"innerContent\"> <h6>Red Card!</h6> <p>([A-Z\w\-\s]*\s[A-Z]\w*)\s\(([A-Z]\w*\s*[A-Z]*\w*)\)",
        line11)
    for i in RedCard:
        if "Second yellow card to" in i[1]:
            Reds.append([time_convert(i[0]), i[1].replace("Second yellow card to ", ""), i[2], 'Yellow'])
            Reds.append([time_convert(i[0]), i[1].replace("Second yellow card to ", ""), i[2], 'Red'])
        else:
            Reds.append([time_convert(i[0]), i[1], i[2], 'Red'])
    return Reds


def Time_Eval_foul(line12, type_foul):
    Time_Uni = line12[0].split("+")
    Time_Full = sum([int(x) for x in Time_Uni])
    return [Time_Full, line12[1], line12[2], type_foul]


def time_convert(tiempo):
    TimeA = tiempo.split("+")
    TimeB = sum([int(x) for x in TimeA])
    return TimeB


def all_cards(yellow_fouls, red_fouls, MatchID):
    yellow_fouls.extend(red_fouls)
    counter = 0
    for foul in yellow_fouls:
        foul.insert(0, f'{MatchID}-C-{counter}')
        foul.insert(1, MatchID)
        counter += 1
    return yellow_fouls


def get_substitutions(line13, Match_ID):
    Substitutions = re.findall(
        r"<div\sclass=\"blogCard\ssubstitution\sminorEvent\">\s<div\sclass=\"cardMeta\">\s<div class=\"icon\">\s<div\sclass=\"icn\ssub-n\"></div>\s</div>\s*<time>(.*?)'</time>\s*</div>\s<div\sclass=\"cardContent\">\s<div\sclass=\"innerContent\">\s<h6>Substitution</h6>\s<p>Substitution,\s(.*?)\.\s(.*?)\sreplaces\s(.*?)\.",
        line13)
    SubstitutionsRet = []
    counter = 0
    for Sub in Substitutions:
        SubstitutionsRet.append([f'{Match_ID}-S-{counter}', Match_ID,time_convert(Sub[0]), Sub[1], Sub[2], Sub[3]])
        counter += 1
    return SubstitutionsRet
