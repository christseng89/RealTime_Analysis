from airflow.timetables.base import DagRunInfo, DataInterval, Timetable
from pendulum import DateTime, duration
import pendulum

# Define a list of holidays
HOLIDAYS = [
    pendulum.date(2024, 1, 1),  # New Year's Day
    pendulum.date(2024, 12, 25),  # Christmas Day
    # Add other holidays here
]

class CustomHolidayTimetable(Timetable):
    def infer_manual_data_interval(self, run_after: DateTime) -> DataInterval:
        start = run_after - duration(days=1)
        end = run_after
        return DataInterval(start=start, end=end)

    def next_dagrun_info(
        self,
        last_automated_data_interval: DataInterval,
        restriction: Timetable.Restriction,
    ) -> DagRunInfo | None:
        if last_automated_data_interval is None:
            next_start = DateTime(2023, 1, 1)
        else:
            next_start = last_automated_data_interval.end

        if restriction.earliest and next_start < restriction.earliest:
            next_start = restriction.earliest

        # Find the next valid day that is not a holiday or weekend
        while next_start in HOLIDAYS or next_start.weekday() in (5, 6):  # 5 and 6 are Saturday and Sunday
            next_start += duration(days=1)

        next_end = next_start + duration(days=1)

        if restriction.latest and next_start > restriction.latest:
            return None

        return DagRunInfo.interval(start=next_start, end=next_end)
