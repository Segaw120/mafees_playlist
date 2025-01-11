# Use multi-stage build
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /app/frontend

# Install dependencies first (better layer caching)
COPY frontend/mini-project/package*.json ./
RUN npm cache clean --force && \
    npm install

# Copy frontend source
COPY frontend/mini-project/ ./

# Set environment variables for Next.js
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

# Build the application
RUN npm run build

# Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3-distutils \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy frontend build
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package*.json /app/frontend/
COPY --from=frontend-builder /app/frontend/node_modules /app/frontend/node_modules

# Set up backend
WORKDIR /app/backend
COPY backend/rss_polling/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/rss_polling/src/ ./src/

# Create logs directory
RUN mkdir -p logs

# Copy start script
COPY start.sh /app/
RUN chmod +x /app/start.sh

WORKDIR /app
CMD ["/app/start.sh"]