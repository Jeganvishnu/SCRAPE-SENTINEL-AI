# Scrape Sentinel AI — Vercel Deployment Guide

This project is fully configured for seamless, one-click deployment on **Vercel** as a unified full-stack application (FastAPI Python backend + React Vite frontend).

---

## 1. Automated Architecture on Vercel

- **Frontend**: Vite React SPA served statically from `frontend/dist` with client-side routing rewrites.
- **Backend API**: FastAPI Python application executed as Vercel Serverless Functions via `/api/index.py`.
- **API Rewrites**: Endpoints (`/health`, `/sources`, `/runs`, `/failures`, `/metrics`, `/ai`, `/docs`) are automatically proxied to the Python serverless runtime.

---

## 2. Environment Variables Required on Vercel

In your **Vercel Project Settings $\rightarrow$ Environment Variables**, configure the following keys:

| Environment Variable | Description | Example Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | Supabase PostgreSQL Connection String | `postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres` |
| `BRIGHTDATA_API_KEY` | Bright Data API Key | `your_bright_data_api_key` |
| `BRIGHT_DATA_USERNAME` | Bright Data Account Email | `your_email@example.com` |
| `BRIGHT_DATA_COLLECTOR_ID` | Scraper Studio Collector ID | `c_mt46lngz2asqzj8tkj` |
| `AI_PROVIDER` | AI provider (`google`, `openai`, `mock`) | `google` |
| `AI_MODEL` | Gemini LLM model | `gemini-1.5-flash` |
| `AI_API_KEY` | Google Gemini API Key | `your_gemini_api_key` |
| `AI_ENABLED` | Enable AI Intelligence layer | `true` |

---

## 3. Option A: Deploy via GitHub (Recommended)

1. Push code to your GitHub repository: `https://github.com/Jeganvishnu/SCRAPE-SENTINEL-AI`.
2. Log into [Vercel Dashboard](https://vercel.com).
3. Click **"Add New..." $\rightarrow$ "Project"**.
4. Import `Jeganvishnu/SCRAPE-SENTINEL-AI`.
5. Keep default settings (Vercel automatically detects `vercel.json`).
6. Add your **Environment Variables** (listed above).
7. Click **"Deploy"**.

---

## 4. Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Log in to Vercel account
vercel login

# Deploy to production
vercel --prod
```
