from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import date
from enum import Enum, Flag, auto
from typing import List, Literal, Optional, Optional
from pendulum import (
    Date,
    Duration,
    FixedTimezone,
    Timezone,
    interval,
    now,
    Time,
    local_timezone,
    UTC,
    today,
)
import pendulum
from pendulum.datetime import DateTime
from pendulum.day import WeekDay as PDWeekDay
from src.shelly.dimmer2 import Dimmer2

dimmer = Dimmer2()
tz: Timezone | FixedTimezone = local_timezone()
if not isinstance(tz, Timezone):
    tz = UTC


"""
def day_comparator(
    day: PDWeekDay | DayOfMonth | DateTime, comparison_date: DateTime = today()
) -> DayComparison:
    p = {}
    output = DayComparison(0)
    if isinstance(day, DayOfMonth):
        day = today().replace(day=day.day)


    if day.week_of_month is not None:

        week1, week2 = day.week_of_month, comparison_date.week_of_month
        p.update(
            {"week": {"gt": week1 > week2, "lt": week1 < week2, "eq": week1 == week2}}
        )

    if isinstance(day, (DateTime, WeekDay)):
        wd1 = day.day_of_week
        wd2 = comparison_date.day_of_week
        p.update({"weekday": {"gt": wd1 > wd2, "lt": wd1 < wd2, "eq": wd1 == wd2}})

    match p:
        case {"weekday": {"eq": True}}:
            output |= DayComparison.same_weekday
        case {"weekday": {"lt": True}}:
            output |= DayComparison.earlier_weekday
        case {"weekday": {"gt": True}}:
            output |= DayComparison.later_weekday

    return output

"""
class DayComparison(Flag):
    same_week = auto()
    same_weekday = auto()
    earlier_weekday = auto()
    later_weekday = auto()
    earlier_week = auto()
    later_week = auto()
    same_day = 3
    earlier_in_week = 5
    later_in_week = 9


@dataclass
class DayOfMonth:
    day: int

    def __post_init__(self):
        if self.day < 1 or self.day > 31:
            raise ValueError(f"Invalid day: {self.day}")


class WeekOfMonth(Enum):
    first = 1
    second = 2
    third = 3
    fourth = 4
    fifth = 5


def all_weekday_in_month(weekday: PDWeekDay, month: int, year: int) -> List[DateTime]:

    days_in_month = pendulum.DateTime(year=year, month=month, day=1).days_in_month

    result = [
        pendulum.DateTime(year=year, month=month, day=day)
        for day in range(1,  days_in_month + 1)
        if pendulum.DateTime(year=year, month=month, day=day).day_of_week == weekday
    ]

    return result

def nth_weekday_in_month(
    weekday: PDWeekDay, month: int, year: int, week_of_month: WeekOfMonth,
) -> DateTime:
    weekdays = all_weekday_in_month(weekday, month, year)
    return weekdays[week_of_month.value - 1]


from dataclasses import dataclass
from typing import Optional, Union, Literal

@dataclass
class Repeater:
    """
    A class to manage and calculate repeating intervals based on durations,
    weekdays, and specific days of the month.

    Attributes
    ----------
    interval : Duration or PDWeekDay or DayOfMonth
        The interval specification, which can be a duration, weekday, or day of the month.
    start : DateTime or Date, optional
        The start date and time of the interval. Defaults to the current time if not provided.
    expires : DateTime or Date, optional
        The expiration date and time of the interval.
    week_of_month : WeekOfMonth, optional
        Specifies the week of the month to consider when dealing with intervals.
    last_run : DateTime, optional
        The last run time of the interval.
    """

    interval: Union[Duration, PDWeekDay, DayOfMonth]
    start: Optional[Union[DateTime, Date]] = None
    expires: Optional[Union[DateTime, Date]] = None
    week_of_month: Optional[WeekOfMonth] = None
    last_run: Optional[DateTime] = None

    def __post_init__(self):
        """
        Post-initialization to validate the interval and set the start time.

        Raises
        ------
        ValueError
            If the interval is invalid or inverted for durations.
        """
        if isinstance(self.interval, Duration) and self.interval.invert:
            raise ValueError(f"Invalid interval: {self.interval}")
        if self.start is None:
            self.start = now()

    @property
    def by_duration(self) -> bool:
        """
        Checks if the interval is based on a duration.

        Returns
        -------
        bool
            True if the interval is a Duration, False otherwise.
        """
        return isinstance(self.interval, Duration)

    @property
    def is_week_of_month(self) -> bool:
        """
        Checks if the current week of the month matches the specified week.

        Returns
        -------
        bool
            True if the week of the month matches, False otherwise.
        """
        return self.week_of_month is not None and self.week_of_month.value == today().week_of_month

    @property
    def by_weekday(self) -> bool:
        """
        Checks if the interval is based on a weekday.

        Returns
        -------
        bool
            True if the interval is a PDWeekDay and no specific week of the month is specified.
        """
        return isinstance(self.interval, PDWeekDay) and self.week_of_month is None

    @property
    def is_weekday(self) -> bool:
        """
        Checks if today is the specified weekday.

        Returns
        -------
        bool
            True if today is the interval's weekday, False otherwise.
        """
        return isinstance(self.interval, PDWeekDay) and self.interval == today().day_of_week

    @property
    def next(self) -> Optional[Union[DateTime, Date]]:
        """
        Calculates the next occurrence of the interval.

        Returns
        -------
        DateTime or Date, optional
            The next occurrence of the interval, or None if not applicable.

        Raises
        ------
        ValueError
            If the pattern is invalid or unsupported.
        """
        now_ = now()

        prop_attr_dict = {
            "expired": self.expired,
            "after_start": self.started,
            "running": self.running,
            "by_weekday": self.by_weekday,
            "is_week_of_month": self.is_week_of_month,
            "is_weekday": self.is_weekday,
            "last_run_is_none": self.last_run is None,
            "by_duration": self.by_duration,
            # "after_week_of_month": self.after_week_of_month,
            # "before_week_of_month": self.before_week_of_month,
            # "after_weekday": self.after_weekday,
            # "before_weekday": self.before_weekday,
            # "after_week_of_month_or_weekday": (
            #     self.after_week_of_month or self.after_weekday
            # ),
            # "before_week_of_month_or_weekday": (
            #     self.before_week_of_month or self.before_weekday
            # ),
            # "by_week_of_month_weekday": self.by_week_of_month_weekday,
            # "by_day_of_month": self.by_day_of_month,
            **self.__dict__,
        }

        ptn = {
            **{f"{k}_type": type(v).__name__ for k, v in self.__dict__.items()},
            **{k: v for k, v in prop_attr_dict.items()},
        }
        match ptn:
            # Specific cases for calculating the next interval occurrence
            case {'running': False, 'by_weekday': True}:
                assert isinstance(self.interval, PDWeekDay)
                assert isinstance(self.start, DateTime)
                if self.start.day_of_week == self.interval:
                    return self.start
                elif self.start.day_of_week < self.interval:
                    return self.start.add(days=self.interval - self.start.day_of_week)
                else:
                    return (
                        self.start.add(weeks=1)
                        .subtract(days=self.start.day_of_week - self.interval)
                    )

            case {'running': False, 'by_day_of_month': True}:
                assert isinstance(self.interval, DayOfMonth)
                assert isinstance(self.start, DateTime)
                compare = self.start.replace(day=self.interval.day)
                if self.start <= compare:
                    return compare
                return self.target_date_for_month_delta(date=self.start, month_delta=1)

            case {'running': False, 'by_week_of_month_weekday': True}:
                assert isinstance(self.start, DateTime)
                return self._month_week_of_month(date=self.start, next_or_prev="next")

            case {'by_duration': True}:
                assert isinstance(self.interval, Duration)
                assert self.last_run is not None
                return self.last_run

            case {'by_weekday': True, "is_weekday": True}:
                return now_

            case {"by_weekday": True, "before_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return now_.add(days=self.interval - now_.day_of_week)

            case {"by_weekday": True, "after_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return now_.add(weeks=1).subtract(days=now_.day_of_week - self.interval)

            case {"by_week_of_month_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return self.next_week_of_month

            case {"by_day_of_month": True, "running": True}:
                assert isinstance(self.interval, DayOfMonth)
                return self.target_date_for_month_delta(1)

            case _:
                raise ValueError(f"Invalid repeater pattern: {ptn}")

    @property
    def prev(self) -> Optional[Union[DateTime, Date]]:
        """
        Calculates the previous occurrence of the interval.

        Returns
        -------
        DateTime or Date, optional
            The previous occurrence of the interval, or None if not applicable.

        Raises
        ------
        ValueError
            If the pattern is invalid or unsupported.
        """
        now_ = now()

        prop_attr_dict = {
            "expired": self.expired,
            "after_start": self.started,
            "running": self.running,
            "by_weekday": self.by_weekday,
            # "after_week_of_month": self.after_week_of_month,
            # "before_week_of_month": self.before_week_of_month,
            # "is_week_of_month": self.is_week_of_month,
            # "after_weekday": self.after_weekday,
            # "before_weekday": self.before_weekday,
            # "is_weekday": self.is_weekday,
            # "after_week_of_month_or_weekday": (
            #     self.after_week_of_month or self.after_weekday
            # ),
            # "before_week_of_month_or_weekday": (
            #     self.before_week_of_month or self.before_weekday
            # ),
            # "last_run_is_none": self.last_run is None,
            # "by_day_of_month": self.by_day_of_month,
            # "by_duration": self.by_duration,
            # "by_week_of_month_weekday": self.by_week_of_month_weekday,
            **self.__dict__,
        }

        ptn = {
            **{f"{k}_type": type(v).__name__ for k, v in self.__dict__.items()},
            **{k: v for k, v in prop_attr_dict.items()},
        }
        match ptn:
            # Specific cases for calculating the previous interval occurrence
            case {'running': False}:
                return

            case {'by_duration': True}:
                assert isinstance(self.interval, Duration)
                assert self.last_run is not None
                return self.last_run

            case {'by_weekday': True, "is_weekday": True}:
                return now_

            case {"by_weekday": True, "before_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return now_.subtract(weeks=1).add(days=self.interval - now_.day_of_week)

            case {"by_weekday": True, "after_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return now_.subtract(days=now_.day_of_week - self.interval)

            case {"by_week_of_month_weekday": True}:
                assert isinstance(self.interval, PDWeekDay)
                return self.prev_week_of_month

            case {"by_day_of_month": True, "running": True}:
                assert isinstance(self.interval, DayOfMonth)
                return self.target_date_for_month_delta(-1)

            case _:
                raise ValueError(f"Invalid repeater pattern: {ptn}")

    def target_date_for_month_delta(
        self,
        month_delta: int,
        date: DateTime = today(),
    ) -> DateTime:
        """
        Calculate the target date for a different month, adjusting for months
        where the target day might not exist (e.g., February 31).

        Parameters
        ----------
        month_delta : int
            The number of months to add or subtract.
        date : DateTime, optional
            The base date from which to calculate the new date. Defaults to today.

        Returns
        -------
        DateTime
            The adjusted target date.

        Raises
        ------
        AssertionError
            If the interval is not a DayOfMonth.
        """
        operator = "add" if month_delta > 0 else "subtract"
        assert isinstance(self.interval, DayOfMonth)

        result = getattr(date.replace(day=1), operator)(months=month_delta)

        while result.days_in_month < self.interval.day:
            result = getattr(result, operator)(months=month_delta)

        return result.replace(day=self.interval.day)

    def _month_week_of_month(
        self,
        next_or_prev: Literal["next", "prev"],
        date: DateTime = today(),
    ) -> DateTime:
        """
        Get the date corresponding to the next or previous occurrence of the specified
        week of the month.

        Parameters
        ----------
        next_or_prev : {"next", "prev"}
            The direction to move: "next" for the upcoming week, "prev" for the previous week.
        date : DateTime, optional
            The base date to use for calculation. Defaults to today.

        Returns
        -------
        DateTime
            The calculated date for the specified week of the month.

        Raises
        ------
        ValueError
            If the interval or week_of_month is invalid.
        """
        typechecks = [
            (self.interval, PDWeekDay),
            (self.week_of_month, WeekOfMonth),
        ]
        if not all(isinstance(a, b) for a, b in typechecks):
            raise ValueError(f"Invalid interval: {self.interval}")

        date_current_month = date.replace(day=1)
        date_next_month = date.replace(day=1).add(months=1)
        date_prev_month = date.replace(day=1).subtract(months=1)

        current_month, year = date_current_month.month, date_current_month.year
        next_month, year = date_next_month.month, date_next_month.year
        prev_month, year = date_prev_month.month, date_prev_month.year

        assert isinstance(self.interval, PDWeekDay)
        assert isinstance(self.week_of_month, WeekOfMonth)
        result = nth_weekday_in_month(
            weekday=self.interval,
            month=current_month,
            year=year,
            week_of_month=self.week_of_month,
        )
        if (
            (next_or_prev == "next" and result > date)
            or (next_or_prev == "prev" and result < date)
        ):
            return result

        result = nth_weekday_in_month(
            weekday=self.interval,
            month={'next': next_month, 'prev': prev_month}[next_or_prev],
            year=year,
            week_of_month=self.week_of_month,
        )
        return result

    @property
    def next_week_of_month(self) -> DateTime:
        """
        Calculates the date for the next occurrence of the specified week of the month.

        Returns
        -------
        DateTime
            The calculated date for the next occurrence.
        """
        return self._month_week_of_month("next")

    @property
    def prev_week_of_month(self) -> DateTime:
        """
        Calculates the date for the previous occurrence of the specified week of the month.

        Returns
        -------
        DateTime
            The calculated date for the previous occurrence.
        """
        return self._month_week_of_month("prev")

    @property
    def started(self) -> bool:
        """
        Checks if the interval has started.

        Returns
        -------
        bool
            True if the interval's start time is in the past, False otherwise.

        Raises
        ------
        ValueError
            If the start attribute is invalid.
        """
        if isinstance(self.start, (DateTime, Date)):
            return self.start < now()
        else:
            raise ValueError(f"Invalid start: {self.start}")

    @property
    def expired(self) -> bool:
        """
        Checks if the interval has expired.

        Returns
        -------
        bool
            True if the interval's expiration time is in the past, False otherwise.
        """
        return self.expires is not None and self.expires < now()

    @property
    def running(self) -> bool:
        """
        Checks if the interval is currently running.

        Returns
        -------
        bool
            True if the interval has started and has not expired, False otherwise.
        """
        return self.started and not self.expired

class WeekDay:
    day_of_week: PDWeekDay
    week_of_month: Optional[Literal[1, 2, 3, 4, 5]] = None
    tz: Timezone = tz

    def __init__(
        self,
        weekday: PDWeekDay | str | int,
        nth_weekday: Optional[Literal[1, 2, 3, 4, 5]] = None,
    ):
        if isinstance(weekday, str):
            weekday = weekday.upper()
            weekday_candidate = [
                d for d in [*PDWeekDay.__members__] if d.startswith(weekday)
            ]
            if len(weekday_candidate) == 1:
                weekday = PDWeekDay[weekday_candidate[0]]
            else:
                raise ValueError(f"Invalid weekday: {weekday}")
        elif isinstance(weekday, int):
            if weekday < 1 or weekday > 6:
                raise ValueError(f"Invalid weekday: {weekday}")
            weekday = PDWeekDay(weekday)
        self.day_of_week = weekday

        if nth_weekday is None:
            self.week_of_month = None
        elif nth_weekday < 1 or nth_weekday > 5:
            raise ValueError(f"Invalid nth_of_month: {nth_weekday}")
        else:
            self.week_of_month = nth_weekday

    def __lt__(self, other):
        if isinstance(other, DateTime):
            return self.day_of_week < other.day_of_week
        elif isinstance(other, WeekDay):
            return self.day_of_week < other.day_of_week
        elif isinstance(other, PDWeekDay):
            return self.day_of_week < other
        else:
            raise ValueError(f"Invalid comparison: {other}")

    def __eq__(self, other):
        if isinstance(other, DateTime):
            return self.day_of_week == other.day_of_week
        elif isinstance(other, WeekDay):
            return self.day_of_week == other.day_of_week
        elif isinstance(other, PDWeekDay):
            return self.day_of_week == other
        else:
            raise ValueError(f"Invalid comparison: {other}")

    def __gt__(self, other):
        if isinstance(other, DateTime):
            return self.day_of_week > other.day_of_week
        elif isinstance(other, WeekDay):
            return self.day_of_week > other.day_of_week
        elif isinstance(other, PDWeekDay):
            return self.day_of_week > other
        else:
            raise ValueError(f"Invalid comparison: {other}")


class When:
    tz: Timezone = tz

    def __init__(
        self,
        time: Time | str,
        start: Optional[DateTime] = None,
        end: Optional[DateTime] = None,
        repeater: Repeater = None,
    ):
        if start is None:
            start = now(tz=self.tz)
        if isinstance(time, str):
            self.time = self._parse_time(time)

        self.start: DateTime = start or now()
        self.end = end
        self.repeater = repeater
        self.last_run: Optional[DateTime] = None

    def next_run(self):
        today_ = today()

    def previous_run(self) -> Optional[DateTime]: ...

    # def next_run(self) -> Optional[DateTime]:
    #     pattern = dict(
    #         running=self.running,
    #         repeating=self.repeater is None,
    #         has_run=self.last_run is not None,
    #     )
    #     comparison = day_comparator(self.repeater)
    #     match pattern:
    #
    #         case {"running": True, "has_run": False}:
    #             return self.start
    #
    #         case {"running": True, "repeating": False, "has_run": True}:
    #             return None
    #
    #         case {"running": True, "repeating": True, "has_run": True}:
    #             match comparison:
    #                 case
    #
    #
    #
    #
    #         case _:
    #             ...
    #

    @property
    def day_of_month(self) -> Optional[int]:
        if isinstance(self.repeater, DayOfMonth):
            return self.repeater.day

    @property
    def expired(self) -> bool:
        if self.end is not None and self.end < now():
            return True
        return False

    @property
    def running(self) -> bool:
        return not self.started or self.expired

    @property
    def started(self) -> bool:
        if self.start < now():
            return True
        return False

    @property
    def week_of_month(self) -> Optional[Literal[1, 2, 3, 4, 5]]:
        if isinstance(self.repeater, WeekDay):
            return self.repeater.week_of_month

    @property
    def weekday(self) -> Optional[PDWeekDay]:
        if isinstance(self.repeater, WeekDay):
            return self.repeater.day_of_week

    @staticmethod
    def _parse_time(time: str) -> Time:
        if "PM" not in time.upper():
            parsed = pendulum.parse(time.upper().replace("AM", ""))
            if isinstance(parsed, DateTime):
                return parsed.time()
            else:
                raise ValueError(f"Invalid time: {time}")

        parts = [int(t) for t in time.split(":")]
        parts[0] += 12
        return Time(*parts, tzinfo=local_timezone())


class ScheduledEvent:
    def __init__(self, dimmer: Dimmer2, when: When, action: str):
        self.dimmer = dimmer
        self.when = when
        self.action = action

    @property
    def time(self):
        return self.when.time

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time

    def __repr__(self):
        return f"<ScheduledEvent {self.dimmer} {self.time} {self.action}>"
