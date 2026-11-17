#!/usr/bin/env python3
import datetime
import functools
import sys


def with_unique_ts_pfx(func):
    """decorator that wraps a function whose first argument is a string; that
    first argument will be prefixed with a unique timestamp"""

    @functools.wraps(func)
    def unique_ts(s, *args, **kwargs):
        unique_ts.seconds_incr += 1
        ts = datetime.datetime.now().replace(microsecond=0)
        logtime = ts + datetime.timedelta(seconds=unique_ts.seconds_incr)
        return func(f'{logtime}: {s}', *args, **kwargs)

    unique_ts.seconds_incr = 0
    return unique_ts


@with_unique_ts_pfx
def log(s):
    print(s, file=sys.stderr)


log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')


