import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'C:/Users/Owner/udacity-git-course/bikeshare/data/chicago.csv',
              'new york city': 'C:/Users/Owner/udacity-git-course/bikeshare/data/new_york_city.csv',
              'washington': 'C:/Users/Owner/udacity-git-course/bikeshare/data/washington.csv' }

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

db_city = {
        1: {'city_name': 'chicago'},
        2: {'city_name': 'new york city'},
        3: {'city_name': 'washington'},
    }
    db_month = {
        1: {'month_name': 'january'},
        2: {'month_name': 'february'},
        3: {'month_name': 'march'},
        4: {'month_name': 'april'},
        5: {'month_name': 'may'},
        6: {'month_name': 'june'},
        7: {'month_name': 'all'},
    }
    db_dow = {
        1: {'dow_name': 'Sunday'},
        2: {'dow_name': 'Monday'},
        3: {'dow_name': 'Tuesday'},
        4: {'dow_name': 'Wednesday'},
        5: {'dow_name': 'Thursday'},
        6: {'dow_name': 'Friday'},
        7: {'dow_name': 'Saturday'},
        8: {'dow_name': 'all'},
    }

    def input1(flag,db_city,db_month,db_dow):
        if flag == 1:
            dt_base = db_city
            dt_name = 'city_name'
            dt_question = 'Select a city: '
        elif flag == 2:
            dt_base = db_month
            dt_name = 'month_name'
            dt_question = 'Select a month: '
        else:
            dt_base = db_dow
            dt_name = 'dow_name'
            dt_question = 'Select day of week: '
        while True:
            print(dt_question)
            #x = int(input())
            z = int(input(dt_question))

            if z in dt_base.keys():
                print("\nYou have chosen {0}".format(dt_base[z][dt_name]))
                print('-'*40)
                return dt_base[z][dt_name]
                break
            else:
                print('\nInvalid input.  Please try again.')

    print("Cities:")
    for x, y in db_city.items():
        print(x, ':', db_city[x]['city_name'])
    city = input1(1,db_city,db_month,db_dow)
        ######################################
    print("Months:")
    for x, y in db_month.items():
        print(x, ':', db_month[x]['month_name'])
    month = input1(2,db_city,db_month,db_dow)
        ######################################
    print("Days of the week:")
    for x, y in db_dow.items():
        print(x, ':', db_dow[x]['dow_name'])
    day = input1(3,db_city,db_month,db_dow)
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    # extract day_of_week and start_hour to be used in stats
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month:', most_common_month)


    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day_of_week)


    # Display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print('Most common start hour:', most_common_start_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    def most_common(mc,df):
        m_common = df[mc].mode()[0]
        return m_common

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most common start station:', most_common('Start Station',df))


    # Display most commonly used end station
    print('Most common end station:', most_common('End Station',df))


    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' | ' + df['End Station']
    print('Most common trip:', most_common('trip',df))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = np.sum(df['Trip Duration']/3600)
    print(f'Total travel time (hours): {total_travel_time:.2f}')

    # Display mean travel time
    mean_travel_time = np.mean(df['Trip Duration']/3600)
    print(f'Mean travel time (hours): {mean_travel_time:.2f}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_types.to_csv(sep='\t'))


    # Display counts of gender
    if city == 'washington':
        print("Gender counts not available for Washington.")
    else:
        gender = df['Gender'].value_counts()
        print('Counts of gender:')
        print(gender.to_csv(sep='\t'))


    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print("Earliest birth year not available for Washington.")
    else:
       earliest_birth_year = df['Birth Year'].min()
       print(f'Earliest birth year: {earliest_birth_year:.0f}')

    if city == 'washington':
        print("Most recent birth year not available for Washington.")
    else:
        most_recent_birth_year = df['Birth Year'].max()
        print(f'Most recent birth year: {most_recent_birth_year:.0f}')

    if city == 'washington':
        print("Most common birth year not available for Washington.")
    else:
       most_common_birth_year = df['Birth Year'].mode()[0]
       print(f'Most common birth year: {most_common_birth_year:.0f}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displays raw data, five lines at a time, at user's request."""

    def print1(df,j):
        print('Raw data:' + '\n')
        print(df[j-5:j])
        print('-'*40)

    show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no. \n')
    if show_data.lower() == 'yes':
       blankIndex=[''] * len(df)
       df.index = blankIndex
       for i, item in enumerate(df['User Type']):
           j = (i+1)*5
           if j > len(df.index):
               print('No more data to display.')
               print('-'*40)
               break
           else:
               if i == 0:
                   print1(df,j)
               else:
                   show_more = input('n\Would you like to see 5 more lines? Enter yes or no. \n')
                   if show_more.lower() == 'yes':
                       print1(df,j)
                   else:
                       break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
