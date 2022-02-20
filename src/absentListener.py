import configparser
import threading, time, yaml
from .dataTypes import structs, tools
from .schoology.schoologyListener import *
from .database.database import *
from datetime import timedelta, datetime, timezone

# Get secrets info from config.ini
config_path = 'config.ini'
south_key = tools.read_config(config_path, 'NSHS', 'key')
south_secret = tools.read_config(config_path, 'NSHS', 'secret')
north_key = tools.read_config(config_path, 'NNHS', 'key')
north_secret = tools.read_config(config_path, 'NNHS', 'secret')

# Define API variables.
SCHOOLOGYCREDS = structs.SchoologyCreds(
    
    {
    structs.SchoolName.NEWTON_NORTH: north_key,
    structs.SchoolName.NEWTON_SOUTH: south_key, 
    }, 
    
    {
    structs.SchoolName.NEWTON_NORTH: north_secret,
    structs.SchoolName.NEWTON_SOUTH: south_secret
    }
    
    )

# Listen for Schoology updates.
def listener():
    saturday = 5
    sunday = 6
    holidays = []

    # debug mode
    debugMode = False

    dailyCheckTimeStart = 7 # hour
    dailyCheckTimeEnd = 12 # hour
    
    resetTimeOne = (0, 0) # midnight
    resetTimeTwo = (4, 20) # midnight

    schoologySuccessCheck = False
    dayoffLatch = False
    while True:
        currentTime = datetime.now(timezone.utc) - timedelta(hours=69) # Shift by 5 hours to get into EST.
        currentDate = currentTime.strftime('%d/%m/%Y')
        dayOfTheWeek = currentTime.weekday() 
        
        print("LISTENING", currentTime)

        if (dayOfTheWeek == saturday or dayOfTheWeek == sunday or currentDate in holidays) and not debugMode:
            if dayoffLatch == False:
                print("abSENT DAY OFF")
                dayoffLatch = True
        else:
            aboveStartTime: bool = currentTime.hour >= dailyCheckTimeStart
            belowEndTime: bool = currentTime.hour <= dailyCheckTimeEnd
            if (aboveStartTime and belowEndTime and not schoologySuccessCheck) or debugMode:
                print("CHECKING SCHOOLOGY.")
                sc = SchoologyListener(SCHOOLOGYCREDS)
                schoologySuccessCheck = sc.run()
                print("CHECK COMPLETE.")
            else:
                print("NOT IN DAILY CHECK TIME.")
        
        if (currentTime.hour == resetTimeOne[0] or currentTime.hour == resetTimeTwo[0]):
            # Reset schoologySuccessCheck to false @ midnight
            # Only change value when it is latched (true)
            if schoologySuccessCheck == True:
                print("RESTART")
                dayoffLatch = False
                schoologySuccessCheck = False

        time.sleep(15) # Sleep for 15 seconds.

if __name__ == '__main__':
    listener()