import React, { useState } from 'react';

/**
 * Bar Chart Component
 * Displays grouped/stacked bars with proper scaling and dynamic labels
 */
const SimpleBarChart = ({ data, xKey, yKeys, title, colors = ['#00cc66', '#ef4444'], height = 220 }) => {
    const [tooltip, setTooltip] = useState(null);

    if (!data || data.length === 0) {
        return (
            <div className="flex items-center justify-center h-40 text-gray-500 text-sm">
                No data available
            </div>
        );
    }

    const svgWidth = 600;
    const svgHeight = height;
    const paddingLeft = 40;
    const paddingRight = 20;
    const paddingTop = 16;
    const paddingBottom = 36;

    const chartWidth = svgWidth - paddingLeft - paddingRight;
    const chartHeight = svgHeight - paddingTop - paddingBottom;

    // Max value across all yKeys per data point (stacked sum)
    const maxValue = Math.max(
        ...data.map(d => yKeys.reduce((sum, key) => sum + (d[key] || 0), 0)),
        1
    );

    // Nice round max for y-axis
    const niceMax = Math.ceil(maxValue / 5) * 5 || 5;
    const yTicks = 5;

    const groupWidth = chartWidth / data.length;
    const barWidth = Math.min(groupWidth * 0.55, 28);

    return (
        <div className="w-full">
            {title && <h4 className="text-sm font-medium text-gray-400 mb-3">{title}</h4>}
            <div className="relative">
                <svg
                    viewBox={`0 0 ${svgWidth} ${svgHeight}`}
                    className="w-full"
                    style={{ height: `${svgHeight}px` }}
                    onMouseLeave={() => setTooltip(null)}
                >
                    {/* Y-axis grid lines and labels */}
                    {Array.from({ length: yTicks + 1 }, (_, i) => {
                        const ratio = i / yTicks;
                        const y = paddingTop + chartHeight * (1 - ratio);
                        const value = Math.round(niceMax * ratio);
                        return (
                            <g key={i}>
                                <line
                                    x1={paddingLeft}
                                    y1={y}
                                    x2={paddingLeft + chartWidth}
                                    y2={y}
                                    stroke="#1f2937"
                                    strokeWidth="1"
                                    strokeDasharray={i === 0 ? 'none' : '4,4'}
                                />
                                <text
                                    x={paddingLeft - 6}
                                    y={y}
                                    textAnchor="end"
                                    dominantBaseline="middle"
                                    fontSize="10"
                                    fill="#6b7280"
                                >
                                    {value}
                                </text>
                            </g>
                        );
                    })}

                    {/* X-axis baseline */}
                    <line
                        x1={paddingLeft}
                        y1={paddingTop + chartHeight}
                        x2={paddingLeft + chartWidth}
                        y2={paddingTop + chartHeight}
                        stroke="#374151"
                        strokeWidth="1"
                    />

                    {/* Bars */}
                    {data.map((d, i) => {
                        const groupX = paddingLeft + i * groupWidth + groupWidth / 2;
                        const barX = groupX - barWidth / 2;
                        let currentY = paddingTop + chartHeight;

                        return (
                            <g
                                key={i}
                                onMouseEnter={(e) => {
                                    const rect = e.currentTarget.closest('svg').getBoundingClientRect();
                                    setTooltip({
                                        x: groupX,
                                        y: paddingTop + chartHeight * 0.3,
                                        label: d[xKey],
                                        values: yKeys.map(k => ({ key: k, value: d[k] || 0 }))
                                    });
                                }}
                                style={{ cursor: 'pointer' }}
                            >
                                {yKeys.map((key, ki) => {
                                    const value = d[key] || 0;
                                    const barH = (value / niceMax) * chartHeight;
                                    const y = currentY - barH;
                                    currentY = y;
                                    return (
                                        <rect
                                            key={ki}
                                            x={barX}
                                            y={y}
                                            width={barWidth}
                                            height={Math.max(barH, 0)}
                                            fill={colors[ki] || '#6b46c1'}
                                            rx="2"
                                            opacity="0.9"
                                        />
                                    );
                                })}
                            </g>
                        );
                    })}

                    {/* X-axis labels */}
                    {data.map((d, i) => {
                        const groupX = paddingLeft + i * groupWidth + groupWidth / 2;
                        // Show every label if ≤12 items, else thin out
                        const step = data.length <= 12 ? 1 : Math.ceil(data.length / 12);
                        if (i % step !== 0 && i !== data.length - 1) return null;
                        return (
                            <text
                                key={i}
                                x={groupX}
                                y={paddingTop + chartHeight + 16}
                                textAnchor="middle"
                                fontSize="10"
                                fill="#6b7280"
                            >
                                {d[xKey]}
                            </text>
                        );
                    })}

                    {/* Tooltip */}
                    {tooltip && (
                        <g>
                            <rect
                                x={Math.min(tooltip.x + 8, svgWidth - 110)}
                                y={tooltip.y - 10}
                                width={100}
                                height={16 + tooltip.values.length * 16}
                                rx="4"
                                fill="#1f2937"
                                stroke="#374151"
                                strokeWidth="1"
                            />
                            <text
                                x={Math.min(tooltip.x + 58, svgWidth - 60)}
                                y={tooltip.y + 6}
                                textAnchor="middle"
                                fontSize="10"
                                fill="#d1d5db"
                                fontWeight="600"
                            >
                                {tooltip.label}
                            </text>
                            {tooltip.values.map((v, i) => (
                                <text
                                    key={i}
                                    x={Math.min(tooltip.x + 58, svgWidth - 60)}
                                    y={tooltip.y + 20 + i * 16}
                                    textAnchor="middle"
                                    fontSize="10"
                                    fill={colors[i] || '#9ca3af'}
                                >
                                    {v.key}: {v.value}
                                </text>
                            ))}
                        </g>
                    )}
                </svg>
            </div>

            {/* Legend */}
            <div className="flex justify-center gap-5 mt-2">
                {yKeys.map((key, i) => (
                    <div key={i} className="flex items-center gap-1.5">
                        <div
                            className="w-3 h-3 rounded-sm"
                            style={{ backgroundColor: colors[i] || '#6b46c1' }}
                        />
                        <span className="text-xs text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SimpleBarChart;
