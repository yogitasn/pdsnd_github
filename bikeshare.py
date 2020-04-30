import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

mon_dic={'jan':'january',
         'feb':'february',
         'mar':'march',
         'apr':'april',
         'may':'may',
         'june':'june',
         'all':'all'
        }
day_dic={1:'Sunday',2:'Monday',
     3:'Tuesday',
     4:'Wednesday',5:'Thursday',
     6:'Friday',7:'Saturday',
     8:'all'}



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #Use a while loop for user input till user correctly inputs city data
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington: ")
        if city.lower() not in('chicago','new york','washington'):
           print("Please enter a correct input for city")
        else:
            city=city.lower()
            break

    month=input("Which month? Please type your response as Jan,Feb,Mar,Apr,May, June or All: ")
    month=mon_dic.get(month.lower())

    day_in=int(input("Which day? Please type your response as an integer (e.g. 1=Sunday or 8=All): "))
    day=day_dic.get(day_in)

    print('-'*40)
    return city, month, day

def display_raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """
    data=0
    #Use a while loop for user input till user wants to view raw data
    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if answer.lower() == 'yes':
            print(df[data : data+5])
            data += 5
        else:
            break

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

    df=pd.read_csv(CITY_DATA.get(city))

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        months=months.index(month) + 1

        df = df[df.month == months]

    if day != 'all':
        df = df[df.day_of_week == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common month: ',df['month'].mode()[0])

    print('Most common day of the week: ',df['day_of_week'].mode()[0])

    print('Most common start hour: ',df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most commonly used start station: ',df['Start Station'].mode()[0])

    print('Most commonly used end station: ',df['End Station'].mode()[0])

    print('Most frequent combination of start and end station trip ',df.groupby(['Start Station','End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel time: ',df['Trip Duration'].sum())

    print('Mean Travel time: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User type counts ',df['User Type'].value_counts())

    print('Display count of Genders: ',df['Gender'].value_counts())

    print('Earliest birth: ',int(df['Birth Year'].min()))
    print('Most Recent birth: ',int(df['Birth Year'].max()))
    print('Most common birth year: ',int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        ## There is no gender column in washington data hence displaying user stats only for other cities chicago or new york
        if city.lower()!='washington':
           user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
