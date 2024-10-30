# services/analytics/app/models/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, date
from enum import Enum


class TimeRange(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    CUSTOM = "custom"


class MetricType(str, Enum):
    COUNT = "count"
    AVERAGE = "average"
    SUM = "sum"
    PERCENTAGE = "percentage"


class DateRange(BaseModel):
    start_date: date
    end_date: date


class AnalyticsFilter(BaseModel):
    time_range: TimeRange
    custom_range: Optional[DateRange] = None
    granularity: str = "day"  # day, week, month
    categories: Optional[List[str]] = None
    user_segments: Optional[List[str]] = None


class MetricValue(BaseModel):
    value: float
    change_percentage: Optional[float] = None
    trend: Optional[str] = None  # up, down, stable


class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    value: float


class TimeSeriesMetric(BaseModel):
    name: str
    data: List[TimeSeriesPoint]
    total: float
    average: float
    change_percentage: float


class UserActivityMetrics(BaseModel):
    total_users: MetricValue
    active_users: MetricValue
    new_registrations: MetricValue
    user_growth: TimeSeriesMetric
    retention_rate: MetricValue
    churn_rate: MetricValue


class ContentMetrics(BaseModel):
    total_posts: MetricValue
    engagement_rate: MetricValue
    popular_categories: List[Dict[str, float]]
    content_distribution: Dict[str, float]
    posting_frequency: TimeSeriesMetric
    media_usage: Dict[str, float]


class EngagementMetrics(BaseModel):
    total_interactions: MetricValue
    interaction_types: Dict[str, float]
    engagement_by_time: TimeSeriesMetric
    avg_session_duration: MetricValue
    peak_activity_hours: List[Dict[str, float]]
    user_segments: List[Dict[str, float]]


class PlatformMetrics(BaseModel):
    system_health: Dict[str, MetricValue]
    response_times: TimeSeriesMetric
    error_rates: TimeSeriesMetric
    resource_usage: Dict[str, MetricValue]
    api_usage: TimeSeriesMetric


class DashboardMetrics(BaseModel):
    user_metrics: UserActivityMetrics
    content_metrics: ContentMetrics
    engagement_metrics: EngagementMetrics
    platform_metrics: PlatformMetrics
