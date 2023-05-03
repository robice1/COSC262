'''Compare search times with Python's inbuilt lists and sets.'''
import sys
import time
import random
# uncomment the following line to import matplotlib stuff
import matplotlib.pyplot as plt


# Get the time units given by the perf_counter
# Note: time.clock has been deprecated in Python 3.3
# and replaced with the more precise perf_counter method
# time.perf_counter returns time as seconds since some arbitrary time
# so only the difference between two times is useful...
REZ = time.get_clock_info('perf_counter').resolution
print('Smallest time resolution is ' + str(REZ) + ' seconds')


def run_list_trials(num_trials=1):
    """ Creates lists filled with a range of values
    then searches for a randomly generated number in each list.
    Note: we are being nice here is that the number will be in the list...
    Returns two lists, the first contains all the list sizes tried and
    the second contains the average time per locate operation for each list size. """
    list_of_times = []
    # we will test for sizes [20000, 40000, 60000, etc...]
    list_of_sizes = list(range(20000, 1000001, 20000))
    for list_size in list_of_sizes:
        num_list = list(range(list_size))  # creates a list of n items

        # run trials, each on simply trying to locate the number in the list
        start = time.perf_counter()
        for i in range(num_trials):
            # try to find random number (between 1 and n) in the list
            value_to_find = random.randrange(list_size)
            found = value_to_find in num_list
        end = time.perf_counter()

        # print number of trials and time taken (with a tab in between)
        time_taken_per_locate = (end - start) / num_trials
        print(f"{list_size}\t{time_taken_per_locate:>10.8f}")

        # keep track of all the times
        list_of_times.append(time_taken_per_locate)
    return list_of_sizes, list_of_times


def run_set_trials(num_trials=1):
    """ Creates a set and fills it with values,
    then searches for a randomly generated number in the set.
    Note: we are being nice here, as the number will be in the set..."""
    list_of_times = []
    list_of_sizes = list(range(20000, 1000001, 20000))
    for set_size in list_of_sizes:
        # fill test set with n items {0,1,2,....}
        test_set = {i for i in range(set_size)}
        
        # run trials, each on simply trying to locate the number in the list
        start = time.perf_counter()
        for i in range(num_trials):
            # try to find random number (between 1 and n) in the list
            value_to_find = random.randrange(set_size)
            found = value_to_find in test_set
        end = time.perf_counter()

        # print number of trials and time taken (with a tab in between)
        time_taken_per_locate = (end - start) / num_trials
        print(f"{set_size}\t{time_taken_per_locate:>10.8f}")        
        list_of_times.append(time_taken_per_locate)
    return list_of_sizes, list_of_times


def graph_one_series_example(n_trials):
    """An example of how to graph one series.
    Currently plots the list results.
    Try changing so that set results are shown :)
    IMPORTANT NOTE: Make sure the matplotlib import is uncommented
    at the top of this file before using this function
    """

    print('Getting list data for graph...')
    x1, y1 = run_set_trials(n_trials)

    # We use the following instead of axes = plt.axes()
    # as it opens new figures (figs) in new windows
    # for example if you call graph_one_series_example
    # then call graph_one_series_example you will get
    # two graph windows :)
    fig, axes = plt.subplots()

    axes.plot(x1, y1, color='blue', marker='o', label='list')

    axes.set_title(f'List Locate Testing, {n_trials} Trial runs')
    axes.set_xlabel('n')
    axes.set_ylabel('Average Time per locate')
    axes.grid(True)

    # set format for ticks to simple decimal, otherwise defaults to exp
    # notation
    axes.xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

    legend = axes.legend(loc='upper left')
    plt.show()


def graph_two_series_example(n_trials):
    """An example of how to graph two series.
    Currently plots the list and set results.
    IMPORTANT NOTE: Make sure the matplotlib import is uncommented
    at the top of this file before using this function
    """
    print('Getting list data for graph...')
    list_xs, list_ys = run_list_trials(n_trials)
    print()
    print('Getting set data for graph...')
    set_xs, set_ys = run_set_trials(n_trials)

    # We use the following instead of axes = plt.axes()
    # as it opens new figures (figs) in new windows
    # for example if you call graph_one_series_example
    # then call graph_one_series_example you will get
    # two graph windows :)
    fig, axes = plt.subplots()

    axes.plot(list_xs, list_ys, color='blue', marker='o', label='list')
    axes.plot(set_xs, set_ys, color='red', marker='o', label='set')

    axes.set_title(f'List Locate Testing, {n_trials} Trial runs')
    axes.set_xlabel('n')
    axes.set_ylabel('Average Time per locate')
    axes.grid(True)

    # set format for ticks to simple decimal, otherwise defaults to exp
    # notation
    axes.xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

    legend = axes.legend(loc='upper left')
    plt.show()


def run_tests(n_trials):
    '''Function that runs various tests. Put your test calls in here'''

    print("LIST TRIAL RUN")
    print(f"Averages over {n_trials} trials.")
    print('size(n)\tAvg. Time')
    sizes, times = run_list_trials(n_trials)


def main():
    """ Put your tests in here """
    # run_tests(n_trials=10)

    # uncomment either of the following lines to run some graphs

    # IMPORTANT NOTE: make sure you uncomment out the
    # import for matplotlib at the start of the file
    # before you start trying to do graph things
    graph_one_series_example(n_trials=100)
    # graph_two_series_example(n_trials=10)
    #
    #
    # if you can't get matplotlib to run
    # then you can cut and paste the output from
    # run_tests into a spreadsheet, eg, Excel or Libre Office Calc
    # and do some graphing there


if __name__ == "__main__":
    main()
