# Dockerfile for SvelteKit Application

# ---- Base Node ----
FROM node:18-alpine AS base
WORKDIR /app

# ---- Dependencies ----
FROM base AS deps
COPY package.json package-lock.json* ./
RUN npm install

# ---- Builder ----
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Build the SvelteKit app
RUN npm run build

# ---- Runner ----
FROM base AS runner
ENV NODE_ENV=production
# Copy built assets and necessary files
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .

# Expose the port the app will run on
EXPOSE 3000

# The command to start the Node.js server produced by adapter-node
CMD ["node", "build"]