import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const data = [
  { name: "Mon", temp: 24 },
  { name: "Tue", temp: 27 },
  { name: "Wed", temp: 26 },
  { name: "Thu", temp: 29 },
  { name: "Fri", temp: 27 },
  { name: "Sat", temp: 31 },
  { name: "Sun", temp: 28 },
];

function TelemetryChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="temp" fill="#6366f1" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default TelemetryChart;