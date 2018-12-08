from collections import defaultdict, Counter
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

from enum import Enum
from typing import List, Dict, Iterable
from functools import reduce
from operator import add


class Event(Enum):
    BEGIN = 1
    WAKE_UP = 2
    FALL_ASLEEP  = 3

BEGIN, WAKE_UP, FALL_ASLEEP = Event.BEGIN, Event.WAKE_UP, Event.FALL_ASLEEP

@dataclass
class LogEntry:
    timestamp: datetime
    guard_id: int
    event: Event



def wakeups(ts: List[LogEntry]) -> Iterable[LogEntry]:
    return filter(lambda x: x.event is WAKE_UP , ts)

def asleeps(ts: List[LogEntry]) -> Iterable[LogEntry]:
    return filter(lambda x: x.event is FALL_ASLEEP , ts)

def time_sleep(ts: List[LogEntry]) -> float:
    return reduce(
        add,
        (
            x.timestamp - y.timestamp
            for x, y in zip(wakeups(ts), asleeps(ts))
        ),
        timedelta(0)
    ).total_seconds()


def parse_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M')


def parse_event(x: str) -> Event:
    if 'begins' in x:
        return BEGIN
    elif 'falls asleep' in x:
        return FALL_ASLEEP
    elif 'wakes up' in x:
        return WAKE_UP
    else:
        assert False, '💩'


def parse_log(pathname: str) -> List[LogEntry]:
    log = []
    with open(pathname) as fp:
        previous_guard_id = None
        for line in fp:
            log_entry: LogEntry = parse_line(
                line.rstrip(),
                previous_guard_id=previous_guard_id)
            log.append(log_entry)
            previous_guard_id = log_entry.guard_id
    return log


def groupby(xs, f) -> Dict[any, List]:
    acc = defaultdict(list)
    for x in xs:
        acc[f(x)].append(x)
    return acc


def parse_guards(log: List[LogEntry]) -> Dict[int, List]:
    return groupby(log, lambda x: x.guard_id)


def minute_range(start: datetime, end: datetime) -> Iterable[datetime]:
    print(f'START {start}    END {end}')
    dt = start
    while dt < end:
        # print(dt)
        yield dt.time()
        dt += timedelta(minutes=1)


def starts_and_stops(ts: List[LogEntry]):
    return list(zip(
        map(lambda x: x.timestamp, asleeps(ts)),
        map(lambda x: x.timestamp, wakeups(ts))
    ))


def log_to_histogram(ts: List[LogEntry]) -> Counter:
    counts = Counter()
    TS = starts_and_stops(ts)
    for start, stop in TS:
        print(start, stop)
        counts.update(minute_range(start, stop))
    return counts


def parse_line(line: str, previous_guard_id: int=None) -> LogEntry:
    if '#' in line:
        raw_dt, guard_id = re.match(
            '\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] Guard #(\d+) begins shift',
            line
        ).groups()

        return LogEntry(
            guard_id=int(guard_id),
            event=Event.BEGIN,
            timestamp=parse_datetime(raw_dt),
        )

    else:
        assert previous_guard_id is not None
        raw_dt, raw_event = re.match(
            '^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)$',
            line
        ).groups()

        event_dt: datetime = parse_datetime(raw_dt)
        event: Event = parse_event(raw_event)

        return LogEntry(
            guard_id=previous_guard_id,
            event=event,
            timestamp=event_dt,
        )

def ever_asleep(ts: List[LogEntry]) -> bool:
    return any(x.event is FALL_ASLEEP for x in ts)

def part_two(log_by_guard: Dict[int, List[LogEntry]]) -> Dict[int, Counter]:
    return {
        k: log_to_histogram(v).most_common(1)
        for k, v in log_by_guard.items()
        if ever_asleep(v)
    }

ls = parse_log('d4_sorted.txt')
gs = parse_guards(ls)
G = gs[1319]
time_sleep(G)

_g_id, _ts  = max(gs.items(), key=lambda x: time_sleep(x[1]))
TS = log_to_histogram(_ts)

