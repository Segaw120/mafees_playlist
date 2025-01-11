import type { Metadata } from 'next';
import React from 'react';

export const metadata: Metadata = {
  title: 'Mafees Playlist',
  description: 'RSS Feed Aggregator with Spotify Integration',
};

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">Mafees Playlist</h1>
        <p className="text-xl mb-4">
          Welcome to Mafees Playlist - Your RSS Feed Aggregator with Spotify Integration
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-4">RSS Feeds</h2>
            <p>Real-time updates from your favorite sources</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-semibold mb-4">Spotify Integration</h2>
            <p>Control your music while staying informed</p>
          </div>
        </div>
      </div>
    </main>
  );
} 