# Sebastian Rowe
# Disney Reservation Assistant 

# Queries Disney's reservation site for a given date and park
# and loops until a reservation is available. 

from os import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime 
import time


class UserInfo:
    def __init__(self, tickettype  =  None, month = None, day = None, year = None, park = None, passtype = None, tabID = None):
        self.tickettype = tickettype # [1 - 3]
        self.month = month  # [0 - 11]
        self.day = day  # [1 - 31]
        self.year = year #[current year - current year + 2]
        self.park = park  # [0 - 3]
        self.passtype = passtype # [0 - 4]
        self.tabID = tabID #[ID of the tab]

    def printinfo(self):
        tickettypes = ["Theme Park Tickets", "Select Resort Hotel Tickets"]
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
        passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']

        if self.passtype == 0:
            print(f'You want to go to {parks[self.park]} on {months[self.month]}, {str(self.day)} using {tickettypes[self.tickettype - 1]}.') # FIX NONETYPE ERROR HERE
        else:
            print('You want to go to ' + parks[int(self.park)] + ' on ' + months[int(self.month)] + ' ' + str(self.day) + ' using your ' + passes[int(self.passtype)] + '.')

def opensite(site):
    driver.get(site) # opens website
    driver.maximize_window()
    print("webpage title --> \"" + driver.title + "\"\n") # prints title of website
def gettickettype():
    print("Please select a ticket category:\n")
    print("[1] - Theme Park Tickets")
    print("[2] - Select Resort Hotels")
    print("[3] - Annual Passes")

    tickettype = int(input("\nType a number 1-3 and hit Enter ----> "))
    if tickettype <=3 and tickettype >= 1:
        return tickettype
    else:
        print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 3")
        gettickettype()
def getdate():
    daysinmonth = [31,28,31,30,31,30,31,31,30,31,30,31]
    currentyear = datetime.now().year

    while True: 
        month = int(input("What month would you like to go? (1-12) --> ")) - 1
        day = int(input("What day would you like to go? (1-31) --> "))
        year = int(input(f"What year would you like to go? ({currentyear} - {currentyear + 2}) --> "))

        #leap year check
        if month == 1 and day == 29:
            if year % 4 == 0:
                return month, day, year
            else:  
                print("[INVALID INPUT] -- NOT A LEAP YEAR, PLEASE INPUT A VALID DATE")
        elif day <= daysinmonth[month] and day > 0 and month >= 0 and month <= 11 and year >= currentyear and year <= currentyear + 2: #asserts valid date
            return month, day, year
        else:
            print(f"[INVALID INPUT] -- {month}, {day} IS NOT A VALID DATE")                
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
    print("What pass do you have?\n")
    print("[1] - Incredipass")
    print("[2] - Sorcerer Pass")
    print("[3] - Pirate Pass")
    print("[4] - Pixie Dust Pass")

    passtype = int(input("\nType a number 1-4 and hit Enter ----> "))
    if (passtype <= 3 and passtype >= 0):
        return passtype
    else:
        print("[INVALID INPUT] -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")
        getpasstype()
        return passtype
def getavail(info):
    # will return 1 if available, 0 if unavailable

    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
    passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']
    tickettypes = ["Theme Park Tickets", "Select Resort Hotel Tickets"]
    currentday  = datetime.now().day
    currentmonth = datetime.now().month # 1-12
    currentyear = datetime.now().year

    # clicks correct ticket button for class
    placehold1 = driver.find_element(By.TAG_NAME,"awakening-selector")
    placehold2 = placehold1.shadow_root
    if info.tickettype == 1:
        btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=tickets]")
    elif info.tickettype == 2:
        btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=resort]")
    else:
        btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=passholder]") # to new webpage!!!!
    btn_themeparktickets.click()
    driver.implicitly_wait(5)

    #passholder / non-passholder split
    if info.passtype == 0: #non-passholder 
        # get and press non-passholder month
        month_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
        month_placehold2 = month_placehold1.shadow_root
        month_placehold3 = month_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
        month_placehold4 = month_placehold3.shadow_root
        btn_nextmonth = month_placehold4.find_element(By.CSS_SELECTOR, "#nextArrow")
        monthheader = month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text
        yearheader = month_placehold4.find_element(By.CSS_SELECTOR, "#year").text
        oncorrectmonth = False
        if months[info.month] == monthheader:
            oncorrectmonth = True   
        while not oncorrectmonth:
            btn_nextmonth.click()
            monthheader = month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text
            if months[info.month] == monthheader:
                oncorrectmonth = True

        # get and press non-passholder day
        day_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
        day_placehold2 = day_placehold1.shadow_root
        day_placehold3 = day_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
        if info.month + 1 == currentmonth:
            day_placehold4 = "wdat-date[" + str(info.day - currentday + 1) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        else:
            day_placehold4 = "wdat-date[" + str(info.day - 1) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        button.click()

        # check avail for desired park
        avail_placehold1 = driver.find_element(By.TAG_NAME, "awakening-availability-information")
        avail_placehold2 = avail_placehold1.shadow_root
        avail_placehold3 = avail_placehold2.find_element(By.CSS_SELECTOR, "#parkAvailabilityContainer")
        xpath = "div[" + str(info.park + 1) + "]"
        parkcontainer = avail_placehold3.find_element(By.XPATH, xpath)
        available = parkcontainer.get_attribute("class")
        if available == "available":
            print(f"{str(parks[info.park])} IS available on {str(info.month + 1)}/{str(info.day)}/{str(currentyear)} with {str(tickettypes[info.tickettype - 1])}! --- {str(time.ctime())}")
            return 1
        else:
            print(f"{str(parks[info.park])} IS NOT available on {str(info.month + 1)}/{str(info.day)}/{str(currentyear)} with {str(tickettypes[info.tickettype - 1])}! --- {str(time.ctime())}")
            return 0
    else: # passholder
        # presses correct pass button
        pass_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-pass-selection")
        pass_placehold2 = pass_placehold1.shadow_root
        if park == 1:
            pass_button = pass_placehold2.find_element(By.ID, "#disney-incredi-pass")
        elif park == 2:
            pass_button = pass_placehold2.find_element(By.ID, "#disney-sorcerer-pass")
        elif park == 3:
            pass_button = pass_placehold2.find_element(By.ID, "#disney-pirate-pass")
        else:
            pass_button = pass_placehold2.find_element(By.ID, "#disney-pixie-dust-pass")
        pass_button.click()

        # presses correct park button 
        park_placehold1 = driver.find_element(By.TAG_NAME, "com-park-admission-calendar-park-selection")
        park_placehold2 = park_placehold1.shadow_root
        if park == 1:
            park_button = park_placehold2.find_element(By.ID, "#WDW_MK")
        elif park == 2:
            park_button = park_placehold2.find_element(By.ID, "#WDW_AK")
        elif park == 3:
            park_button = park_placehold2.find_element(By.ID, "#WDW_EP")
        else:
            park_button = park_placehold2.find_element(By.ID, "#WDW_HS")
        park_button.click()

        # gets to correct day element
        month_placehold1 = driver.find_element(By.ID, "#admissionCalendar")
        month_placehold2 = month_placehold1.shadow_root
        monthid = "#calendar" + str(info.month - currentmonth - 1)
        print(f"monthid = {monthid}")
        month_placehold3 = month_placehold2.find_element(By.ID, monthid)
        if info.month == currentmonth - 1: # if desired month is the current month
            dayid = "div[" + str(info.day - currentday + 1) + "]"
            print(f"dayid = {dayid}")
            desiredday = month_placehold3.find_element(By.CSS_SELECTOR, dayid)
            available = desiredday.get_attribute("class")
            if available == "all-green":
                print(f"{str(parks[info.park])} IS available on {str(info.month)}/{str(info.day)}/{str(currentyear)} for the {passes[info.passtype]}! --- {str(time.ctime())}")
                return 1
            elif available == "no-reservations":
                print(f"{str(parks[info.park])} is NOT available on {str(info.month)}/{str(info.day)}/{str(currentyear)} for the {passes[info.passtype]}. --- {str(time.ctime())}")
                return 0
            else:
                print(f"The {passes[info.passtype]} is BLOCKED OUT for {str(info.month)}/{str(info.day)}/{str(currentyear)}. Searches will stop for this entry. --- {str(time.ctime())}")
                return 2
def setuptab(info):

    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
    passes = [0,'Incredipass', 'Sorcerer Pass', 'Pirate Pass', 'Pixie Dust Pass']
    tickettypes = ["Theme Park Tickets", "Select Resort Hotel Tickets"]
    currentday  = datetime.now().day
    currentmonth = datetime.now().month # 1-12
    currentyear = datetime.now().year

    if info.tickettype != 3: #sets up non-passholder

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
        monthheader = month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text
        yearheader = month_placehold4.find_element(By.CSS_SELECTOR, "#year").text
        oncorrectmonth = False
        if months[info.month] == monthheader:
            oncorrectmonth = True   
        while not oncorrectmonth:
            btn_nextmonth.click()
            monthheader = month_placehold4.find_element(By.CSS_SELECTOR, "#monthHeader").text
            if months[info.month] == monthheader:
                oncorrectmonth = True
        
        # get and press non-passholder day
        day_placehold1 = driver.find_element(By.CSS_SELECTOR, "awakening-calendar")
        day_placehold2 = day_placehold1.shadow_root
        day_placehold3 = day_placehold2.find_element(By.CSS_SELECTOR, "wdat-calendar")
        if info.month + 1 == currentmonth:
            day_placehold4 = "wdat-date[" + str(info.day - currentday + 1) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        else:
            day_placehold4 = "wdat-date[" + str(info.day - 1) + "]"
            button = day_placehold3.find_element(By.XPATH, day_placehold4)
        button.click()

    else: #sets up passholder

        #selects new page passholder reservation page
        placehold1 = driver.find_element(By.TAG_NAME,"awakening-selector")
        placehold2 = placehold1.shadow_root
        btn_themeparktickets = placehold2.find_element(By.CSS_SELECTOR, "[name=passholder]")
        btn_themeparktickets.click()
        driver.implicitly_wait(5)



# ------------------------- B O D Y -------------------------
path = Service("/Applications/chromedriver") # path where chromedriver lies
driver = webdriver.Chrome(path)

# Populates as many UserInfo's as user desires to be queried
print('Please enter however many dates and parks you would like to search for.')
numofdesireddates = 0
infodesired = [] # [info1, info2, info3, .....]
blockedout = [] # [info4, info8, info10, ...] used to skip verified blockout dates. 

# populates class
while True:
    opensite('https://disneyworld.disney.go.com/availability-calendar')
    tabID = driver.current_window_handle
    numofdesireddates += 1
    name = "info" + str(numofdesireddates)
    tickettype = gettickettype()
    month, day, year = getdate()
    park = getpark()
    if tickettype == 3:
        passtype = getpasstype()
    else:
        passtype = 0   

    name = UserInfo(tickettype, month, day, year, park, passtype, tabID)
    infodesired.append(name)
    name.printinfo()

    again = input('\nWould you like to add another day? (input \"Y\" to add another day, input any other key to continue) ----> ')
    if again == "Y" or again == "y":
        driver.switch_to.new_window('tab')
        continue
    else:
        break

try:
    print("press ctrl-c ('^C') to terminate")
    while True:
        for info in infodesired: 
            if info in blockedout: # skips blocked out dates
                continue 
            availability = getavail(info)
            if availability == 2:
                blockedout.append(info)
except KeyboardInterrupt:
    pass

driver.quit()

