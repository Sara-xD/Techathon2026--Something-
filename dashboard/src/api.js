// REST helpers for the dashboard. Live state still arrives over the WebSocket;
// this is only for manual actions like toggling a device.
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function toggleDevice(id) {
  try {
    await fetch(`${API_BASE}/api/devices/${id}/toggle`, { method: 'POST' })
    // No local state update needed — the backend broadcasts the new snapshot
    // over the WebSocket, which re-renders every client.
  } catch (err) {
    console.error('toggle failed', err)
  }
}
