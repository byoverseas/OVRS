import { motion } from 'framer-motion'

type Props = {
  title: string
  value: string
}

export default function MetricsCard({ title, value }: Props) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, boxShadow: '0 0 8px #67F7D0' }}
      className="btn-glow rounded-lg bg-[#1f2030] p-4"
    >
      <h3 className="font-heebo text-sm uppercase text-accent">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
    </motion.div>
  )
}
