# Mini Spotify News App

A minimalist web application that combines Spotify playback with a news feed. Built with Next.js, TypeScript, and Tailwind CSS.

## Features

- Spotify Authentication
- Playlist Selection and Playback
- Real-time News Feed with SSE
- Client-side Image Caching
- Responsive Design
- Dark Mode Support

## Prerequisites

- Node.js 18 or later
- Spotify Developer Account
- Spotify Client ID and Secret
- News Feed SSE endpoint

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/api/auth/callback/spotify
```

## Development

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Docker

Build the Docker image:
```bash
docker build -t mini-spotify-app .
```

Run the container:
```bash
docker run -p 3000:3000 \
  -e SPOTIFY_CLIENT_ID=your_spotify_client_id \
  -e SPOTIFY_CLIENT_SECRET=your_spotify_client_secret \
  -e SPOTIFY_REDIRECT_URI=http://localhost:3000/api/auth/callback/spotify \
  mini-spotify-app
```

## Project Structure

```
├── app/                  # Next.js app directory
├── components/          # React components
├── lib/                # Utility functions
├── public/            # Static assets
├── types/            # TypeScript type definitions
└── utils/           # Helper functions
```

## License

MIT 