import { useEffect, useState } from 'react'
import { fetchWithToken } from '@/services/api'
import { Button } from '@/components/ui/button'

interface SettingsForm {
  jwt_expiration_hours: number
  bcrypt_salt_rounds: number
  negative_sentiment_threshold: number
  enable_logging: boolean
  enable_background_tasks: boolean
  default_export_format: string
}

export default function AdminSettings() {
  const [form, setForm] = useState<SettingsForm | null>(null)
  const [msg, setMsg] = useState('')
  const [unauth, setUnauth] = useState(false)
  const role = localStorage.getItem('role')

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    if (role !== 'admin') {
      setUnauth(true)
      return
    }
    fetchWithToken(token, '/op/settings').then((data) => {
      if (data.detail) setUnauth(true)
      else setForm(data)
    })
  }, [role])

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value, type, checked } = e.target
    const parsed = type === 'number' ? Number(value) : value
    setForm((prev) => (prev ? { ...prev, [name]: type === 'checkbox' ? checked : parsed } : prev))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const token = localStorage.getItem('token') || ''
    await fetchWithToken(token, '/op/settings', {
      method: 'POST',
      body: JSON.stringify(form)
    })
    setMsg('Settings updated')
    const data = await fetchWithToken(token, '/op/settings')
    setForm(data)
    setTimeout(() => setMsg(''), 2000)
  }

  if (unauth) return <div className="p-4">You are not authorized</div>
  if (!form) return null

  return (
    <div className="max-w-md space-y-4">
      {msg && <div className="rounded bg-green-600 p-2">{msg}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm">JWT Expiration (hours)</label>
          <input
            type="number"
            name="jwt_expiration_hours"
            value={form.jwt_expiration_hours}
            onChange={handleChange}
            className="w-full rounded bg-[#10111a] p-2"
          />
        </div>
        <div>
          <label className="block text-sm">Bcrypt Rounds</label>
          <input
            type="number"
            name="bcrypt_salt_rounds"
            value={form.bcrypt_salt_rounds}
            onChange={handleChange}
            className="w-full rounded bg-[#10111a] p-2"
          />
        </div>
        <div>
          <label className="block text-sm">Negative Threshold</label>
          <input
            type="number"
            name="negative_sentiment_threshold"
            value={form.negative_sentiment_threshold}
            onChange={handleChange}
            className="w-full rounded bg-[#10111a] p-2"
          />
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="enable_logging"
            checked={form.enable_logging}
            onChange={handleChange}
          />
          <span>Enable Logging</span>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="enable_background_tasks"
            checked={form.enable_background_tasks}
            onChange={handleChange}
          />
          <span>Enable Background Tasks</span>
        </div>
        <div>
          <label className="block text-sm">Default Export Format</label>
          <select
            name="default_export_format"
            value={form.default_export_format}
            onChange={handleChange}
            className="w-full rounded bg-[#10111a] p-2"
          >
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
          </select>
        </div>
        <Button type="submit" className="w-full">
          Save
        </Button>
      </form>
    </div>
  )
}
