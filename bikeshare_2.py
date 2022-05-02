import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january','february','march','april','may','june','all']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter a city. Choose either chicago, new york city or washington: ").lower()
        if city in CITY_DATA:
            break
        else:
           print("This is not the right city")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month to filter by or enter 'all' to view all months: ").lower()
        if month in months:
            break
        else :
            print("This month is unavailable, please choose another")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True :
        day = str(input("Enter the day to filter by or enter 'all' to view all days: ")).lower()
        if day in days :
            break
        else :
            print("Please enter a day of the week or choose all...")

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['months'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month !='all':
        months =['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['months'] == month]

    if day !='all':
        df = df[df['weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['months'].mode()[0]
    print("The most common month is: ", most_common_month)

    # display the most common day of week
    most_common_day = df['weekday'].mode()[0]
    print("The most common day is: ", most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: ", common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combo = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station is: ", most_frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    print("The total trip duration is {} hours, {} minutes and {} seconds.".format(h, m, s))

    # display mean travel time in a format optimised for humans.
    mean_travel_time = round(df['Trip Duration'].mean())
    avg_min, avg_sec = divmod(mean_travel_time, 60)
    avg_hour, avg_min = divmod(avg_min, 60)
    print("The average travel time is {} hours, {} minutes and {} seconds." .format(avg_hour, avg_min, avg_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_type_count = df['User Type'].value_counts()
        print(user_type_count)
    else:
        print("This data does not exist.")

    # Display counts of gender
    if'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print("Gender data does not exist for the selected city.")

    # Display earliest, most recent, and most common year of birth
    if'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("The earliest year of birth is", int(earliest_year))
        most_recent_year = df['Birth Year'].max()
        print("The most recent year of birth is", int(most_recent_year))
        common_year = df['Birth Year'].mode()
        print("The most common year of birth is", int(common_year))
    else:
        print("Birth year data does not exist for the selected city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #ask for user input - 5 rows of data
    raw_data = input("Would you like to see 5 rows of raw data? Enter 'yes' or 'no' ").lower()
    if raw_data in ('yes','y'):
        i = 0
        while True :
            print(df.iloc[i:i+5])
            i += 5
            next_rows = input("Would you like to see another 5 rows of data? Enter 'yes' or 'no': ").lower()
            if next_rows not in ('yes','y'):
                break

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
