from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    POST = "post"
    COMMENT = "comment"
    GROUP = "group"
    GROUP_POST = "group_post"
    USER = "user"
    PET = "pet"
    MESSAGE = "message"
    PROFILE = "profile"

class ReportReason(str, Enum):
    INAPPROPRIATE = "inappropriate"
    SPAM = "spam"
    HARASSMENT = "harassment"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    FAKE_ACCOUNT = "fake_account"
    IMPERSONATION = "impersonation"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    OTHER = "other"

class ModerationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"
    APPEALED = "appealed"
    AUTO_FLAGGED = "auto_flagged"
    AUTO_REJECTED = "auto_rejected"

class ModerationAction(str, Enum):
    WARNING = "warning"
    REMOVE_CONTENT = "remove_content"
    TEMPORARY_BAN = "temporary_ban"
    PERMANENT_BAN = "permanent_ban"
    NO_ACTION = "no_action"

class ReportCreate(BaseModel):
    content_type: ContentType
    content_id: int
    reason: ReportReason
    description: Optional[str] = Field(None, max_length=500)
    evidence_urls: Optional[List[str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content_type": "post",
                "content_id": 123,
                "reason": "inappropriate",
                "description": "Este post contiene contenido inapropiado",
                "evidence_urls": ["url/to/evidence1.jpg", "url/to/evidence2.jpg"]
            }
        }
    )

class ReportResponse(ReportCreate):
    report_id: int
    reporter_id: int
    created_at: datetime
    status: ModerationStatus
    moderated_by: Optional[int] = None
    moderated_at: Optional[datetime] = None
    action_taken: Optional[ModerationAction] = None
    notes: Optional[str] = None
    appeal_status: Optional[ModerationStatus] = None

    model_config = ConfigDict(from_attributes=True)

class ContentFilter(BaseModel):
    enabled: bool = True
    sensitivity_level: int = Field(1, ge=1, le=3, description="1: Low, 2: Medium, 3: High")
    filter_types: List[str] = Field(
        default=["profanity", "hate_speech", "adult_content"],
        description="Types of content to filter"
    )
    custom_keywords: Optional[List[str]] = None
    excluded_terms: Optional[List[str]] = None
    language: str = "es"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enabled": True,
                "sensitivity_level": 2,
                "filter_types": ["profanity", "hate_speech", "adult_content"],
                "custom_keywords": ["palabra1", "palabra2"],
                "excluded_terms": ["término_excluido"],
                "language": "es"
            }
        }
    )

class FilterResult(BaseModel):
    is_flagged: bool
    confidence_score: float
    matched_filters: List[str]
    filtered_content: Optional[str] = None
    recommendations: List[str]

class ModerationQueueItem(BaseModel):
    queue_id: int
    content_type: ContentType
    content_id: int
    content_preview: str
    reports_count: int
    latest_report_at: datetime
    status: ModerationStatus
    priority_score: float
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ModerationDecision(BaseModel):
    queue_item_id: int
    decision: ModerationStatus
    action: ModerationAction
    notes: Optional[str] = None
    ban_duration: Optional[int] = Field(
        None,
        description="Duration of ban in days, if applicable"
    )

class Appeal(BaseModel):
    report_id: int
    reason: str = Field(..., min_length=10, max_length=1000)
    evidence_urls: Optional[List[str]] = None
    contact_email: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "report_id": 123,
                "reason": "Este reporte es incorrecto porque...",
                "evidence_urls": ["url/to/evidence.jpg"],
                "contact_email": "user@example.com"
            }
        }
    )

class AppealResponse(Appeal):
    appeal_id: int
    created_at: datetime
    status: ModerationStatus
    resolved_at: Optional[datetime] = None
    resolver_id: Optional[int] = None
    resolution_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ModerationStats(BaseModel):
    total_reports: int
    pending_reports: int
    resolved_reports: int
    auto_moderated: int
    manual_moderated: int
    reports_by_reason: Dict[ReportReason, int]
    reports_by_content_type: Dict[ContentType, int]
    average_response_time: float  # en horas
    moderation_accuracy: float  # porcentaje
    top_reporters: List[Dict[str, Any]]
    recent_actions: List[Dict[str, Any]]

class ModeratorActivity(BaseModel):
    moderator_id: int
    total_reviewed: int
    accuracy_rate: float
    average_response_time: float
    actions_taken: Dict[ModerationAction, int]
    active_assignments: int
    last_active: datetime

class AutoModSettings(BaseModel):
    enabled: bool = True
    confidence_threshold: float = Field(0.8, ge=0.0, le=1.0)
    auto_reject_threshold: float = Field(0.95, ge=0.0, le=1.0)
    min_reports_for_auto_review: int = Field(3, ge=1)
    allowed_actions: List[ModerationAction]
    notification_settings: Dict[str, bool]
    exclusion_rules: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enabled": True,
                "confidence_threshold": 0.8,
                "auto_reject_threshold": 0.95,
                "min_reports_for_auto_review": 3,
                "allowed_actions": ["warning", "remove_content"],
                "notification_settings": {
                    "notify_on_auto_reject": True,
                    "notify_on_multiple_reports": True
                }
            }
        }
    )