"""
This script allows users to interactively analyze Motivate bikesharing data from any city for which
one of Motivate's CSV data files is available. The script allows the user to specify the city's CSV
file to be loaded for analysis, and the month or months and day or days of week to be analyzed. It
shows when and where is most popular for a ride, total and average trip durations, and attributes of
the riders.
"""
import time
import pandas as pd
import numpy as np

# The cities for which data is currently available
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington), with a reminder for invalid data
    city = ''
    while city not in CITY_DATA:
        city = input('Which city would you like to explore? ').lower()
        if city not in CITY_DATA:
            message = 'You may choose from: '
            for key in CITY_DATA:
                message += '|' + key + '| '
            print(message)

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input('Which month would you like to explore ("All" for all months)? ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Which day would you like to explore ("All" for all days of the week)? ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load complete data for selected city into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create 'month', 'day_of_week', and 'hour' columns from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # Filter by selected month if all is not selected
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by selected day if all is not selected
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour: {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most common end station: {}'.format(df['End Station'].mode()[0]))

    # create 'trip' column from 'Start Station' and 'End Station' of each trip
    df['trip'] = df['Start Station'] + ' TO ' + df['End Station']

    # display most frequent combination of start station and end station trip
    print('Most common trip: {}'.format(df['trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # determine the duration of each trip in seconds
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['duration'] = df['End Time'] - df['Start Time']
    df['duration'] = df['duration']/np.timedelta64(1, 's')

    # display total travel time in minutes and seconds
    total_travel_seconds = df['duration'].sum()
    total_travel_time = str('{}:{}'.format(int(total_travel_seconds // 60), str(int(total_travel_seconds % 60)).zfill(2)))
    print('Total travel time = {}'.format(total_travel_time))

    # display mean travel time in minutes and seconds
    mean_travel_seconds = df['duration'].mean()
    mean_travel_time = str('{}:{}'.format(int(mean_travel_seconds // 60), str(int(mean_travel_seconds % 60)).zfill(2)))
    print('Mean travel time = {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types:\n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender if available in data
    if 'Gender' in df.columns:
        print('Gender:\n{}\n'.format(df['Gender'].value_counts()))
    else:
        print('Gender statistics not available for this city.')

    # Display earliest, most recent, and most common year of birth, if available in data
    if 'Birth Year' in df.columns:
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('Birth statistics not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
