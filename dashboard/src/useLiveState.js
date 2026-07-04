import { useEffect, useRef, useState } from 'react'
import { API_BASE } from './api'

// Single source of truth lives in the backend; we just subscribe to its
// WebSocket and render whatever snapshot it pushes. Auto-reconnects so the
// dashboard survives a backend restart during the demo.
const WS_URL = API_BASE.replace(/^http/, 'ws') + '/ws/live'

export function useLiveState() {
  const [state, setState] = useState(null)
  const [connected, setConnected] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    let stopped = false
    let reconnectTimer

    function connect() {
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws
      ws.onopen = () => setConnected(true)
      ws.onmessage = (e) => setState(JSON.parse(e.data))
      ws.onclose = () => {
        setConnected(false)
        if (!stopped) reconnectTimer = setTimeout(connect, 1500)
      }
      ws.onerror = () => ws.close()
    }

    connect()
    return () => {
      stopped = true
      clearTimeout(reconnectTimer)
      wsRef.current?.close()
    }
  }, [])

  return { state, connected }
}
