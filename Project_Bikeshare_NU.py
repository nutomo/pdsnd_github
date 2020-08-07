#Project Bikeshare_Nathania Utomo
import time
import pandas as pd
import numpy as np

CITY_DATA           = { 'chicago': 'chicago.csv',
                        'new york city': 'new_york_city.csv',
                        'washington': 'washington.csv' }
data_cities     = [ "new york city", "chicago", "washington" ]
data_months     = [ "january", "february", "march", "april", "may", "june", "all" ]
data_days_of_week       = [ "monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday", "all" ]

def ask_user_selection(options, prompt_message):
    answer = ""
    while len(answer) == 0:
        answer = input(prompt_message)
        answer = answer.strip().lower()

        if answer in options:
            return answer
        else:
            answer = ""
            print("Please enter one of the offered options.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n ---- Hello! Let\'s explore some US bikeshare data! ----\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ask_user_selection(data_cities,
            "Would you like to see data for New York City, Chicago or Washington? \n")

    # get user input for month (all, january, february, ... , june)
    month = ask_user_selection(data_months,
            "Which month? January, February, March, April, May, June or All? \n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_user_selection(data_days_of_week,
            "Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All? \n")

    print('-'*80)
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

    df = pd.read_csv(CITY_DATA[city], index_col = 0)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['start_end'] = df['Start Station'].astype(str) + ' to ' + df['End Station']

    if month != 'all':
        month_index = data_months.index(month) + 1
        df = df[df["month"] == month_index ]

    if day != 'all':
        df = df[df["week_day"] == day.title() ]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel ... \n')
    start_time = time.time()

    # display the most common month
    month_index = df["month"].mode()[0] - 1
    most_common_month = data_months[month_index].title()

    print("Most common month: ", most_common_month)

    # display the most common day of week
    most_common_day = df["week_day"].mode()[0]
    print("Most common day of week: ", most_common_day)

    # display the most common start hour
    most_common_hour = df["start_hour"].mode()[0]
    print("Most common start hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip ...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start = df['Start Station'].mode()[0]
    print("Most used start station: ", most_used_start)

    # display most commonly used end station
    most_used_end = df['End Station'].mode()[0]
    print("Most used end station: ", most_used_end)

    # display most frequent combination of start station and end station trip
    most_common_combination = df["start_end"].mode()[0]
    print("Most common combination concerning start- and end-station: ",
            most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration ...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time: ", total_travel_time)

    # display mean travel time
    average_time = df["Trip Duration"].mean()
    print("Average travel time: ", average_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats ...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts by user types: \n",
            df["User Type"].value_counts())

    # Display counts of gender
    if "Gender" in df:
        print("\nCounts by gender:")
        print("Male: ", df.query("Gender == 'Male'").Gender.count())
        print("Female: ", df.query("Gender == 'Female'").Gender.count())

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nData regarding year of birth:")
        print("Earliest year: ", df["Birth Year"].min())
        print("Latest year: ", df["Birth Year"].max())
        print("Most common year: ", df["Birth Year"].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    responses = ['yes', 'no']
    answer = ''
    counter = 0
    while answer not in responses:
        print("Do you wish to see the raw data? Yes or No? \n")
        answer = input().lower()
        if answer == "yes":
            print(df.head())
        elif answer not in responses:
            print("Please enter one of the offered options.\n")

    while answer == 'yes':
        print("Do you wish to view more raw data? \n")
        counter += 5
        again = input().lower()
        if again == "yes":
             print(df[counter:counter+5])
        elif again != "yes":
             break

    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
