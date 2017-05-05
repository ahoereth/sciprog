import os
import sys
import subprocess
import shutil


def check():
    files = os.listdir('.')
    
    log = []
    
    # folder existence
    if "numpy_exercises" not in files:
        log.append("folder 'numpy_exercises' not found!")
        return False, log
        
    os.chdir('numpy_exercises')
    
    # file existence
    sub_files = os.listdir('.')
    if "array_tools.py" not in sub_files:
        log.append("file 'array_tools.py' not found!")
        return False, log
    
    # side effect free importing
    timeout = 10
    try:
        proc = subprocess.run(['python', '-c', 'from array_tools import sub_array'],
        encoding='utf-8',
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        timeout=timeout)
    except subprocess.TimeoutExpired:
        log.append("array_tools.py timeouted after {} seconds".format(timeout))
        return False, log
    if proc.returncode != 0:
        log.append("array_tools.py returned error:\n" + proc.stderr.strip())
        return False, log
    result = proc.stdout.strip()
    if result != "":
        log.append("importing array_tools.py resulted in printed output... please test from separate file or use if-main-statement!")
    
    ###
    # ACTUAL TESTING
    ###
    try:
        from numpy_exercises.array_tools import sub_array
    except Exception as e:
        log.append("importing your function failed with unexpected error:\n{}: {}".format(type(e).__name__, e))
        return False, log
    
    
    import numpy as np
    
    # dummy array
    a = np.arange(1, 31).reshape((5, 6))

    params_sets = [
        # simple behavior
        dict(shape=(3, 3), center=(2, 2), fill=None),
        # even rows/cols
        dict(shape=(4, 3), center=(2, 2), fill=None),
        dict(shape=(3, 4), center=(2, 2), fill=None),
        dict(shape=(4, 4), center=(2, 2), fill=None),
        # fill value for non-overlapping
        dict(shape=(3, 3), center=(2, 2), fill=0),
        # overlaps without fill
        dict(shape=(3, 5), center=(2, 0), fill=None),
        dict(shape=(3, 5), center=(2, 5), fill=None),
        dict(shape=(5, 3), center=(0, 2), fill=None),
        dict(shape=(5, 3), center=(4, 2), fill=None),
        dict(shape=(9, 9), center=(2, 2), fill=None),
        # overlaps with fill
        dict(shape=(3, 5), center=(2, 0), fill=0),
        dict(shape=(3, 5), center=(2, 5), fill=0),
        dict(shape=(5, 3), center=(0, 2), fill=0),
        dict(shape=(5, 3), center=(4, 2), fill=0),
        dict(shape=(9, 9), center=(2, 2), fill=0),
    ]

    targets = [
        [[8, 9, 10], [14, 15, 16], [20, 21, 22]],
        [[8, 9, 10], [14, 15, 16], [20, 21, 22], [26, 27, 28]],
        [[8, 9, 10, 11], [14, 15, 16, 17], [20, 21, 22, 23]],
        [[8, 9, 10, 11], [14, 15, 16, 17], [20, 21, 22, 23], [26, 27, 28, 29]],
        [[8, 9, 10], [14, 15, 16], [20, 21, 22]],
        [[7, 8, 9], [13, 14, 15], [19, 20, 21]],
        [[10, 11, 12], [16, 17, 18], [22, 23, 24]],
        [[2, 3, 4], [8, 9, 10], [14, 15, 16]],
        [[14, 15, 16], [20, 21, 22], [26, 27, 28]],
        [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24], [25, 26, 27, 28, 29, 30]],
        [[0, 0, 7, 8, 9], [0, 0, 13, 14, 15], [0, 0, 19, 20, 21]],
        [[10, 11, 12, 0, 0], [16, 17, 18, 0, 0], [22, 23, 24, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [2, 3, 4], [8, 9, 10], [14, 15, 16]],
        [[14, 15, 16], [20, 21, 22], [26, 27, 28], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 3, 4, 5, 6, 0], [0, 0, 7, 8, 9, 10, 11, 12, 0], [0, 0, 13, 14, 15, 16, 17, 18, 0], [0, 0, 19, 20, 21, 22, 23, 24, 0], [0, 0, 25, 26, 27, 28, 29, 30, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ]

    test_string_template = """Test parameters:
array:
{}
shape: {shape}
center: {center}
fill: {fill}
"""
    
    # iterate over test cases
    for test_n, (params, target) in enumerate(zip(params_sets, targets)):
        
        # format template string
        test_string = test_string_template.format(a, **params)
        
        # run function
        try:
            result = sub_array(array=a, **params)
        except Exception as e:
            log.append(
                "Test run {} got unexpected error while calling sub_array function!\n".format(test_n)
                +test_string
                +str(e)
            )
            continue
        
        # check return type is ndarray
        if type(result) is not np.ndarray:
            log.append(
                "Result of test run {} is not a numpy-array!\n".format(test_n)
                +test_string
            )
            continue
        
        # compare results
        if result.tolist() != target:
            log.append(
                "Test run {} returned wrong result!\n".format(test_n)
                +test_string
                +"Expected result:\n"
                +str(np.array(target))+"\n"
                +"Actual result:\n"
                +str(result)+"\n"
            )
    
    
    # all fine
    if len(log) == 0:
        return True, log
    else:
        return False, log
    
    
    


current_dir = os.getcwd()
_stdout = sys.stdout
null = open(os.devnull, 'wb')
sys.stdout = null
try:
    correct, log = check()
finally:
    os.chdir(current_dir)
    sys.stdout = _stdout
    null.close()

returnstring = 'pass' if correct else 'fail'
returnstring += '\n'
returnstring += '\n'.join(["- " + entry.replace('\n', '\n  ') for entry in log])
print(returnstring)