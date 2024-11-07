# services/analytics/app/models/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, Union
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
    model_config = ConfigDict(from_attributes=True)
    start_date: date
    end_date: date

class MetricValue(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    value: float
    change_percentage: Optional[float] = None
    trend: Optional[str] = None  # up, down, stable

class TimeSeriesPoint(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    timestamp: datetime
    value: float

class TimeSeriesMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    data: List[TimeSeriesPoint]
    total: float
    average: float
    change_percentage: float

class UserSegment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    percentage: float

class PeakHour(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hour: str
    percentage: float

class PopularCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    percentage: float

class UserActivityMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_users: MetricValue
    active_users: MetricValue
    new_registrations: MetricValue
    user_growth: TimeSeriesMetric
    retention_rate: MetricValue
    churn_rate: MetricValue

class ContentMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_posts: MetricValue
    engagement_rate: MetricValue
    popular_categories: List[PopularCategory]
    content_distribution: Dict[str, float]
    posting_frequency: TimeSeriesMetric
    media_usage: Dict[str, float]

class EngagementMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_interactions: MetricValue
    interaction_types: Dict[str, float]
    engagement_by_time: TimeSeriesMetric
    avg_session_duration: MetricValue
    peak_activity_hours: List[PeakHour]
    user_segments: List[UserSegment]

class PlatformMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    system_health: Dict[str, MetricValue]
    response_times: TimeSeriesMetric
    error_rates: TimeSeriesMetric
    resource_usage: Dict[str, MetricValue]
    api_usage: TimeSeriesMetric

class DashboardMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_metrics: UserActivityMetrics
    content_metrics: ContentMetrics
    engagement_metrics: EngagementMetrics
    platform_metrics: PlatformMetrics

class AnalyticsFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    time_range: TimeRange
    custom_range: Optional[DateRange] = None
    granularity: str = "day"
    categories: Optional[List[str]] = None
    user_segments: Optional[List[str]] = None