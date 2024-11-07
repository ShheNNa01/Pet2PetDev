import { useState, useCallback } from 'react';
import { analyticsService } from '../services/analyticsService';

export const useAnalyticsData = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dashboardData, setDashboardData] = useState({
        userMetrics: null,
        contentMetrics: null,
        engagementMetrics: null,
        platformMetrics: null,
        systemHealth: null
    });

    const fetchAllMetrics = useCallback(async (timeRange = 'day', startDate = null, endDate = null) => {
        setLoading(true);
        setError(null);
        try {
            const [
                userMetrics,
                contentMetrics,
                engagementMetrics,
                platformMetrics,
                systemHealth
            ] = await Promise.all([
                analyticsService.getUserMetrics(timeRange, startDate, endDate),
                analyticsService.getContentMetrics(timeRange, startDate, endDate),
                analyticsService.getEngagementMetrics(timeRange, startDate, endDate),
                analyticsService.getPlatformMetrics(timeRange, startDate, endDate),
                analyticsService.getSystemHealth()
            ]);

            setDashboardData({
                userMetrics,
                contentMetrics,
                engagementMetrics,
                platformMetrics,
                systemHealth
            });
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }, []);

    const exportAnalytics = async () => {
        try {
            const blob = await analyticsService.exportMetricsCsv();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analytics-export-${new Date().toISOString()}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            setError(error.message);
        }
    };

    return {
        loading,
        error,
        dashboardData,
        fetchAllMetrics,
        exportAnalytics
    };
};
