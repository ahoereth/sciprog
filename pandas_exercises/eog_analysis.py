from os import path

import matplotlib.pyplot as plt
import pandas as pd


def read_data():
    """1. Reading in the data

    First you should read in the data and parse it appropriately for
    handling a timeseries.
    """
    directory = path.dirname(__file__)
    stimuli = pd.read_csv(path.join(directory, 'stimuli.csv')).timestamp
    data = pd.read_csv(path.join(directory, 'data.csv'))
    data = data.set_index('timestamp')
    return data, stimuli


def clean_data(data):
    """2. Cleaning the data

    You will notice that it looks weird. There are a couple of outliers, where
    the electrodes recorded weird noise at singular timestamps. We dont want
    that so think of a way of removing the noise without loosing too much
    structure of your data.
    """
    return data.rolling(3, center=True, min_periods=0).median()


def window(data, timestamp):
    """3. Extracting windows around stimuli

    Now you have ”mostly” clean data and also the stimulus times. Create a
    function that extracts a window around a stimulus timestamp from the
    original data. You should be able to look at a slice of the data from 0.5
    seconds before e.g. the first stimulus to 1 seconds after it.
    """
    left, right = [timestamp + t for t in [-.5, 1]]
    data = data[left:right]
    data.index -= timestamp
    return data


def get_jumps(window):
    """4. Detecting jumps

    For later fitting of a model it would be important to find the positions
    of the jumps in EOG data after the stimulus. So you need to write a
    function that gets a slice of data, like the one returned by your
    previous function, and detects the timestamp of the biggest jump in there.
    You can assume that those jumps will take place over something like 50
    milliseconds. Since there are 2 channels you will probably also compute
    two slightly different jump times, that is fine.
    """
    return window.diff(50).abs().idxmax()


def plot(data, timestamps):
    """5. Plotting

    Since there is a lot of noise in the data your detection algorithm will
    probably not show good results for all stimuli. This is okay, normally
    you would now filter out bad stimuli somehow. We will just require you
    to pick 4 stimuli where your detection works well and run your algorithm
    for those stimuli. Then make a plot where you show your results.
    """
    for i, timestamp in enumerate(timestamps):
        ax = plt.subplot(2, 2, 1 + i)
        columns = window(data, timestamp)
        jumps = get_jumps(columns)
        for color, label, jump in zip(['r', 'b'], columns, jumps):
            ax.plot(columns[label], label=label, color=color)
            ax.axvline(jump, label='{} jump'.format(label), color=color)
        ax.legend()
    plt.show()


def main():
    """Main function."""
    data, stimuli = read_data()
    data = clean_data(data)
    plot(data, stimuli[[1, 4, 7, 12]])


if __name__ == '__main__':
    main()
