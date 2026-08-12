import React from 'react';

interface ScoreGaugeProps {
  score: number;
  size?: number;
  label?: string;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score, size = 160, label = "CONCEPT SCORE" }) => {
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  let colorClass = 'stroke-emerald-500';
  let bgGlow = 'rgba(16, 185, 129, 0.15)';
  let statusText = 'Strong Understanding';
  let statusColor = 'text-emerald-400';

  if (score < 60) {
    colorClass = 'stroke-rose-500';
    bgGlow = 'rgba(239, 68, 68, 0.15)';
    statusText = 'Needs Improvement';
    statusColor = 'text-rose-400';
  } else if (score < 80) {
    colorClass = 'stroke-amber-500';
    bgGlow = 'rgba(245, 158, 11, 0.15)';
    statusText = 'Partial Mastery';
    statusColor = 'text-amber-400';
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className="stroke-slate-800"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className={`${colorClass} transition-all duration-1000 ease-out`}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            style={{
              filter: `drop-shadow(0px 0px 8px ${bgGlow})`
            }}
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-white tracking-tight">{Math.round(score)}</span>
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">out of 100</span>
        </div>
      </div>

      <div className="mt-3 text-center">
        <span className={`text-sm font-bold ${statusColor} tracking-wide`}>
          ● {statusText}
        </span>
      </div>
    </div>
  );
};
