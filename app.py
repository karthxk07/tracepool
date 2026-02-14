from flask import Flask, request, render_template_string
from supabase import create_client, Client
import os
from datetime import datetime
import socket

app = Flask(__name__)

# Initialize Supabase client
# Set these environment variables before running:
# SUPABASE_URL and SUPABASE_KEY
supabase_url = os.environ.get("SUPABASE_URL", "")
supabase_key = os.environ.get("SUPABASE_KEY", "")

supabase: Client = None
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

# HTML template with retro aesthetic rickroll
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>You've Been Logged</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'VT323', monospace;
            background: #000;
            color: #00ff00;
            overflow: hidden;
            cursor: crosshair;
        }

        .scanlines {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to bottom,
                transparent 50%,
                rgba(0, 255, 0, 0.05) 50%
            );
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 999;
            animation: flicker 0.15s infinite;
        }

        @keyframes flicker {
            0%, 100% { opacity: 0.95; }
            50% { opacity: 1; }
        }

        .crt-effect {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
            pointer-events: none;
            z-index: 998;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        .glitch {
            font-family: 'Press Start 2P', cursive;
            font-size: clamp(1.5rem, 5vw, 3rem);
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            text-shadow: 
                2px 2px #ff00ff,
                -2px -2px #00ffff;
            animation: glitch 1s infinite;
        }

        @keyframes glitch {
            0%, 100% {
                transform: translate(0);
            }
            20% {
                transform: translate(-2px, 2px);
            }
            40% {
                transform: translate(-2px, -2px);
            }
            60% {
                transform: translate(2px, 2px);
            }
            80% {
                transform: translate(2px, -2px);
            }
        }

        .video-container {
            position: relative;
            width: min(800px, 90vw);
            aspect-ratio: 16/9;
            border: 4px solid #00ff00;
            box-shadow: 
                0 0 20px #00ff00,
                inset 0 0 20px rgba(0, 255, 0, 0.2);
            margin-bottom: 2rem;
            animation: borderPulse 2s infinite;
        }

        @keyframes borderPulse {
            0%, 100% {
                box-shadow: 
                    0 0 20px #00ff00,
                    inset 0 0 20px rgba(0, 255, 0, 0.2);
            }
            50% {
                box-shadow: 
                    0 0 40px #00ff00,
                    inset 0 0 40px rgba(0, 255, 0, 0.4);
            }
        }

        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .terminal-text {
            font-size: clamp(1rem, 2.5vw, 1.5rem);
            text-align: center;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            animation: typing 2s steps(40) 1;
        }

        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        .blink {
            animation: blink 1s step-end infinite;
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }

        .info-box {
            margin-top: 2rem;
            padding: 1.5rem;
            border: 2px solid #00ff00;
            background: rgba(0, 255, 0, 0.05);
            max-width: 600px;
            text-align: left;
            font-size: clamp(0.9rem, 2vw, 1.2rem);
        }

        .info-box p {
            margin: 0.5rem 0;
        }

        .ascii-art {
            font-size: clamp(0.5rem, 1vw, 0.8rem);
            line-height: 1;
            margin-bottom: 1rem;
            white-space: pre;
            color: #00ff00;
        }

        @media (max-width: 768px) {
            .glitch {
                font-size: 1.2rem;
            }
            .ascii-art {
                font-size: 0.4rem;
            }
        }
    </style>
</head>
<body>
    <div class="scanlines"></div>
    <div class="crt-effect"></div>
    
    <div class="container">
        <div class="ascii-art">
 ███▄    █ ▓█████ ██▒   █▓▓█████  ██▀███      ▄████  ▒█████   ███▄    █  ███▄    █ ▄▄▄      
 ██ ▀█   █ ▓█   ▀▓██░   █▒▓█   ▀ ▓██ ▒ ██▒   ██▒ ▀█▒▒██▒  ██▒ ██ ▀█   █  ██ ▀█   █▒████▄    
▓██  ▀█ ██▒▒███   ▓██  █▒░▒███   ▓██ ░▄█ ▒  ▒██░▄▄▄░▒██░  ██▒▓██  ▀█ ██▒▓██  ▀█ ██▒██  ▀█▄  
▓██▒  ▐▌██▒▒▓█  ▄  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄    ░▓█  ██▓▒██   ██░▓██▒  ▐▌██▒▓██▒  ▐▌██░██▄▄▄▄██ 
▒██░   ▓██░░▒████▒  ▒▀█░  ░▒████▒░██▓ ▒██▒  ░▒▓███▀▒░ ████▓▒░▒██░   ▓██░▒██░   ▓██░▓█   ▓██▒
░ ▒░   ▒ ▒ ░░ ▒░ ░  ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░   ░▒   ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ▒▒   ▓▒█░
░ ░░   ░ ▒░ ░ ░  ░  ░ ░░   ░ ░  ░  ░▒ ░ ▒░    ░   ░   ░ ▒ ▒░ ░ ░░   ░ ▒░░ ░░   ░ ▒░ ▒   ▒▒ ░
   ░   ░ ░    ░       ░░     ░     ░░   ░   ░ ░   ░ ░ ░ ░ ▒     ░   ░ ░    ░   ░ ░  ░   ▒   
         ░    ░  ░     ░     ░  ░   ░             ░     ░ ░           ░          ░      ░  ░
                      ░                                                                      
        </div>

        <h1 class="glitch">NEVER GONNA GIVE YOU UP</h1>
        
        <div class="video-container">
            <iframe 
                src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&controls=1" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>

        <div class="terminal-text">
            <p>&gt; SYSTEM ALERT: Your IP address has been logged<span class="blink">_</span></p>
            <p>&gt; Thanks for visiting! You just got rickrolled 😎</p>
        </div>

        <div class="info-box">
            <p>&gt; IP: {{ ip_address }}</p>
            <p>&gt; User-Agent: {{ user_agent }}</p>
            <p>&gt; Timestamp: {{ timestamp }}</p>
            <p>&gt; Status: LOGGED TO DATABASE ✓</p>
        </div>
    </div>

    <script>
        // Easter egg: Konami code
        let konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
        let konamiIndex = 0;

        document.addEventListener('keydown', (e) => {
            if (e.key === konamiCode[konamiIndex]) {
                konamiIndex++;
                if (konamiIndex === konamiCode.length) {
                    document.body.style.background = 'linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff00ff)';
                    document.body.style.backgroundSize = '400% 400%';
                    document.body.style.animation = 'gradient 3s ease infinite';
                    konamiIndex = 0;
                }
            } else {
                konamiIndex = 0;
            }
        });

        const style = document.createElement('style');
        style.textContent = `
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

def get_client_ip():
    """Get the real client IP, accounting for proxies"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

def log_to_supabase(ip_address, user_agent, referer):
    """Log visitor data to Supabase"""
    if not supabase:
        print("⚠️  Supabase not configured. Set SUPABASE_URL and SUPABASE_KEY environment variables.")
        return False
    
    try:
        data = {
            "ip_address": ip_address,
            "user_agent": user_agent,
            "referer": referer,
            "timestamp": datetime.utcnow().isoformat(),
            "hostname": socket.getfqdn() if socket.getfqdn() else "unknown"
        }
        
        response = supabase.table("ip_logs").insert(data).execute()
        print(f"✅ Logged: {ip_address}")
        return True
    except Exception as e:
        print(f"❌ Error logging to Supabase: {e}")
        return False

@app.route('/')
def index():
    # Get visitor information
    ip_address = get_client_ip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')
    
    # Log to Supabase
    log_to_supabase(ip_address, user_agent, referer)
    
    # Render the rickroll page
    return render_template_string(
        HTML_TEMPLATE,
        ip_address=ip_address,
        user_agent=user_agent,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "supabase_configured": supabase is not None
    }, 200

if __name__ == '__main__':
    print("🚀 Starting IP Logger Server...")
    print("📊 Make sure to set SUPABASE_URL and SUPABASE_KEY environment variables")
    print("🎵 Get ready to rickroll some visitors!")
    app.run(host='0.0.0.0', port=5000, debug=False)
