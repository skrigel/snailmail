"use client";

import type { DailyAnalytics } from '@/lib/types';
import { cn } from '@/lib/utils';

type SnailProps = {
  analytics: DailyAnalytics;
  onClick?: () => void;
  isStatic?: boolean;
};

const Snail = ({ analytics, onClick, isStatic = false }: SnailProps) => {
  const { emailsReceived, emailsReplied, responseTime } = analytics;

  const getShellColor = () => {
    if (emailsReceived > 60) return '#c22f2f'; // Red - high load
    if (emailsReceived > 40) return '#e08031'; // Orange - medium load
    return '#8ED14F'; // Green - normal load
  };

  const getBodyColor = () => {
    const replyRatio = emailsReplied / emailsReceived;
    if (replyRatio > 0.7) return '#FFC857'; // Yellow - very responsive
    if (replyRatio > 0.5) return '#a2a8b3'; // Grey - responsive
    return '#6b4d3b'; // Brown - less responsive
  };

  const getPatternColor = () => {
    if (responseTime < 15) return '#ffffff'; // White - super fast
    if (responseTime < 30) return '#dddddd'; // Light grey - fast
    return '#a7a7a7'; // Dark grey - slow
  };

  const shellColor = getShellColor();
  const bodyColor = getBodyColor();
  const patternColor = getPatternColor();

  const SnailSVG = (
    <svg viewBox="0 0 40 30" shapeRendering="crispEdges" className="pixelated w-full h-full">
      {/* Body */}
      <rect x="5" y="20" width="30" height="5" fill={bodyColor} />
      <rect x="30" y="15" width="5" height="5" fill={bodyColor} />
      {/* Eye */}
      <rect x="35" y="15" width="3" height="3" fill="#000000" />
      {/* Shell */}
      <rect x="0" y="5" width="25" height="20" fill={shellColor} />
      <rect x="5" y="0" width="15" height="5" fill={shellColor} />
      {/* Shell Pattern */}
      <rect x="5" y="15" width="5" height="5" fill={patternColor} />
      <rect x="15" y="5" width="5" height="5" fill={patternColor} />
    </svg>
  );

  if (isStatic) {
    return <div className="w-16 h-12">{SnailSVG}</div>;
  }

  return (
    <div>
        <button
      onClick={onClick}
      className={cn(
        'w-16 h-12 p-1 rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:ring-offset-background',
        'hover:scale-110 hover:-translate-y-1'
      )}
      aria-label={`View analytics for ${analytics.date}`}
    >
      {SnailSVG}
    </button>
    </div>
  );
};

export default Snail;
