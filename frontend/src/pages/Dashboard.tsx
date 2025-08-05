import { useEffect, useState } from 'react'
import MetricsCard from '@/components/MetricsCard'
import SentimentRow from '@/components/SentimentRow'
import { fetchWithToken } from '@/services/api'

interface Funnel {
  impressions: number
  clicks: number
  signups: number
  purchases: number
}

interface Mention {
  id: number
  text: string
  score: number
  platform: string
}

export default function Dashboard() {
  const [funnel, setFunnel] = useState<Funnel | null>(null)
  const [mentions, setMentions] = useState<Mention[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    fetchWithToken(token, '/analytics/funnel').then(setFunnel)
    fetchWithToken(token, '/listening/analyze').then((data) => setMentions(data.mentions || []))
  }, [])

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <MetricsCard title="CTR" value={funnel ? (funnel.clicks / funnel.impressions).toFixed(2) : '--'} />
        <MetricsCard title="ROI" value="--" />
        <MetricsCard title="CPA" value="--" />
      </div>
      <section className="rounded bg-[#1f2030] p-4">
        <h3 className="mb-2 font-heebo text-lg">Sentiment Feed</h3>
        <div className="max-h-64 overflow-y-auto">
          {mentions.map((m) => (
            <SentimentRow key={m.id} text={m.text} score={m.score} platform={m.platform} />
          ))}
        </div>
      </section>
    </div>
  )
}
