function MetricCard({ title, value, unit, status }) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <h2>
        {value}
        {unit}
      </h2>
      <p>{status}</p>
    </div>
  );
}

export default MetricCard;