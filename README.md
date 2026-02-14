# 🎵 IP Logger with Rickroll

A fun Flask app that logs visitor IPs to Supabase and rewards them with a retro-styled rickroll experience!

## Features

- 🎨 Retro CRT terminal aesthetic with glitch effects
- 🎵 Auto-playing rickroll video
- 📊 Logs IP, user agent, referer, and timestamp to Supabase
- 🔒 Handles proxy headers (X-Forwarded-For, X-Real-IP)
- 🎮 Hidden Konami code easter egg
- 📱 Fully responsive design

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Go to [Supabase](https://supabase.com) and create a new project
2. In the SQL Editor, run the contents of `supabase_setup.sql`
3. Get your project credentials:
   - Go to Project Settings → API
   - Copy the **Project URL** (SUPABASE_URL)
   - Copy the **anon/public key** (SUPABASE_KEY)

### 3. Set Environment Variables

Create a `.env` file (copy from `env.example`):

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

Or export them directly:

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-key-here"
```

### 4. Run the App

**Development:**
```bash
python app.py
```

**Production (with Gunicorn):**
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

Visit `http://localhost:5000` to see it in action!

## Hosting Options

### Option 1: **Render.com** (Recommended - Free Tier Available)

**Pros:** Free tier, easy setup, custom domains, auto-deployment from GitHub
**Steps:**
1. Push your code to GitHub
2. Go to [Render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - Add environment variables (SUPABASE_URL, SUPABASE_KEY)
6. Deploy!

**Custom Domain with FreeDNS:**
- In Render, go to Settings → Custom Domain
- Add your FreeDNS subdomain (e.g., `yourname.freeDNS.org`)
- Render will give you a CNAME target
- In FreeDNS, create a CNAME record pointing to the Render URL

### Option 2: **Railway.app** (Free $5 credit/month)

**Pros:** Easy, great for Python apps, auto-scaling
**Steps:**
1. Push code to GitHub
2. Sign up at [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Add environment variables in Variables tab
5. Railway auto-detects Python and deploys

**FreeDNS Setup:**
- Go to Settings → Domains → Custom Domain
- Add your subdomain
- Update FreeDNS with the CNAME record

### Option 3: **PythonAnywhere** (Free tier available)

**Pros:** Simple, Python-focused, free HTTPS
**Steps:**
1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your files via Files tab
3. Go to Web tab → Add a new web app
4. Choose Flask and Python version
5. Point to your `app.py` file
6. Add environment variables in the web app config

**FreeDNS Setup:**
- PythonAnywhere requires paid plan for custom domains
- Free tier gets `username.pythonanywhere.com`

### Option 4: **Fly.io** (Free tier available)

**Pros:** Edge deployment, fast globally
**Steps:**
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Login: `flyctl auth login`
3. Create `fly.toml`:

```toml
app = "your-app-name"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
  
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

4. Deploy: `flyctl launch`
5. Set secrets: `flyctl secrets set SUPABASE_URL=... SUPABASE_KEY=...`

**FreeDNS Setup:**
- Add custom domain: `flyctl certs add yourname.freeDNS.org`
- Update FreeDNS with the A record Fly.io provides

### Option 5: **Vercel** (with Serverless Functions)

**Pros:** Free, fast CDN, auto-deployment
**Note:** Requires converting to serverless format
**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. Deploy: `vercel --prod`
4. Add environment variables in Vercel dashboard

## FreeDNS Configuration

Your FreeDNS subdomain can be configured once you have a hosting provider:

1. Log in to [FreeDNS](https://freedns.afraid.org)
2. Go to "Subdomains" → Edit your subdomain
3. Choose record type based on your host:
   - **CNAME**: For Render, Railway, Heroku (point to their URL)
   - **A Record**: For Fly.io, VPS (point to IP address)
4. Set the target/destination as provided by your hosting service
5. Save and wait for DNS propagation (5-30 minutes)

## Monitoring Your Logs

View logs in Supabase:
1. Go to Table Editor
2. Select `ip_logs` table
3. See all visitor data in real-time

Or query via SQL:
```sql
SELECT * FROM ip_logs ORDER BY timestamp DESC LIMIT 100;
```

## Security Notes

- The `anon` key is safe to use in client-side code
- Row Level Security (RLS) is enabled to protect data
- Never commit your `.env` file to Git
- Add `.env` to `.gitignore`

## Easter Egg

Try entering the Konami Code on the page: ↑ ↑ ↓ ↓ ← → ← → B A

Enjoy rickrolling your visitors! 🎵
