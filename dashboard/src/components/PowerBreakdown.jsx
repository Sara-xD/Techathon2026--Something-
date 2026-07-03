// Live power meter: total draw + a per-room bar breakdown.
// A room's theoretical max = sum of every device's rated wattage (all ON).
function roomMaxWatts(room) {
  return room.devices.reduce((sum, d) => sum + d.watts, 0)
}

export default function PowerBreakdown({ usage, rooms }) {
  return (
    <div className="card power-card">
      <h2>Power Consumption</h2>

      <div className="power-total">
        <span className="power-total-value">{usage.total_watts}</span>
        <span className="power-total-unit">Watts now</span>
      </div>

      <div className="power-bars">
        {rooms.map((room) => {
          const pct = Math.round((room.power / roomMaxWatts(room)) * 100)
          return (
            <div key={room.room} className="power-bar-row">
              <div className="power-bar-label">
                <span>{room.room_name}</span>
                <span className="power-bar-watts">{room.power} W</span>
              </div>
              <div className="power-bar-track">
                <div
                  className="power-bar-fill"
                  style={{ width: `${pct}%` }}
                  data-level={pct > 80 ? 'high' : pct > 40 ? 'mid' : 'low'}
                />
              </div>
            </div>
          )
        })}
      </div>

      <div className="power-footer">
        Estimated energy today: <strong>{usage.today_kwh} kWh</strong>
      </div>
    </div>
  )
}
