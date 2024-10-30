# services/analytics/app/services/metrics_aggregator.py
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from services.analytics.app.models.schemas import (
    MetricType,
    MetricValue,
    TimeRange,
    TimeSeriesPoint,
)
from shared.database.models import User, Post, Comment, Reaction, Pet, Group, MediaFile


class MetricsAggregator:
    @staticmethod
    async def calculate_growth(current_value: float, previous_value: float) -> float:
        if previous_value == 0:
            return 100.0 if current_value > 0 else 0.0
        return ((current_value - previous_value) / previous_value) * 100

    @staticmethod
    async def get_time_range_dates(
        time_range: TimeRange,
        custom_start: Optional[datetime] = None,
        custom_end: Optional[datetime] = None,
    ) -> tuple[datetime, datetime]:
        end_date = custom_end or datetime.utcnow()

        if time_range == TimeRange.CUSTOM and custom_start:
            return custom_start, end_date

        if time_range == TimeRange.DAY:
            start_date = end_date - timedelta(days=1)
        elif time_range == TimeRange.WEEK:
            start_date = end_date - timedelta(weeks=1)
        elif time_range == TimeRange.MONTH:
            start_date = end_date - timedelta(days=30)
        else:  # YEAR
            start_date = end_date - timedelta(days=365)

        return start_date, end_date

    @staticmethod
    async def get_time_series_data(
        db: Session,
        query,
        time_range: TimeRange,
        custom_start: Optional[datetime] = None,
        custom_end: Optional[datetime] = None,
        granularity: str = "day",
    ) -> List[TimeSeriesPoint]:
        start_date, end_date = await MetricsAggregator.get_time_range_dates(
            time_range, custom_start, custom_end
        )

        # Ajustar la agrupación según la granularidad
        if granularity == "hour":
            group_by = func.date_trunc("hour", query.timestamp)
        elif granularity == "week":
            group_by = func.date_trunc("week", query.timestamp)
        elif granularity == "month":
            group_by = func.date_trunc("month", query.timestamp)
        else:  # default to day
            group_by = func.date_trunc("day", query.timestamp)

        results = (
            db.query(group_by.label("timestamp"), func.count().label("value"))
            .filter(and_(query.timestamp >= start_date, query.timestamp <= end_date))
            .group_by("timestamp")
            .order_by("timestamp")
            .all()
        )

        return [
            TimeSeriesPoint(timestamp=r.timestamp, value=float(r.value))
            for r in results
        ]

    @staticmethod
    async def get_metric_value(
        current_value: float,
        previous_value: float,
        metric_type: MetricType = MetricType.COUNT,
    ) -> MetricValue:
        if metric_type == MetricType.PERCENTAGE:
            value = (current_value / previous_value * 100) if previous_value > 0 else 0
        else:
            value = current_value

        change_percentage = await MetricsAggregator.calculate_growth(
            current_value, previous_value
        )

        trend = (
            "up"
            if change_percentage > 0
            else "down" if change_percentage < 0 else "stable"
        )

        return MetricValue(
            value=value, change_percentage=change_percentage, trend=trend
        )

    @staticmethod
    async def get_distribution_data(
        db: Session,
        query,
        group_by_column,
        time_range: TimeRange,
        custom_start: Optional[datetime] = None,
        custom_end: Optional[datetime] = None,
    ) -> Dict[str, float]:
        start_date, end_date = await MetricsAggregator.get_time_range_dates(
            time_range, custom_start, custom_end
        )

        results = (
            db.query(group_by_column, func.count().label("count"))
            .filter(and_(query.timestamp >= start_date, query.timestamp <= end_date))
            .group_by(group_by_column)
            .all()
        )

        total = sum(r.count for r in results)

        return {str(r[0]): (r.count / total * 100) if total > 0 else 0 for r in results}
