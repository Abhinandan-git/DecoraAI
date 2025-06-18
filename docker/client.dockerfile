# Install dependencies
FROM node:20-alpine AS builder

WORKDIR /app

COPY ./ ./

# Build Next.js
RUN npm install && npm run build

# Serving with distroless image
FROM node:20-alpine AS runner

WORKDIR /app

COPY --from=builder /app ./

EXPOSE 3000

CMD ["npm", "run", "start"]