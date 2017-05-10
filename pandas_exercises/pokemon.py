"""Scientific Programming in Python Homework 5."""
import pandas as pd


def first_gen(df):
    """Find the names of all Pokemon from generation 1."""
    return df[df['Generation'] == 1]['Name']


def highest_hp(df):
    """Find the name(s) of Pokemon with the highest HP."""
    return df[df['HP'] == df['HP'].max()]['Name']


def mean_attack_by_type(df):
    """Find mean attack power of type 1.

    Return: dataframe with type and attack columns
    """
    return pd.DataFrame(df.groupby('Type 1')['Attack'].mean()).reset_index()


def high_defense(df):
    """Find Name and Defense of Pokemon that have an above average Defense."""
    return df[df['Defense'] > df['Defense'].mean()][['Name', 'Defense']]


def deduplicated(df):
    """Find unique pokemons.

    Some Pokemon are in the list multiple times with different names.
    Find the names of the pokemon but without these duplicates. You
    can use the # column to tell if they're the same pokemon. Example:
    Venusaur has # 3 and there is a VenusaurMega Venusaur also
    with # 3, the result should have just Venusaur
    """
    return df.drop_duplicates('#')['Name']


def main():
    """Main function."""
    try:
        df = pd.read_csv('Pokemon.csv')
    except:
        pass


if __name__ == '__main__':
    main()
