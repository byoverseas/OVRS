import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '@/services/api'
import { Button } from '@/components/ui/button'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const res = await register(email, password)
    if (res.id) {
      navigate('/login')
    }
  }

  return (
    <div className="flex h-full items-center justify-center">
      <form onSubmit={handleSubmit} className="space-y-4 rounded bg-[#1f2030] p-8 shadow-lg">
        <h2 className="mb-4 font-heebo text-xl">Register</h2>
        <input
          className="w-full rounded bg-[#10111a] p-2"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          className="w-full rounded bg-[#10111a] p-2"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit" className="w-full">
          Create account
        </Button>
      </form>
    </div>
  )
}
