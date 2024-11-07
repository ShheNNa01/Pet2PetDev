# services/analytics/app/services/platform_analytics.py
from datetime import datetime, timedelta
from sqlalchemy import func, and_, text
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from services.analytics.app.models.schemas import (
    MetricValue,
    PlatformMetrics,
    TimeRange,
    TimeSeriesMetric,
    TimeSeriesPoint,
)
from services.analytics.app.services.metrics_aggregator import MetricsAggregator
from shared.database.models import User, Post, Comment, Reaction, Pet, Group, MediaFile

import psutil
import logging
import json

logger = logging.getLogger(__name__)


class PlatformAnalyticsService:
    def __init__(self):
        self.metrics = MetricsAggregator()
        self._error_cache = {}
        self._performance_cache = {}
        self.cache_enabled = False
        
        # Intentar verificar si Redis está disponible
        try:
            import redis
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            redis_client.ping()
            self.cache_enabled = True
        except:
            logger.warning("Redis cache unavailable, running without cache")

    async def get_platform_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        custom_start: datetime = None,
        custom_end: datetime = None,
    ) -> PlatformMetrics:
        start_date, end_date = await self.metrics.get_time_range_dates(
            time_range, custom_start, custom_end
        )

        # Obtener métricas de salud del sistema
        system_health = await self.get_system_health_metrics()

        # Obtener tiempos de respuesta
        response_times = await self.get_response_time_metrics(
            db, time_range, start_date, end_date
        )

        # Obtener tasas de error
        error_rates = await self.get_error_rate_metrics(
            time_range, start_date, end_date
        )

        # Obtener uso de recursos
        resource_usage = await self.get_resource_usage_metrics()

        # Obtener uso de API
        api_usage = await self.get_api_usage_metrics(
            db, time_range, start_date, end_date
        )

        return PlatformMetrics(
            system_health=system_health,
            response_times=response_times,
            error_rates=error_rates,
            resource_usage=resource_usage,
            api_usage=api_usage,
        )

    async def get_system_health_metrics(self) -> Dict[str, MetricValue]:
        """Obtiene métricas de salud del sistema"""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory Usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk Usage
            disk = psutil.disk_usage("/")
            disk_percent = disk.percent

            # Database Connections
            db_connections = await self.get_db_connection_count()

            return {
                "cpu_usage": MetricValue(
                    value=cpu_percent,
                    change_percentage=0.0,  # Calcular cambio si se tiene histórico
                    trend="up" if cpu_percent > 75 else "stable",
                ),
                "memory_usage": MetricValue(
                    value=memory_percent,
                    change_percentage=0.0,
                    trend="up" if memory_percent > 80 else "stable",
                ),
                "disk_usage": MetricValue(
                    value=disk_percent,
                    change_percentage=0.0,
                    trend="up" if disk_percent > 85 else "stable",
                ),
                "db_connections": MetricValue(
                    value=db_connections, change_percentage=0.0, trend="stable"
                ),
            }
        except Exception as e:
            logger.error(f"Error getting system health metrics: {str(e)}")
            return {}

    async def get_response_time_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> TimeSeriesMetric:
        """Obtiene métricas de tiempo de respuesta"""
        try:
            # En una implementación real, estos datos vendrían de logs o un servicio de monitoreo
            # Aquí simulamos algunos datos de ejemplo
            response_times = [
                {
                    "timestamp": start_date + timedelta(hours=i),
                    "value": 150
                    + (i % 5) * 10,  # Simula tiempos de respuesta entre 150-200ms
                }
                for i in range(int((end_date - start_date).total_seconds() / 3600))
            ]

            data_points = [
                TimeSeriesPoint(timestamp=point["timestamp"], value=point["value"])
                for point in response_times
            ]

            average = sum(point["value"] for point in response_times) / len(
                response_times
            )

            return TimeSeriesMetric(
                name="Average Response Time",
                data=data_points,
                total=sum(point["value"] for point in response_times),
                average=average,
                change_percentage=0.0,  # Calcular cambio si se tiene histórico
            )
        except Exception as e:
            logger.error(f"Error getting response time metrics: {str(e)}")
            return TimeSeriesMetric(
                name="Average Response Time",
                data=[],
                total=0,
                average=0,
                change_percentage=0,
            )

    async def get_error_rate_metrics(
        self, time_range: TimeRange, start_date: datetime, end_date: datetime
    ) -> TimeSeriesMetric:
        """Obtiene métricas de tasa de errores"""
        try:
            # En una implementación real, estos datos vendrían de logs o un servicio de monitoreo
            error_rates = [
                {
                    "timestamp": start_date + timedelta(hours=i),
                    "value": (i % 3) * 0.5,  # Simula tasas de error entre 0-1%
                }
                for i in range(int((end_date - start_date).total_seconds() / 3600))
            ]

            data_points = [
                TimeSeriesPoint(timestamp=point["timestamp"], value=point["value"])
                for point in error_rates
            ]

            average = sum(point["value"] for point in error_rates) / len(error_rates)

            return TimeSeriesMetric(
                name="Error Rate",
                data=data_points,
                total=sum(point["value"] for point in error_rates),
                average=average,
                change_percentage=0.0,
            )
        except Exception as e:
            logger.error(f"Error getting error rate metrics: {str(e)}")
            return TimeSeriesMetric(
                name="Error Rate", data=[], total=0, average=0, change_percentage=0
            )

    async def get_resource_usage_metrics(self) -> Dict[str, MetricValue]:
        """Obtiene métricas de uso de recursos"""
        try:
            # Memory Details
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # Disk I/O
            disk_io = psutil.disk_io_counters()

            # Network I/O
            net_io = psutil.net_io_counters()

            return {
                "ram_available": MetricValue(
                    value=memory.available / (1024 * 1024 * 1024),  # GB
                    change_percentage=0.0,
                    trend="stable",
                ),
                "swap_usage": MetricValue(
                    value=swap.percent,
                    change_percentage=0.0,
                    trend="up" if swap.percent > 50 else "stable",
                ),
                "disk_read_rate": MetricValue(
                    value=disk_io.read_bytes / (1024 * 1024),  # MB
                    change_percentage=0.0,
                    trend="stable",
                ),
                "disk_write_rate": MetricValue(
                    value=disk_io.write_bytes / (1024 * 1024),  # MB
                    change_percentage=0.0,
                    trend="stable",
                ),
                "network_in_rate": MetricValue(
                    value=net_io.bytes_recv / (1024 * 1024),  # MB
                    change_percentage=0.0,
                    trend="stable",
                ),
                "network_out_rate": MetricValue(
                    value=net_io.bytes_sent / (1024 * 1024),  # MB
                    change_percentage=0.0,
                    trend="stable",
                ),
            }
        except Exception as e:
            logger.error(f"Error getting resource usage metrics: {str(e)}")
            return {}

    async def get_api_usage_metrics(
        self,
        db: Session,
        time_range: TimeRange,
        start_date: datetime,
        end_date: datetime,
    ) -> TimeSeriesMetric:
        """Obtiene métricas de uso de la API"""
        try:
            # Aquí deberías implementar la lógica para obtener el uso real de la API
            # Este es un ejemplo simulado
            api_calls = [
                {
                    "timestamp": start_date + timedelta(hours=i),
                    "value": 1000
                    + (i % 12) * 100,  # Simula entre 1000-2200 llamadas por hora
                }
                for i in range(int((end_date - start_date).total_seconds() / 3600))
            ]

            data_points = [
                TimeSeriesPoint(timestamp=point["timestamp"], value=point["value"])
                for point in api_calls
            ]

            average = sum(point["value"] for point in api_calls) / len(api_calls)

            return TimeSeriesMetric(
                name="API Calls",
                data=data_points,
                total=sum(point["value"] for point in api_calls),
                average=average,
                change_percentage=0.0,
            )
        except Exception as e:
            logger.error(f"Error getting API usage metrics: {str(e)}")
            return TimeSeriesMetric(
                name="API Calls", data=[], total=0, average=0, change_percentage=0
            )

    async def get_db_connection_count(self) -> int:
        """Obtiene el número de conexiones activas a la base de datos"""
        try:
            # En una implementación real, esto vendría de la base de datos
            # Por ejemplo, para PostgreSQL:
            # SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
            return 10  # Valor de ejemplo
        except Exception as e:
            logger.error(f"Error getting DB connection count: {str(e)}")
            return 0

    async def log_error(self, error_type: str, error_details: Dict):
        """Registra un error para las métricas"""
        timestamp = datetime.utcnow()
        if error_type not in self._error_cache:
            self._error_cache[error_type] = []

        self._error_cache[error_type].append(
            {"timestamp": timestamp, "details": error_details}
        )

        # Limpiar errores antiguos (más de 24 horas)
        cutoff = timestamp - timedelta(hours=24)
        self._error_cache[error_type] = [
            error
            for error in self._error_cache[error_type]
            if error["timestamp"] > cutoff
        ]

    async def log_performance_metric(self, metric_name: str, value: float):
        """Registra una métrica de rendimiento"""
        timestamp = datetime.utcnow()
        if metric_name not in self._performance_cache:
            self._performance_cache[metric_name] = []

        self._performance_cache[metric_name].append(
            {"timestamp": timestamp, "value": value}
        )

        # Limpiar métricas antiguas (más de 24 horas)
        cutoff = timestamp - timedelta(hours=24)
        self._performance_cache[metric_name] = [
            metric
            for metric in self._performance_cache[metric_name]
            if metric["timestamp"] > cutoff
        ]
