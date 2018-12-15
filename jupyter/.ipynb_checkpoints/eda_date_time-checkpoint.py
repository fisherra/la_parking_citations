import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# load individual sets
la_ticket_2017_1 = pd.read_csv("~/Documents/data_science/py_la_tickets/input/la_ticket_2017_1.csv")
la_ticket_2017_2 = pd.read_csv("~/Documents/data_science/py_la_tickets/input/la_ticket_2017_2.csv")
la_ticket_2017_3 = pd.read_csv("~/Documents/data_science/py_la_tickets/input/la_ticket_2017_3.csv")
la_ticket_2017_4 = pd.read_csv("~/Documents/data_science/py_la_tickets/input/la_ticket_2017_4.csv")


# combine dataset
la_ticket_2017 = pd.concat([la_ticket_2017_1, la_ticket_2017_2, la_ticket_2017_3, la_ticket_2017_4])

# view dataset
la_ticket_2017.head()

la_ticket_2017.hist('Day of Year', bins=365, color = 'seagreen')

plt.rcParams['figure.figsize'] = (10,8)

sum_fine_by_day = la_ticket_2017.groupby('Day of Year')['Fine amount'].sum()

sum_fine_by_day.plot.density(color = 'lightslategray')
plt.rcParams['figure.figsize'] = (10,8)

# create a ticket count for each day
tickets_by_day = la_ticket_2017.groupby('Day of Year').count()
# create a stand alone series
ticket_by_day = tickets_by_day.iloc[:,0]
# show created series
ticket_by_day.head()


i = 1 
sunday = []

# while counter is within dataset
while i <= len(ticket_by_day):
    # extract element and append to results array
    sunday.append(ticket_by_day[i])
    # proceed to next week
    i = i + 7

# format and display results
np.hstack(sunday)

# define the function name
def by_weekday(day):
    # set the counter equal to the arguement
    i = day
    # create an empty array for results
    day = []
    
    # apply while loop to extract data
    while i <= 365:
        day.append(ticket_by_day[i])
        i = i + 7
    
    # format data
    np.hstack(day)
    day = pd.Series(day)
    
    # return results
    return(day)


# testing the function on Sunday
sunday = by_weekday(1)
sunday.head()

monday = by_weekday(2)
tuesday = by_weekday(3)
wednesday = by_weekday(4)
thursday = by_weekday(5)
friday = by_weekday(6)
saturday = by_weekday(7)


ticket_by_weekday = pd.concat([sunday, monday, tuesday, wednesday, thursday, friday, saturday], axis = 1)
ticket_by_weekday.columns = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
ticket_by_weekday.head()


ticket_by_weekday.plot()
plt.rcParams['figure.figsize'] = (10,8)


ticket_by_weekday.boxplot()
plt.rcParams['figure.figsize'] = (10,8)


import warnings
warnings.filterwarnings('ignore')

# drop the 53rd sunday (removing NA's) to make sample sizes equal
ticket_by_weekday = ticket_by_weekday.drop([52,])


# t-test Sunday and Monday
stats.ttest_ind(ticket_by_weekday['Sunday'], ticket_by_weekday['Monday'])


# initial day to compare
for day in range(7):
    # second day for the comparison
    for day_2 in range(day+1, 7):
        # print the days being compared
        print(list(ticket_by_weekday)[day], list(ticket_by_weekday)[day_2])
        # conduct the t-test
        print(stats.ttest_ind(ticket_by_weekday.iloc[:,day], ticket_by_weekday.iloc[:,day_2]))
        
        
la_ticket_2017.hist('Month', bins=12, color = 'indigo', edgecolor='black', linewidth=1)
plt.rcParams['figure.figsize'] = (10,8)


la_ticket_2017.hist('Day', bins=31, color = 'firebrick', edgecolor = 'black')
plt.rcParams['figure.figsize'] = (10,8)

la_ticket_2017[la_ticket_2017['Month'] != 2].hist('Day', bins = 31, color = 'firebrick', edgecolor = 'black')
plt.rcParams['figure.figsize'] = (10,8)

la_ticket_2017.hist('Issue time', range=(0, 2400), bins=200, color = 'forestgreen')
plt.rcParams['figure.figsize'] = (10,8)


la_ticket_2017.hist('Issue time', range=(800, 859), bins=60, color = 'forestgreen')
plt.rcParams['figure.figsize'] = (10,8)


# these are the holidays that came to my mind and their dates in 2017
holidays = pd.Series(['2017/01/01',
                      '2017/01/16',
                      '2017/02/14',
                      '2017/05/29',
                      '2017/07/04',
                      '2017/09/04',
                      '2017/10/31',
                      '2017/11/10',
                      '2017/11/23',
                      '2017/12/25'],
                     index = ['New Years Day',
                              'MLK Day',
                              'Valentines Day',
                              'Memorial Day',
                              'Independence Day',
                              'Labor Day',
                              'Halloween',
                              'Veterans Day',
                              'Thanksgiving',
                              'Christmas']
                    )

holidays


# change the date format to day of the year for easy use
holidays_date = pd.to_datetime(holidays, format='%Y/%m/%d')
holidays_doy = holidays_date.dt.dayofyear
holidays_doy



# create the empty dataframe, named after each holiday
holiday_tickets = pd.DataFrame(columns=['Number of Tickets'], index = holidays_doy.index)


# set a counter equal to zero
i = 0

# for each of the hoidays
while i <= len(holidays_doy) - 1:
    # sum the number of tickets given on that day and save the output to the new DataFrame
    holiday_tickets.iloc[i, ] = sum(la_ticket_2017['Day of Year'] == holidays_doy.iloc[i])
    # move to the next holiday
    i = i + 1
    
    
holiday_tickets.plot(kind = 'barh', color = 'slateblue').invert_yaxis()
plt.rcParams['figure.figsize'] = (10,8)


holiday_tickets


ticket_by_day.min()

