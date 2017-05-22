"""Homework 6."""
import pandas as pd


def mean_routes(airlines, airports, routes):
    '''Find the mean number of routes per airport by country.

    Use the source airport to determine the country and don't worry about
    whether the flight is interational or domestic.

    Example:
        Some country has 3 airports
        Airport1 is the source of 5 flights
        Airport2 is the source of 3 flights
        Airport3 is the source of 8 flights
        Average for the country: 5.333

    Returns:
        Series where the index is the country name and the values are the
        means rounded to 3 decimal places

    Other notes:
        It might be possible to do this using just one groupby but the solution
        used two.
    '''
    data = routes.merge(airports, left_on='src_airport', right_on='iata')
    flights = data.groupby(['country', 'src_airport']).count()
    return flights.mean(level='country').iloc[:, 0].round(3)


def main():
    """Run code when file is called directly and csvs are available."""
    try:
        airlines = pd.read_csv('airlines.csv')
        airports = pd.read_csv('airports.csv')
        routes = pd.read_csv('routes.csv')
    except:
        pass
    else:
        print(mean_routes(airlines, airports, routes))


if __name__ == '__main__':
    main()
