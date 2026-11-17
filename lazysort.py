#!/usr/bin/env python3
import datetime
import functools
import sys
import time


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


# just to prove seconds_incr state is working...
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')


def log_generator(stream_name, stop_at=99, pause_every=0, pause_length=0.5):
    """generator that yields {stop_at} messages, pausing for {pause_length}
    every {pause_every} seconds"""

    @with_unique_ts_pfx
    def _log(s):
        return s

    count = 1
    for i in range(stop_at):
        msg = f'Stream {stream_name} Message {count}'
        yield _log(msg)
        count += 1


def lazymerge(*streams):
    """*streams being a series of iterators each emitting a timestamp-prefixed
    string, this generator yields one message at a time from all upstream
    inputs in sorted order"""
    log(f'lazymerge: merging/sorting input from {len(streams)} upstream sources')
    heads = {}
    for s in streams:
        heads[next(s)] = s
    log(heads)


def main():
    streams = []
    streams.append(log_generator('A'))
    lazymerge(*streams)


if __name__ == '__main__':
    main()

