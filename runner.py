import tkinter as tk
from tkcalendar import DateEntry
from datetime import date


teamList = [
'Select team...',
'Arizona Diamondbacks',
'Atlanta Braves',
'Baltimore Orioles',
'Boston Red Sox',
'Chicago White Sox',
'Chicago Cubs',
'Cincinnati Reds',
'Cleveland Indians',
'Colorado Rockies',
'Detroit Tigers',
'Houston Astros',
'Kansas City Royals',
'Los Angeles Angels',
'Los Angeles Dodgers',
'Miami Marlins',
'Milwaukee Brewers',
'Minnesota Twins',
'New York Yankees',
'New York Mets',
'Oakland Athletics',
'Philadelphia Phillies',
'Pittsburgh Pirates',
'San Diego Padres',
'San Francisco Giants',
'Seattle Mariners',
'St. Louis Cardinals',
'Tampa Bay Rays',
'Texas Rangers',
'Toronto Blue Jays',
'Washington Nationals'
]

# get today's date
today = str(date.today()).split('-')

# setup stuff
master = tk.Tk()
master.title('MLB Simulator 2.0')


# functions
# simulate all games for today
def simAll():
    pass

# simulate a custom game
def simCustom():
    print('Away team: {}'.format(awayTeamVar.get()))
    print('Home team: {}'.format(homeTeamVar.get()))

# center the GUI
def center_window(width, height):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/2)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))


# simulate games button
tk.Button(master, text="  Simulate All  ", relief='groove', overrelief='sunken', command=simAll).grid(row=1, column=0, sticky='nsew')


# drop down calendar
tk.Label(text=' Select date ').grid(row=0, column=0)
cal = DateEntry(master, width=12, year=int(today[0]), month=int(today[1]), day=int(today[2]), background='darkblue', forground='white', borderwidth=2)
cal.grid(row=0, column=1)

# simulate a custom game
tk.Button(master, text="Simulate Custom", relief='groove', overrelief='sunken', command=simCustom).grid(row=2, column=0, sticky='nsew')


# away team entries

awayTeamVar = tk.StringVar(master)
awayTeamVar.set(teamList[0])

tk.Label(master, text="  Away Team  ", bg='dodger blue').grid(row=3, column=0, padx=6, sticky='nsew')
tk.Label(master, text=" Away Pitcher ", bg='dodger blue').grid(row=4, column=0, padx=6, sticky='nsew')
cAwayTeam = tk.ttk.Combobox(master, textvariable=awayTeamVar, values=teamList)
cAwayTeam.grid(row=3, column=1)
cAwayPitcher = tk.Entry(master, relief = 'groove')
cAwayPitcher.grid(row=4, column=1)


# home team entries

homeTeamVar = tk.StringVar(master)
homeTeamVar.set(teamList[0])

tk.Label(master, text="  Home Team  ", bg='tomato2').grid(row=3, column=2, padx=6, sticky='nsew')
tk.Label(master, text=" Home Pitcher ", bg='tomato2').grid(row=4, column=2, padx=6, sticky='nsew')
cHomeTeam = tk.ttk.Combobox(master, textvariable=homeTeamVar, values=teamList)
cHomeTeam.grid(row=3, column=3)
cHomePitcher = tk.Entry(master, relief = 'groove')
cHomePitcher.grid(row=4, column=3)


# custom lineups checkbox
tk.Label(text='Custom Lineups', padx=3).grid(row=3, column=4)
tk.Checkbutton(master, onvalue=1, offvalue=0).grid(row=3, column=5)


# quit button
quitB = tk.Button(master, relief='groove', text='  Quit  ', overrelief='sunken', command=master.destroy)
quitB.grid(row=5, column=4, sticky='nsew')


# center window and run
center_window(650, 500)
tk.mainloop()