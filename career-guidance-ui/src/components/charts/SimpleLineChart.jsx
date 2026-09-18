import React, { useState } from 'react';

/**
 * Line Chart Component
 * Displays a smooth line chart with area fill, proper axis labels, and tooltips
 */
const SimpleLineChart = ({ data, xKey, yKey, title, color = '#00cccc', height = 220 }) => {
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
    const paddingLeft = 44;
    const paddingRight = 20;
    const paddingTop = 16;
    const paddingBottom = 36;

    const chartWidth = svgWidth - paddingLeft - paddingRight;
    const chartHeight = svgHeight - paddingTop - paddingBottom;

    const values = data.map(d => Number(d[yKey]) || 0);
    const maxValue = Math.max(...values, 1);
    const niceMax = Math.ceil(maxValue / 5) * 5 || 5;
    const yTicks = 5;

    // Map data to SVG coordinates
    const points = data.map((d, i) => {
        const x = data.length === 1
            ? paddingLeft + chartWidth / 2
            : paddingLeft + (i / (data.length - 1)) * chartWidth;
        const y = paddingTop + chartHeight - ((Number(d[yKey]) || 0) / niceMax) * chartHeight;
        return { x, y, d };
    });

    const polylinePoints = points.map(p => `${p.x},${p.y}`).join(' ');

    // Area fill path
    const areaPath = [
        `M ${points[0].x} ${paddingTop + chartHeight}`,
        ...points.map(p => `L ${p.x} ${p.y}`),
        `L ${points[points.length - 1].x} ${paddingTop + chartHeight}`,
        'Z'
    ].join(' ');

    // Decide how many x-axis labels to show
    const maxLabels = 10;
    const labelStep = Math.ceil(data.length / maxLabels);

    // Format x-axis label: if it looks like a date (YYYY-MM-DD), show day/month
    const formatXLabel = (val) => {
        if (!val) return '';
        // ISO date: YYYY-MM-DD
        if (/^\d{4}-\d{2}-\d{2}$/.test(val)) {
            const d = new Date(val);
            return `${d.getDate()}/${d.getMonth() + 1}`;
        }
        // Month label like "Jan 2024" → "Jan"
        if (/^[A-Za-z]{3}\s\d{4}$/.test(val)) {
            return val.split(' ')[0];
        }
        return val;
    };

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

                    {/* Area fill */}
                    <path
                        d={areaPath}
                        fill={color}
                        fillOpacity="0.12"
                    />

                    {/* Line */}
                    <polyline
                        points={polylinePoints}
                        fill="none"
                        stroke={color}
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {/* Data points + hover targets */}
                    {points.map((p, i) => (
                        <g key={i}>
                            <circle
                                cx={p.x}
                                cy={p.y}
                                r="4"
                                fill={color}
                                stroke="#0f0f1a"
                                strokeWidth="1.5"
                            />
                            {/* Invisible larger hit area */}
                            <circle
                                cx={p.x}
                                cy={p.y}
                                r="10"
                                fill="transparent"
                                style={{ cursor: 'pointer' }}
                                onMouseEnter={() => setTooltip({ x: p.x, y: p.y, label: p.d[xKey], value: p.d[yKey] })}
                            />
                        </g>
                    ))}

                    {/* X-axis labels */}
                    {points.map((p, i) => {
                        if (i % labelStep !== 0 && i !== data.length - 1) return null;
                        return (
                            <text
                                key={i}
                                x={p.x}
                                y={paddingTop + chartHeight + 16}
                                textAnchor="middle"
                                fontSize="10"
                                fill="#6b7280"
                            >
                                {formatXLabel(p.d[xKey])}
                            </text>
                        );
                    })}

                    {/* Tooltip */}
                    {tooltip && (
                        <g>
                            <line
                                x1={tooltip.x}
                                y1={paddingTop}
                                x2={tooltip.x}
                                y2={paddingTop + chartHeight}
                                stroke={color}
                                strokeWidth="1"
                                strokeDasharray="3,3"
                                opacity="0.5"
                            />
                            <rect
                                x={Math.min(tooltip.x + 8, svgWidth - 110)}
                                y={tooltip.y - 28}
                                width={100}
                                height={36}
                                rx="4"
                                fill="#1f2937"
                                stroke="#374151"
                                strokeWidth="1"
                            />
                            <text
                                x={Math.min(tooltip.x + 58, svgWidth - 60)}
                                y={tooltip.y - 14}
                                textAnchor="middle"
                                fontSize="10"
                                fill="#d1d5db"
                                fontWeight="600"
                            >
                                {tooltip.label}
                            </text>
                            <text
                                x={Math.min(tooltip.x + 58, svgWidth - 60)}
                                y={tooltip.y + 2}
                                textAnchor="middle"
                                fontSize="11"
                                fill={color}
                                fontWeight="700"
                            >
                                {tooltip.value}
                            </text>
                        </g>
                    )}
                </svg>
            </div>
        </div>
    );
};

export default SimpleLineChart;
