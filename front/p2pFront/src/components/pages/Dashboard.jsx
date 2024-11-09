import React, { useState, useEffect } from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    BarElement,
} from 'chart.js';
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from 'react-router-dom';
import {
    Users,
    Activity,
    Heart,
    TrendingUp,
    AlertCircle,
    Clock,
    Layers,
    Target,
    Loader2,
    Home
} from 'lucide-react';
import { analyticsService } from '../services/analyticsService';

// Registro de componentes de Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    BarElement
);

const COLORS = {
    primary: '#d55b49',
    secondary: '#509ca2',
    light: '#eeede8',
    dark: '#1a1a1a',
};

const Dashboard = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [dashboardData, setDashboardData] = useState({
        user_metrics: null,
        content_metrics: null,
        engagement_metrics: null,
        platform_metrics: null
    });
    const [timeRange, setTimeRange] = useState('day');

    const fetchDashboardData = async () => {
        setLoading(true);
        try {
            const data = await analyticsService.getDashboardMetrics(timeRange);
            setDashboardData(data);
            setError(null);
        } catch (err) {
            setError('Error al cargar los datos');
            console.error('Error:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 300000); // 5 minutos
        return () => clearInterval(interval);
    }, [timeRange]);

    if (loading) {
        return (
            <div className="min-h-screen bg-[#1a1a1a] flex items-center justify-center">
                <Loader2 className="h-12 w-12 animate-spin text-[#d55b49]" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-[#1a1a1a] flex items-center justify-center">
                <div className="text-center p-6 border border-[#d55b49] rounded-lg">
                    <AlertCircle className="h-12 w-12 text-[#d55b49] mx-auto" />
                    <p className="mt-4 text-[#eeede8]">{error}</p>
                    <button
                        onClick={fetchDashboardData}
                        className="mt-4 px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    const { user_metrics, content_metrics, engagement_metrics, platform_metrics } = dashboardData;

    return (
        <div className="min-h-screen bg-[#1a1a1a] p-6">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8 flex justify-between items-center">
                    <div>
                        <h1 className="text-4xl font-bold text-[#eeede8] mb-2">PET2PET Dashboard</h1>
                        <p className="text-[#509ca2]">Monitoreo en tiempo real de la actividad de la plataforma</p>
                    </div>
                    <div className="flex gap-4">
                        <button
                            onClick={() => navigate('/')}
                            className="px-4 py-2 bg-[#509ca2] text-white rounded-lg hover:bg-[#509ca2]/90 flex items-center gap-2"
                        >
                            <Home className="w-4 h-4" />
                            Volver al Inicio
                        </button>
                        <select
                            value={timeRange}
                            onChange={(e) => setTimeRange(e.target.value)}
                            className="px-4 py-2 bg-[#1a1a1a] text-[#eeede8] border border-[#509ca2] rounded-lg"
                        >
                            <option value="day">Hoy</option>
                            <option value="week">Esta semana</option>
                            <option value="month">Este mes</option>
                            <option value="year">Este año</option>
                        </select>
                        <button
                            onClick={fetchDashboardData}
                            className="px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                        >
                            Actualizar
                        </button>
                    </div>
                </div>

                {/* Métricas principales */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Usuarios Totales</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {user_metrics?.total_users?.value?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#d55b49]/20 text-[#d55b49] mt-2">
                                        <TrendingUp className="w-3 h-3 mr-1" />
                                        {user_metrics?.total_users?.change_percentage?.toFixed(1)}%
                                    </Badge>
                                </div>
                                <Users className="w-12 h-12 text-[#d55b49]" />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Usuarios Activos</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {user_metrics?.active_users?.value?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#509ca2]/20 text-[#509ca2] mt-2">
                                        <Activity className="w-3 h-3 mr-1" />
                                        {user_metrics?.active_users?.change_percentage?.toFixed(1)}%
                                    </Badge>
                                </div>
                                <Clock className="w-12 h-12 text-[#509ca2]" />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Interacciones</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {engagement_metrics?.total_interactions?.value?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#d55b49]/20 text-[#d55b49] mt-2">
                                        <Heart className="w-3 h-3 mr-1" />
                                        {engagement_metrics?.total_interactions?.change_percentage?.toFixed(1)}%
                                    </Badge>
                                </div>
                                <Target className="w-12 h-12 text-[#d55b49]" />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Salud Sistema</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {platform_metrics?.system_health?.cpu_usage?.value?.toFixed(1)}%
                                    </h3>
                                    <Badge className="bg-[#509ca2]/20 text-[#509ca2] mt-2">
                                        <AlertCircle className="w-3 h-3 mr-1" />
                                        CPU
                                    </Badge>
                                </div>
                                <Layers className="w-12 h-12 text-[#509ca2]" />
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Gráficos principales */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Crecimiento de Usuarios</h3>
                        </CardHeader>
                        <CardContent className="h-80">
                            {user_metrics?.user_growth?.data && (
                                <Line
                                    data={{
                                        labels: user_metrics.user_growth.data.map(point =>
                                            new Date(point.timestamp).toLocaleTimeString()
                                        ),
                                        datasets: [{
                                            label: 'Nuevos Usuarios',
                                            data: user_metrics.user_growth.data.map(point => point.value),
                                            borderColor: COLORS.primary,
                                            backgroundColor: 'rgba(213, 91, 73, 0.1)',
                                            tension: 0.4,
                                            fill: true,
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                                position: 'top',
                                                labels: { color: COLORS.light }
                                            }
                                        },
                                        scales: {
                                            y: {
                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                ticks: { color: COLORS.light }
                                            },
                                            x: {
                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                ticks: {
                                                    color: COLORS.light,
                                                    maxRotation: 45,
                                                    minRotation: 45
                                                }
                                            }
                                        }
                                    }}
                                />
                            )}
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Distribución de Contenido</h3>
                        </CardHeader>
                        <CardContent className="h-80">
                            {content_metrics?.content_distribution && (
                                <Doughnut
                                    data={{
                                        labels: Object.keys(content_metrics.content_distribution).map(
                                            key => key.replace('_', ' ').toUpperCase()
                                        ),
                                        datasets: [{
                                            data: Object.values(content_metrics.content_distribution),
                                            backgroundColor: [
                                                COLORS.primary,
                                                COLORS.secondary,
                                                'rgba(238, 237, 232, 0.2)'
                                            ],
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                                position: 'bottom',
                                                labels: { color: COLORS.light }
                                            }
                                        }
                                    }}
                                />
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Engagement Metrics */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Engagement por Tiempo</h3>
                        </CardHeader>
                        <CardContent className="h-80">
                            {engagement_metrics?.engagement_by_time?.data && (
                                <Line
                                    data={{
                                        labels: engagement_metrics.engagement_by_time.data.map(point =>
                                            new Date(point.timestamp).toLocaleTimeString()
                                        ),
                                        datasets: [{
                                            label: 'Interacciones',
                                            data: engagement_metrics.engagement_by_time.data.map(point => point.value),
                                            borderColor: COLORS.primary,
                                            backgroundColor: 'rgba(213, 91, 73, 0.1)',
                                            tension: 0.4,
                                            fill: true,
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                                position: 'top',
                                                labels: { color: COLORS.light }
                                            }
                                        },
                                        scales: {
                                            y: {
                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                ticks: { color: COLORS.light }
                                            },
                                            x: {
                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                ticks: {
                                                    color: COLORS.light,
                                                    maxRotation: 45,
                                                    minmaxRotation: 45,
                                                    minRotation: 45
                                                                }
                                                            }
                                                        }
                                                    }}
                                                />
                                            )}
                                        </CardContent>
                                    </Card>
                
                                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                                        <CardHeader>
                                            <h3 className="text-xl font-semibold text-[#eeede8]">Segmentos de Usuarios</h3>
                                        </CardHeader>
                                        <CardContent className="h-80">
                                            {engagement_metrics?.user_segments && (
                                                <Bar
                                                    data={{
                                                        labels: engagement_metrics.user_segments.map(
                                                            segment => segment.segment
                                                        ),
                                                        datasets: [{
                                                            label: 'Distribución de usuarios',
                                                            data: engagement_metrics.user_segments.map(
                                                                segment => segment.percentage
                                                            ),
                                                            backgroundColor: COLORS.secondary,
                                                        }]
                                                    }}
                                                    options={{
                                                        responsive: true,
                                                        maintainAspectRatio: false,
                                                        plugins: {
                                                            legend: {
                                                                position: 'top',
                                                                labels: { color: COLORS.light }
                                                            }
                                                        },
                                                        scales: {
                                                            y: {
                                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                                ticks: {
                                                                    color: COLORS.light,
                                                                    callback: (value) => `${value}%`
                                                                }
                                                            },
                                                            x: {
                                                                grid: { color: 'rgba(238, 237, 232, 0.1)' },
                                                                ticks: { color: COLORS.light }
                                                            }
                                                        }
                                                    }}
                                                />
                                            )}
                                        </CardContent>
                                    </Card>
                                </div>
                
                                {/* Detalles adicionales */}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                                    {/* Horas pico */}
                                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                                        <CardHeader>
                                            <h3 className="text-xl font-semibold text-[#eeede8]">Horas Pico</h3>
                                        </CardHeader>
                                        <CardContent>
                                            {engagement_metrics?.peak_activity_hours?.map((hour, index) => (
                                                <div key={hour.hour} className="mb-4">
                                                    <div className="flex justify-between text-sm text-[#eeede8] mb-1">
                                                        <span>{hour.hour}</span>
                                                        <span>{hour.percentage.toFixed(1)}%</span>
                                                    </div>
                                                    <div className="w-full bg-[#1a1a1a] rounded-full h-2">
                                                        <div
                                                            className="bg-[#d55b49] h-2 rounded-full"
                                                            style={{ width: `${hour.percentage}%` }}
                                                        />
                                                    </div>
                                                </div>
                                            ))}
                                        </CardContent>
                                    </Card>
                
                                    {/* Tipos de interacción */}
                                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                                        <CardHeader>
                                            <h3 className="text-xl font-semibold text-[#eeede8]">Tipos de Interacción</h3>
                                        </CardHeader>
                                        <CardContent>
                                            {engagement_metrics?.interaction_types && Object.entries(engagement_metrics.interaction_types).map(([type, value]) => (
                                                <div key={type} className="mb-4">
                                                    <div className="flex justify-between text-sm text-[#eeede8] mb-1">
                                                        <span>{type.replace('reaction_', '').replace('_', ' ').toUpperCase()}</span>
                                                        <span>{value.toFixed(1)}%</span>
                                                    </div>
                                                    <div className="w-full bg-[#1a1a1a] rounded-full h-2">
                                                        <div
                                                            className="bg-[#509ca2] h-2 rounded-full"
                                                            style={{ width: `${value}%` }}
                                                        />
                                                    </div>
                                                </div>
                                            ))}
                                        </CardContent>
                                    </Card>
                
                                    {/* Salud del sistema */}
                                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                                        <CardHeader>
                                            <h3 className="text-xl font-semibold text-[#eeede8]">Salud del Sistema</h3>
                                        </CardHeader>
                                        <CardContent>
                                            {platform_metrics?.system_health && Object.entries(platform_metrics.system_health).map(([metric, data]) => (
                                                <div key={metric} className="mb-4">
                                                    <div className="flex justify-between text-sm text-[#eeede8] mb-1">
                                                        <span>{metric.replace('_', ' ').toUpperCase()}</span>
                                                        <span>{data.value.toFixed(1)}%</span>
                                                    </div>
                                                    <div className="w-full bg-[#1a1a1a] rounded-full h-2">
                                                        <div
                                                            className={`h-2 rounded-full ${
                                                                data.value > 80 ? 'bg-red-500' :
                                                                data.value > 60 ? 'bg-yellow-500' :
                                                                'bg-green-500'
                                                            }`}
                                                            style={{ width: `${data.value}%` }}
                                                        />
                                                    </div>
                                                </div>
                                            ))}
                                        </CardContent>
                                    </Card>
                                </div>
                
                                {/* Footer con exportación */}
                                <div className="mt-6 p-4 bg-[#1a1a1a] border border-[#509ca2]/20 rounded-lg">
                                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                                        <div className="text-[#eeede8]">
                                            <p>Última actualización: {new Date().toLocaleString()}</p>
                                        </div>
                                        <div className="flex gap-4">
                                            <button
                                                onClick={() => analyticsService.exportMetrics({
                                                    metricsType: 'all',
                                                    timeRange,
                                                    format: 'csv'
                                                })}
                                                className="px-4 py-2 bg-[#509ca2] text-white rounded-lg hover:bg-[#509ca2]/90"
                                            >
                                                Exportar CSV
                                            </button>
                                            <button
                                                onClick={() => analyticsService.exportMetrics({
                                                    metricsType: 'all',
                                                    timeRange,
                                                    format: 'json'
                                                })}
                                                className="px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                                            >
                                                Exportar JSON
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                };
                
                export default Dashboard;