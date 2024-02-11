############################################################################

### library imports ########################

############################################################################

import time
import pandas as pd
import numpy as np
import regex as re

############################################################################

### CONSTANTS ########################

############################################################################

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# lists for valid inputs to be validated against
CITIES = ["chicago", "new york", "washington"]

OPTIONS = ["month", "day", "both", "none"]

MONTHS = ["january", "february", "march", "april", "may",
          "june"]

DAYS = ["1", "2", "3", "4", "5", "6", "7"]

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
             "Saturday", "Sunday"]

START_INDEX = 0 # constant to indicate beginning index 

FIVE_ROWS = 5 # constant to iterate for next 5 rows when printing dataframe for user

MIN_IN_HOUR = 60


############################################################################

### HELPER FUNCTIONS FOR VALIDATION PROCESSING ########################

############################################################################

"""
The following functions are to assist with the validation of the inputs
received from users when they use the progam

"""

def pre_process(user_input):
    """ 
    Pre process the inputs from the user
    
    Args:
        user_input (str): the input that the user provides
        
    Returns:
        clean_input (str): the cleaned string from input that the user provides
    
    """
    
    ## set all to lower case
    user_input = str(user_input).strip().lower()
    
    ## then, let's remove all symbols and spaces from the input
    
    # regex to identify non-word chars
    non_word_chars = re.compile(r'[^a-zA-Z\s]') 
    
    # clean the string
    clean_input = non_word_chars.sub('', user_input)
    
    return clean_input

def get_valid_input(prompt, valid_inputs):
    """
    Get valid user input based on a given prompt and list of valid options.

    Args:
        prompt (str): The prompt to display to the user.
        valid_inputs (list): List of valid input options.

    Returns:
        str: Valid user input.
    """
    
    # loop to check for valid input. return if valid, ask again if not
    while True:
        user_input = input(prompt)
        
        # check validity, include digit checks for day inputs
        if user_input in valid_inputs or user_input.isdigit() and int(user_input) in valid_inputs:
            return user_input
        
        # ask user again, presenting them with the valid options
        else:
            print(f"Sorry, that input was invalid. Please choose from {', '.join(valid_inputs)}.\n")
            
def get_first_5_rows(df):
    """
    This function shows the first 5 rows if the yser wants to see it.

    Args:
        (Pandas Dataframe) df: The dataframe to display the first 5 rows of.

    """
    
    # while loop to get input and show data if they would like. 
    # we use an index to keep track of where in the dataframe we are 
    # and use it to show the next 5 rows at a time
    
    curr_row = START_INDEX
    first_print = True
    while True:
        
        # show the first 5 rows
        if first_print:
            show_data = input('Would you like to see the first 5 rows of your filtered data? Please answer yes or no.\n').lower()
            first_print = False
            
        # or show the next 5 rows
        else:
            show_data = input('Would you like to see the next 5 rows of your filtered data? Please answer yes or no.\n').lower()
        
        # pre process the input
        show_data = pre_process(show_data)
        
        # execute the user's request to see or not to see the data
        if show_data == 'yes':
            print(df.iloc[curr_row:curr_row+FIVE_ROWS])
            curr_row += FIVE_ROWS
        elif show_data == 'no':
            break
        
        # handler for invalid inputs
        else:
            print("Sorry, that input is invalid. Please answer 'yes' or 'no'.")


############################################################################

### CORE FUNCTIONS PROVIDED BY UDACITY ########################

############################################################################

def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # initialise blank variables. this will handle 
    # if the user only selects for month or day only
    city = False
    option = False
    month = False
    day = False
    
    # get user input for the city they want to see
    city = get_valid_input("Would you like to see data for Chicago, New York, or Washington?\n", CITIES)
    
    # see what filer the user would like to use
    option = get_valid_input("Would you like to filter the data by month, day, both or not at all?\n", OPTIONS)

   # get user input for the month they want to view
    if option == "month" or option == "both":
       month = get_valid_input("Which month - January, February, March, April, May, or June?\n", MONTHS)

   # get user input for the day of the week
    if option == "day" or option == "both":
        day = get_valid_input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please enter an integer (i.e., 1= Sunday)\n", DAYS)

    print('-'*40)
    
    # convert month and day to workable data types for further use
    if month:
        month = MONTHS.index(month) + 1
    
    if day:
        day = int(day) - 1
    
        
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (Pandas DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # first, we read in the relevant csv for the city we are interested in
    df = pd.read_csv(CITY_DATA[city])
    
    
    # then, we convert the start and end time columns to datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    
    # then, we filter the data as per the users' preference
    # day of week function sourced from: https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date
    if day != False:
        df = df[(df['Start Time'].dt.dayofweek == day) & 
                (df['End Time'].dt.dayofweek == day)]

    if month != False:
        df = df[(df['Start Time'].dt.month == month) & 
                (df['End Time'].dt.month == month)]

    return df, month, day


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (Pandas DataFrame) df - the dataframe containing the cyclubg data that contains the travel information
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    max_month_index = df['Start Time'].dt.month.value_counts().idxmax()
    max_month = MONTHS[max_month_index - 1].capitalize()
    print(f'The most common month in this dataset is {max_month}')
    

    # display the most common day of week
    days_count = df['Start Time'].dt.dayofweek.value_counts()
    max_day = DAY_NAMES[days_count.idxmax()]
    print(f'The most common day in this dataset is {max_day}')

    # display the most common start hour
    hours_count = df['Start Time'].dt.hour.value_counts()
    max_hour = hours_count.idxmax()
    print(f'The most common hour in this dataset is {max_hour}')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (Pandas DataFrame) df - the dataframe containing the cyclubg data that contains the travel information.
        
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # idxmax function sourced from: https://www.w3schools.com/python/pandas/ref_df_idxmax.asp#:~:text=Definition%20and%20Usage,maximum%20value%20for%20each%20row.
    start_stn_common = df['Start Station'].value_counts().idxmax()
    print(f'The most common start station is {start_stn_common}')
    

    # display most commonly used end station
    end_stn_common = df['End Station'].value_counts().idxmax()
    print(f'The most common end station is {end_stn_common}')

    # display most frequent combination of start station and end station trip
    stn_combo = df['Start Station'] + " to " + df['End Station'].astype(str)
    combo_common = stn_combo.value_counts().idxmax()
    print(f'The most common trip made is from {combo_common}')
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (Pandas DataFrame) df - the dataframe containing the cyclubg data that contains the travel information.
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_times = df['Trip Duration']
    total_travel_time = trip_times.sum()
    print(f'The total trip time for this data is {round(total_travel_time/60, 2)} hours')
    
    # get the total travel time in hours
    total_in_days = total_travel_time/24 # assign variable for number
    
    if total_in_days > 24: # assign variable for number (HOURS IN DAY)
        print(f'This is equivalent to {round(float(total_in_days/24), 2)} days!')
    

    # display mean travel time
    mean_time = round(trip_times.mean(), 2)
    mean_mins = round(mean_time/MIN_IN_HOUR, 2)
    print(f'The average trip time was {mean_time} seconds or {mean_mins} mins.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Args:
        (Pandas DataFrame) df - the dataframe containing the cyclubg data that contains the travel information.
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print(user_counts)


    # Display counts of gender
    if city == 'washington':
        print("Washington has no data on gender")
    else:
        gender_counts = df['Gender'].value_counts(dropna = True)
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth
    
    if city == 'washington':
        print("Washington has no data on the birth year")
    
    else:
        early_year = int(df['Birth Year'].min())
        print(f'The earliest birth year of all users in this dataset is {early_year}')
        recent_year = int(df['Birth Year'].max())
        print(f'The most recent birth year of all users in this dataset is {recent_year}')
        common_year = int(df['Birth Year'].value_counts().idxmax())
        print(f'The most common birth year of all users in this dataset is {common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


############################################################################

### MAIN PROGRAM FUNCTION TO EXECUTE USER'S REQUESTS ########################

############################################################################

def main():
    while True:
        city, month, day = get_filters()
        df, month, day = load_data(city, month, day)
        get_first_5_rows(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
