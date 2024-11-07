# services/analytics/app/services/user_analytics.py
from datetime import datetime
from typing import Dict, List
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session
from services.analytics.app.models.schemas import (
    MetricType,
    TimeRange,
    TimeSeriesMetric,
    UserActivityMetrics,
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import User, Post, Reaction, Comment
from sqlalchemy import or_
import logging

logger = logging.getLogger(__name__)

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

        # Usuarios activos (con alguna actividad en el período)
        current_active = (
            db.query(User.user_id)
            .distinct()
            .join(Post, User.user_id == Post.user_id, isouter=True)
            .join(Comment, User.user_id == Comment.user_id, isouter=True)
            .join(Reaction, User.user_id == Reaction.user_id, isouter=True)
            .filter(
                or_(
                    and_(Post.created_at >= start_date, Post.created_at <= end_date),
                    and_(Comment.created_at >= start_date, Comment.created_at <= end_date),
                    and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
                )
            )
            .count()
        )

        previous_active = (
            db.query(User.user_id)
            .distinct()
            .join(Post, User.user_id == Post.user_id, isouter=True)
            .join(Comment, User.user_id == Comment.user_id, isouter=True)
            .join(Reaction, User.user_id == Reaction.user_id, isouter=True)
            .filter(
                or_(
                    and_(Post.created_at >= prev_start, Post.created_at <= start_date),
                    and_(Comment.created_at >= prev_start, Comment.created_at <= start_date),
                    and_(Reaction.created_at >= prev_start, Reaction.created_at <= start_date)
                )
            )
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

        # Tasa de retención (usuarios activos / total usuarios)
        retention_rate = (current_active / current_total * 100) if current_total > 0 else 0
        prev_retention = (previous_active / previous_total * 100) if previous_total > 0 else 0

        # Tasa de abandono (100% - tasa de retención)
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

    async def get_user_segments(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, float]]:
        """
        Clasifica usuarios por nivel de actividad
        """
        try:
            # Contar actividades por usuario
            activity_counts = (
                db.query(
                    User.user_id,
                    func.count(Post.post_id).label('post_count'),
                    func.count(Comment.comment_id).label('comment_count'),
                    func.count(Reaction.reaction_id).label('reaction_count')
                )
                .join(Post, User.user_id == Post.user_id, isouter=True)
                .join(Comment, User.user_id == Comment.user_id, isouter=True)
                .join(Reaction, User.user_id == Reaction.user_id, isouter=True)
                .filter(
                    or_(
                        and_(Post.created_at >= start_date, Post.created_at <= end_date),
                        and_(Comment.created_at >= start_date, Comment.created_at <= end_date),
                        and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
                    )
                )
                .group_by(User.user_id)
                .all()
            )

            total_users = len(activity_counts)
            if total_users == 0:
                return [
                    {"segment": "High Activity", "percentage": 0},
                    {"segment": "Medium Activity", "percentage": 0},
                    {"segment": "Low Activity", "percentage": 0}
                ]

            # Clasificar usuarios
            high_activity = len([u for u in activity_counts 
                               if (u.post_count + u.comment_count + u.reaction_count) > 50])
            medium_activity = len([u for u in activity_counts 
                                 if 20 <= (u.post_count + u.comment_count + u.reaction_count) <= 50])
            low_activity = len([u for u in activity_counts 
                              if (u.post_count + u.comment_count + u.reaction_count) < 20])

            return [
                {
                    "segment": "High Activity",
                    "percentage": (high_activity / total_users * 100)
                },
                {
                    "segment": "Medium Activity",
                    "percentage": (medium_activity / total_users * 100)
                },
                {
                    "segment": "Low Activity",
                    "percentage": (low_activity / total_users * 100)
                }
            ]
        except Exception as e:
            logger.error(f"Error getting user segments: {str(e)}")
            return []