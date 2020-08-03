import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from lineupAPI import updateJSON
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
def updateLineups():
    year, month, day = str(cal.get_date()).split('-')
    year = year[2:]
    date =str(month + '/' + day + '/' + year)
    updateJSON(date)

# print lineups for selected team on selected date
def displayLineups():
    updateLineups()
    lineups_json = json.load(open('data/lineups.json'))
    away_team = cleanTeamName(awayTeamVar.get())
    home_team = cleanTeamName(homeTeamVar.get())
    away_lineup = lineups_json[away_team]
    home_lineup = lineups_json[home_team]

    awayListBox.delete(0, tk.END)
    homeListBox.delete(0, tk.END)

    for i in range(9):
        awayListBox.insert(i+1, ' {}. '.format(i+1) + away_lineup[i])
        homeListBox.insert(i+1, ' {}. '.format(i+1) + home_lineup[i])

    awayPitcherVar.set(away_lineup[-1])
    homePitcherVar.set(home_lineup[-1])

# center the GUI
def center_window(width, height):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/2)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))

# remove location from team name
def cleanTeamName(name):
    for location in locations:
        name = name.replace(location, '').replace(' ', '')

    return(name)

def clearAll():
    awayListBox.delete(0, tk.END)
    homeListBox.delete(0, tk.END)
    awayPitcherVar.set('')
    homePitcherVar.set('')
    awayTeamVar.set(teamList[0])
    homeTeamVar.set(teamList[0])

# date selection
tk.Label(text=' Select date ').grid(row=0, column=0)
cal = DateEntry(master, width=12, year=int(today[0]), month=int(today[1]), day=int(today[2]), background='darkblue', forground='white', borderwidth=2)
cal.grid(row=0, column=1)

# display lineups of selected team for selected date
tk.Button(master, text="Display Lineups", relief='groove', overrelief='sunken', command=displayLineups).grid(row=2, column=0, sticky='nsew')

# clears all entry boxes
tk.Button(master, text="Clear All", relief='groove', overrelief='sunken', command=clearAll).grid(row=6, column=4, sticky='nsew')

# away team entries
awayTeamVar = tk.StringVar(master)
awayTeamVar.set(teamList[0])
awayPitcherVar = tk.StringVar(master)

tk.Label(master, text="  Away Team  ", bg='dodger blue').grid(row=3, column=0, padx=6, sticky='nsew')
tk.Label(master, text=" Away Pitcher ", bg='dodger blue').grid(row=4, column=0, padx=6, sticky='nsew')
cAwayTeam = tk.ttk.Combobox(master, textvariable=awayTeamVar, values=teamList)
cAwayTeam.grid(row=3, column=1)
cAwayPitcher = tk.Entry(master, relief = 'groove', textvariable=awayPitcherVar)
cAwayPitcher.grid(row=4, column=1, sticky='we')

# home team entries
homeTeamVar = tk.StringVar(master)
homeTeamVar.set(teamList[0])
homePitcherVar = tk.StringVar(master)

tk.Label(master, text="  Home Team  ", bg='tomato2').grid(row=3, column=2, padx=6, sticky='nsew')
tk.Label(master, text=" Home Pitcher ", bg='tomato2').grid(row=4, column=2, padx=6, sticky='nsew')
cHomeTeam = tk.ttk.Combobox(master, textvariable=homeTeamVar, values=teamList)
cHomeTeam.grid(row=3, column=3)
cHomePitcher = tk.Entry(master, relief = 'groove', textvariable=homePitcherVar)
cHomePitcher.grid(row=4, column=3, sticky='we')

# away lineup display
awayListBox = tk.Listbox(master)
awayListBox.grid(row=5, column=1, sticky='we')
awayListBox.config(height=9)

# home lineup display
homeListBox = tk.Listbox(master)
homeListBox.grid(row=5, column=2, sticky='we')
homeListBox.config(height=9)

'''
tk.Label(text='Custom Lineups', padx=3).grid(row=3, column=4)
tk.Checkbutton(master, onvalue=1, offvalue=0).grid(row=3, column=5)
'''
# quit button
quitB = tk.Button(master, relief='groove', text='  Quit  ', overrelief='sunken', command=master.destroy)
quitB.grid(row=6, column=5, sticky='nsew')

# center window and run
center_window(650, 500)
tk.mainloop()