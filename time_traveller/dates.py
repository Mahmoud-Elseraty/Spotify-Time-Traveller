import calendar
import re
from datetime import date, datetime, timezone

_MONTH_YEAR = re.compile(r"^(\d{1,2})-(\d{4})$")


def parse_date(value, end=False):
    """Parse YYYY-MM-DD, MM-YYYY or a date object. Month-only values span the whole month."""
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        year, month, day = value.year, value.month, value.day
    else:
        text = str(value).strip()
        match = _MONTH_YEAR.match(text)
        if match:
            month, year = int(match.group(1)), int(match.group(2))
            day = calendar.monthrange(year, month)[1] if end else 1
        else:
            parsed = datetime.strptime(text, "%Y-%m-%d")
            year, month, day = parsed.year, parsed.month, parsed.day
    if end:
        return datetime(year, month, day, 23, 59, 59, 999999, tzinfo=timezone.utc)
    return datetime(year, month, day, tzinfo=timezone.utc)


def parse_range(start, end):
    start_dt, end_dt = parse_date(start), parse_date(end, end=True)
    if start_dt > end_dt:
        raise ValueError("start date is after end date")
    return start_dt, end_dt


def parse_added_at(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def in_range(added_at, start, end):
    return start <= parse_added_at(added_at) <= end
