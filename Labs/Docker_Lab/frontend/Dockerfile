# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

COPY src/ ./src/


# Stage 2: Production with lightweight server
FROM node:20-alpine AS production

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/src ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]