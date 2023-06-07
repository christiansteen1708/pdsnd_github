"""This module explores US Bikeshare data.
It takes raw user input for specific filters for locations and times to then display calculated statistical and raw data.
"""

import time
import calendar
import pandas as pd
import numpy as np

# dictionaries with valid input
city_data = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'new york': 'new_york_city.csv',
             'newyork': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = {'january': 1, 'february': 2, 'march': 3,
          'april': 4, 'may': 5, 'june': 6, 'all': 99, 'a': 99}
days = {'monday': 0, 'tuesday': 1, 'wednesday': 2,
        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6, 'all': 99, 'a': 99}
yes_no = {'no': False, 'yes': True, 'y': True, 'n': False}


def get_input(prompt, reference_dict):
    """
    takes input from user and returns value from dictionary

    Args:
        (str) prompt - prompt to ask user for input
        (python dictionary) reference_dict - dictionary to reference user input with, asks for key
    Returns:
        reference_dict[user_input] - value from dictionary
    """

    try:
        user_input = str(input(prompt+'\n')).lower()

        while user_input not in reference_dict:
            print('Sorry... it seems like you\'re not typing a correct entry. ')
            print("Let's try again")
            user_input = str(input(prompt+'\n')).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return reference_dict[user_input]

    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    city = get_input(
        "Would you like to see data for Chicago, New York, Washington?", city_data)

    userInput = get_input(
        "Would you like to filter the data set? ([Y]es/[N]o)?", yes_no)
    if not userInput:
        print('-'*40)
        return city, 99, 99

    # get user input for month (all, january, february, ... , june)
    month = get_input(
        "Would you like to see data for a specific month (january to june) or [a]ll data?", months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input(
        "Would you like to see data for a week day(monday to sunday) or [a]ll data?", days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city-file - name of the city-csv to load
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print("Loading Dataframe...")
    start_time = time.time()  # set start time

    # load data file for city into dataframe
    df = pd.read_csv(city)

    # data wrangling; washington doesn't have gender/Birth Year column, add dummy col
    if not 'Birth Year' in df.columns or not 'Gender' in df.columns:
        df['Birth Year'] = np.nan
        df['Gender'] = np.nan

    # df['Birth Year'] = df['Birth Year'].astype(np.float64).astype('Int32')
    df['Birth Year'] = df['Birth Year'].astype('Int32')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if 0 < month < 7:
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if 0 <= day < 6:
        df = df[df['day_of_week'] == day]

    # calculate time needed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Calculating The Most Frequent Times of Travel...')
    start_time = time.time()  # set start time

    print("\nWhat are the most common month, day and hour of the data set?")

    # display the most common month
    print('\nThe most common month is:\t{}'.format(calendar.month_name[
        df['month'].mode()[0]]))

    # display the most common day of week
    print('\nThe most common day of week is:\t{}'.format(calendar.day_name[
        df['day_of_week'].mode()[0]]))

    # display the most common start hour
    print('\nThe most common hour is:\t{}'.format(
        df['hour'].mode()[0]))

    # calculate time needed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()  # set start time

    print("\nWhat are the most commonly used start stations, end stations and combinations of start/end station?")

    # display most commonly used start station
    print('\nThe most commonly used start station is:\t{}'.format(
        df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nThe most commonly used end station is:  \t{}'.format(
        df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of\nstart station and end station trip is:\t\t{}'.format(
        (df['Start Station']+' to '+df['End Station']).mode()[0]))

    # calculate time needed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    def get_duration(seconds):
        """Returns days, hours, minutes, seconds calculated from seconds"""
        days = seconds // (24*60*60)
        seconds %= (24*60*60)
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60

        # formatting output evenly
        days = str(int(days)).rjust(5)
        hours = str(int(hours)).rjust(5)
        minutes = str(int(minutes)).rjust(5)
        seconds = str(int(seconds)).rjust(5)
        return days, hours, minutes, seconds

    print('Calculating Trip Duration...')
    start_time = time.time()  # set start time

    print("\nWhat are the total and mean travel time?")

    # display total travel time
    print('\nTotal travel time is:    {} days {} hours {} minutes {} seconds'.format(
        *get_duration(df['Trip Duration'].sum())))

    # display mean travel time
    print('\nThe mean travel time is: {} days {} hours {} minutes {} seconds'.format(
        *get_duration(df['Trip Duration'].mean())))

    # calculate time needed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating User Stats...\n')
    start_time = time.time()  # set start time

    print("\nWhat are the counts of user types and gender?")

    # Display counts of user types
    print('Counts of user types:  \n{}'.format(
        df.groupby(['User Type'])['Unnamed: 0'].count()))

    # Display counts of gender
    if not df['Gender'].isnull().all():
        print('\nCounts of gender:  \n{}'.format(
            df.groupby(['Gender'])['Unnamed: 0'].count()))
    else:
        print("\nThere is no data for gender in this DataFrame/Filter")

    print("\nWhat are the oldest, youngest, most common and median year of birth?")

    # Calculate & display oldest, youngest, most common and median year of birth
    if not df['Birth Year'].isnull().all():
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        median = df['Birth Year'].median().astype('int32')
        print('\nOldest: {} Youngest: {} Most Common: {} Median: {}'.format(
            oldest, youngest, most_common, median))
    else:
        print("\nThere is no data for birth year in this DataFrame/Filter")

    # calculate time needed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_data(df, index=0):
    """Displays next 5 Rows from DataFrame from index-argument"""
    print(df[index:index+5])


def main():
    while True:
        # get filter for data set and load DataFrame
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # display statistical data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # display rows from the data set
        index = 0
        while True:
            userInput = get_input(
                "Would you like to see five (more) rows of data? ([Y]es/[N]o)", yes_no)
            if userInput:
                get_data(df, index)
                index += 5
            else:
                break

        # restart
        userInput = get_input(
            "Would you like to restart ([Y]es/[N]o)?", yes_no)
        if userInput:
            continue
        else:
            print("Bye")
            break


if __name__ == "__main__":
    main()
