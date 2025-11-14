'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Writer, MetricType } from '@/types';

interface EvolutionChartProps {
  data: any[];
  writers: Writer[];
  metric: MetricType;
  onPointClick: (writerId: string, round: number) => void;
}

export default function EvolutionChart({ data, writers, metric, onPointClick }: EvolutionChartProps) {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-semibold mb-2">Round {label}</p>
          {payload.map((entry: any, index: number) => {
            const writer = writers.find(w => w.writer_id === entry.dataKey);
            return (
              <div key={index} className="flex items-center gap-2 mb-1">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: entry.color }}
                />
                <span className="text-sm">
                  {writer?.name}: <strong>{entry.value.toFixed(1)}</strong>
                </span>
              </div>
            );
          })}
        </div>
      );
    }
    return null;
  };

  const handleClick = (data: any) => {
    if (data && data.activePayload && data.activePayload.length > 0) {
      const writerId = data.activePayload[0].dataKey;
      const round = data.activeLabel;
      onPointClick(writerId, round);
    }
  };

  return (
    <div className="w-full h-[500px] bg-white dark:bg-gray-900 p-6 rounded-lg shadow">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          onClick={handleClick}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            dataKey="round"
            label={{ value: 'Round', position: 'insideBottom', offset: -5 }}
            className="text-gray-700 dark:text-gray-300"
          />
          <YAxis
            domain={[0, 100]}
            label={{ value: 'Score', angle: -90, position: 'insideLeft' }}
            className="text-gray-700 dark:text-gray-300"
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            onClick={(e) => {
              // Handle legend click for writer selection
              console.log('Legend clicked:', e);
            }}
          />
          {writers.map((writer) => (
            <Line
              key={writer.writer_id}
              type="monotone"
              dataKey={writer.writer_id}
              stroke={writer.color}
              strokeWidth={2}
              name={writer.name}
              dot={{ r: 5, cursor: 'pointer' }}
              activeDot={{ r: 8, cursor: 'pointer' }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
