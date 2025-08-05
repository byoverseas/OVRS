import { useState } from 'react'
import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/brand', label: 'Brand Monitoring' }
]

export default function Sidebar() {
  const [open, setOpen] = useState(true)
  const { pathname } = useLocation()

  return (
    <div className={`bg-[#10111a] text-white transition-all ${open ? 'w-56' : 'w-16'} flex flex-col`}>
      <div className="flex items-center justify-between p-4 font-heebo text-accent">
        <span className="text-xl">OVRS</span>
        <button onClick={() => setOpen(!open)} className="btn-glow">{open ? '<' : '>'}</button>
      </div>
      <nav className="flex-1">
        {navItems.map((item) => (
          <Link key={item.to} to={item.to}>
            <motion.div
              whileHover={{ boxShadow: '0 0 8px #67F7D0' }}
              className={`m-2 rounded px-4 py-2 hover:bg-[#1f2030] ${pathname === item.to ? 'bg-[#1f2030]' : ''}`}
            >
              {item.label}
            </motion.div>
          </Link>
        ))}
      </nav>
    </div>
  )
}
