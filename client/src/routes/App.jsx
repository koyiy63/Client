import React from 'react'
import { Link, Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b bg-white">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="font-semibold text-lg">YT Share Portal</Link>
          <nav className="text-sm space-x-4">
            <Link className="hover:underline" to="/">Home</Link>
            <Link className="hover:underline" to="/terms">Terms</Link>
            <a className="hover:underline" href="https://policies.google.com/terms" target="_blank" rel="noreferrer">YouTube Terms</a>
          </nav>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="border-t bg-white">
        <div className="max-w-5xl mx-auto px-4 py-6 text-xs text-gray-500">
          Built for compliant sharing and promotion. No automation of views.
        </div>
      </footer>
    </div>
  )
}