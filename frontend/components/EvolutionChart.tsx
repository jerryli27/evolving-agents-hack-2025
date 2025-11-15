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
        <div className="bg-white p-3 border-2 border-black">
          <p className="font-mono text-xs font-bold mb-2 uppercase">ROUND {label}</p>
          {payload.map((entry: any, index: number) => {
            const writer = writers.find(w => w.writer_id === entry.dataKey);
            return (
              <div key={index} className="flex items-center gap-2 mb-1">
                <div
                  className="w-2 h-2 border border-black"
                  style={{ backgroundColor: entry.color }}
                />
                <span className="text-xs font-mono">
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
    <div className="w-full h-[400px] md:h-[500px] bg-white p-3 md:p-6">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          onClick={handleClick}
        >
          <CartesianGrid stroke="#e5e7eb" strokeDasharray="3 3" />
          <XAxis
            dataKey="round"
            label={{ value: 'ROUND', position: 'insideBottom', offset: -5, style: { fontFamily: 'monospace', fontSize: 11, fontWeight: 'bold' } }}
            tick={{ fontSize: 12, fontFamily: 'monospace' }}
          />
          <YAxis
            domain={[0, 100]}
            label={{ value: 'SCORE', angle: -90, position: 'insideLeft', style: { fontFamily: 'monospace', fontSize: 11, fontWeight: 'bold' } }}
            tick={{ fontSize: 12, fontFamily: 'monospace' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: '20px', fontFamily: 'monospace', fontSize: 12 }}
          />
          {writers.map((writer) => (
            <Line
              key={writer.writer_id}
              type="monotone"
              dataKey={writer.writer_id}
              stroke={writer.color}
              strokeWidth={3}
              name={writer.name.toUpperCase()}
              dot={{ r: 4, cursor: 'pointer', strokeWidth: 2, stroke: '#000' }}
              activeDot={{ r: 7, cursor: 'pointer', strokeWidth: 2, stroke: '#000' }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
