import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). 
    available_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('Which city would you like to see your data from chicago, new york city or washington?\n').lower()
        if city in available_cities:
            break
        else:
            print('You have entered an invalid city')

    # Get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    months_dec = input('Do you want to analyse all months or a specific month\nPlease enter yes for all and no for specific day\n').lower()
    if months_dec == 'yes' :
        month = 'all'
    else:
        while True:
            month = input('Kindly choose the Month to filter from; January, February, March, April, May or June?\n').lower()
            if month in months:
                break
            else:
                print('Please enter a valid month')

    # Get user input for day of week (all, monday, tuesday, ... sunday)n
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days_dec = input('Do you want to analyse all days of the week or a specific day\nPlease enter yes for all and no for specific     day\n').lower()
    if days_dec == 'yes' :
        day = 'all'
    else:
        while True:
            day = input('Kindly choose the days of the week. Select from monday to sunday\n').lower()
            if day in days:
                break
            else:
                print('Please enter a valid day')

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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    raw = input('would you like to display raw data?. choose yes or no\n').lower()
    if raw == 'yes':
        count = 0
        while True:
            pd.set_option('display.max_columns',200)
            print(df.iloc[count: count+5])
            count += 5
            ask = input('next 5 lines?')
            if ask != 'yes':
                break
                            
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    
    # extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    month_index = {'january', 'february', 'march', 'april', 'may', 'june'}
    if month != 'all':
        df = df.loc[df['Month'] == month_index[month]]
    return df
     # filter by day of week if applicable
    day_index = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    if day != 'all':
        df = df.loc[df['Day'] == day_index[day]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month is : {}'.format(df['Month'].mode()[0]))

    # display the most common day of week
    print('Most common day of the week is : {}'.format(df['Day'].mode()[0]))

    # display the most common start hour
    print('Most common start hour is : {}'.format(df['Hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is : {}'.format(df['Start Station'].mode()))

    # display most commonly used end station
    print('Most commonly used end station is : {}'.format(df['End Station'].mode()))

    # display most frequent combination of start station and end station trip
    # Create a Start_End column before filtering
    df['Start_End'] = df['Start Station'] + "-" + df['End Station']
    print('most frequent combination of start and end station is : {}'.format(df['Start_End'].mode()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    print('Total travel time is : {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time is : {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user type is : {}'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of gender is : {}'.format(df['Gender'].value_counts()))
    else:
        print('No available data for gender')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('earliest year of birth is : {}'.format(df['Birth Year'].min()))
        print('most recent of birth is : {}'.format(df['Birth Year'].max()))
        print('most common year of birth is : {}'.format(df['Birth Year'].mode()))
    else:
        print('No available data for birth year')
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
