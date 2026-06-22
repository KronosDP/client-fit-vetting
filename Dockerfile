# Stage 1: Build the React frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Run the FastAPI backend
FROM python:3.11-slim
WORKDIR /app

# Copy python requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend assets from builder stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose port and set production environment variables
ENV PORT=8080
EXPOSE 8080

WORKDIR /app/backend

# Seed database and start uvicorn
CMD ["sh", "-c", "python -m app.seed_dummy && uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
