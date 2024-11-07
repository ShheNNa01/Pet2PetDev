import React, { useState, useEffect } from 'react';
import { Line, Pie, Bar, Doughnut } from 'react-chartjs-2';
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
import { Card, CardContent, CardHeader } from "../ui/card";
import { Badge } from "../ui/badge";
import { 
    Users, 
    Activity,
    Heart,
    TrendingUp,
    AlertCircle,
    Clock,
    Layers,
    Target,
    Loader2
} from 'lucide-react';
import { analyticsService } from '../services/analyticsService';

const COLORS = {
    primary: '#d55b49',
    secondary: '#509ca2',
    light: '#eeede8',
    dark: '#1a1a1a',
};

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

const Dashboard = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [analytics, setAnalytics] = useState(null);

    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await analyticsService.getDashboardMetrics();
            setAnalytics(data);
            setError(null);
        } catch (err) {
            setError('Error al cargar los datos');
            console.error('Error:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 300000); // 5 minutos
        return () => clearInterval(interval);
    }, []);

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
                        onClick={fetchData}
                        className="mt-4 px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#1a1a1a] p-6">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8 flex justify-between items-center">
                    <div>
                        <h1 className="text-4xl font-bold text-[#eeede8] mb-2">PET2PET Dashboard</h1>
                        <p className="text-[#509ca2]">Monitoreo en tiempo real de la actividad de la plataforma</p>
                    </div>
                    <button 
                        onClick={fetchData} 
                        className="px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                    >
                        Actualizar Datos
                    </button>
                </div>

                {/* Métricas principales */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Usuarios Totales</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {analytics?.metrics?.totalUsers?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#d55b49]/20 text-[#d55b49] mt-2">
                                        <TrendingUp className="w-3 h-3 mr-1" />
                                        {analytics?.metrics?.userGrowth}%
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
                                        {analytics?.metrics?.activeUsers?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#509ca2]/20 text-[#509ca2] mt-2">
                                        <Clock className="w-3 h-3 mr-1" />
                                        Ahora
                                    </Badge>
                                </div>
                                <Activity className="w-12 h-12 text-[#509ca2]" />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardContent className="p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-[#509ca2] mb-1">Interacciones</p>
                                    <h3 className="text-2xl font-bold text-[#eeede8]">
                                        {analytics?.metrics?.totalInteractions?.toLocaleString()}
                                    </h3>
                                    <Badge className="bg-[#d55b49]/20 text-[#d55b49] mt-2">
                                        <Heart className="w-3 h-3 mr-1" />
                                        Hoy
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
                                        {analytics?.metrics?.systemHealth}
                                    </h3>
                                    <Badge className="bg-[#509ca2]/20 text-[#509ca2] mt-2">
                                        <AlertCircle className="w-3 h-3 mr-1" />
                                        {analytics?.metrics?.errorCount} errores
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
                        <CardContent>
                            {analytics?.userGrowth && (
                                <Line
                                    data={{
                                        labels: analytics.userGrowth.labels,
                                        datasets: [{
                                            label: 'Nuevos Usuarios',
                                            data: analytics.userGrowth.data,
                                            borderColor: COLORS.primary,
                                            backgroundColor: 'rgba(213, 91, 73, 0.1)',
                                            tension: 0.4,
                                            fill: true,
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
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
                                                ticks: { color: COLORS.light }
                                            }
                                        }
                                    }}
                                />
                            )}
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Categorías Populares</h3>
                        </CardHeader>
                        <CardContent>
                            {analytics?.categories && (
                                <Bar
                                    data={{
                                        labels: analytics.categories.map(cat => cat.name),
                                        datasets: [{
                                            label: 'Posts',
                                            data: analytics.categories.map(cat => cat.count),
                                            backgroundColor: COLORS.secondary,
                                        }]
                                    }}
                                    options={{
                                        indexAxis: 'y',
                                        responsive: true,
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
                                                ticks: { color: COLORS.light }
                                            }
                                        }
                                    }}
                                />
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Gráficos de engagement */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Actividad por Hora</h3>
                        </CardHeader>
                        <CardContent>
                            {analytics?.hourlyActivity && (
                                <Line
                                    data={{
                                        labels: analytics.hourlyActivity.hours,
                                        datasets: [{
                                            label: 'Usuarios Activos',
                                            data: analytics.hourlyActivity.counts,
                                            borderColor: COLORS.primary,
                                            backgroundColor: 'rgba(213, 91, 73, 0.1)',
                                            tension: 0.4,
                                            fill: true,
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
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
                                                ticks: { color: COLORS.light }
                                            }
                                        }
                                    }}
                                />
                            )}
                        </CardContent>
                    </Card>

                    <Card className="bg-[#1a1a1a] border border-[#509ca2]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Distribución de Usuarios</h3>
                        </CardHeader>
                        <CardContent>
                            {analytics?.userSegments && (
                                <Doughnut
                                    data={{
                                        labels: analytics.userSegments.map(segment => segment.name),
                                        datasets: [{
                                            data: analytics.userSegments.map(segment => segment.value),
                                            backgroundColor: [
                                                COLORS.primary,
                                                COLORS.secondary,
                                                'rgba(238, 237, 232, 0.2)'
                                            ],
                                        }]
                                    }}
                                    options={{
                                        responsive: true,
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

                {/* Footer */}
                <div className="mt-6 p-4 bg-[#1a1a1a] border border-[#509ca2]/20 rounded-lg">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <div className="text-[#eeede8]">
                            <p>Última actualización: {analytics?.lastUpdated || new Date().toLocaleString()}</p>
                        </div>
                        <div className="flex gap-4">
                            <button 
                                className="px-4 py-2 bg-[#509ca2] text-white rounded-lg hover:bg-[#509ca2]/90"
                                onClick={() => analyticsService.exportMetricsCsv()}
                            >
                                Exportar CSV
                            </button>
                            <button 
                                className="px-4 py-2 bg-[#d55b49] text-white rounded-lg hover:bg-[#d55b49]/90"
                                onClick={() => analyticsService.generateReport()}
                            >
                                Generar Reporte
                            </button>
                        </div>
                    </div>
                </div>

                {/* Panel de métricas detalladas */}
                <div className="mt-6">
                    <Card className="bg-[#1a1a1a] border border-[#d55b49]/20">
                        <CardHeader>
                            <h3 className="text-xl font-semibold text-[#eeede8]">Métricas Detalladas</h3>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {analytics?.detailedMetrics?.map((metric, index) => (
                                    <div 
                                        key={metric.name} 
                                        className="p-4 bg-[#1a1a1a] border border-[#d55b49]/20 rounded-lg"
                                    >
                                        <p className="text-[#509ca2] text-sm mb-1">{metric.name}</p>
                                        <h4 className="text-xl font-bold text-[#eeede8]">{metric.value}</h4>
                                        <span 
                                            className={`text-sm ${
                                                metric.change > 0 ? 'text-[#d55b49]' : 'text-[#509ca2]'
                                            }`}
                                        >
                                            {metric.change > 0 ? '+' : ''}{metric.change}% vs último mes
                                        </span>
                                    </div>
                                ))}
                            </div>

                            {analytics?.weeklyMetrics && (
                                <div className="mt-6">
                                    <Bar
                                        data={{
                                            labels: analytics.weeklyMetrics.days,
                                            datasets: [{
                                                label: 'Engagement Score',
                                                data: analytics.weeklyMetrics.values,
                                                backgroundColor: COLORS.secondary,
                                            }]
                                        }}
                                        options={{
                                            responsive: true,
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
                                                    ticks: { color: COLORS.light }
                                                }
                                            }
                                        }}
                                    />
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;