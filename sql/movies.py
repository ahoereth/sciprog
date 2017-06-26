#!/usr/bin/env python3
import os
import sqlite3
from io import BytesIO
from urllib.request import urlopen
from pathlib import Path
from zipfile import ZipFile

import pandas as pd


REMOTE = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
CWD = Path(os.path.dirname(__file__))
DBFILE = str(CWD / 'tmp.db')


def get_data():
    """Download the ml-latest-small dataset."""
    res = urlopen(REMOTE)
    with ZipFile(BytesIO(res.read())) as zipped:
        zipped.extractall(str(CWD))


def load_data():
    """Read csv source files and write to database."""
    with sqlite3.connect(DBFILE) as db:
        kwargs = {'con': db, 'if_exists': 'replace'}
        DIR = CWD / 'ml-latest-small'
        pd.read_csv(DIR / 'links.csv').to_sql('links', **kwargs)
        pd.read_csv(DIR / 'movies.csv').to_sql('movies', **kwargs)
        pd.read_csv(DIR / 'ratings.csv').to_sql('ratings', **kwargs)
        pd.read_csv(DIR / 'tags.csv').to_sql('tags', **kwargs)
        db.commit()


def top():
    """Create `top.csv`.

    Get the top 5 highest rated movies in the database along with their
    average rating.

    Creates a csv file with two columns: `title` (str), `rating` (float)
    """
    query = """
        SELECT title, AVG(rating) as rating
        FROM movies LEFT JOIN ratings USING (movieId)
        GROUP BY title
        ORDER BY rating DESC
        LIMIT ?
    """
    with sqlite3.connect(DBFILE) as db, open(CWD / 'top.csv', 'w') as f:
        pd.read_sql(query, db, params=(5,)).to_csv(f, index=False)


def titanic():
    """Create `titanic.csv`.

    Find all the users that didn’t rate Titanic (1997) a 5.0, along with what
    their ratings were. Feel free to hardcode the movie id in the query and
    not do a join.

    Creates a csv file with two columns: `userId` (int), `rating` (float)
    """
    query = """
        SELECT userId, rating
        FROM ratings LEFT JOIN movies USING (movieId)
        WHERE title = 'Titanic (1997)' and rating != 5
        ORDER BY rating DESC
    """
    with sqlite3.connect(DBFILE) as db, open(CWD / 'titanic.csv', 'w') as f:
        pd.read_sql(query, db).to_csv(f, index=False)


def common_tag():
    """Create `common_tag.csv`.

    Find just the titles of all movies that are tagged with the most commonly
    used tag. Don’t hardcode the tag that you’re looking for, use a subquery
    instead.

    Creates a csv file with a single column: `title` (str)
    """
    query = """
        SELECT title
        FROM movies LEFT JOIN tags USING (movieId)
        WHERE tag = (
            SELECT tag
            FROM tags
            GROUP BY tag
            ORDER BY COUNT(tag) DESC
            LIMIT 1
        )
    """
    with sqlite3.connect(DBFILE) as db, open(CWD / 'common_tag.csv', 'w') as f:
        pd.read_sql(query, db).to_csv(f, index=False)


if __name__ == '__main__':
    get_data()
    load_data()
    top()
    titanic()
    common_tag()
