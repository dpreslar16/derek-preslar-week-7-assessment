

import datetime
import json
from bs4 import BeautifulSoup
#from numpy import full
import requests
from dataclasses import dataclass


#used for web scraping
def getHTML(url):
    response = requests.get(url)
    return response.text

#declaring class for holidays
class Holiday:
      
    def __init__(self,name:str, year:int, month:int, day:int):
        #Your Code Here        
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.holiday_date = datetime.date(year, month, day)
    
    def __repr__(self):
        return '%s, %s' % (self.name, self.holiday_date)
                  
#Holiday list class declared
class HolidayList: 
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self, holidayObj: Holiday):
        self.innerHolidays.append(holidayObj)
        print("We've added your holiday: " + str(holidayObj.name) + " " + str(holidayObj.holiday_date))

    def __repr__(self):
        for i in self.innerHolidays:
            return '%s, %s' % (i.name, i.holiday_date)

    def findHoliday(self, HolidayName: str, holidayyear: int, holidaymonth: int, holidayday: int):
        for i in self.innerHolidays:
            if i.name == HolidayName and i.holiday_date == datetime.date(holidayyear, holidaymonth, holidayday):
                return i
        
    def removeHoliday(self, HolidayName: str, holidayyear: int, holidaymonth: int, holidayday: int):
        holiday_on_list = False
        for i in self.innerHolidays:
            if i.name == HolidayName and i.holiday_date == datetime.date(holidayyear, holidaymonth, holidayday):
                self.innerHolidays.remove(i)
                print("The holiday has been removed.")
                holiday_on_list = True

        if holiday_on_list == False: print("The holiday you entered is not on the list.")
    
    def scrapeHolidays(self, a_year: int):
        html = getHTML("https://www.timeanddate.com/holidays/us/" +str(a_year)+ "?hol=43122559")
        soup = BeautifulSoup(html,'html.parser')

        dates_1 = soup.find_all('th', attrs={'class':'nw'})             #holiday dates
        dates_current = []
        for i in dates_1:
            dates_current.append(str(i)[str(i).index(">")+1:str(i).index("<",1)])
        dates_months = []
        dates_days = []
        for i in dates_current:
            dates_days.append(i.split(" ")[1])
            dates_months.append(i.split(" ")[0])
        dates_months_nums = []
        for i in dates_months:
            if i == 'Jan': dates_months_nums.append(1)
            elif i == 'Feb': dates_months_nums.append(2)
            elif i == 'Mar': dates_months_nums.append(3)
            elif i == 'Apr': dates_months_nums.append(4)
            elif i == 'May': dates_months_nums.append(5)
            elif i == 'Jun': dates_months_nums.append(6)
            elif i == 'Jul': dates_months_nums.append(7)
            elif i == 'Aug': dates_months_nums.append(8)
            elif i == 'Sep': dates_months_nums.append(9)
            elif i == 'Oct': dates_months_nums.append(10)
            elif i == 'Nov': dates_months_nums.append(11)
            elif i == 'Dec': dates_months_nums.append(12)

        names_1 = soup.find_all('a', attrs={'href': lambda L: L and (L.startswith('/holidays/') or L.startswith('/calendar/') or L.startswith('/time/'))})         #holiday names
        names_1 = names_1[27:]
        names_current = []
        for i in names_1:
            names_current.append(str(i)[str(i).index(">")+1:str(i).index("<",1)])
        names_current = names_current[0:-13]

        for i in range(0,len(names_current)):
            if self.findHoliday(names_current[i], a_year, dates_months_nums[i], int(dates_days[i])) is None:
                self.addHoliday(Holiday(names_current[i], a_year, dates_months_nums[i], int(dates_days[i])))

    def numHolidays(self):
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year:int, week_number:int):
        weekly_holidays = list(filter(lambda x: x.holiday_date.isocalendar()[1] == week_number and x.holiday_date.isocalendar()[0] == year, self.innerHolidays))
        return weekly_holidays

    def displayHolidaysInWeek(self, week_num:int, year:int):
        week_holidays = self.filter_holidays_by_week(year, week_num)
        for i in week_holidays:
            print(i)

def getWeather():   #grabs weather for next 7 days
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    querystring = {"cnt":"7","units":"imperial","id":"4406271"}
    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": "af04faea85msh7e568f89b05c0eep1ee791jsndd1c6db692e8"
    }
    weather_data = requests.request("GET", url, headers=headers, params=querystring).json()
    weather_list = []
    for i in weather_data['list']:
        for j in i['weather']:
#            print(j['description'])
            weather_list.append(j['description'])
    return weather_list

#web scraping the years:
full_holiday_list = HolidayList()
full_holiday_list.scrapeHolidays(2020)
full_holiday_list.scrapeHolidays(2021)
full_holiday_list.scrapeHolidays(2022)
full_holiday_list.scrapeHolidays(2023)
full_holiday_list.scrapeHolidays(2024)

#writing to json file
full_holiday_data = {}
for i in range(0, len(full_holiday_list.innerHolidays)):
    full_holiday_data[str(full_holiday_list.innerHolidays[i].holiday_date)[0:4] + ' ' + str(full_holiday_list.innerHolidays[i].name)] = str(full_holiday_list.innerHolidays[i].holiday_date)
with open('holiday_data.json', 'w') as outfile:
    json.dump(full_holiday_data, outfile)


#Main program
print("Holiday Management\n===================\nThere are currently " + str(len(full_holiday_list.innerHolidays)) + " holidays stored in the system.")

run_management = True
while run_management == True:
    user_input = input("Holiday Menu\n================\n1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit\n")
    if user_input.lower() in ['1.', '1', 'add a holiday']:
        print('Add a Holiday\n=============\n')
        try:
            user_holiday_name = input("Holiday: ")
            user_holiday_date_year = int(input('Date Year: '))
            user_holiday_date_month = int(input('Date Month: '))
            user_holiday_date_day = int(input('Date Day: '))
            full_holiday_list.addHoliday(Holiday(user_holiday_name,user_holiday_date_year,user_holiday_date_month,user_holiday_date_day))
        except:
            print("Invalid input- please input integers for the year, month, and date next time.")
    elif user_input.lower() in ['2.', '2', 'remove a holiday']:
        print('Remove a Holiday\n=============\n')
        try:
            user_holiday_name = input("Holiday Name: ")
            user_holiday_date_year = int(input('Date Year: '))
            user_holiday_date_month = int(input('Date Month: '))
            user_holiday_date_day = int(input('Date Day: '))
            full_holiday_list.removeHoliday(Holiday(user_holiday_name,user_holiday_date_year,user_holiday_date_month,user_holiday_date_day))
        except:
            print("Invalid input- please input integers for the year, month, and date next time.")
    elif user_input.lower() in ['3.', '3', 'save holiday list']:
        print('Save Holiday List\n=============\n')
        new_input = str(input('Are you sure you want to save your changes? [y/n]: '))
        if new_input.lower() in ['yes', 'y']:
            full_holiday_data = {}
            empty_data = {}
            for i in range(0, len(full_holiday_list.innerHolidays)):
                full_holiday_data[str(full_holiday_list.innerHolidays[i].holiday_date)[0:4] + ' ' + str(full_holiday_list.innerHolidays[i].name)] = str(full_holiday_list.innerHolidays[i].holiday_date)
            with open('holidays.json', 'w') as outfile:
                json.dump(empty_data, outfile) #taking out the previous times the json has been added to
                json.dump(full_holiday_data, outfile)
            print('Success:\nYour changes have been saved.')
        elif new_input.lower() in ['no', 'n']:
            print('Canceled:\nHoliday list file save canceled.')
        else:
            print("I did not recognize your response: going back to menu")
    elif user_input.lower() in ['4.', '4', 'view holidays']:
        print('View Holidays\n=============\n')
        try:
            user_holiday_date_year = int(input('Which Year?: '))
            user_holiday_date_week = input('Which week? #[1-52, Leave blank for the current week]: ')
            if user_holiday_date_week == '' and user_holiday_date_year == datetime.date.today().isocalendar()[0]: 
                weather_or_not = str(input("Would you like to see this week's weather? [y/n]: "))
                if weather_or_not.lower() in ['yes', 'y']:
                    print("These are the holidays for the next seven days: ")
                    next_seven_days = []
                    current_date = datetime.date.today()
                    for i in range(0,7):
                        next_seven_days.append(current_date+datetime.timedelta(days=i))
                    current_week_holidays = list(filter(lambda x: x.holiday_date in next_seven_days, full_holiday_list.innerHolidays))
                    current_week_weather_list = getWeather()
                    for i in range(0,7):
                        for j in current_week_holidays:
                            if j.holiday_date == next_seven_days[i]:
                                print("Date: " + str(next_seven_days[i]) + " Holiday: " + str(j.name) + " Weather: " + str(current_week_weather_list[i])) 
                elif weather_or_not.lower() in ['no', 'n']:
                    print("\nThese are the holidays for the next seven days: " )
                    full_holiday_list.displayHolidaysInWeek(user_holiday_date_week, user_holiday_date_year)
                else:
                    print("Invalid input- returning to menu")
            else:
                print("\nThese are the holidays for " +str(user_holiday_date_year) + "week #" + str(user_holiday_date_week) +':')
                full_holiday_list.displayHolidaysInWeek(int(user_holiday_date_week), user_holiday_date_year)
        except:
            print("Invalid input- please input a valid year and week.")
    elif user_input.lower() in ['5.', '5', 'exit']:
        print('Exit\n=====')
        new_input = str(input("Are you sure you want to exit? [y|n] "))
        if new_input.lower() in ['yes', 'y']:
            print("Are you sure you want to exit?\nYour changes will be lost.")
            another_input = str(input('[y|n] '))
            if another_input.lower() in ['yes', 'y']:
                print("Goodbye!")
                run_management = False
            elif another_input.lower() in ['no','n']:
                print("Returning to main menu.\n")
            else:
                print("Invalid input- returning to menu.")
        elif new_input.lower() in ['no', 'n']:
            print("Returning to main menu.\n")
        else:
            print("Invalid input- returning to menu.")
    else:
        print("Invalid input, please try again.")


