import React from 'react';

/**
 * Simple Pie Chart Component
 * Displays a donut chart without external dependencies
 */
const SimplePieChart = ({ data, labelKey, valueKey, title, colors = ['#00cccc', '#6b46c1', '#f59e0b', '#00cc66', '#ef4444'] }) => {
    if (!data || data.length === 0) {
        return (
            <div className="flex items-center justify-center h-64 text-gray-500">
                No data available
            </div>
        );
    }

    const size = 100;
    const center = size / 2;
    const radius = 35;
    const innerRadius = 20;

    const total = data.reduce((sum, d) => sum + (d[valueKey] || 0), 0);
    
    if (total === 0) {
        return (
            <div className="flex items-center justify-center h-64 text-gray-500">
                No progress data yet
            </div>
        );
    }

    let currentAngle = -90; // Start from top

    const slices = data.map((d, i) => {
        const value = d[valueKey] || 0;
        const percentage = (value / total) * 100;
        const angle = (value / total) * 360;
        const startAngle = currentAngle;
        const endAngle = currentAngle + angle;
        currentAngle = endAngle;

        // Calculate arc path
        const startRad = (startAngle * Math.PI) / 180;
        const endRad = (endAngle * Math.PI) / 180;

        const x1 = center + radius * Math.cos(startRad);
        const y1 = center + radius * Math.sin(startRad);
        const x2 = center + radius * Math.cos(endRad);
        const y2 = center + radius * Math.sin(endRad);

        const x3 = center + innerRadius * Math.cos(endRad);
        const y3 = center + innerRadius * Math.sin(endRad);
        const x4 = center + innerRadius * Math.cos(startRad);
        const y4 = center + innerRadius * Math.sin(startRad);

        const largeArc = angle > 180 ? 1 : 0;

        const path = [
            `M ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
            `L ${x3} ${y3}`,
            `A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${x4} ${y4}`,
            'Z'
        ].join(' ');

        return {
            path,
            color: colors[i % colors.length],
            label: d[labelKey],
            value: value,
            percentage: percentage.toFixed(1)
        };
    });

    return (
        <div className="w-full">
            {title && <h4 className="text-sm font-medium text-gray-400 mb-3">{title}</h4>}
            <div className="flex flex-col md:flex-row items-center gap-6">
                {/* Chart */}
                <svg
                    viewBox={`0 0 ${size} ${size}`}
                    className="w-48 h-48 shrink-0"
                >
                    {slices.map((slice, i) => (
                        <path
                            key={i}
                            d={slice.path}
                            fill={slice.color}
                            opacity="0.9"
                            className="hover:opacity-100 transition-opacity cursor-pointer"
                        >
                            <title>{`${slice.label}: ${slice.value}%`}</title>
                        </path>
                    ))}
                    {/* Center text */}
                    <text
                        x={center}
                        y={center - 4}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        fontSize="6"
                        fill="#9ca3af"
                        fontWeight="500"
                    >
                        Total
                    </text>
                    <text
                        x={center}
                        y={center + 6}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        fontSize="8"
                        fill="white"
                        fontWeight="bold"
                    >
                        {data.length}
                    </text>
                </svg>

                {/* Legend */}
                <div className="flex-1 space-y-2">
                    {slices.map((slice, i) => (
                        <div key={i} className="flex items-center justify-between gap-3 p-2 bg-[#0f0f1a] rounded-lg border border-gray-800">
                            <div className="flex items-center gap-2 flex-1 min-w-0">
                                <div
                                    className="w-3 h-3 rounded shrink-0"
                                    style={{ backgroundColor: slice.color }}
                                />
                                <span className="text-sm text-gray-300 truncate">{slice.label}</span>
                            </div>
                            <span className="text-sm font-semibold shrink-0" style={{ color: slice.color }}>
                                {slice.value}%
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SimplePieChart;
