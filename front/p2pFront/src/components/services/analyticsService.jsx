import axios from './config/axios';

export const analyticsService = {
    async getDashboardMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const response = await axios.get('/analytics/dashboard', {
                headers: {
                    'Accept': 'application/json'
                },
                params
            });

            return {
                user_metrics: {
                    total_users: {
                        value: response.data?.user_metrics?.total_users?.value || 0,
                        change_percentage: response.data?.user_metrics?.total_users?.change_percentage || 0,
                        trend: response.data?.user_metrics?.total_users?.trend || 'stable'
                    },
                    active_users: {
                        value: response.data?.user_metrics?.active_users?.value || 0,
                        change_percentage: response.data?.user_metrics?.active_users?.change_percentage || 0,
                        trend: response.data?.user_metrics?.active_users?.trend || 'stable'
                    },
                    new_registrations: {
                        value: response.data?.user_metrics?.new_registrations?.value || 0,
                        change_percentage: response.data?.user_metrics?.new_registrations?.change_percentage || 0,
                        trend: response.data?.user_metrics?.new_registrations?.trend || 'stable'
                    },
                    user_growth: {
                        name: 'user_growth',
                        data: response.data?.user_metrics?.user_growth?.data || [],
                        total: response.data?.user_metrics?.user_growth?.total || 0,
                        average: response.data?.user_metrics?.user_growth?.average || 0,
                        change_percentage: response.data?.user_metrics?.user_growth?.change_percentage || 0
                    }
                }
            };
        } catch (error) {
            console.error('Error en getDashboardMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas del dashboard');
        }
    },

    async getUserMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.get('/analytics/users', { params });
            return {
                total_users: {
                    value: data?.total_users?.value || 0,
                    change_percentage: data?.total_users?.change_percentage || 0,
                    trend: data?.total_users?.trend || 'stable'
                },
                active_users: {
                    value: data?.active_users?.value || 0,
                    change_percentage: data?.active_users?.change_percentage || 0,
                    trend: data?.active_users?.trend || 'stable'
                },
                new_registrations: {
                    value: data?.new_registrations?.value || 0,
                    change_percentage: data?.new_registrations?.change_percentage || 0,
                    trend: data?.new_registrations?.trend || 'stable'
                },
                retention_rate: {
                    value: data?.retention_rate?.value || 0,
                    change_percentage: data?.retention_rate?.change_percentage || 0,
                    trend: data?.retention_rate?.trend || 'stable'
                }
            };
        } catch (error) {
            console.error('Error en getUserMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas de usuarios');
        }
    },

    async getUserGrowth(timeRange = 'month', granularity = 'day') {
        try {
            const params = {
                time_range: timeRange,
                granularity
            };

            const { data } = await axios.get('/analytics/users/growth', { params });
            return data;
        } catch (error) {
            console.error('Error en getUserGrowth:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener crecimiento de usuarios');
        }
    },

    async getContentMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.get('/analytics/content', { params });
            return {
                total_posts: {
                    value: data?.total_posts?.value || 0,
                    change_percentage: data?.total_posts?.change_percentage || 0,
                    trend: data?.total_posts?.trend || 'stable'
                },
                engagement_rate: {
                    value: data?.engagement_rate?.value || 0,
                    change_percentage: data?.engagement_rate?.change_percentage || 0,
                    trend: data?.engagement_rate?.trend || 'stable'
                },
                popular_categories: data?.popular_categories || [],
                content_distribution: data?.content_distribution || {},
                posting_frequency: {
                    name: data?.posting_frequency?.name || '',
                    data: data?.posting_frequency?.data || []
                }
            };
        } catch (error) {
            console.error('Error en getContentMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas de contenido');
        }
    },

    async getPopularCategories(timeRange = 'week') {
        try {
            const params = {
                time_range: timeRange
            };

            const { data } = await axios.get('/analytics/content/popular-categories', { params });
            return {
                additionalProp1: data?.additionalProp1 || 0,
                additionalProp2: data?.additionalProp2 || 0,
                additionalProp3: data?.additionalProp3 || 0
            };
        } catch (error) {
            console.error('Error en getPopularCategories:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener categorías populares');
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
                total_interactions: {
                    value: data?.total_interactions?.value || 0,
                    change_percentage: data?.total_interactions?.change_percentage || 0,
                    trend: data?.total_interactions?.trend || 'stable'
                },
                interaction_types: {
                    additionalProp1: data?.interaction_types?.additionalProp1 || 0,
                    additionalProp2: data?.interaction_types?.additionalProp2 || 0,
                    additionalProp3: data?.interaction_types?.additionalProp3 || 0
                },
                engagement_by_time: {
                    name: data?.engagement_by_time?.name || '',
                    data: data?.engagement_by_time?.data || [],
                    total: data?.engagement_by_time?.total || 0,
                    average: data?.engagement_by_time?.average || 0,
                    change_percentage: data?.engagement_by_time?.change_percentage || 0
                },
                avg_session_duration: {
                    value: data?.avg_session_duration?.value || 0,
                    change_percentage: data?.avg_session_duration?.change_percentage || 0,
                    trend: data?.avg_session_duration?.trend || 'stable'
                }
            };
        } catch (error) {
            console.error('Error en getEngagementMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas de engagement');
        }
    },

    async getPeakHours(timeRange = 'week') {
        try {
            const params = {
                time_range: timeRange
            };

            const { data } = await axios.get('/analytics/engagement/peak-hours', { params });
            return {
                additionalProp1: data?.additionalProp1 || 0,
                additionalProp2: data?.additionalProp2 || 0,
                additionalProp3: data?.additionalProp3 || 0
            };
        } catch (error) {
            console.error('Error en getPeakHours:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener horas pico');
        }
    },

    async getUserSegments(timeRange = 'month') {
        try {
            const params = {
                time_range: timeRange
            };

            const { data } = await axios.get('/analytics/engagement/user-segments', { params });
            return {
                additionalProp1: data?.additionalProp1 || 0,
                additionalProp2: data?.additionalProp2 || 0,
                additionalProp3: data?.additionalProp3 || 0
            };
        } catch (error) {
            console.error('Error en getUserSegments:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener segmentos de usuarios');
        }
    },

    async getPlatformMetrics(timeRange = 'day', startDate = null, endDate = null) {
        try {
            const params = {
                time_range: timeRange,
                ...(startDate && { start_date: startDate }),
                ...(endDate && { end_date: endDate })
            };

            const { data } = await axios.get('/analytics/platform', { params });
            return {
                system_health: {
                    additionalProp1: {
                        value: data?.system_health?.additionalProp1?.value || 0,
                        change_percentage: data?.system_health?.additionalProp1?.change_percentage || 0,
                        trend: data?.system_health?.additionalProp1?.trend || 'stable'
                    },
                    additionalProp2: {
                        value: data?.system_health?.additionalProp2?.value || 0,
                        change_percentage: data?.system_health?.additionalProp2?.change_percentage || 0,
                        trend: data?.system_health?.additionalProp2?.trend || 'stable'
                    },
                    additionalProp3: {
                        value: data?.system_health?.additionalProp3?.value || 0,
                        change_percentage: data?.system_health?.additionalProp3?.change_percentage || 0,
                        trend: data?.system_health?.additionalProp3?.trend || 'stable'
                    }
                },
                response_times: {
                    name: data?.response_times?.name || '',
                    data: data?.response_times?.data || [],
                    total: data?.response_times?.total || 0,
                    average: data?.response_times?.average || 0,
                    change_percentage: data?.response_times?.change_percentage || 0
                }
            };
        } catch (error) {
            console.error('Error en getPlatformMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener métricas de plataforma');
        }
    },

    async getSystemHealth() {
        try {
            const { data } = await axios.get('/analytics/platform/health');
            return {
                additionalProp1: {
                    value: data?.additionalProp1?.value || 0,
                    change_percentage: data?.additionalProp1?.change_percentage || 0,
                    trend: data?.additionalProp1?.trend || 'stable'
                },
                additionalProp2: {
                    value: data?.additionalProp2?.value || 0,
                    change_percentage: data?.additionalProp2?.change_percentage || 0,
                    trend: data?.additionalProp2?.trend || 'stable'
                },
                additionalProp3: {
                    value: data?.additionalProp3?.value || 0,
                    change_percentage: data?.additionalProp3?.change_percentage || 0,
                    trend: data?.additionalProp3?.trend || 'stable'
                }
            };
        } catch (error) {
            console.error('Error en getSystemHealth:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener estado del sistema');
        }
    },

    async getErrorRates(timeRange = 'day') {
        try {
            const params = {
                time_range: timeRange
            };

            const { data } = await axios.get('/analytics/platform/errors', { params });
            return {
                name: data?.name || '',
                data: data?.data || [],
                total: data?.total || 0,
                average: data?.average || 0,
                change_percentage: data?.change_percentage || 0
            };
        } catch (error) {
            console.error('Error en getErrorRates:', error);
            throw new Error(error.response?.data?.message || 'Error al obtener tasas de error');
        }
    },

    async exportMetrics(params) {
        try {
            const exportParams = {
                metrics_type: params.metricsType,
                time_range: params.timeRange || 'month',
                format: params.format || 'csv',
                ...(params.startDate && { start_date: params.startDate }),
                ...(params.endDate && { end_date: params.endDate })
            };

            const { data } = await axios.post('/analytics/export', exportParams);
            return data;
        } catch (error) {
            console.error('Error en exportMetrics:', error);
            throw new Error(error.response?.data?.message || 'Error al iniciar exportación de métricas');
        }
    },

    async getExportStatus(jobId) {
        try {
            const { data } = await axios.get(`/analytics/export/status/${jobId}`);
            return {
                status: data?.status || 'pending',
                progress: data?.progress || 0,
                message: data?.message || '',
                error: data?.error || null
            };
        } catch (error) {
            console.error('Error en getExportStatus:', error);
            throw new Error(error.response?.data?.message || 'Error al verificar estado de exportación');
        }
    },

    async getExportFile(filename) {
        try {
            const response = await axios.get(`/analytics/exports/${filename}`, {
                responseType: 'blob'
            });

            // Crear URL del blob y descargar
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

            return true;
        } catch (error) {
            console.error('Error en getExportFile:', error);
            throw new Error(error.response?.data?.message || 'Error al descargar archivo de exportación');
        }
    },

    async cleanupExports(maxAgeHours = 24) {
        try {
            const { data } = await axios.post('/analytics/export/cleanup', {
                max_age_hours: maxAgeHours
            });
            return data;
        } catch (error) {
            console.error('Error en cleanupExports:', error);
            throw new Error(error.response?.data?.message || 'Error al limpiar exportaciones antiguas');
        }
    },

    // Método utilitario para manejar exportaciones completas
    async handleFullExport(metricsType, timeRange = 'month', format = 'csv', startDate = null, endDate = null) {
        try {
            const exportResponse = await this.exportMetrics({
                metricsType,
                timeRange,
                format,
                startDate,
                endDate
            });
    
            const jobId = exportResponse.job_id;
            
            let attempts = 0;
            const maxAttempts = 30;
    
            while (attempts < maxAttempts) {
                const statusResponse = await this.getExportStatus(jobId);
                
                if (statusResponse.status === 'completed') {
                    const filename = `${metricsType}_${timeRange}_${new Date().toISOString()}.${format}`;
                    await this.getExportFile(filename);
                    return { success: true, filename };
                } else if (statusResponse.status === 'failed') {
                    throw new Error(statusResponse.error || 'La exportación falló');
                }
    
                await new Promise(resolve => setTimeout(resolve, 2000));
                attempts++;
            }
    
            throw new Error('Tiempo de espera agotado para la exportación');
        } catch (error) {
            console.error('Error en handleFullExport:', error);
            throw error;
        }
    }
};