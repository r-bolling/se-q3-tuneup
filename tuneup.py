#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = '''r-bolling with help from Kenzie Academy
Learned a bit about dict optimization from this:
https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
'''

import cProfile
import pstats
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # Be sure to review the lesson material on decorators.
    # You need to understand how they are constructed and used.
    def wrapper(*args):
        pr = cProfile.Profile()
        pr.enable()
        func(*args)
        pr.disable()
        ps = (
            pstats.Stats(pr).strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE)
        )
        ps.print_stats(10)
    return wrapper
    raise NotImplementedError("Complete this decorator function")


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    # Not optimized
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

#
# Students: write a better version of find_duplicate_movies
#


def optimized_find_duplicate_movies(src):
    movies = read_movies(src)
    duplicates = {}
    for movie in movies:
        if movie in duplicates:
            duplicates[movie] += 1
        else:
            duplicates[movie] = 1
    return set([x for x in movies if duplicates[x] > 1])


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    stmt = f"{func_name}('{func_param}')"
    setup = (
        f'from {__name__} import {func_name} as {func_name}; '
        f'func_param = "{func_param}"'
        )
    t = timeit.Timer(stmt, setup)
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    time_cost = min([(x / 3) for x in result])
    print(
        f"func={func_name}  num_repeats={num_repeats} "
        f"runs_per_repeat={runs_per_repeat} time_cost={time_cost:.3f} sec"
        )
    return t


def main():
    """Computes a list of duplicate movie entries."""
    # Students should not run two profiling functions at the same time,
    # e.g. they should not be running 'timeit' on a function that is
    # already decorated with @profile

    filename = 'movies.txt'

    print("--- Before optimization ---")
    result = find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)

    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)

    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    main()
    print("Completed.")
