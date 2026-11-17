# ── Frontend Dockerfile (multi-stage) ───────────────────────────────────────
# Stage 1: BUILD
# Node 22 matches the package.json engines requirement (^22.18.0).
# VITE_API_BASE_URL is baked into the bundle at build time.
FROM node:22-alpine AS build

WORKDIR /app

# Install deps
COPY package*.json ./
RUN npm install

# Copy source and build
COPY . .

# Accept the API base URL as a Docker build arg; default to localhost for local dev
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build-only

# Stage 2: SERVE
# nginx:alpine is tiny (~25 MB). We only copy the compiled dist/ folder.
FROM nginx:alpine

# Our SPA config (try_files for Vue Router)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the compiled frontend from stage 1
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
