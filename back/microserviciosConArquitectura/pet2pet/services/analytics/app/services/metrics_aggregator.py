# services/analytics/app/services/metrics_aggregator.py
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract, text
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from services.analytics.app.models.schemas import (
    MetricType,
    MetricValue,
    TimeRange,
    TimeSeriesPoint,
)
import logging

logger = logging.getLogger(__name__)

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
        date_column,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
        granularity: str = "day",
    ) -> List[TimeSeriesPoint]:
        try:
            # Ajustar la agrupación según la granularidad
            if granularity == "hour":
                group_by = func.date_trunc("hour", date_column)
            elif granularity == "week":
                group_by = func.date_trunc("week", date_column)
            elif granularity == "month":
                group_by = func.date_trunc("month", date_column)
            else:  # default to day
                group_by = func.date_trunc("day", date_column)

            results = (
                db.query(
                    group_by.label("timestamp"),
                    func.count().label("value")
                )
                .filter(and_(date_column >= start_date, date_column <= end_date))
                .group_by("timestamp")
                .order_by("timestamp")
                .all()
            )

            return [
                TimeSeriesPoint(timestamp=r.timestamp, value=float(r.value))
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error getting time series data: {str(e)}")
            return []

    @staticmethod
    async def get_metric_value(
        current_value: float,
        previous_value: float,
        metric_type: MetricType = MetricType.COUNT,
    ) -> MetricValue:
        try:
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
                value=value,
                change_percentage=change_percentage,
                trend=trend
            )
        except Exception as e:
            logger.error(f"Error calculating metric value: {str(e)}")
            return MetricValue(value=0, change_percentage=0, trend="stable")

    @staticmethod
    async def get_distribution_data(
        db: Session,
        date_column,
        group_by_column,
        time_range: TimeRange,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, float]:
        try:
            results = (
                db.query(
                    group_by_column,
                    func.count().label("count")
                )
                .filter(and_(date_column >= start_date, date_column <= end_date))
                .group_by(group_by_column)
                .all()
            )

            total = sum(r.count for r in results)

            return {
                str(r[0]): (r.count / total * 100) if total > 0 else 0
                for r in results
            }
        except Exception as e:
            logger.error(f"Error getting distribution data: {str(e)}")
            return {}