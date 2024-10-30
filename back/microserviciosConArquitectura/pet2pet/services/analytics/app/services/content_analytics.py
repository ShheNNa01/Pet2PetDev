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
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import Comment, GroupPost, MediaFile, Post, Reaction


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
                    GroupPost.created_at >= start_date, GroupPost.created_at <= end_date
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
                    Reaction.created_at >= prev_start, Reaction.created_at <= start_date
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
        posting_frequency = await self.metrics.get_time_series_data(
            db, Post.created_at, time_range, start_date, end_date, "hour"
        )

        # Distribución de contenido por tipo de media
        media_distribution = await self.get_media_distribution(
            db, time_range, start_date, end_date
        )

        # Categorías populares (basadas en hashtags o contenido)
        popular_categories = await self.get_popular_categories(
            db, time_range, start_date, end_date
        )

        return ContentMetrics(
            total_posts=await self.metrics.get_metric_value(
                total_current_posts, total_previous_posts
            ),
            engagement_rate=await self.metrics.get_metric_value(
                current_engagement, previous_engagement, MetricType.PERCENTAGE
            ),
            popular_categories=popular_categories,
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
            media_usage=media_distribution,
        )

    async def get_media_distribution(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        results = (
            db.query(MediaFile.media_type, func.count().label("count"))
            .filter(
                and_(
                    MediaFile.created_at >= start_date, MediaFile.created_at <= end_date
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

    async def get_popular_categories(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Dict[str, float]]:
        # Aquí podrías implementar lógica para extraer categorías de hashtags,
        # análisis de texto del contenido, o usar categorías predefinidas
        # Este es un ejemplo simplificado
        return [
            {"category": "pets", "percentage": 45.0},
            {"category": "lifestyle", "percentage": 25.0},
            {"category": "health", "percentage": 15.0},
            {"category": "events", "percentage": 10.0},
            {"category": "other", "percentage": 5.0},
        ]

    async def get_content_type_distribution(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
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
                    GroupPost.created_at >= start_date, GroupPost.created_at <= end_date
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

        total = regular_posts + group_posts

        return {
            "regular_posts": (regular_posts / total * 100) if total > 0 else 0,
            "group_posts": (group_posts / total * 100) if total > 0 else 0,
            "media_posts": (media_posts / total * 100) if total > 0 else 0,
        }
