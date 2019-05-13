import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
city_dict =  {'chicago': ['chicago'],
              'new york city': ['new york city', 'nyc', 'ny', 'new york'],
              'washington': ['washington', 'dc', 'washington dc']}
month_dict = {'january': ['january', 'jan'],
              'february': ['february', 'feb'],
              'march': ['march', 'mar'],
              'april': ['april', 'apr'],
              'may': ['may'],
              'june': ['june', 'jun'],
              'all': ['all']}
day_dict = {'monday': ['monday', 'mon'],
            'tuesday': ['tuesday', 'tue'],
            'wednesday': ['wednesday', 'wed'],
            'thursday': ['thursday', 'thu'],
            'friday': ['friday', 'fri'],
            'saturday': ['saturday', 'sat'],
            'sunday': ['sunday', 'sun'],
            'all': ['all']}

def validate_input(user_input, validating_dict):
    '''Validate user's input'''
    valid = False
    for key, values in validating_dict.items():
        if user_input in values:
            print('\nYou chose {} as your input.'.format(key.title()))
            valid = True
            break
    return (valid, key)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    city = str(input('Which city do you want to explore: Chicago, New York City, or Washington DC? ')).lower()
    city_flag, city = validate_input(city, city_dict)
    # Checking for valid city
    while not city_flag:
        print('\nThat was not a valid city.')
        city_input = str(input('Please specify which city: ')).lower()
        city_flag, city = validate_input(city_input, city_dict)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input('Which month - from January to June - do you want to explore? Or type "all" to apply no month filter: ')).lower()
    month_flag, month = validate_input(month, month_dict)
    # Checking for valid month
    while not month_flag:
        print('\nThat was not a valid month.')
        month_input = str(input('Please specify which month: ')).lower()
        month_flag, month = validate_input(month_input, month_dict)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Please specify which day of week, or type "all" to apply no day filter: ')).lower()
    day_flag, day = validate_input(day, day_dict)
    # Checking for valid day
    while not day_flag:
        print('\nThat was not a valid day of the week.')
        day_input = str(input('Please specify which day of the week: ')).lower()
        day_flag, day = validate_input(day_input, day_dict)

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
    if city == 'new york city':
        df = pd.read_csv('./new_york_city.csv')
    elif city == 'chicago':
        df = pd.read_csv('./chicago.csv')
    else:
        df = pd.read_csv('./washington.csv')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]
    return df

def raw_data(df):
    '''Prompt user about displaying 5 rows of raw data'''
    raw_row_ct = 0
    while True:
        raw_dat = input('\nWould you like to see 5 rows of raw data? Enter "yes" or "no".\n').lower()
        if raw_dat == 'yes':
            print(df[raw_row_ct:raw_row_ct + 5])
            print()
            raw_row_ct += 5
        else:
            break

def df_convert(df):
    '''Convert clolumns to datetime and extract month, day, hour'''
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    return df['Start Time'], df['End Time'], df['month'], df['day'], df['hour']

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df_convert(df)
    popular_month = months[int(df['month'].mode()[0]) - 1].title()
    popular_day = df['day'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    if month == 'all' and day == 'all':
        print('The most popular month is {}.'.format(popular_month))
        print('The most popular day of the week is {}.'.format(popular_day))
        print('The most popular hour is {}.'.format(popular_hour))
    elif month != 'all' and day == 'all':
        print('The most popular day of the week is {}.'.format(popular_day))
        print('The most popular hour is {}.'.format(popular_hour))
    elif month == 'all' and day != 'all':
        print('The most popular month is {}.'.format(popular_month))
        print('The most popular hour is {}.'.format(popular_hour))
    else:
        print('The most popular hour is {}.'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station is {}.'.format(popular_start))
    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most popular end station is {}.'.format(popular_end))
    # TO DO: display most frequent combination of start station and end station trip
    df['Start & End Stations'] = df['Start Station'] + ' / ' + df['End Station']
    popular_combo = df['Start & End Stations'].mode()[0]
    print('The most frequent combination of start station and end station trip is {}.'.format(popular_combo))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df_convert(df)
    # TO DO: display total travel time
    tot_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('The total travel time is {}.'.format(tot_travel_time))
    # TO DO: display mean travel time
    mean_time = (df['End Time'] - df['Start Time']).mean()
    print('The mean travel time is {}.'.format(mean_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types:\n')
    print(df['User Type'].dropna(axis = 0).value_counts())
    print()
    # TO DO: Display counts of gender, earliest, most recent, and most common year of birth
    if city != 'washington':
        print('Counts of genders:\n')
        print(df['Gender'].dropna(axis = 0).value_counts())
        print('\nThe earliest year of birth is: ', int(df['Birth Year'].min()))
        print('\nThe most recent year of birth is ', int(df['Birth Year'].max()))
        print('\nThe most common year of birth is ', int(df['Birth Year'].mode()))
    else:
        print('\nThere is no gender and birth year data for Washington DC.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        df_convert(df)
        trip_duration_stats(df)
        user_stats(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
