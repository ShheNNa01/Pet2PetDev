# services/analytics/app/services/engagement_analytics.py
from datetime import datetime
from typing import Dict, List
from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session
from services.analytics.app.models.schemas import (
    EngagementMetrics,
    TimeRange,
    TimeSeriesMetric,
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import Post, Comment, Reaction, User, Pet, GroupMember


class EngagementAnalyticsService:
    def __init__(self):
        self.metrics = MetricsAggregator()

    async def get_engagement_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        custom_start: datetime = None,
        custom_end: datetime = None,
    ) -> EngagementMetrics:
        start_date, end_date = await self.metrics.get_time_range_dates(
            time_range, custom_start, custom_end
        )
        prev_start = start_date - (end_date - start_date)

        # Total interacciones
        current_interactions = await self.get_total_interactions(
            db, start_date, end_date
        )

        previous_interactions = await self.get_total_interactions(
            db, prev_start, start_date
        )

        # Interacciones por tipo
        interaction_distribution = await self.get_interaction_type_distribution(
            db, time_range, start_date, end_date
        )

        # Engagement por tiempo
        engagement_timeline = await self.metrics.get_time_series_data(
            db, Reaction.created_at, time_range, start_date, end_date, "hour"
        )

        # Duración promedio de sesión (simulada o calculada desde logs)
        current_session_duration = await self.get_avg_session_duration(
            db, start_date, end_date
        )

        previous_session_duration = await self.get_avg_session_duration(
            db, prev_start, start_date
        )

        # Horas pico de actividad
        peak_hours = await self.get_peak_activity_hours(db, start_date, end_date)

        # Segmentos de usuarios por nivel de engagement
        user_segments = await self.get_user_segments(db, start_date, end_date)

        return EngagementMetrics(
            total_interactions=await self.metrics.get_metric_value(
                current_interactions, previous_interactions
            ),
            interaction_types=interaction_distribution,
            engagement_by_time=TimeSeriesMetric(
                name="Hourly Engagement",
                data=engagement_timeline,
                total=sum(point.value for point in engagement_timeline),
                average=(
                    sum(point.value for point in engagement_timeline)
                    / len(engagement_timeline)
                    if engagement_timeline
                    else 0
                ),
                change_percentage=await self.metrics.calculate_growth(
                    current_interactions, previous_interactions
                ),
            ),
            avg_session_duration=await self.metrics.get_metric_value(
                current_session_duration, previous_session_duration
            ),
            peak_activity_hours=peak_hours,
            user_segments=user_segments,
        )

    async def get_total_interactions(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> int:
        reactions = (
            db.query(Reaction)
            .filter(
                and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
            )
            .count()
        )

        comments = (
            db.query(Comment)
            .filter(
                and_(Comment.created_at >= start_date, Comment.created_at <= end_date)
            )
            .count()
        )

        return reactions + comments

    async def get_interaction_type_distribution(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        # Obtener diferentes tipos de interacciones
        reactions = (
            db.query(Reaction.reaction_type, func.count().label("count"))
            .filter(
                and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
            )
            .group_by(Reaction.reaction_type)
            .all()
        )

        comments = (
            db.query(Comment)
            .filter(
                and_(Comment.created_at >= start_date, Comment.created_at <= end_date)
            )
            .count()
        )

        total = sum(r.count for r in reactions) + comments

        distribution = {
            f"reaction_{r.reaction_type}": (r.count / total * 100) if total > 0 else 0
            for r in reactions
        }
        distribution["comments"] = (comments / total * 100) if total > 0 else 0

        return distribution

    async def get_avg_session_duration(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> float:
        # En una implementación real, esto vendría de logs de sesión
        # Este es un ejemplo simulado
        return 15.5  # minutos

    async def get_peak_activity_hours(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, float]]:
        hour_counts = (
            db.query(
                extract("hour", Reaction.created_at).label("hour"),
                func.count().label("count"),
            )
            .filter(
                and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
            )
            .group_by("hour")
            .order_by(func.count().desc())
            .limit(5)
            .all()
        )

        total = sum(r.count for r in hour_counts)

        return [
            {
                "hour": f"{int(hour):02d}:00",
                "percentage": (count / total * 100) if total > 0 else 0,
            }
            for hour, count in hour_counts
        ]

    async def get_user_segments(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, float]]:
        # Clasificar usuarios por nivel de engagement
        user_interactions = (
            db.query(User.user_id, func.count().label("interaction_count"))
            .join(Reaction)
            .filter(
                and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
            )
            .group_by(User.user_id)
            .all()
        )

        total_users = len(user_interactions)

        # Clasificar usuarios en segmentos
        high_engagement = len(
            [u for u in user_interactions if u.interaction_count > 50]
        )
        medium_engagement = len(
            [u for u in user_interactions if 20 <= u.interaction_count <= 50]
        )
        low_engagement = len([u for u in user_interactions if u.interaction_count < 20])

        return [
            {
                "segment": "High Engagement",
                "percentage": (
                    (high_engagement / total_users * 100) if total_users > 0 else 0
                ),
            },
            {
                "segment": "Medium Engagement",
                "percentage": (
                    (medium_engagement / total_users * 100) if total_users > 0 else 0
                ),
            },
            {
                "segment": "Low Engagement",
                "percentage": (
                    (low_engagement / total_users * 100) if total_users > 0 else 0
                ),
            },
        ]
