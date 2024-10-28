# services/moderation/app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    POST = "post"
    COMMENT = "comment"
    GROUP_POST = "group_post"
    GROUP_COMMENT = "group_comment"
    PROFILE = "profile"
    MESSAGE = "message"

class ReportReason(str, Enum):
    INAPPROPRIATE = "inappropriate_content"
    SPAM = "spam"
    HARASSMENT = "harassment"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    FAKE_ACCOUNT = "fake_account"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ANIMAL_ABUSE = "animal_abuse"
    OTHER = "other"

class ContentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"
    FLAGGED = "flagged"

class ReportCreate(BaseModel):
    reported_content_id: int
    content_type: ContentType
    reason: ReportReason
    description: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

class ReportUpdate(BaseModel):
    status: ContentStatus
    moderation_notes: Optional[str] = None
    action_taken: Optional[str] = None

class ReportResponse(BaseModel):
    report_id: int
    reported_by_user_id: int
    reported_content_id: int
    content_type: ContentType
    reason: ReportReason
    description: Optional[str]
    evidence: Optional[Dict[str, Any]]
    status: ContentStatus
    created_at: datetime
    updated_at: Optional[datetime]
    moderation_notes: Optional[str]
    action_taken: Optional[str]

    class Config:
        from_attributes = True

class AutoModResult(BaseModel):
    is_approved: bool
    confidence_score: float
    flags: List[str]
    detected_issues: Dict[str, float]
    recommendation: ContentStatus

class ContentFilter(BaseModel):
    profanity_check: bool = True
    spam_check: bool = True
    toxic_content_check: bool = True
    image_moderation: bool = True
    sensitivity_level: int = Field(ge=1, le=5, default=3)

class ContentReview(BaseModel):
    content_id: int
    content_type: ContentType
    content_data: Dict[str, Any]
    filter_settings: Optional[ContentFilter] = None

class ModerationAction(BaseModel):
    content_id: int
    content_type: ContentType
    action: str
    reason: str
    duration: Optional[int] = None  # Duración en días para acciones temporales
    moderated_by: int
    notes: Optional[str] = None

class ModerationStats(BaseModel):
    total_reports: int
    pending_reports: int
    resolved_reports: int
    automated_actions: int
    manual_actions: int
    average_response_time: float  # en horas
    common_reasons: Dict[str, int]
    daily_stats: Dict[str, int]

class UserModerationProfile(BaseModel):
    user_id: int
    total_reports_received: int
    total_reports_made: int
    warning_count: int
    temporary_ban_count: int
    last_warning_date: Optional[datetime]
    last_ban_date: Optional[datetime]
    current_status: str
    trust_score: float
    moderation_history: List[Dict[str, Any]]

class ContentType(str, Enum):
    POST = "post"
    COMMENT = "comment"
    GROUP_POST = "group_post"
    GROUP_COMMENT = "group_comment"
    PROFILE = "profile"
    MESSAGE = "message"

class ModerationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"
    UNDER_REVIEW = "under_review"

class ContentFilter(BaseModel):
    filter_types: List[str] = ["profanity", "hate_speech", "adult_content"]
    sensitivity_level: int = Field(ge=1, le=5, default=3)
    language: str = "es"
    custom_keywords: Optional[List[str]] = None
    excluded_terms: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "filter_types": ["profanity", "hate_speech", "adult_content"],
                "sensitivity_level": 3,
                "language": "es",
                "custom_keywords": ["palabra1", "palabra2"],
                "excluded_terms": ["término1", "término2"]
            }
        }

class FilterResult(BaseModel):
    is_flagged: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    matched_filters: List[str]
    filtered_content: Optional[str]
    recommendations: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "is_flagged": True,
                "confidence_score": 0.85,
                "matched_filters": ["profanity", "hate_speech"],
                "filtered_content": "Texto filtrado con ***",
                "recommendations": [
                    "El contenido contiene lenguaje inapropiado que debe ser revisado",
                    "Se detectó posible discurso de odio que requiere revisión"
                ]
            }
        }

class FilterConfiguration(BaseModel):
    config_id: Optional[int]
    name: str
    description: Optional[str]
    filter_types: List[str]
    sensitivity_level: int = Field(ge=1, le=5)
    language: str
    custom_keywords: Optional[List[str]]
    excluded_terms: Optional[List[str]]
    created_by: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Configuración Estricta",
                "description": "Configuración con alta sensibilidad para contenido familiar",
                "filter_types": ["profanity", "hate_speech", "adult_content"],
                "sensitivity_level": 5,
                "language": "es",
                "custom_keywords": ["palabra1", "palabra2"],
                "excluded_terms": ["término1", "término2"]
            }
        }

class CustomFilterRule(BaseModel):
    rule_id: Optional[int]
    name: str
    description: Optional[str]
    keywords: List[str]
    excluded_terms: Optional[List[str]]
    sensitivity_level: int = Field(ge=1, le=5)
    is_active: bool = True
    created_by: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Regla Personalizada 1",
                "description": "Regla para detectar contenido específico",
                "keywords": ["palabra1", "palabra2"],
                "excluded_terms": ["término1", "término2"],
                "sensitivity_level": 3,
                "is_active": True
            }
        }

class ContentReview(BaseModel):
    content: str
    content_type: ContentType
    filter_settings: ContentFilter = ContentFilter()
    metadata: Optional[Dict[str, Any]]

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Texto a revisar",
                "content_type": "post",
                "filter_settings": {
                    "filter_types": ["profanity", "hate_speech"],
                    "sensitivity_level": 3,
                    "language": "es",
                    "custom_keywords": ["palabra1", "palabra2"],
                    "excluded_terms": ["término1", "término2"]
                },
                "metadata": {
                    "user_id": 123,
                    "post_id": 456
                }
            }
        }