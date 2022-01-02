# Sebastian Rowe
# Disney World Reservation Assistant

# "You are a beloved son of the father" = True - Preston Richter
# "^^ this is true" - Sebastian Rowe

from selenium import webdriver
import datetime 
import time

def opensite(site):
    driver.get(site) # opens website
    print("webpage title --> \"" + driver.title + "\"\n") # prints title of website
def expand_shadow_element(element): # OUT OF DATE FOR SELENIUM 4, WILL NOT WORK!!!!!!
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root
def getdesiredpark():
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
    print("What park would you like to visit?\n")
    print("[1] - " + parks[0])
    print("[2] - " + parks[1])
    print("[3] - " + parks[2])
    print("[4] - " + parks[3])
    park = int(input("\nType a number 1-4 and hit Enter ----> ")) - 1
    if (park <= 3 and park >= 0):
        print("You chose --> "+ parks[park])
    else:
        print("INVALID INPUT -- PLEASE INPUT A NUMBER BETWEEN 1 and 4")
        getdesiredpark()
        return park
def pass_park_select(park):
        getting_park = driver.find_element_by_tag_name("com-park-admission-calendar-park-selection")
        getting_park_2 = expand_shadow_element(getting_park)

        if park == 1:
            park_button = getting_park_2.find_element_by_id("WDW_MK")
            park_button.click()
        elif park == 2:
            park_button = getting_park_2.find_element_by_id("WDW_AK")
            park_button.click()
        elif park == 3:
            park_button = getting_park_2.find_element_by_id("WDW_EP")
            park_button.click()
        else:
            park_button = getting_park_2.find_element_by_id("WDW_HS")
            park_button.click()
def getdesiredavailability(chosen_park, date):
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
    avail1 = driver.find_element_by_tag_name("awakening-availability-information")
    avail2 = expand_shadow_element(avail1)
    avail3 = avail2.find_element_by_tag_name("div")
    xpath = "div[" + str(chosen_park + 1) + "]"
    parkcontainer = avail3.find_element_by_xpath(xpath)
    available = parkcontainer.get_attribute("class")
    if available == "available":
        print(str(parks[chosen_park]) + " IS available on " + str(date[0]) + "/" + str(date[1]) + "/" + str(date[2]) +"! --- " + str(time.ctime()))
        return 1
    else:
        print(str(parks[chosen_park]) + " is NOT available on " + str(date[0]) + "/" + str(date[1]) + "/" + str(date[2]) +"! --- " + str(time.ctime()))
        return 0
def selectcategory():

    a = int(input("Select a ticket category:\n[1] - Theme Park Tickets\n[2] - Select Resort Hotels\n[3] - Annual Passes\ninput --> "))
    one = driver.find_element_by_xpath("/html/body/app-root/div/app-availability-selector/awakening-selector")
    two = expand_shadow_element(one) # first shadow root
    three = two.find_element_by_tag_name("dprd-radio-group")
    ispass = False

    if a == 1:
        four = three.find_element_by_name("tickets")
        four.click()
    elif a == 2:
        four = three.find_element_by_name("resort")
        four.click()
    elif a == 3:
        four = three.find_element_by_name("passholder")
        four.click() #new webpage
        driver.implicitly_wait(10)
        pass_select()
        ispass = True
    else:
        print("Input Invalid -- Please select a corresponding Number between 1 and 3")
        selectcategory()  

    return ispass
def pass_selectdate(date, park):
    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    currentday  = datetime.datetime.now().day
    currentmonth = datetime.datetime.now().month

    # gets date info from user
    if date[0] == 0:
        date[0] = int(input("What month would you like to go?  (1 - 12) --> "))
        date[1] = int(input("What day would you like to go? (1 - ~31) --> "))
        currentday  = datetime.datetime.now().day
        currentmonth = datetime.datetime.now().month
        date[2] = int(input("What year would you like to go? --> "))
        print('You want to go on ' + months[date[0] - 1]  + ' ' + str(date[1]) + ', ' + str(date[2]) + '.')

        # gets and presses correct non pass month button
        monf_1 = driver.find_element_by_xpath("/html/body/app-root/div/app-availability-calendar/awakening-calendar")
        monf_2 = expand_shadow_element(monf_1)
        monf_3 = monf_2.find_element_by_id("calendarContainer")
        monf_4 = monf_3.find_element_by_tag_name("wdat-calendar")
        monf_5 = expand_shadow_element(monf_4)
        monf_button = monf_5.find_element_by_id("nextArrow")

        monthheader = monf_5.find_element_by_id("monthHeader").text

        oncorrectmonth = False
        if months[date[0] - 1] == monthheader:
            oncorrectmonth = True
        
        while not oncorrectmonth:
            monf_button.click()
            monthheader = monf_5.find_element_by_id("monthHeader").text
            if months[date[0] - 1] == monthheader:
                oncorrectmonth = True
        
        # gets and presses correct day button
        dayf_1 = driver.find_element_by_xpath("/html/body/app-root/div/app-availability-calendar/awakening-calendar")
        dayf_2 = expand_shadow_element(dayf_1)
        dayf_3 = dayf_2.find_element_by_tag_name("wdat-calendar")
        dayf_4 = dayf_3.find_elements_by_tag_name("wdat-date")
        if date[0] == currentmonth:
            button = dayf_4[date[1] - currentday]
        else:
            button = dayf_4[date[1] - 1]
        driver.implicitly_wait(10) # waits for proccesses to finish
        button.click()

    return date
def pass_select():
        b = int(input("\nSelect your pass:\n[1] - Incredipass\n[2] - Sorcerer Pass\n[3] - Pirate Pass\n[4] - Pixie Dust Pass\ninput --> "))

        pone = driver.find_element_by_xpath("/html/body/app-root/div/app-layout/div/div[2]/div[1]/div/app-blockout-dates-page/div/div[2]/app-section-pass-selection/div/com-park-admission-calendar-pass-selection")
        ptwo = expand_shadow_element(pone)
        
        if b == 1:
            pthree = ptwo.find_element_by_id("disney-incredi-pass")
            pthree.click()
        elif b == 2:
            pthree  = ptwo.find_element_by_id("disney-sorcerer-pass")
            pthree.click()
        elif b == 3:
            pthree = ptwo.find_element_by_id("disney-pirate-pass")
            pthree.click()
        elif b == 4:
            pthree = ptwo.find_element_by_id("disney-pixie-dust-pass")
            pthree.click()
        else:
            print("Input Invalid -- Please select a corresponding Number between 1 and 4")
            pass_select()   
def pass_getdesiredavailability(chosen_park, date):
    parks = ['Magic Kingdom', 'Animal Kingdom', 'Epcot', 'Hollywood Studios']
    currentday  = datetime.datetime.now().day
    currentmonth = datetime.datetime.now().month

    day1 = driver.find_element_by_xpath("/html/body/app-root/div/app-layout/div/div[2]/div[1]/div/app-blockout-dates-page/div/div[2]/div[4]/app-section-calendar-container/div/com-park-admission-calendar-container")
    day2 = expand_shadow_element(day1)
    day3 = day2.find_element_by_id("admissionCalendar")
    day4 = expand_shadow_element(day3)
    day5 = day4.find_element_by_tag_name("com-calendar-date")
    if date[0] == currentmonth:
        selectedday = day5[date[1] - currentday]
    else:
        selectedday = day5[date[1] - 1]

    selecteddayclass = selectedday.get_attribute("class")

    if selecteddayclass == "all green":
        print(str(parks[chosen_park]) + " IS available on " + str(date[0]) + "/" + str(date[1]) + "/" + str(date[2]) +"! --- " + str(time.ctime()))
        return 1
    else:
        print(str(parks[chosen_park]) + " is NOT available on " + str(date[0]) + "/" + str(date[1]) + "/" + str(date[2]) +"! --- " + str(time.ctime()))
        return 0
def selectdate(date, park):
    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    currentday  = datetime.datetime.now().day
    currentmonth = datetime.datetime.now().month

    # gets date info from user
    if date[0] == 0:
        date[0] = int(input("What month would you like to go?  (1 - 12) --> "))
        date[1] = int(input("What day would you like to go? (1 - ~31) --> "))
        currentday  = datetime.datetime.now().day
        currentmonth = datetime.datetime.now().month
        date[2] = int(input("What year would you like to go? --> "))
        print('You want to go on ' + months[date[0] - 1]  + ' ' + str(date[1]) + ', ' + str(date[2]) + '.')
    
   
    #gets and presses correct pass month button
    pass_monf_1 = driver.find_element_by_id("calendar0")
    pass_monf_2 = expand_shadow_element(pass_monf_1)
    monf_button = pass_monf_2.find_element_by_id("nextArrow")
    monthheader = pass_monf_2.find_element_by_id("monthHeader").text

    oncorrectmonth = False
    if months[date[0] - 1] == monthheader:
        oncorrectmonth = True
        
    while not oncorrectmonth:
        monf_button.click()
        monthheader = pass_monf_2.find_element_by_id("monthHeader").text
        if months[date[0] - 1] == monthheader:
            oncorrectmonth = True

# ---- BODY ----
date = [0,0,0]
park = 0
path = "/Applications/chromedriver" # path where chromedriver lies
driver = webdriver.Chrome(path) 
opensite("https://disneyworld.disney.go.com/availability-calendar/")
ispass = selectcategory()
park = getdesiredpark()
isavail = False
if ispass == True:
    pass_park_select(park)
    date = pass_selectdate(date,park)
    pass_getdesiredavailability(park,date)
    while not isavail:
        driver.refresh()
        driver.implicitly_wait(10)
        selectdate(date)
        driver.implicitly_wait(10)
        a = pass_getdesiredavailability(park, date)

        if a == 1:
            isavail = True
        else:
            isavail = False
else:
    date = selectdate(date, park)
    getdesiredavailability(park,date)
    while not isavail:
        driver.refresh()
        driver.implicitly_wait(10)
        selectdate(date)
        driver.implicitly_wait(10)
        a = getdesiredavailability(park, date)

        if a == 1:
            isavail = True
        else:
            isavail = False
    
