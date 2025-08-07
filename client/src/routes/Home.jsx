import React, { useState } from 'react'

export default function Home() {
  const [url, setUrl] = useState('')
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState('')
  const [createdId, setCreatedId] = useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    setCreating(true)
    try {
      const res = await fetch('/api/videos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed')
      setCreatedId(data.id)
    } catch (e) {
      setError(e.message)
    } finally {
      setCreating(false)
    }
  }

  const watchLink = createdId ? `${window.location.origin}/watch/${createdId}` : ''

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Share a YouTube Video</h1>
      <form onSubmit={onSubmit} className="bg-white rounded-lg border p-4 space-y-3 max-w-2xl">
        <label className="text-sm font-medium">YouTube URL</label>
        <input
          type="url"
          required
          placeholder="https://www.youtube.com/watch?v=..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full border rounded px-3 py-2 focus:outline-none focus:ring"
        />
        <div className="flex items-center gap-3">
          <button disabled={creating} className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50">
            {creating ? 'Creating...' : 'Create Watch Page'}
          </button>
          {error && <span className="text-red-600 text-sm">{error}</span>}
        </div>
      </form>

      {watchLink && (
        <div className="bg-white rounded-lg border p-4 space-y-3 max-w-2xl">
          <div className="font-medium">Your shareable watch link</div>
          <div className="flex gap-2 items-center">
            <input readOnly value={watchLink} className="flex-1 border rounded px-3 py-2" />
            <button
              className="bg-gray-800 text-white px-3 py-2 rounded"
              onClick={() => navigator.clipboard.writeText(watchLink)}
            >Copy</button>
          </div>
          <div className="text-xs text-gray-500">This page embeds the video and tracks visits on this site only.</div>
        </div>
      )}
    </div>
  )
}