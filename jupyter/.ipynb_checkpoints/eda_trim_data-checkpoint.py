import numpy as np
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

# return file size in GB
os.path.getsize('input/parking_citation.csv') / (1*10**9)

# read full data csv from input folder
la_ticket_full = pd.read_csv("~/Documents/data_science/py_la_tickets/input/parking_citation.csv")

# return shape of newly created dataframe
la_ticket_full.shape

# check out what the dataframe looks like
la_ticket_full.head()

# pull Issue Date variable from the main Dataframe to create a Pandas Series of just date-times
la_ticket_issue = la_ticket_full['Issue Date']
la_ticket_issue.head()

# how many of the issue date variables contain '2017'
sum(la_ticket_issue.str.contains('2017') == True)

# how many of the issue date variables contain '2017'
sum(la_ticket_issue.str.contains('2017') == True)

# create a True / False list for indexing the data
la_ticket_2017_index = la_ticket_issue.str.contains('2017')
la_ticket_2017_index.head()

# apply the index to the full dataframe to create a new '2017' Dataframe
la_ticket_2017 = la_ticket_full[la_ticket_2017_index]
# make sure length of dataset matches previously determined 'sum' of 2017 strings
len(la_ticket_2017)

# ensure variables remain untouched
la_ticket_2017.head()

# first issue date in the new 2017 dataset
min(la_ticket_2017['Issue Date'])

# last issue date in the new 2017 dataset
max(la_ticket_2017['Issue Date'])

# create a new Series to work with outside of the main Dataframe
date_time = la_ticket_2017['Issue Date']
# check what data type 'Issue Date' is stored as
type(date_time.iloc[0,])

# split string into date and time based on the space between them
date_time_split = date_time.str.split(' ', n=1, expand = True)
date_time_split.head()


# use only date, as we have accurate issue times in another dataset variable
date = date_time_split.iloc[:,0]
date.head()


# convert datatype to date-time using pandas function
date = pd.to_datetime(date, format='%Y/%m/%d')
date.head()


# use built-in datetime functionality 'dt' to create 3 new variables
day_of_year = date.dt.dayofyear
month = date.dt.month
day = date.dt.day

# create a new_date dataframe, consisting of the date, month, day, and day of the year
new_date = pd.concat([date, month, day, day_of_year], axis = 1)
new_date.columns = ['Date', 'Month', 'Day', 'Day of Year']
new_date.head()


# Copy the new_date variables into the original dataframe, la_ticket_2017
la_ticket_2017['Month'] = new_date['Month']
la_ticket_2017['Day'] = new_date['Day']
la_ticket_2017['Day of Year'] = new_date['Day of Year']

# view la_ticket_2017 dataframe
la_ticket_2017.head()

# drop variables, create reduced dataframe
la_ticket_2017_reduced = la_ticket_2017.drop(['Ticket number', 'Issue Date', 'Marked Time',
                                              'Plate Expiry Date', 'VIN', 'Body Style',
                                              'Route', 'Agency'],
                                             axis=1)

# view reduced dataframe
la_ticket_2017_reduced.head()


# unique plates
pd.unique(la_ticket_2017_reduced['RP State Plate'])

# see if we have 50 entries for the 50 states
len(pd.unique(la_ticket_2017_reduced['RP State Plate']))

# how many different makers?
len(pd.unique(la_ticket_2017_reduced['Make']))

# unique car colors
pd.unique(la_ticket_2017_reduced['Color'])

len(pd.unique(la_ticket_2017_reduced['Violation code']))

len(pd.unique(la_ticket_2017_reduced['Violation Description']))

sum(la_ticket_2017_reduced['Meter Id'].str.contains('N') == False) / len(la_ticket_2017_reduced)
#/ len(la_ticket_2017_reduced)

# write full reduced dataframe
la_ticket_2017_reduced.to_csv('input/la_ticket_2017.csv')

# check size again
os.path.getsize('input/la_ticket_2017.csv') / (1*10**9)
# still too big, must be < 100 mb

# create 4 sequences of 3 months for indexing the reduced dataset
seq_1 = ['01','02','03']
seq_2 = ['04','05','06']
seq_3 = ['07','08','09']
seq_4 = ['10','11','12']

# create the index
index_1 = la_ticket_2017_reduced['Month'].isin(seq_1)
index_2 = la_ticket_2017_reduced['Month'].isin(seq_2)
index_3 = la_ticket_2017_reduced['Month'].isin(seq_3)
index_4 = la_ticket_2017_reduced['Month'].isin(seq_4)


# apply index to separate dataset into 4 pieces
la_ticket_2017_1 = la_ticket_2017_reduced[index_1]
la_ticket_2017_2 = la_ticket_2017_reduced[index_2]
la_ticket_2017_3 = la_ticket_2017_reduced[index_3]
la_ticket_2017_4 = la_ticket_2017_reduced[index_4]

# save the four pieces
la_ticket_2017_1.to_csv('la_ticket_2017_1.csv')
la_ticket_2017_2.to_csv('la_ticket_2017_2.csv')
la_ticket_2017_3.to_csv('la_ticket_2017_3.csv')
la_ticket_2017_4.to_csv('la_ticket_2017_4.csv')

# check size of the jan-mar piece
os.path.getsize('la_ticket_2017_1.csv') / (1*10**9)

# check size of the second piece
os.path.getsize('la_ticket_2017_2.csv') / (1*10**9)

# check size of the third piece
os.path.getsize('la_ticket_2017_3.csv') / (1*10**9)

# check size of the final piece
os.path.getsize('la_ticket_2017_4.csv') / (1*10**9)
