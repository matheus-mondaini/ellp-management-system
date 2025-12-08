export function BurndownChart() {
  const points = [100, 78, 62, 40, 25, 12];

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-white">
      <header className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-400">Sprint</p>
          <h3 className="text-lg font-semibold">Burndown</h3>
        </div>
        <span className="text-sm text-emerald-300">Semana 2</span>
      </header>

      <svg viewBox="0 0 200 120" className="mt-4 w-full">
        <polyline
          fill="none"
          stroke="rgba(16, 185, 129, 0.6)"
          strokeWidth="4"
          strokeLinecap="round"
          points={points
            .map((value, index) => {
              const x = (index / (points.length - 1)) * 180 + 10;
              const y = 110 - (value / 100) * 100;
              return `${x},${y}`;
            })
            .join(" ")}
        />
      </svg>

      <div className="mt-4 flex justify-between text-xs text-slate-400">
        {points.map((_, idx) => (
          <span key={idx}>Dia {idx + 1}</span>
        ))}
      </div>
    </div>
  );
}
