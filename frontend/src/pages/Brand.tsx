import { useEffect, useState } from 'react'
import SentimentRow from '@/components/SentimentRow'
import { fetchWithToken } from '@/services/api'

export default function Brand() {
  const [mentions, setMentions] = useState<any[]>([])
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    fetchWithToken(token, '/listening/analyze').then((data) => setMentions(data.mentions || []))
  }, [])

  const filtered = mentions.filter((m) =>
    filter === 'all' ? true : m.platform === filter
  )

  return (
    <div className="rounded bg-[#1f2030] p-4">
      <div className="mb-2 flex gap-2">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="rounded bg-[#10111a] p-2"
        >
          <option value="all">All</option>
          <option value="twitter">Twitter</option>
          <option value="facebook">Facebook</option>
        </select>
      </div>
      <div>
        {filtered.map((m) => (
          <SentimentRow key={m.id} text={m.text} score={m.score} platform={m.platform} />
        ))}
      </div>
    </div>
  )
}
