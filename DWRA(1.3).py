# Sebastian Rowe
# Disney Reservation Assistant 

# Queries Disney's reservation site for a given date and park
# and loops until a reservation is available. 

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchShadowRootException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime 
import time


class UserInfo:
    def __init__(self, tickettype  =  None, month = None, day = None, year = None, park = None, passtype = None, tabID = None, currentavail = 3, mostrecenttimestamp = None):
        self.tickettype = tickettype # [1 - 3]
        self.month = month  # [0 - 11]
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
            print(f' -- {parks[self.park]} on {str(self.month + 1)}-{str(self.day)}-{str(self.year)} using {tickettypes[self.tickettype - 1]}.')
        else:
            print(f' -- {parks[self.park]} on {str(self.month + 1)}-{str(self.day)}-{str(self.year)} using your {passes[self.passtype]}.')

    def getavail(self):
        # will return 1 if available, 0 if unavailable, 2 if passholder and blocked out
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        parks = ['Magic Kingdom', 'Animal Kingdom', 'EPCOT', 'Hollywood Studios']
        passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']
        tickettypes = ['Theme Park Tickets', 'Select Resort Hotel Tickets']
        currentmonth = datetime.now().month
        currentday = datetime.now().day


        slot = str(f"[slot=\"{info.year}-{info.month}-{info.day}\"]")
        
        #passholder / non-passholder split
        if info.passtype == 0: #non-passholder 

            #selects correct ticket button
            placehold1 = driver.find_element(By.TAG_NAME,"awakening-selector")
            driver.implicitly_wait(5)
            placehold2 = placehold1.shadow_root
            driver.implicitly_wait(5)
            if info.tickettype == 1:
                btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=tickets]")
            else:
                btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=resort]")
            driver.implicitly_wait(5)
            btn_themeparktickets.click()
            driver.implicitly_wait(5)

            # presses correct month
            month_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
            driver.implicitly_wait(5)
            month_placehold2 = month_placehold1.shadow_root
            driver.implicitly_wait(5)
            month_placehold3 = month_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
            driver.implicitly_wait(5)
            month_placehold4 = month_placehold3.shadow_root
            driver.implicitly_wait(5)
            btn_nextmonth = month_placehold4.find_element(By.CSS_SELECTOR, "#nextArrow")
            driver.implicitly_wait(5)
            monthheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text)
            driver.implicitly_wait(5)
            yearheader =  str(month_placehold4.find_element(By.CSS_SELECTOR, "#year").text)  
            driver.implicitly_wait(5) 
            oncorrectmonth = False
            if str(months[info.month]) == monthheader and str(info.year) == yearheader:
                oncorrectmonth = True   
            while not oncorrectmonth:
                btn_nextmonth.click()
                driver.implicitly_wait(5)
                monthheader = str(month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text)
                driver.implicitly_wait(5)
                yearheader =  str(month_placehold4.find_element(By.CSS_SELECTOR, "#year").text)
                driver.implicitly_wait(5)  
                if str(months[info.month]) == monthheader and str(info.year) == yearheader:
                    oncorrectmonth = True
            driver.implicitly_wait(5)
            
            # get and press non-passholder day
            day_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
            driver.implicitly_wait(5)
            day_placehold2 = day_placehold1.shadow_root
            driver.implicitly_wait(5)
            day_placehold3 = day_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
            driver.implicitly_wait(5)
            if info.month + 1 == currentmonth:
                button = day_placehold3.find_element(By.CSS_SELECTOR, slot)
            else:
                button = day_placehold3.find_element(By.XPATH, slot)
                driver.implicitly_wait(5)
            button.click()
            driver.implicitly_wait(5)

            # check avail for desired park
            avail_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-availability-information")
            driver.implicitly_wait(5)
            avail_placehold2 = avail_placehold1.shadow_root
            driver.implicitly_wait(5)
            avail_placehold3 = avail_placehold2.find_element(By.CSS_SELECTOR, "#parkAvailabilityContainer")
            driver.implicitly_wait(5)
            xpath = "div[" + str(info.park + 1) + "]"
            parkcontainer = avail_placehold3.find_element(By.XPATH, xpath)
            driver.implicitly_wait(5)
            available = parkcontainer.get_attribute("class")
            driver.implicitly_wait(5)
            info.mostrecenttimestamp = str(time.ctime())
            if available == "available":
                return 1
            else:
                return 0
        else: # passholder

            # presses correct pass button
            pass_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-pass-selection")
            driver.implicitly_wait(5)
            pass_placehold2 = pass_placehold1.shadow_root
            driver.implicitly_wait(5)
            if info.passtype == 1:
                pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-incredi-pass")
            elif info.passtype == 2:
                pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-sorcerer-pass")
            elif info.passtype == 3:
                pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-pirate-pass")
            else:
                pass_button = pass_placehold2.find_element(By.CSS_SELECTOR, "#disney-pixie-dust-pass")

            driver.implicitly_wait(5)
            pass_button.click()
            driver.implicitly_wait(5)

            # presses correct park button 
            park_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-park-selection")
            driver.implicitly_wait(5)
            park_placehold2 = park_placehold1.shadow_root
            driver.implicitly_wait(5)
            if info.park == 0:
                park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_MK")
            elif info.park == 1:
                park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_AK")
            elif info.park == 2:
                park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_EP")
            else:
                park_button = park_placehold2.find_element(By.CSS_SELECTOR, "#WDW_HS")

            driver.implicitly_wait(5)    
            park_button.click()
            driver.implicitly_wait(5)

            # gets to correct day element ......
            month_placehold1 = driver.find_element(By.TAG_NAME, 'com-park-admission-calendar-container')
            driver.implicitly_wait(5)
            month_placehold2 = month_placehold1.shadow_root
            driver.implicitly_wait(5)
            month_placehold3 = month_placehold2.find_element(By.CSS_SELECTOR, "#admissionCalendar")
            driver.implicitly_wait(5)
            month_placehold4 = month_placehold3.shadow_root
            driver.implicitly_wait(5)


            desiredday = month_placehold4.find_element(By.CSS_SELECTOR, slot)
            driver.implicitly_wait(5)
            available = str(desiredday.get_attribute("class"))
            driver.implicitly_wait(5)

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

def gettickettype():
    while True:
        print("Please select a ticket category:\n")
        print("[1] - Theme Park Tickets")
        print("[2] - Select Resort Hotels")
        print("[3] - Annual Passes")

        tickettype = int(input("\nType a number 1-3 and hit Enter ----> "))
        if tickettype <=3 and tickettype >= 1:
            return tickettype
        else:
            print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 3")
def getdate():
    daysinmonth = [31,28,31,30,31,30,31,31,30,31,30,31]
    currentyear = datetime.now().year
    currentday = datetime.now().day
    currentmonth = datetime.now().month

    while True: 
        raw_date = input("Please enter the date you would like to go (MM-DD-YYYY) --> ")
        date_list = raw_date.split('-')
        month = int(date_list[0]) - 1
        day = int(date_list[1])
        year = int(date_list[2])

        #valid date check
        if month == 1 and day == 29: #leap year
            if year % 4 == 0:
                return month, day, year
            else:  
                print("[INVALID INPUT] -- NOT A LEAP YEAR, PLEASE INPUT A VALID DATE")
        elif year == currentyear:
            if month == currentmonth - 1:
                if day >= currentday and day <= daysinmonth[month]:
                    return month, day, year
                else:
                    print(f"[INVALID INPUT] -- {month + 1}-{day}-{year} IS NOT A VALID DATE") 
                    continue
            elif month >= currentmonth - 1 and month <= 11 and day >= 1 and day <= daysinmonth[month]:
                return month, day, year
            else:
                print(f"[INVALID INPUT] -- {month + 1}-{day}-{year} IS NOT A VALID DATE")
        else:
            if month >= 0 and month <= 11 and day >= 1 and day <= daysinmonth[month] and year >= currentyear and year <= currentyear + 2:
                return month, day, year
            else:
                print(f"[INVALID INPUT] -- {month + 1}-{day}-{year} IS NOT A VALID DATE")
                       
def getpark():
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios'] #[0,1,2,3]
    print("What park would you like to visit?\n")
    print("[1] - " + parks[0])
    print("[2] - " + parks[1])
    print("[3] - " + parks[2])
    print("[4] - " + parks[3])

    park = int(input("\nType a number 1-4 and hit Enter ----> ")) - 1
    if (park <= 3 and park >= 0):
        print("You chose --> "+ parks[park])
        return park
    else:
        print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")
        getpark()  
def getpasstype():
    while True:
        print("What pass do you have?\n")
        print("[1] - Incredipass")
        print("[2] - Sorcerer Pass")
        print("[3] - Pirate Pass")
        print("[4] - Pixie Dust Pass")

        passtype = int(input("\nType a number 1-4 and hit Enter ----> "))
        if (passtype <= 4 and passtype >= 0):
            return passtype
        else:
            print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")
def printavail(infodesired):
    parks = ['Magic Kingdom', 'Animal Kingdom', 'EPCOT', 'Hollywood Studios']
    passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']
    tickettypes = ['Theme Park Tickets', 'Select Resort Hotel Tickets']

    os.system('clear')
    print('Theme Park Live Availability')
    print('---------------------------------')
    for info in infodesired:
        if info.currentlyavail == 3: #for first time around. will be obsolete when .currentlyavail is populated 
                print('[NOT QUERIED YET] hold on.......')
        elif info.tickettype != 3: #non passholder
            if info.currentlyavail == 1:
                print(f"[   AVAILABLE   ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month + 1)}/{str(info.day)}/{str(info.year)} with {str(tickettypes[info.tickettype - 1])}!")
            else:
                print(f"[ NOT AVAILABLE ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month + 1)}/{str(info.day)}/{str(info.year)} with {str(tickettypes[info.tickettype - 1])}!")
        else: #passholder
            if info.currentlyavail == 1:
                print(f"[   AVAILABLE   ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month + 1)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}!")
            elif info.currentlyavail == 0:
                print(f"[ NOT AVAILABLE ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month + 1)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}.")
            else:
                print(f"[  BLOCKED OUT  ] - {info.mostrecenttimestamp} --- {str(parks[info.park])}, for {str(info.month + 1)}/{str(info.day)}/{str(info.year)} for the {passes[info.passtype]}. Searches have stopped for this entry.")

            




# ------------------------- B O D Y -------------------------
path = Service("/Applications/chromedriver") # path where chromedriver lies
driver = webdriver.Chrome(service = path)
wait = WebDriverWait(driver, 10)


# Populates as many UserInfo's as user desires to be queried
numofdesireddates = 0
infodesired = [] # [info1, info2, info3, .....] list of requested dates/parks
blockedout = [] # [info4, info8, info10, ...] used to skip verified blockout dates. 


try:
    # populates classes
    while True:
        os.system('clear')
        print("Press ctrl-c at any time ('^C') to terminate.")
        print('Please enter however many dates and parks you would like to search for.\n')
        if numofdesireddates != 0:
            for info in infodesired:
                info.printinfo()
            print('\n')
        numofdesireddates += 1
        name = "info" + str(numofdesireddates)
        tickettype = gettickettype()
        wait.until(expected_conditions.number_of_windows_to_be(numofdesireddates)) # waits until correct number of tabs are open
        tabID = driver.window_handles[numofdesireddates - 1]
        month, day, year = getdate()
        park = getpark()
        if tickettype == 3:
            passtype = getpasstype()
        else:
            passtype = 0   

        if tickettype == 3: #handles AP/nonAP websites
            driver.get('https://disneyworld.disney.go.com/passes/blockout-dates/disney-incredi-pass/')
        else:
            driver.get('https://disneyworld.disney.go.com/availability-calendar') 
        driver.maximize_window()

        name = UserInfo(tickettype, month, day, year, park, passtype, tabID)
        infodesired.append(name)

        again = input('\nWould you like to add another day? (input \"Y\" to add another day, input any other key to continue) ----> ')
        if again == "Y" or again == "y":
            driver.switch_to.new_window('tab')
            continue
        else:
            break


# loops and rerturns availability

    while True:
        for info in infodesired: 
            if info in blockedout: # skips blocked out dates
                continue 
            driver.switch_to.window(info.tabID)
            driver.refresh()
            driver.implicitly_wait(10)
            try:
                info.currentlyavail = info.getavail()
            except NoSuchElementException:
                try:
                    driver.implicitly_wait(5)
                    info.currentlyavail = info.getavail()
                except NoSuchElementException:
                    print("[WEBSITE ERROR] --- CLOSING PROGRAM")
                    driver.quit()
            printavail(infodesired)
            if info.currentlyavail == 2:
                blockedout.append(info)
except KeyboardInterrupt:
    os.system('clear')

driver.quit()
