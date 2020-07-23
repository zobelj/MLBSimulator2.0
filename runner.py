import tkinter as tk


# setup stuff
master = tk.Tk()
master.title('MLB Simulator 2.0')


# functions
# simulate all games for today
def simAll():
    pass

# simulate a custom game
def simCustom():
    pass


def center_window(width, height):
    # get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/3) - (height/2)
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))


# simulate games button
tk.Button(master, text="  Simulate All  ", relief='groove', overrelief='sunken', command=simAll).grid(row=0, column=0, sticky='nsew')


# simulate a custom game
tk.Button(master, text="Simulate Custom", relief='groove', overrelief='sunken', command=simCustom).grid(row=1, column=0, sticky='nsew')


# away team entries
tk.Label(master, text=" Away Team ", bg='dodger blue').grid(row=2, column=0, padx=6, sticky='nsew')
tk.Label(master, text="Away Pitcher", bg='dodger blue').grid(row=3, column=0, padx=6, sticky='nsew')
cAwayTeam = tk.Entry(master, relief = 'groove')
cAwayTeam.grid(row=2, column=1)
cAwayPitcher = tk.Entry(master, relief = 'groove')
cAwayPitcher.grid(row=3, column=1)


# home team entries
tk.Label(master, text=" Away Team ", bg='tomato2').grid(row=2, column=2, padx=6, sticky='nsew')
tk.Label(master, text="Away Pitcher", bg='tomato2').grid(row=3, column=2, padx=6, sticky='nsew')
cHomeTeam = tk.Entry(master, relief = 'groove')
cHomeTeam.grid(row=2, column=3)
cHomePitcher = tk.Entry(master, relief = 'groove')
cHomePitcher.grid(row=3, column=3)


# custom lineups checkbox
tk.Label(text='Custom Lineups', padx=3).grid(row=2, column=4)
tk.Checkbutton(master, onvalue=1, offvalue=0).grid(row=2, column=5)


# quit button
quitB = tk.Button(master, relief='groove', text='  Quit  ', overrelief='sunken', command=master.destroy)
quitB.grid(row=16, column=4, sticky='nsew')


# center window and run
center_window(575, 500)
tk.mainloop()