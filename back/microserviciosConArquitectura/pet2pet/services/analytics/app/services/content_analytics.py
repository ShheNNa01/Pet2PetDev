# services/analytics/app/services/content_analytics.py
from datetime import datetime
from typing import Dict, List
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session

from services.analytics.app.models.schemas import (
    ContentMetrics,
    MetricType,
    TimeRange,
    TimeSeriesMetric,
    PopularCategory,
    TimeSeriesPoint
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import Comment, GroupPost, MediaFile, Post, Reaction
import logging

logger = logging.getLogger(__name__)


class ContentAnalyticsService:
    def __init__(self):
        self.metrics = MetricsAggregator()

    async def get_content_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        custom_start: datetime = None,
        custom_end: datetime = None,
    ) -> ContentMetrics:
        try:
            start_date, end_date = await self.metrics.get_time_range_dates(
                time_range, custom_start, custom_end
            )
            prev_start = start_date - (end_date - start_date)

            # Total posts (incluye posts regulares y de grupos)
            current_posts = (
                db.query(Post)
                .filter(and_(Post.created_at >= start_date, Post.created_at <= end_date))
                .count()
            )

            current_group_posts = (
                db.query(GroupPost)
                .filter(
                    and_(
                        GroupPost.created_at >= start_date, 
                        GroupPost.created_at <= end_date
                    )
                )
                .count()
            )

            total_current_posts = current_posts + current_group_posts

            # Posts del período anterior
            previous_posts = (
                db.query(Post)
                .filter(and_(Post.created_at >= prev_start, Post.created_at <= start_date))
                .count()
            )

            previous_group_posts = (
                db.query(GroupPost)
                .filter(
                    and_(
                        GroupPost.created_at >= prev_start,
                        GroupPost.created_at <= start_date,
                    )
                )
                .count()
            )

            total_previous_posts = previous_posts + previous_group_posts

            # Tasa de engagement (reacciones + comentarios) / posts
            current_reactions = (
                db.query(Reaction)
                .filter(
                    and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
                )
                .count()
            )

            current_comments = (
                db.query(Comment)
                .filter(
                    and_(Comment.created_at >= start_date, Comment.created_at <= end_date)
                )
                .count()
            )

            current_engagement = (
                (current_reactions + current_comments) / total_current_posts
                if total_current_posts > 0
                else 0
            )

            previous_reactions = (
                db.query(Reaction)
                .filter(
                    and_(
                        Reaction.created_at >= prev_start, 
                        Reaction.created_at <= start_date
                    )
                )
                .count()
            )

            previous_comments = (
                db.query(Comment)
                .filter(
                    and_(Comment.created_at >= prev_start, Comment.created_at <= start_date)
                )
                .count()
            )

            previous_engagement = (
                (previous_reactions + previous_comments) / total_previous_posts
                if total_previous_posts > 0
                else 0
            )

            # Frecuencia de publicación por tiempo
            posting_frequency_data = await self.metrics.get_time_series_data(
                db=db,
                date_column=Post.created_at,
                time_range=time_range,
                start_date=start_date,
                end_date=end_date,
                granularity="hour"
            )

            # Añadir datos de posts de grupos
            group_posting_data = await self.metrics.get_time_series_data(
                db=db,
                date_column=GroupPost.created_at,
                time_range=time_range,
                start_date=start_date,
                end_date=end_date,
                granularity="hour"
            )

            # Combinar datos de posts regulares y de grupos
            posting_frequency = []
            timestamps = set(p.timestamp for p in posting_frequency_data + group_posting_data)
            
            for timestamp in sorted(timestamps):
                regular_value = next(
                    (p.value for p in posting_frequency_data if p.timestamp == timestamp),
                    0
                )
                group_value = next(
                    (p.value for p in group_posting_data if p.timestamp == timestamp),
                    0
                )
                posting_frequency.append(
                    TimeSeriesPoint(
                        timestamp=timestamp,
                        value=regular_value + group_value
                    )
                )

            return ContentMetrics(
                total_posts=await self.metrics.get_metric_value(
                    total_current_posts, total_previous_posts
                ),
                engagement_rate=await self.metrics.get_metric_value(
                    current_engagement, previous_engagement, MetricType.PERCENTAGE
                ),
                popular_categories=await self.get_popular_categories(
                    db, time_range, start_date, end_date
                ),
                content_distribution=await self.get_content_type_distribution(
                    db, time_range, start_date, end_date
                ),
                posting_frequency=TimeSeriesMetric(
                    name="Posting Frequency",
                    data=posting_frequency,
                    total=sum(point.value for point in posting_frequency),
                    average=(
                        sum(point.value for point in posting_frequency)
                        / len(posting_frequency)
                        if posting_frequency
                        else 0
                    ),
                    change_percentage=await self.metrics.calculate_growth(
                        total_current_posts, total_previous_posts
                    ),
                ),
                media_usage=await self.get_media_distribution(
                    db, time_range, start_date, end_date
                ),
            )
        except Exception as e:
            logger.error(f"Error getting content metrics: {str(e)}", exc_info=True)
            raise


    async def get_media_distribution(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        try:
            results = (
                db.query(MediaFile.media_type, func.count().label("count"))
                .filter(
                    and_(
                        MediaFile.created_at >= start_date, 
                        MediaFile.created_at <= end_date
                    )
                )
                .group_by(MediaFile.media_type)
                .all()
            )

            total = sum(r.count for r in results)
            return {
                media_type: (count / total * 100) if total > 0 else 0
                for media_type, count in results
            }
        except Exception as e:
            logger.error(f"Error getting media distribution: {str(e)}", exc_info=True)
            return {}

    async def get_popular_categories(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> List[PopularCategory]:
        try:
            # En una implementación real, esto vendría de los posts o hashtags
            # Por ahora, retornamos datos de ejemplo
            return [
                PopularCategory(name="pets", percentage=45.0),
                PopularCategory(name="lifestyle", percentage=25.0),
                PopularCategory(name="health", percentage=15.0),
                PopularCategory(name="events", percentage=10.0),
                PopularCategory(name="other", percentage=5.0)
            ]
        except Exception as e:
            logger.error(f"Error getting popular categories: {str(e)}", exc_info=True)
            return []

    async def get_content_type_distribution(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        try:
            # Query para contar diferentes tipos de contenido
            regular_posts = (
                db.query(Post)
                .filter(and_(Post.created_at >= start_date, Post.created_at <= end_date))
                .count()
            )

            group_posts = (
                db.query(GroupPost)
                .filter(
                    and_(
                        GroupPost.created_at >= start_date, 
                        GroupPost.created_at <= end_date
                    )
                )
                .count()
            )

            media_posts = (
                db.query(Post)
                .join(MediaFile)
                .filter(and_(Post.created_at >= start_date, Post.created_at <= end_date))
                .distinct()
                .count()
            )

            total = regular_posts + group_posts if (regular_posts + group_posts) > 0 else 1

            return {
                "regular_posts": (regular_posts / total * 100),
                "group_posts": (group_posts / total * 100),
                "media_posts": (media_posts / total * 100)
            }
        except Exception as e:
            logger.error(f"Error getting content type distribution: {str(e)}", exc_info=True)
            return {
                "regular_posts": 0,
                "group_posts": 0,
                "media_posts": 0
            }

    async def get_content_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        custom_start: datetime = None,
        custom_end: datetime = None,
    ) -> ContentMetrics:
        try:
            start_date, end_date = await self.metrics.get_time_range_dates(
                time_range, custom_start, custom_end
            )
            prev_start = start_date - (end_date - start_date)

            # Total posts (incluye posts regulares y de grupos)
            current_posts = (
                db.query(Post)
                .filter(and_(Post.created_at >= start_date, Post.created_at <= end_date))
                .count()
            )

            current_group_posts = (
                db.query(GroupPost)
                .filter(
                    and_(
                        GroupPost.created_at >= start_date, 
                        GroupPost.created_at <= end_date
                    )
                )
                .count()
            )

            total_current_posts = current_posts + current_group_posts

            # Posts del período anterior
            previous_posts = (
                db.query(Post)
                .filter(and_(Post.created_at >= prev_start, Post.created_at <= start_date))
                .count()
            )

            previous_group_posts = (
                db.query(GroupPost)
                .filter(
                    and_(
                        GroupPost.created_at >= prev_start,
                        GroupPost.created_at <= start_date,
                    )
                )
                .count()
            )

            total_previous_posts = previous_posts + previous_group_posts

            # Métricas de engagement
            engagement_metrics = await self.calculate_engagement_metrics(
                db, start_date, end_date, prev_start, 
                total_current_posts, total_previous_posts
            )

            # Frecuencia de publicación
            posting_metrics = await self.calculate_posting_frequency(
                db, time_range, start_date, end_date, 
                total_current_posts, total_previous_posts
            )

            return ContentMetrics(
                total_posts=await self.metrics.get_metric_value(
                    total_current_posts, total_previous_posts
                ),
                engagement_rate=engagement_metrics["engagement_rate"],
                popular_categories=await self.get_popular_categories(
                    db, time_range, start_date, end_date
                ),
                content_distribution=await self.get_content_type_distribution(
                    db, time_range, start_date, end_date
                ),
                posting_frequency=posting_metrics,
                media_usage=await self.get_media_distribution(
                    db, time_range, start_date, end_date
                ),
            )
        except Exception as e:
            logger.error(f"Error getting content metrics: {str(e)}", exc_info=True)
            raise

    async def calculate_engagement_metrics(
        self, db: Session, 
        start_date: datetime, 
        end_date: datetime, 
        prev_start: datetime,
        total_current_posts: int,
        total_previous_posts: int
    ) -> Dict:
        # Calcular interacciones actuales
        current_reactions = (
            db.query(Reaction)
            .filter(
                and_(Reaction.created_at >= start_date, Reaction.created_at <= end_date)
            )
            .count()
        )

        current_comments = (
            db.query(Comment)
            .filter(
                and_(Comment.created_at >= start_date, Comment.created_at <= end_date)
            )
            .count()
        )

        current_engagement = (
            (current_reactions + current_comments) / total_current_posts
            if total_current_posts > 0
            else 0
        )

        # Calcular interacciones previas
        previous_reactions = (
            db.query(Reaction)
            .filter(
                and_(
                    Reaction.created_at >= prev_start, 
                    Reaction.created_at <= start_date
                )
            )
            .count()
        )

        previous_comments = (
            db.query(Comment)
            .filter(
                and_(Comment.created_at >= prev_start, Comment.created_at <= start_date)
            )
            .count()
        )

        previous_engagement = (
            (previous_reactions + previous_comments) / total_previous_posts
            if total_previous_posts > 0
            else 0
        )

        return {
            "engagement_rate": await self.metrics.get_metric_value(
                current_engagement, previous_engagement, MetricType.PERCENTAGE
            ),
            "current_engagement": current_engagement,
            "previous_engagement": previous_engagement
        }

    async def calculate_posting_frequency(
        self, 
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
        total_current_posts: int,
        total_previous_posts: int
    ) -> TimeSeriesMetric:
        # Obtener datos de frecuencia de posts regulares
        posts_frequency = await self.metrics.get_time_series_data(
            db=db,
            date_column=Post.created_at,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            granularity="hour"
        )

        # Obtener datos de posts de grupos
        group_posts_frequency = await self.metrics.get_time_series_data(
            db=db,
            date_column=GroupPost.created_at,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            granularity="hour"
        )

        # Combinar los datos de frecuencia
        combined_frequency = []
        all_timestamps = sorted(set(
            p.timestamp for p in posts_frequency + group_posts_frequency
        ))

        for timestamp in all_timestamps:
            regular_value = next(
                (p.value for p in posts_frequency if p.timestamp == timestamp),
                0
            )
            group_value = next(
                (p.value for p in group_posts_frequency if p.timestamp == timestamp),
                0
            )
            combined_frequency.append(
                TimeSeriesPoint(
                    timestamp=timestamp,
                    value=regular_value + group_value
                )
            )

        return TimeSeriesMetric(
            name="Posting Frequency",
            data=combined_frequency,
            total=sum(point.value for point in combined_frequency),
            average=(
                sum(point.value for point in combined_frequency)
                / len(combined_frequency)
                if combined_frequency
                else 0
            ),
            change_percentage=await self.metrics.calculate_growth(
                total_current_posts, total_previous_posts
            ),
        )