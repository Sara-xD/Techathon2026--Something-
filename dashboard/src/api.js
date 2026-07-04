// Where the backend lives. Resolution order:
//   1. VITE_API_BASE (explicit override, e.g. a separately-hosted backend)
//   2. In a production build, the page's own origin -- the backend serves this
//      bundle, so REST + WebSocket are same-origin and wss "just works".
//   3. In local dev (vite on :5173), the backend on :8000.
export const API_BASE =
  import.meta.env.VITE_API_BASE ||
  (import.meta.env.PROD && typeof window !== 'undefined'
    ? window.location.origin
    : 'http://localhost:8000')

export async function toggleDevice(id) {
  try {
    await fetch(`${API_BASE}/api/devices/${id}/toggle`, { method: 'POST' })
    // No local state update needed -- the backend broadcasts the new snapshot
    // over the WebSocket, which re-renders every client.
  } catch (err) {
    console.error('toggle failed', err)
  }
}
