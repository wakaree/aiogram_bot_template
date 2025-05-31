from datetime import datetime

from fluent.runtime.types import FluentDateTime


def ftl_time(
    value: datetime,
    date_style: str = "medium",
    time_style: str = "medium",
) -> FluentDateTime:
    return FluentDateTime.from_date_time(
        dt_obj=value,
        dateStyle=date_style,
        timeStyle=time_style,
    )
