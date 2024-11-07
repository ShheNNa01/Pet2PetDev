import axios from './config/axios';

export const analyticsService = {
    async getDashboardMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.get('/analytics/dashboard', {
                params
            });

            return {
                user_metrics: {
                    total_users: data?.user_metrics?.total_users || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    active_users: data?.user_metrics?.active_users || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    new_registrations: data?.user_metrics?.new_registrations || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    user_growth: data?.user_metrics?.user_growth || {
                        name: 'User Growth',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    },
                    retention_rate: data?.user_metrics?.retention_rate || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    churn_rate: data?.user_metrics?.churn_rate || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    }
                },
                content_metrics: {
                    total_posts: data?.content_metrics?.total_posts || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    engagement_rate: data?.content_metrics?.engagement_rate || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    popular_categories: data?.content_metrics?.popular_categories || [],
                    content_distribution: data?.content_metrics?.content_distribution || {},
                    posting_frequency: data?.content_metrics?.posting_frequency || {
                        name: 'Posting Frequency',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    },
                    media_usage: data?.content_metrics?.media_usage || {}
                },
                engagement_metrics: {
                    total_interactions: data?.engagement_metrics?.total_interactions || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    interaction_types: data?.engagement_metrics?.interaction_types || {},
                    engagement_by_time: data?.engagement_metrics?.engagement_by_time || {
                        name: 'Hourly Engagement',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    },
                    avg_session_duration: data?.engagement_metrics?.avg_session_duration || {
                        value: 0,
                        change_percentage: 0,
                        trend: 'stable'
                    },
                    peak_activity_hours: data?.engagement_metrics?.peak_activity_hours || [],
                    user_segments: data?.engagement_metrics?.user_segments || []
                },
                platform_metrics: {
                    system_health: data?.platform_metrics?.system_health || {},
                    response_times: data?.platform_metrics?.response_times || {
                        name: 'Response Times',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    },
                    error_rates: data?.platform_metrics?.error_rates || {
                        name: 'Error Rates',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    },
                    resource_usage: data?.platform_metrics?.resource_usage || {},
                    api_usage: data?.platform_metrics?.api_usage || {
                        name: 'API Usage',
                        data: [],
                        total: 0,
                        average: 0,
                        change_percentage: 0
                    }
                }
            };
        } catch (error) {
            console.error('Error en getDashboardMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas del dashboard');
        }
    },

    async getEngagementMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.get('/analytics/engagement', { params });
            return {
                total_interactions: data?.total_interactions || {
                    value: 0,
                    change_percentage: 0,
                    trend: 'stable'
                },
                interaction_types: data?.interaction_types || {},
                engagement_by_time: data?.engagement_by_time || {
                    name: 'Hourly Engagement',
                    data: [],
                    total: 0,
                    average: 0,
                    change_percentage: 0
                },
                avg_session_duration: data?.avg_session_duration || {
                    value: 0,
                    change_percentage: 0,
                    trend: 'stable'
                },
                peak_activity_hours: data?.peak_activity_hours || [],
                user_segments: data?.user_segments || []
            };
        } catch (error) {
            console.error('Error en getEngagementMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas de engagement');
        }
    },

    async getPeakHours(timeRange = 'week') {
        try {
            const { data } = await axios.get('/analytics/engagement/peak-hours', {
                params: { time_range: timeRange }
            });
            return data || [];
        } catch (error) {
            console.error('Error en getPeakHours:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener horas pico');
        }
    },

    async getUserSegments(timeRange = 'month') {
        try {
            const { data } = await axios.get('/analytics/engagement/user-segments', {
                params: { time_range: timeRange }
            });
            return data || [];
        } catch (error) {
            console.error('Error en getUserSegments:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener segmentos de usuarios');
        }
    },

    async exportMetrics({ metricsType, timeRange = 'month', format = 'csv', startDate = null, endDate = null }) {
        try {
            const params = {
                metrics_type: metricsType,
                time_range: timeRange,
                format,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.post('/analytics/export', null, { params });
            
            if (data.job_id) {
                // Iniciar polling del estado
                let attempts = 0;
                const maxAttempts = 30;
                const pollInterval = setInterval(async () => {
                    try {
                        const status = await this.getExportStatus(data.job_id);
                        if (status.status === 'completed') {
                            clearInterval(pollInterval);
                            window.location.href = status.download_url;
                        } else if (status.status === 'failed' || attempts >= maxAttempts) {
                            clearInterval(pollInterval);
                            throw new Error('Export failed or timed out');
                        }
                        attempts++;
                    } catch (error) {
                        clearInterval(pollInterval);
                        console.error('Error polling export status:', error);
                        throw error;
                    }
                }, 2000);
            }

            return data;
        } catch (error) {
            console.error('Error en exportMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al exportar métricas');
        }
    },

    async getExportStatus(jobId) {
        try {
            const { data } = await axios.get(`/analytics/export/status/${jobId}`);
            return data;
        } catch (error) {
            console.error('Error en getExportStatus:', error);
            throw new Error(error.response?.data?.message || 'Error al verificar estado de exportación');
        }
    }
};