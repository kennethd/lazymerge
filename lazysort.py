#!/usr/bin/env python3
import datetime
import functools
import string
import sys
import time


global_iter = 0

def with_unique_ts_pfx(func):
    """decorator that wraps a function whose first argument is a string; that
    first argument will be prefixed with a unique timestamp"""

    @functools.wraps(func)
    def unique_ts(s, *args, **kwargs):
        global global_iter
        global_iter += 1
        unique_ts.seconds_incr += 1
        ts = datetime.datetime.now().replace(microsecond=0)
        logtime = ts + datetime.timedelta(seconds=unique_ts.seconds_incr)
        return func(f'{logtime} ({global_iter}): {s}', *args, **kwargs)

    unique_ts.seconds_incr = 0
    return unique_ts


@with_unique_ts_pfx
def log(s):
    print(s, file=sys.stderr)


# just to prove seconds_incr state is working...
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')


def log_generator(stream_name, msg_count, pause_every=0, pause_length=0.5):
    """generator that yields {msg_count} messages, pausing for {pause_length}
    every {pause_every} seconds"""

    @with_unique_ts_pfx
    def _log(s):
        return s

    count = 1
    for i in range(msg_count):
        msg = f'Stream {stream_name} msg {count} pausing every {pause_every} for {pause_length} seconds'
        yield _log(msg)
        count += 1
        if pause_every and not count % pause_every:
            log(f'pausing stream {stream_name}')
            time.sleep(pause_length)


def lazymerge(*streams):
    """*streams being a series of generators each emitting a timestamp-prefixed
    string, this generator yields one message at a time from all upstream
    inputs in sorted order"""
    log(f'lazymerge: merging/sorting input from {len(streams)} upstream sources')
    heads = {}
    for s in streams:
        heads[next(s)] = s
    log(heads)
    while len(heads):
        min_head = min(heads)
        yield min_head
        s = heads[min_head]
        try:
            next_s = next(s)
        except StopIteration:
            pass
        heads[next_s] = s
        del heads[min_head]


def main():
    streams = []
    for i, c in enumerate(string.ascii_uppercase):
        msg_count = 26 - i
        # i=0 c=A msg_count=26
        # ...
        # i=25 c=Z msg_count=1
        streams.append(log_generator(c, msg_count, pause_every=i))
    for log in lazymerge(*streams):
        print(log, file=sys.stdout)


if __name__ == '__main__':
    main()

