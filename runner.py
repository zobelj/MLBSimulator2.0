from ctypes import windll, pointer, wintypes
windll.shcore.SetProcessDpiAwareness(1)
user32 = windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from APIs.lineupAPI import updateLineupsJSON
from APIs.matchupsAPI import updateMatchupsJSON
import json
import webbrowser
from APIs.teamStatsAPI import get2020Data

teamList = ['', 'Arizona Diamondbacks','Atlanta Braves','Baltimore Orioles','Boston Red Sox','Chicago White Sox','Chicago Cubs','Cincinnati Reds','Cleveland Indians','Colorado Rockies','Detroit Tigers','Houston Astros','Kansas City Royals','Los Angeles Angels','Los Angeles Dodgers','Miami Marlins','Milwaukee Brewers','Minnesota Twins','New York Yankees','New York Mets','Oakland Athletics','Philadelphia Phillies','Pittsburgh Pirates','San Diego Padres','San Francisco Giants','Seattle Mariners','St. Louis Cardinals','Tampa Bay Rays','Texas Rangers','Toronto Blue Jays','Washington Nationals']
locations = ['Arizona','Atlanta','Baltimore','Boston','Chicago','Cincinnati','Cleveland','Colorado','Detroit','Houston','KansasCity','LosAngeles','Miami','Milwaukee','Minnesota','NewYork','Oakland','Philadelphia','Pittsburgh','SanDiego','SanFrancisco','Seattle','St.Louis','TampaBay','Texas','Toronto','Washington']

# get today's date
today = str(date.today()).split('-')

# setup stuff
master = tk.Tk()
master.title('MLB Simulator 2.0')

# functions
# update lineups to selected dates
def updateData():
    updateMatchupsJSON(cal.get_date())
    year, month, day = str(cal.get_date()).split('-')
    year = year[2:]
    date =str(month + '/' + day + '/' + year)
    updateLineupsJSON(date)
    displayMatchups()

def updateDataHelper(_):
    updateData()

# print lineups for selected team on selected date
def displayLineups():
    awayListbox.delete(0, tk.END)
    homeListbox.delete(0, tk.END)
    awayPitcherVar.set('')
    homePitcherVar.set('')

    lineups_json = json.load(open('data/lineups.json'))
    away_team = cleanTeamName(awayTeamVar.get())
    home_team = cleanTeamName(homeTeamVar.get())

    try:
        away_lineup = lineups_json[away_team]
        awayPitcherVar.set(' ' + away_lineup[-1])
        for i in range(9):
            awayListbox.insert(i+1, ' ' + away_lineup[i])
    except:
        awayPitcherVar.set('Error loading lineup.')

    try:
        home_lineup = lineups_json[home_team]
        homePitcherVar.set(' ' + home_lineup[-1])
        for i in range(9):
            homeListbox.insert(i+1, ' ' + home_lineup[i])
    except:
        homePitcherVar.set('Error loading lineup.')


# displays the day's matchups in matchups listbox
def displayMatchups():
    matchups_json = json.load(open('data/matchups.json'))
    matchups_away = list(matchups_json['away'].keys())
    matchups_home = list(matchups_json['away'].values())

    matchupsListbox.delete(0, tk.END)
    for i in range(len(matchups_json['away'])):
        matchupsListbox.insert(i+1, ' ' + matchups_away[i].title() + ' at ' + matchups_home[i].title())

# displays lineups for matchup selected from matchups listbox
def selectMatchup(event):
    thisWidget = event.widget
    away_selected, home_selected = thisWidget.get(int(thisWidget.curselection()[0])).replace('D-Backs', 'Diamondbacks').replace("A's", "Athletics").split(' at ')

    away_selected_index = [i for i, s in enumerate(teamList) if away_selected.strip() in s]
    home_selected_index = [i for i, s in enumerate(teamList) if home_selected.strip() in s]


    awayTeamVar.set(teamList[away_selected_index[0]])
    homeTeamVar.set(teamList[home_selected_index[0]])
    displayLineups()

def goToBREF(event):
    thisWidget = event.widget
    name_index = int(thisWidget.curselection()[0])

    name = thisWidget.get(name_index)[1:].strip().lower()
    first, last = name.split(' ')[:2]
    url = 'https://www.baseball-reference.com/players/{}/{}{}01.shtml'.format(last[0], last[:5], first[:2])
    webbrowser.open(url)

def displayTeamOPS():
    away_names = list(awayListbox.get(0,9))
    home_names = list(homeListbox.get(0,9))
    away_selected, home_selected = awayTeam.get(), homeTeam.get()

    hitters_2019 = json.load(open('data/hitters_2019.json'))
    hitters_2020_away = get2020Data(away_selected, away_names)
    hitters_2020_home = get2020Data(home_selected, home_names)

    for i in range(len(away_names)):
        away_names[i] = away_names[i].strip()
        home_names[i] = home_names[i].strip()

    away_OPS_2019 = []
    away_PA_2019 = []
    away_wOPS_2019 = 0

    away_OPS_2020 = []
    away_PA_2020 = []
    away_wOPS_2020 = 0

    home_OPS_2019 = []
    home_PA_2019 = []
    home_wOPS_2019 = 0

    home_OPS_2020 = []
    home_PA_2020 = []
    home_wOPS_2020 = 0

    for name in away_names:
        try:
            away_OPS_2019.append(hitters_2019[name.strip()][1])
        except:
            away_OPS_2019.append(0)
        try:
            away_OPS_2020.append(hitters_2020_away[name.strip()][1])
        except:
            away_OPS_2020.append(0)

        try:
            away_PA_2019.append(hitters_2019[name.strip()][0])
        except:
            away_PA_2019.append(0)
        try:
            away_PA_2020.append(hitters_2020_away[name.strip()][0])
        except:
            away_PA_2020.append(0)

    away_wOPS_2019 = int(sum([away_OPS_2019[i] * away_PA_2019[i] for i in range(len(away_OPS_2019))]) / sum(away_PA_2019))
    away_wOPS_2020 = int(sum([away_OPS_2020[i] * away_PA_2020[i] for i in range(len(away_OPS_2020))]) / sum(away_PA_2020))

    for name in home_names:
        try:
            home_OPS_2019.append(hitters_2019[name.strip()][1])
        except:
            home_OPS_2019.append(0)
        try:
            home_OPS_2020.append(hitters_2020_home[name.strip()][1])
        except:
            home_OPS_2020.append(0)
        try:
            home_PA_2019.append(hitters_2019[name.strip()][0])
        except:
            home_PA_2019.append(0)
        try:
            home_PA_2020.append(hitters_2020_home[name.strip()][0])
        except:
            home_PA_2020.append(0)

    home_wOPS_2019 = int(sum([home_OPS_2019[i] * home_PA_2019[i] for i in range(len(home_OPS_2019))]) / sum(home_PA_2019))
    home_wOPS_2020 = int(sum([home_OPS_2020[i] * home_PA_2020[i] for i in range(len(home_OPS_2020))]) / sum(home_PA_2020))

    print(away_names)
    print((away_wOPS_2019 + away_wOPS_2020) / 2)
    print()
    print(home_names)
    print((home_wOPS_2019 + home_wOPS_2020) / 2)

# remove location from team name
def cleanTeamName(name):
    for location in locations:
        name = name.replace(location, '').replace(' ', '')

    return(name)

def clearAll():
    awayListbox.delete(0, tk.END)
    homeListbox.delete(0, tk.END)
    awayPitcherVar.set('')
    homePitcherVar.set('')
    awayTeamVar.set(teamList[0])
    homeTeamVar.set(teamList[0])

# center the GUI
def center_window():
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width/2)  - (width/4)
    y = (screen_height/3) - (height/4)
    master.geometry('%dx%d+%d+%d' % (width/2.5, height/2.5, x, y))


# frame containing update data button and date selection
buttonFrame = tk.Frame(master)
buttonFrame.grid(row=0, column=0, sticky='w', padx=10)

tk.Button(buttonFrame, text='Update Data', relief='groove', overrelief='sunken', command=updateData).grid(row=0, column=0, sticky='nsew', pady=(4,0))
#tk.Label(buttonFrame, text=' Select date ').grid(row=0, column=0)
cal = DateEntry(buttonFrame, width=12, year=int(today[0]), month=int(today[1]), day=int(today[2]), background='darkblue', forground='white', borderwidth=2)
cal.grid(row=1, column=0)
cal.bind('<<DateEntrySelected>>', updateDataHelper)


# frame containing display lineup button and away/home team info
teamsFrame = tk.Frame(master)
teamsFrame.grid(row=1, column=1)
tk.Button(teamsFrame, text="Display Lineups ", relief='groove', overrelief='sunken', command=displayLineups).grid(row=0, column=0, sticky='nsw', pady=4)
tk.Button(teamsFrame, text = "Display OPS", relief='groove', overrelief='sunken', command=displayTeamOPS).grid(row=0, column=1, sticky='nsw', pady=4)

# away team entries
awayFrame = tk.Frame(teamsFrame)
awayFrame.grid(row=1, column=0)
awayTeamVar = tk.StringVar(master)
awayTeamVar.set(teamList[0])
awayPitcherVar = tk.StringVar(master)

tk.Label(awayFrame, text="     Away Team     ", bg='dodger blue').grid(row=1, column=0, padx=1, sticky='nsew')
tk.Label(awayFrame, text="  Away Pitcher  ", bg='dodger blue').grid(row=2, column=0, padx=1, sticky='nsew')
awayTeam = tk.ttk.Combobox(awayFrame, textvariable=awayTeamVar, values=teamList)
awayTeam.grid(row=1, column=1, padx=4)
awayPitcher = tk.Entry(awayFrame, relief = 'groove', textvariable=awayPitcherVar)
awayPitcher.grid(row=2, column=1, sticky='we', padx=4)

# home team entries
homeFrame = tk.Frame(teamsFrame)
homeFrame.grid(row=1, column=1)
homeTeamVar = tk.StringVar(master)
homeTeamVar.set(teamList[0])
homePitcherVar = tk.StringVar(master)

tk.Label(homeFrame, text="    Home Team    ", bg='tomato2').grid(row=1, column=2, padx=1, sticky='nsew')
tk.Label(homeFrame, text="   Home Pitcher   ", bg='tomato2').grid(row=2, column=2, padx=1, sticky='nsew')
homeTeam = tk.ttk.Combobox(homeFrame, textvariable=homeTeamVar, values=teamList)
homeTeam.grid(row=1, column=3, padx=4)
homePitcher = tk.Entry(homeFrame, relief = 'groove', textvariable=homePitcherVar)
homePitcher.grid(row=2, column=3, sticky='we', padx=4)

# away lineup display
awayListbox = tk.Listbox(awayFrame)
awayListbox.grid(row=3, column=1, sticky='we', padx=4)
awayListbox.config(height=9)
awayListbox.bind('<Double-1>', goToBREF)

# home lineup display
homeListbox = tk.Listbox(homeFrame)
homeListbox.grid(row=3, column=3, sticky='we', padx=4)
homeListbox.config(height=9)
homeListbox.bind('<Double-1>', goToBREF)


# frame containing day's matchup and display button
matchupsFrame = tk.Frame(master)
matchupsFrame.grid(row=1, column=0, rowspan=2, pady=4, padx=10)
#tk.Button(matchupsFrame, text='Display Matchups', relief='groove', overrelief='sunken', command=displayMatchups).grid(row=0, column=0, pady=2, sticky='nsew')
matchupsListbox = tk.Listbox(matchupsFrame)
matchupsListbox.grid(row=2, column=0, sticky='nsew')
matchupsListbox.config(height=15)

matchupsListbox.bind('<Double-1>', selectMatchup)
# frame containing quit and clear all button
exitFrame = tk.Frame(master)
exitFrame.grid(row=2, column=1, sticky='e')
tk.Button(exitFrame, text="Clear All", relief='groove', overrelief='sunken', command=clearAll).pack(side='left')
tk.Button(exitFrame, relief='groove', text='  Quit  ', overrelief='sunken', command=master.destroy).pack(side='right')

# center window and run
center_window()
#updateData('foo')
tk.mainloop()
