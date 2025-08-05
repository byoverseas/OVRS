import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { subscribeAlerts } from '@/services/api'

export default function Topbar() {
  const [alert, setAlert] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    const ws = subscribeAlerts(token)
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data)
      if (data.level === 'negative') setAlert(true)
    }
    ws.onclose = () => ws.close()
    return () => ws.close()
  }, [])

  return (
    <div className="flex items-center justify-end gap-4 p-4 shadow-md shadow-black/50">
      <motion.span
        animate={{ opacity: alert ? 1 : 0.2 }}
        className="rounded-full bg-red-500 px-2 py-1 text-xs"
      >
        ●
      </motion.span>
      {['settings', 'profile'].map((item) => (
        <motion.button
          key={item}
          whileHover={{ boxShadow: '0 0 8px #67F7D0' }}
          className="btn-glow rounded bg-[#10111a] px-3 py-1"
        >
          {item}
        </motion.button>
      ))}
    </div>
  )
}
