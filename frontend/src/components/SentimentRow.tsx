type Props = {
  text: string
  score: number
  platform: string
}

export default function SentimentRow({ text, score, platform }: Props) {
  const color = score > 0 ? 'text-green-400' : score < 0 ? 'text-red-400' : 'text-gray-200'

  return (
    <div className="flex items-center justify-between border-b border-white/10 p-2 hover:bg-[#1f2030]">
      <span className="truncate pr-2">[{platform}] {text}</span>
      <span className={color}>{score.toFixed(2)}</span>
    </div>
  )
}
