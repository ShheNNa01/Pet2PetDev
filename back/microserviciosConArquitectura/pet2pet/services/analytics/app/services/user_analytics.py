# services/analytics/app/services/user_analytics.py
from datetime import datetime
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from services.analytics.app.models.schemas import (
    MetricType,
    TimeRange,
    TimeSeriesMetric,
    UserActivityMetrics,
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import User, Pet, Post, Reaction


class UserAnalyticsService:
    def __init__(self):
        self.metrics = MetricsAggregator()

    async def get_user_activity_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        custom_start: datetime = None,
        custom_end: datetime = None,
    ) -> UserActivityMetrics:
        start_date, end_date = await self.metrics.get_time_range_dates(
            time_range, custom_start, custom_end
        )
        prev_start = start_date - (end_date - start_date)

        # Total usuarios
        current_total = db.query(User).filter(User.created_at <= end_date).count()

        previous_total = db.query(User).filter(User.created_at <= prev_start).count()

        # Usuarios activos (con actividad en el período)
        current_active = (
            db.query(User)
            .filter(and_(User.last_login >= start_date, User.last_login <= end_date))
            .count()
        )

        previous_active = (
            db.query(User)
            .filter(and_(User.last_login >= prev_start, User.last_login <= start_date))
            .count()
        )

        # Nuevos registros
        new_users = (
            db.query(User)
            .filter(and_(User.created_at >= start_date, User.created_at <= end_date))
            .count()
        )

        previous_new_users = (
            db.query(User)
            .filter(and_(User.created_at >= prev_start, User.created_at <= start_date))
            .count()
        )

        # Crecimiento de usuarios en el tiempo
        growth_data = await self.metrics.get_time_series_data(
            db, User.created_at, time_range, start_date, end_date
        )

        # Tasa de retención
        retention_rate = (
            (current_active / current_total * 100) if current_total > 0 else 0
        )
        prev_retention = (
            (previous_active / previous_total * 100) if previous_total > 0 else 0
        )

        # Tasa de abandono
        churn_rate = 100 - retention_rate
        prev_churn = 100 - prev_retention

        return UserActivityMetrics(
            total_users=await self.metrics.get_metric_value(
                current_total, previous_total
            ),
            active_users=await self.metrics.get_metric_value(
                current_active, previous_active
            ),
            new_registrations=await self.metrics.get_metric_value(
                new_users, previous_new_users
            ),
            user_growth=TimeSeriesMetric(
                name="User Growth",
                data=growth_data,
                total=sum(point.value for point in growth_data),
                average=(
                    sum(point.value for point in growth_data) / len(growth_data)
                    if growth_data
                    else 0
                ),
                change_percentage=await self.metrics.calculate_growth(
                    new_users, previous_new_users
                ),
            ),
            retention_rate=await self.metrics.get_metric_value(
                retention_rate, prev_retention, MetricType.PERCENTAGE
            ),
            churn_rate=await self.metrics.get_metric_value(
                churn_rate, prev_churn, MetricType.PERCENTAGE
            ),
        )
