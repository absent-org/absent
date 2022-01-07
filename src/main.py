import threading, time, yaml
from dataStructs import *
from driver.schoologyListener import *
from database.databaseHandler import *
from datetime import timedelta, datetime, timezone
from database.logger import Logger

logger = Logger()
logger.systemStartup()

# Open files.
with open('secrets.yml') as f:
    cfg = yaml.safe_load(f)

# Define API variables.
scCreds = SchoologyCreds(cfg['north']['key'], cfg['north']['secret'], cfg['south']['key'], cfg['south']['secret'])
textnowCreds = TextNowCreds(cfg['textnow']['username'], cfg['textnow']['sid'], cfg['textnow']['csrf'])

# Make threads regenerate on fault.
def threadwrapper(func):
    def wrapper():
        while True:
            try:
                func()
            except BaseException as error:
                print('abSENT - {!r}; restarting thread'.format(error))
            else:
                print('abSENT - Exited normally, bad thread, restarting')
    return wrapper

# Listen for Schoology updates.
def sc_listener():
    saturday = 5
    sunday = 6
    holidays = []

    # debug mode
    debugMode = False

    dailyCheckTimeStart = 7 # hour
    dailyCheckTimeEnd = 12 # hour
    
    resetTime = (0, 0) # midnight

    schoologySuccessCheck = False
    dayoffLatch = False
    while True:
        currentTime = datetime.now(timezone.utc) - timedelta(hours=5) # Shift by 5 hours to get into EST.
        currentDate = currentTime.strftime('%d/%m/%Y')
        dayOfTheWeek = currentTime.weekday() 
        
        print("LISTENING", currentTime)

        if (dayOfTheWeek == saturday or dayOfTheWeek == sunday or currentDate in holidays) and not debugMode:
            if dayoffLatch == False:
                logger.schoologyOffDay(currentDate)
                print("abSENT DAY OFF")
                dayoffLatch = True
        else:
            aboveStartTime: bool = currentTime.hour >= dailyCheckTimeStart
            belowEndTime: bool = currentTime.hour <= dailyCheckTimeEnd
            if (aboveStartTime and belowEndTime and not schoologySuccessCheck) or debugMode:
                print("CHECKING SCHOOLOGY.")
                sc = SchoologyListener(textnowCreds, scCreds)
                schoologySuccessCheck = sc.run()
                print("CHECK COMPLETE.")
        
        if currentTime.hour == resetTime[0] and currentTime.minute == resetTime[1]:
            # Reset schoologySuccessCheck to false @ midnight
            # Only change value when it is latched (true)
            if schoologySuccessCheck == True:
                print("RESTART")
                logger.resetSchoologySuccessCheck()
                dayoffLatch = False
                schoologySuccessCheck = False

        time.sleep(15) # Sleep for 15 seconds.
            
# Configure and start threads.
threads = {
        'sc': threading.Thread(target=threadwrapper(sc_listener), name='sc listener'),
}

threads['sc'].start()