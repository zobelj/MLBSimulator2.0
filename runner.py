import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from lineupAPI import updateLineupsJSON
from matchupsAPI import updateMatchupsJSON
import json

# list of strings containing each team name
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

# print lineups for selected team on selected date
def displayLineups():
    awayListbox.delete(0, tk.END)
    homeListbox.delete(0, tk.END)
    awayPitcherVar.set('')
    homePitcherVar.set('')
    
    lineups_json = json.load(open('data/lineups.json'))
    away_team = cleanTeamName(awayTeamVar.get())
    home_team = cleanTeamName(homeTeamVar.get())
    away_lineup = lineups_json[away_team]
    home_lineup = lineups_json[home_team]

    for i in range(9):
        awayListbox.insert(i+1, ' {}. '.format(i+1) + away_lineup[i])
        homeListbox.insert(i+1, ' {}. '.format(i+1) + home_lineup[i])

    awayPitcherVar.set(' ' + away_lineup[-1])
    homePitcherVar.set(' ' + home_lineup[-1])

def displayMatchups():
    matchups_json = json.load(open('data/matchups.json'))
    matchups_away = list(matchups_json['away'].keys())
    matchups_home = list(matchups_json['away'].values())

    matchupsListbox.delete(0, tk.END)
    for i in range(len(matchups_json['away'])):
        matchupsListbox.insert(i+1, matchups_away[i].title() + ' at ' + matchups_home[i].title())

def selectMatchup():
    away_selected = matchupsListbox.get(matchupsListbox.curselection()).split('at')[0].strip()
    home_selected = matchupsListbox.get(matchupsListbox.curselection()).split('at')[1].strip()
    away_selected_index = [i for i, s in enumerate(teamList) if away_selected in s]
    home_selected_index = [i for i, s in enumerate(teamList) if home_selected in s]
    awayTeamVar.set(teamList[away_selected_index[0]])
    homeTeamVar.set(teamList[home_selected_index[0]])
    displayLineups()

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
    matchupsListbox.delete(0, tk.END)

# center the GUI
def center_window(width, height):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/2)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))


# frame containing update data button and date selection
buttonFrame = tk.Frame(master)
buttonFrame.grid(row=0, column=0, sticky='w', padx=10)

tk.Button(buttonFrame, text='Update Data', relief='groove', overrelief='sunken', command=updateData).grid(row=0, column=0, sticky='nsew')
#tk.Label(buttonFrame, text=' Select date ').grid(row=1, column=1)
cal = DateEntry(buttonFrame, width=12, year=int(today[0]), month=int(today[1]), day=int(today[2]), background='darkblue', forground='white', borderwidth=2)
cal.grid(row=1, column=0)


# frame containing display lineup button and away/home team info
teamsFrame = tk.Frame(master)
teamsFrame.grid(row=1, column=1)
tk.Button(teamsFrame, text="Display Lineups", relief='groove', overrelief='sunken', command=displayLineups).grid(row=0, column=0, sticky='nsw')
tk.Button(teamsFrame, text=" Use Selected ", relief='groove', overrelief='sunken', command=selectMatchup).grid(row=0, column=1, sticky='nsw')

# away team entries
awayFrame = tk.Frame(teamsFrame)
awayFrame.grid(row=1, column=0)
awayTeamVar = tk.StringVar(master)
awayTeamVar.set(teamList[0])
awayPitcherVar = tk.StringVar(master)

tk.Label(awayFrame, text="    Away Team    ", bg='dodger blue').grid(row=1, column=0, padx=1, sticky='nsew')
tk.Label(awayFrame, text="  Away Pitcher  ", bg='dodger blue').grid(row=2, column=0, padx=1, sticky='nsew')
awayTeam = tk.ttk.Combobox(awayFrame, textvariable=awayTeamVar, values=teamList)
awayTeam.grid(row=1, column=1)
awayPitcher = tk.Entry(awayFrame, relief = 'groove', textvariable=awayPitcherVar)
awayPitcher.grid(row=2, column=1, sticky='we')

# home team entries
homeFrame = tk.Frame(teamsFrame)
homeFrame.grid(row=1, column=1)
homeTeamVar = tk.StringVar(master)
homeTeamVar.set(teamList[0])
homePitcherVar = tk.StringVar(master)

tk.Label(homeFrame, text="    Home Team    ", bg='tomato2').grid(row=1, column=2, padx=1, sticky='nsew')
tk.Label(homeFrame, text="   Home Pitcher   ", bg='tomato2').grid(row=2, column=2, padx=1, sticky='nsew')
homeTeam = tk.ttk.Combobox(homeFrame, textvariable=homeTeamVar, values=teamList)
homeTeam.grid(row=1, column=3)
homePitcher = tk.Entry(homeFrame, relief = 'groove', textvariable=homePitcherVar)
homePitcher.grid(row=2, column=3, sticky='we')

# away lineup display
awayListbox = tk.Listbox(awayFrame)
awayListbox.grid(row=3, column=1, sticky='we')
awayListbox.config(height=9)

# home lineup display
homeListbox = tk.Listbox(homeFrame)
homeListbox.grid(row=3, column=3, sticky='we')
homeListbox.config(height=9)


# frame containing day's matchup and display button
matchupsFrame = tk.Frame(master)
matchupsFrame.grid(row=1, column=0, rowspan=2, pady=12, padx=10)
tk.Button(matchupsFrame, text='Display Matchups', relief='groove', overrelief='sunken', command=displayMatchups).grid(row=0, column=0, pady=2, sticky='nsew')
matchupsListbox = tk.Listbox(matchupsFrame)
matchupsListbox.grid(row=1, column=0)
matchupsListbox.config(height=15)


# frame containing quit and clear all button
exitFrame = tk.Frame(master)
exitFrame.grid(row=2, column=1, sticky='e')
tk.Button(exitFrame, text="Clear All", relief='groove', overrelief='sunken', command=clearAll).pack(side='left')
tk.Button(exitFrame, relief='groove', text='  Quit  ', overrelief='sunken', command=master.destroy).pack(side='right')

# center window and run
center_window(750, 450)
updateData()
tk.mainloop()
