#!/usr/bin/env python3
import datetime
import sys


SECONDS_INCR = 0

def log(s):
    global SECONDS_INCR
    SECONDS_INCR = SECONDS_INCR + 1
    ts = datetime.datetime.now().replace(microsecond=0)
    logtime = ts + datetime.timedelta(seconds=SECONDS_INCR)
    print(f'{logtime}: {s}', file=sys.stderr)

log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')
log(f'Using Python {sys.version.split(" ")[0]}')


