FROM ghcr.io/puppeteer/puppeteer:latest

USER root
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

# Environment variable for Render
ENV PORT=3000

EXPOSE 3000
CMD ["npm", "start"]
