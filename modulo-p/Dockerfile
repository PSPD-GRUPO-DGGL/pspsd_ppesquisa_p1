# Estagio 1: Build
FROM node:20-alpine AS builder
WORKDIR /usr/src/app
COPY modulo-p/package*.json ./
RUN npm ci
COPY modulo-p/ .
COPY proto/ /usr/src/proto/

# Estagio 2: Execucao enxuta
FROM node:20-alpine
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app ./
COPY --from=builder /usr/src/proto /usr/src/proto

ENV PORT=8080 \
    URL_MODULO_A=modulo-a:50051 \
    URL_MODULO_B=modulo-b:50052

EXPOSE 8080
CMD ["node", "src/app.js"]