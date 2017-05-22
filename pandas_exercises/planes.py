import pandas as pd


def mean_routes(airlines, airports, routes):
    '''
    Find the mean number of routes per airport by country. Use the source
    airport to determine the country and don't worry about whether the flight
    is interational or domestic.
    Example:
    Some country has 3 airports
    Airport1 is the source of 5 flights
    Airport2 is the source of 3 flights
    Airport3 is the source of 8 flights
    Average for the country: 5.333
    Returns: Series where the index is the country name and the values are the
    means rounded to 3 decimal places
    Other notes:
    It might be possible to do this using just one groupby but the solution
    used two
    '''
    data = pd.merge(routes, airports, left_on='src_airport', right_on='iata')
    flights = data.groupby(['country', 'src_airport']).count()
    return flights.groupby('country').mean().iloc[:, 1]


if __name__ == '__main__':
    try:
        airlines = pd.read_csv('airlines.csv')
        airports = pd.read_csv('airports.csv')
        routes = pd.read_csv('routes.csv')
    except:
        pass
    else:
        print(mean_routes(airlines, airports, routes))
