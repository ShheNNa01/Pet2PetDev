# services/analytics/app/services/engagement_analytics.py
from datetime import datetime
from typing import Dict, List
from sqlalchemy import func, and_, extract, or_
from sqlalchemy.orm import Session
import logging
from services.analytics.app.models.schemas import (
    EngagementMetrics,
    TimeRange,
    TimeSeriesMetric,
    MetricValue,
    TimeSeriesPoint,
    UserSegment,
    PeakHour
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import Post, Comment, Reaction, User, Pet, GroupMember

logger = logging.getLogger(__name__)

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
        try:
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
                db, start_date, end_date
            )

            # Engagement por tiempo
            engagement_timeline = await self.metrics.get_time_series_data(
                db=db,
                date_column=Reaction.created_at,
                time_range=time_range,
                start_date=start_date,
                end_date=end_date,
                granularity="hour"
            )

            # Duración promedio de sesión (simulada por ahora)
            current_session_duration = await self.get_avg_session_duration(
                db, start_date, end_date
            )
            previous_session_duration = await self.get_avg_session_duration(
                db, prev_start, start_date
            )

            # Horas pico de actividad
            peak_hours = await self.get_peak_activity_hours(db, start_date, end_date)

            # Segmentos de usuarios
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
        except Exception as e:
            logger.error(f"Error getting engagement metrics: {str(e)}", exc_info=True)
            raise

    async def get_total_interactions(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> int:
        try:
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
        except Exception as e:
            logger.error(f"Error getting total interactions: {str(e)}")
            return 0

    async def get_interaction_type_distribution(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        try:
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
            if total == 0:
                return {"comments": 0}

            distribution = {
                f"reaction_{r.reaction_type}": (r.count / total * 100)
                for r in reactions
            }
            distribution["comments"] = (comments / total * 100)

            return distribution
        except Exception as e:
            logger.error(f"Error getting interaction distribution: {str(e)}")
            return {"comments": 0}

    async def get_avg_session_duration(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> float:
        # Implementación simulada - en una implementación real esto vendría de logs de sesión
        return 15.5  # minutos

    async def get_peak_activity_hours(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> List[PeakHour]:
        try:
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
            if total == 0:
                return []

            return [
                PeakHour(
                    hour=f"{int(hour):02d}:00",
                    percentage=(count / total * 100)
                )
                for hour, count in hour_counts
            ]
        except Exception as e:
            logger.error(f"Error getting peak hours: {str(e)}")
            return []

    async def get_user_segments(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> List[UserSegment]:
        try:
            # Clasificar usuarios por nivel de engagement
            user_interactions = (
                db.query(
                    User.user_id,
                    func.count(Reaction.reaction_id).label("interaction_count")
                )
                .join(Reaction)
                .filter(
                    and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
                )
                .group_by(User.user_id)
                .all()
            )

            total_users = len(user_interactions)
            if total_users == 0:
                return [
                    UserSegment(name="High Engagement", percentage=0),
                    UserSegment(name="Medium Engagement", percentage=0),
                    UserSegment(name="Low Engagement", percentage=0)
                ]

            # Clasificar usuarios en segmentos
            high_engagement = len([u for u in user_interactions if u.interaction_count > 50])
            medium_engagement = len([u for u in user_interactions if 20 <= u.interaction_count <= 50])
            low_engagement = len([u for u in user_interactions if u.interaction_count < 20])

            return [
                UserSegment(
                    name="High Engagement",
                    percentage=(high_engagement / total_users * 100)
                ),
                UserSegment(
                    name="Medium Engagement",
                    percentage=(medium_engagement / total_users * 100)
                ),
                UserSegment(
                    name="Low Engagement",
                    percentage=(low_engagement / total_users * 100)
                )
            ]
        except Exception as e:
            logger.error(f"Error getting user segments: {str(e)}")
            return [
                UserSegment(name="High Engagement", percentage=0),
                UserSegment(name="Medium Engagement", percentage=0),
                UserSegment(name="Low Engagement", percentage=0)
            ]