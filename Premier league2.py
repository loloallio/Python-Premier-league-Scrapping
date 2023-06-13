import DataFunction as DataFunc
from save_thread_result import ThreadWithResult
import pandas as pd

# Creation of CSVMatches
ColumnsMatch = ['Match', 'date', 'referee', 'stadium', 'Attendance', 'HOME', 'Fulltime_Score', 'AWAY',
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

thread1 = ThreadWithResult(
    target=DataFunc.data_creation,
    args=('links1',))

thread2 = ThreadWithResult(
    target=DataFunc.data_creation,
    args=('links2',))

thread3 = ThreadWithResult(
    target=DataFunc.data_creation,
    args=('links3',))

thread4 = ThreadWithResult(
    target=DataFunc.data_creation,
    args=('links4',))

thread5 = ThreadWithResult(
    target=DataFunc.data_creation,
    args=('links5',))

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()

ResultsLinks = [thread1.result, thread2.result, thread3.result, thread4.result, thread5.result]

# data into csv

for Match in ResultsLinks:
    # Goals
    DF_GOLES = pd.DataFrame(Match[0], columns=ColumnsGoals)
    DF_GOLES.to_csv('GOALS.csv', index=False, header=False, mode='a')

    # CARDS
    DF_TARJETAS = pd.DataFrame(Match[1], columns=ColumnsCards)
    DF_TARJETAS.to_csv('CARDS.csv', index=False, header=False, mode='a')

    # FOULS
    DF_FALTAS = pd.DataFrame(Match[2], columns=ColumnsFouls)
    DF_FALTAS.to_csv('FOULS.csv', index=False, header=False, mode='a')

    # SUBS
    DF_SUSTITUCIONES = pd.DataFrame(Match[3], columns=ColumnsSubs)
    DF_SUSTITUCIONES.to_csv('SUBS.csv', index=False, header=False, mode='a')

    # MATCH
    DF_PARTIDO = pd.DataFrame(Match[4], columns=ColumnsMatch)
    DF_PARTIDO.to_csv('MATCHES.csv', index=False, header=False, mode='a')
