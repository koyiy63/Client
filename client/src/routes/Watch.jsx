import React, { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'

function extractYouTubeId(url) {
  try {
    const u = new URL(url)
    if (u.hostname === 'youtu.be') return u.pathname.slice(1)
    if (u.searchParams.get('v')) return u.searchParams.get('v')
    const m = u.pathname.match(/\/embed\/([\w-]{5,})/)
    if (m) return m[1]
    return ''
  } catch {
    return ''
  }
}

export default function Watch() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [webhookUrl, setWebhookUrl] = useState('')
  const [announcing, setAnnouncing] = useState(false)

  useEffect(() => {
    let isMounted = true
    async function load() {
      try {
        const res = await fetch(`/api/videos/${id}`)
        const json = await res.json()
        if (!res.ok) throw new Error(json.error || 'Failed')
        if (isMounted) setData(json)
      } catch (e) {
        setError(e.message)
      }
    }
    load()
    return () => { isMounted = false }
  }, [id])

  useEffect(() => {
    fetch(`/api/videos/${id}/visit`, { method: 'POST' }).catch(() => {})
  }, [id])

  const videoId = useMemo(() => (data ? extractYouTubeId(data.url) : ''), [data])
  const watchUrl = `${window.location.origin}/watch/${id}`

  async function announce() {
    setAnnouncing(true)
    try {
      const res = await fetch(`/api/videos/${id}/announce`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ webhookUrl, publicBaseUrl: window.location.origin })
      })
      const json = await res.json()
      if (!res.ok) throw new Error(json.error || 'Failed')
      alert('Announcement sent')
    } catch (e) {
      alert(e.message)
    } finally {
      setAnnouncing(false)
    }
  }

  if (error) return <div className="text-red-600">{error}</div>
  if (!data) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold">{data.title || 'YouTube Video'}</h1>
        {data.author_name && <div className="text-gray-600">by {data.author_name}</div>}
        <div className="text-sm text-gray-500">Visits (on this site): {data.visitCount}</div>
      </div>
      <div className="aspect-video w-full bg-black rounded overflow-hidden">
        {videoId ? (
          <iframe
            className="w-full h-full"
            src={`https://www.youtube.com/embed/${videoId}`}
            title={data.title || 'YouTube video player'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          />
        ) : (
          <div className="text-white p-4">Unable to determine video embed.</div>
        )}
      </div>

      <div className="bg-white border rounded p-4 space-y-3">
        <div className="font-medium">Share</div>
        <div className="flex gap-2 items-center">
          <input readOnly value={watchUrl} className="flex-1 border rounded px-3 py-2" />
          <button className="bg-gray-800 text-white px-3 py-2 rounded" onClick={() => navigator.clipboard.writeText(watchUrl)}>Copy</button>
        </div>
        <div className="flex gap-2">
          <a className="text-sm text-blue-600 underline" target="_blank" rel="noreferrer" href={`https://twitter.com/intent/tweet?text=${encodeURIComponent('Check this out!')}&url=${encodeURIComponent(watchUrl)}`}>Share on Twitter/X</a>
          <a className="text-sm text-blue-600 underline" target="_blank" rel="noreferrer" href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(watchUrl)}`}>Share on Facebook</a>
        </div>
      </div>

      <div className="bg-white border rounded p-4 space-y-3">
        <div className="font-medium">Announce to Discord</div>
        <input
          type="url"
          placeholder="Discord Webhook URL"
          value={webhookUrl}
          onChange={(e) => setWebhookUrl(e.target.value)}
          className="w-full border rounded px-3 py-2"
        />
        <button disabled={!webhookUrl || announcing} className="bg-indigo-600 text-white px-4 py-2 rounded disabled:opacity-50" onClick={announce}>
          {announcing ? 'Sending...' : 'Send Announcement'}
        </button>
      </div>

      <div className="text-xs text-gray-500">This site does not automate views or interactions. It only helps you share your video.</div>
    </div>
  )
}