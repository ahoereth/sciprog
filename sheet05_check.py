import os
import sys
import subprocess
import shutil
import textwrap
import traceback

import pandas as pd

wrapper = textwrap.TextWrapper(drop_whitespace=True)

def check():
    files = os.listdir('.')
    
    log = []
    
    # folder existence
    if 'pandas_exercises' not in files:
        log.append("Folder 'pandas_exercises' not found!")
        return False, log

    if 'Pokemon.csv' in files:
        # copy it down in case it's one level higher
        shutil.copy2('Pokemon.csv', 'pandas_exercises/Pokemon.csv')

    os.chdir('pandas_exercises')

    pandas_files = os.listdir('.')
    if 'Pokemon.csv' not in pandas_files:
        log.append("'Pokemon.csv' not found in pandas_exercises")
        return False, log

    timeout = 10
    try:
        proc = subprocess.run(['python', '-c', 'import pokemon'],
        # encoding='utf-8',
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        timeout=timeout)
    except subprocess.TimeoutExpired:
        log.append("pokemon.py timeouted after {} seconds".format(timeout))
        return False, log
    if proc.returncode != 0:
        log.append("pokemon.py returned error:\n" + proc.stderr.decode('utf-8').strip())
        return False, log
    result = proc.stdout.decode('utf-8').strip()
    if result != "":
        log.append("importing pokemon.py resulted in printed output... please test from separate file or use if-main-statement!")

    ###
    # ACTUAL TESTING
    ###
    try:
        from pandas_exercises import pokemon
    except Exception as e:
        log.append("importing your module failed with unexpected error:\n{}: {}".format(type(e).__name__, e))
        return False, log


    ans1 = pd.read_pickle('../week05_answers/first_gen.pkl')
    ans2 = pd.read_pickle('../week05_answers/highest_hp.pkl')
    ans3 = pd.read_pickle('../week05_answers/attack_stats.pkl')
    ans4 = pd.read_pickle('../week05_answers/high_defense.pkl')
    ans5 = pd.read_pickle('../week05_answers/deduplicated.pkl')

    test_func(log, ans1, 'first_gen', pokemon.first_gen, series_check)
    test_func(log, ans2, 'highest_hp', pokemon.highest_hp, series_check)
    test_func(log, ans3, 'mean_attack_by_type', pokemon.mean_attack_by_type, mean_attack_check)
    test_func(log, ans4, 'high_defense', pokemon.high_defense, high_defense_check)
    test_func(log, ans5, 'deduplicated', pokemon.deduplicated, series_check)

    if len(log) == 0:
        return True, log
    else:
        return False, log

def test_func(log, answer, func_name, func, check_func):
    df = pd.read_csv('Pokemon.csv')
    try:
        theirs = func(df)
    except Exception as err:
        err_str = traceback.format_exc()
        log.append("""\
{} gave unexpected error!
{}\
            """.format(func_name, err_str)
            )
        return

    if not isinstance(theirs, (pd.DataFrame, pd.Series)):
        log.append(
            "Result of {} is {} and not dataframe or series!\n".format(func_name, type(theirs))
        )
        return
    if not check_func(answer, theirs):
        log.append("""\
{} returned wrong result
Excepted result (just displaying head(10)):
{}
Actual result:
{}\
                """.format(func_name, answer.head(10), theirs.head(10)))

def mean_attack_check(a, b):
    a_i = a.set_index('Type 1')
    b_i = b.set_index('Type 1')
    return a_i.sort_index().equals(b_i.sort_index())

def high_defense_check(a, b):
    a_i = a.set_index('Name')
    b_i = b.set_index('Name')
    return a_i.sort_index().equals(b_i.sort_index())

def series_check(a, b):
    return (a.sort_index().values == b.sort_index().values).all()

def dataframe_check(a, b):
    return a.equals(b)


current_dir = os.getcwd()
_stdout = sys.stdout
# null = open(os.devnull, 'w')
# sys.stdout = null
try:
    correct, log = check()
finally:
    os.chdir(current_dir)
    sys.stdout = _stdout
    # null.close()

returnstring = 'pass' if correct else 'fail'
returnstring += '\n'
returnstring += '\n'.join(["- " + entry.replace('\n', '\n  ') for entry in log])
print(returnstring)

