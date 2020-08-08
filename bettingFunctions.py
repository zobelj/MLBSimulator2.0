def convertToML(winPercent):

    if(winPercent <= 50):
        ml = (100 - winPercent) / winPercent * 100
    elif(winPercent > 50):
        ml = winPercent / (100 - winPercent) * -100

    return((ml))
