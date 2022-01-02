# Sebastian Rowe
# Disney Reservation Assistant 

# Queries Disney's reservation site for a given date and park
# and loops until a reservation is available. 

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime 
from datetime import timedelta
import time

"""
UserInfo is a class created for each date/park/ticket combo. 
It also holds the ID of the tab its information is searched for 
and the most recent time that its information was queried.

printinfo is a function that simply prints the users information to the terminal. 
"""
class UserInfo:
    def __init__(self, tickettype  =  None, month = None, day = None, year = None, park = None, passtype = None, tabID = None, currentavail = 3, mostrecenttimestamp = None):
        self.tickettype = tickettype # [1 - 3]
        self.month = month  # [1 - 12]
        self.day = day  # [1 - 31]
        self.year = year #[current year - current year + 2]
        self.park = park  # [0 - 3]
        self.passtype = passtype # [0 - 4]
        self.tabID = tabID #[ID of relevant tab]
        self.currentlyavail = currentavail #[1 if available, 0 if unavailable, 2 if blocked out]
        self.mostrecenttimestamp = mostrecenttimestamp #timestamp of the most recent query

    def printinfo(self):
        tickettypes = ["Theme Park Tickets", "Select Resort Hotel Tickets"]
        parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
        passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']

        if self.passtype == 0:
            print(f' -- {str(parks[self.park])} on {str(self.month)}-{str(self.day)}-{str(self.year)} using {str(tickettypes[self.tickettype - 1])}.')
        else:
            print(f' -- {str(parks[self.park])} on {str(self.month)}-{str(self.day)}-{str(self.year)} using your {str(passes[self.passtype])}.')

"""
getuserinfo will populate the UserInfo class with the appropriate user information needed.

getavail will navigate in Chrome to get the availability of the given class. Returns 1 if available,
0 if unavailable, 2 if blocked out.

printavail will print the availablity information needed to the terminalin an understandable format.
"""

def getuserinfo(info):

    #ticket category
    while True:
        print("Please select a ticket category:\n")
        print("[1] - Theme Park Tickets")
        print("[2] - Select Resort Hotels")
        print("[3] - Annual Passes")

        info.tickettype = int(input("\nType a number 1-3 and hit Enter ----> "))
        if info.tickettype <= 3 and info.tickettype >= 1:
            break
        else:
            print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 3")
    
    # pass category if needed
    if info.tickettype == 3:
        while True:
            print("What pass do you have?\n")
            print("[1] - Incredipass")
            print("[2] - Sorcerer Pass")
            print("[3] - Pirate Pass")
            print("[4] - Pixie Dust Pass")

            info.passtype = int(input("\nType a number 1-4 and hit Enter ----> "))
            if info.passtype <= 4 and info.passtype >= 0:
                break
            else:
                print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")
    else:
       info.passtype = 0

    # date 
    currentdate = datetime.datetime.now()
    while True:
        rawdate = input("Please enter the date you would like to go (MM-DD-YYYY) --> ")
        splitdate = rawdate.split('-')
        info.month = int(splitdate[0])
        info.day = int(splitdate[1])
        info.year = int(splitdate[2])

        isvaliddate = True
        try:
            formatteddate = datetime.datetime(int(info.year), int(info.month), int(info.day))
        except ValueError:
            isvaliddate = False
        
        if isvaliddate and formatteddate >= currentdate and formatteddate <= currentdate + timedelta(days=730):
            break
        else:
            print(f"[INVALID INPUT] -- {info.month}-{info.day}-{info.year} IS NOT A VALID DATE. DATE MUST BE BETWEEN NOW AND 2 YEARS IN THE FUTURE.")
            continue
    
    # park
    while True:
        parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios'] #[0,1,2,3]
        print("What park would you like to visit?\n")
        print("[1] - " + parks[0])
        print("[2] - " + parks[1])
        print("[3] - " + parks[2])
        print("[4] - " + parks[3])

        info.park = int(input("\nType a number 1-4 and hit Enter ----> ")) - 1
        if (info.park <= 3 and info.park >= 0):
            break
        else:
            print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")  
def getavail(info):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    currentmonth = datetime.datetime.now().month
    currentday = datetime.datetime.now().day

    # return 1 if available, 0 if not available, 2 if blocked out
    if info.passtype == 0:
        #selects correct ticket button
        placehold1 = driver.find_element(By.TAG_NAME,"awakening-selector")
        placehold2 = placehold1.shadow_root
        if info.tickettype == 1:
            btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=tickets]")
        else:
            btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=resort]")
        btn_themeparktickets.click()
        driver.implicitly_wait(5)

        # presses correct month
        month_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
        month_placehold2 = month_placehold1.shadow_root
        month_placehold3 = month_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
        month_placehold4 = month_placehold3.shadow_root
        btn_nextmonth = month_placehold4.find_element(By.CSS_SELECTOR, "#nextArrow")
        monthheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text)    
        yearheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#year").text)
        oncorrectmonth = False
        if months[info.month - 1] == monthheader and str(info.year) == yearheader:
            oncorrectmonth = True   
        while not oncorrectmonth:
            btn_nextmonth.click()
            monthheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text)
            yearheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#year").text)
            if months[info.month - 1] == monthheader and str(info.year) == yearheader:
                oncorrectmonth = True
        driver.implicitly_wait(5)

        # get and press non-passholder day
        day_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
        day_placehold2 = day_placehold1.shadow_root
        day_placehold3 = day_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
        if info.month == currentmonth:
            day_placehold4 = "wdat-date[" + str(info.day - currentday + 1) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        else:
            day_placehold4 = "wdat-date[" + str(info.day) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        button.click()
        driver.implicitly_wait(5)

        # check avail for desired park
        avail_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-availability-information")
        avail_placehold2 = avail_placehold1.shadow_root
        avail_placehold3 = avail_placehold2.find_element(By.CSS_SELECTOR, "#parkAvailabilityContainer")
        xpath = "div[" + str(info.park + 1) + "]"
        parkcontainer = avail_placehold3.find_element(By.XPATH, xpath)
        available = parkcontainer.get_attribute("class")
        info.mostrecenttimestamp = str(time.ctime())
        if available == "available":
            return 1
        else:
            return 0


    else: #passholder

        # presses correct pass button
        pass_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-pass-selection")
        pass_placehold2 = pass_placehold1.shadow_root
        if info.passtype == 1:
            pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-incredi-pass")
        elif info.passtype == 2:
            pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-sorcerer-pass")
        elif info.passtype == 3:
            pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-pirate-pass")
        else:
            pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-pixie-dust-pass")
        pass_button.click()
        driver.implicitly_wait(5)

        # presses correct park button 
        park_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-park-selection")
        park_placehold2 = park_placehold1.shadow_root
        if info.park == 0:
            park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_MK")
        elif info.park == 1:
            park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_AK")
        elif info.park == 2:
            park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_EP")
        else:
            park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_HS")
        park_button.click()
        driver.implicitly_wait(10)

        # gets to correct day element ......
        month_placehold1 = driver.find_element(By.TAG_NAME, 'com-park-admission-calendar-container')
        month_placehold2 = month_placehold1.shadow_root
        month_placehold3 = month_placehold2.find_element(By.CSS_SELECTOR, "#admissionCalendar")
        month_placehold4 = month_placehold3.shadow_root

        if info.month < 10:
            formattedmonth = str(f"0{info.month}") #adds a '0' if necessary to month
        else:
            formattedmonth = str(info.month)
        
        if info.day < 10:
            formattedday = str(f"0{info.day}") #adds a '0' if necessary to day
        else:
            formattedday = str(info.day)

        slot = str(f"[slot=\"{info.year}-{formattedmonth}-{formattedday}\"]")
        desiredday = month_placehold4.find_element(By.CSS_SELECTOR, slot)
        available = str(desiredday.get_attribute("class"))

        #... and checks park availability
        info.mostrecenttimestamp = str(time.ctime())
        if available == "all green":
            return 1
        elif available == "no-reservations":
            return 0
        elif available == "blocked":
            return 2
        else:
            print("[ERROR]")
def printavail(infodesired):
    parks = ['Magic Kingdom', 'Animal Kingdom', 'EPCOT', 'Hollywood Studios']
    passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']
    tickettypes = ['Theme Park Tickets', 'Select Resort Hotel Tickets']

    os.system('clear')
    print("Press ctrl-c at any time ('^C') to terminate.")
    print('Theme Park Live Availability')
    print('---------------------------------')
    for info in infodesired:
        if info.currentlyavail == 3: #for first time around. will be obsolete when .currentlyavail is populated 
                print('[NOT QUERIED YET] hold on.......')
        elif info.tickettype != 3: #non passholder
            if info.currentlyavail == 1:
                print(f"[   AVAILABLE   ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month)}/{str(info.day)}/{str(info.year)} with {str(tickettypes[info.tickettype - 1])}!")
            else:
                print(f"[ NOT AVAILABLE ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month)}/{str(info.day)}/{str(info.year)} with {str(tickettypes[info.tickettype - 1])}!")
        else: #passholder
            if info.currentlyavail == 1:
                print(f"[   AVAILABLE   ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}!")
            elif info.currentlyavail == 0:
                print(f"[ NOT AVAILABLE ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}.")
            else:
                print(f"[  BLOCKED OUT  ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}. Searches have stopped for this entry.")



# ----------------- B O D Y ------------------
path = Service("/Applications/chromedriver") # path where chromedriver lies [MUST BE ADJUSTED PER EACH COMPUTER]
driver = webdriver.Chrome(service = path)
numofdesireddates = 0
infodesired = [] #list of total desired date/ticket combos (will exclude blockout dates)
blockedout =[] #list of blocked out date/ticket combos



try:

    # populates as many user info classes as user desires
    while True:
        # prints header
        os.system('clear')
        print("Press ctrl-c at any time ('^C') to terminate.")
        print('Please enter however many dates and parks you would like to search for.\n')
        if numofdesireddates != 0: 
            print('Requested Dates:\n')
            for info in infodesired:
                info.printinfo()
            print('\n')
        
        numofdesireddates += 1
        name = 'info' + str(numofdesireddates)
        name = UserInfo()
        infodesired.append(name)

        getuserinfo(name)
        if name.tickettype == 3: # handles AP/nonAP websites
            driver.get('https://disneyworld.disney.go.com/passes/blockout-dates/disney-incredi-pass/')
        else:
            driver.get('https://disneyworld.disney.go.com/availability-calendar') 
        driver.maximize_window()
        name.tabID = driver.window_handles[numofdesireddates - 1]

        again = input('\nWould you like to add another day? (input \"Y\" to add another day, input any other key to continue) ----> ')
        if again == "Y" or again == "y":
            driver.switch_to.new_window('tab') # opens a new tab
            continue
        else:
            break
    
    #loops, gets, and prints availability
    while True:
        for info in infodesired:
            if info in blockedout: # skip blockout dates (as they will never become available).
                continue
            driver.switch_to.window(info.tabID)
            driver.refresh()
            driver.implicitly_wait(10)

            try: 
                info.currentlyavail = getavail(info)
            except NoSuchElementException: # if NoSuchElementException is thrown, it gets another shot after a wait for loading. 
                try: 
                    driver.refresh()
                    driver.implicitly_wait(10)
                    info.currentlyavail = getavail(info)
                except NoSuchElementException: # but if it fails twice, there is a website error and adjustments need to be made. 
                    print('[WEBSITE ERROR] --- CLOSING PROGRAM')
                    break
            printavail(infodesired)
            if info.currentlyavail == 2:
                blockedout.append(info)

except KeyboardInterrupt: # quits program on ctrl-c or ^c
    os.system('clear')

driver.quit() # closes browser
