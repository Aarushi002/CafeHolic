# Cafeholic Backend

Node.js API for student login, wallet, and orders.

## Setup

```bash
cd backend
npm install
npm start
```

Server runs at **http://localhost:3001** by default. Set `PORT` env var to change.

## API

- **POST /api/auth/register** — Body: `{ name, email, collegeId, password }`. New users get ₹1000 wallet.
- **POST /api/auth/login** — Body: `{ email, password }`. Returns `{ token, user }`.
- **GET /api/user/me** — Header: `Authorization: Bearer <token>`. Returns current user and wallet.
- **GET /api/wallet** — Header: `Authorization: Bearer <token>`. Returns `{ balance }`.
- **POST /api/wallet/add** — Header: `Authorization: Bearer <token>`. Body: `{ amount }`. Adds to wallet (simulated).
- **POST /api/orders** — Header: `Authorization: Bearer <token>`. Body: `{ items, total, paymentMethod, buyerName, buyerPhone, buyerTable }`. If `paymentMethod === 'wallet'`, amount is deducted from wallet.

## Frontend

- Login page: `htmlcodes/login.html`. After login, token and user are stored in `localStorage` under `cafeholic-auth`.
- Index and menu pages show **Wallet: ₹X** in the nav when logged in, and **Login** when not.
- Orders require login. Payment options: Wallet, UPI, Card, Cash. Wallet balance is deducted on the server when paying with wallet.

## Database

JSON file: `backend/cafeholic.json` (created on first run). Collections: `users`, `orders`, `wallet_transactions`. Uses lowdb (no native build required).

---

## Deployment

### 1. Vercel (with Redis/KV for data)

You can deploy the backend to Vercel. The app runs as a serverless function and needs **Vercel KV** (or another Redis from the Vercel marketplace) for persistent storage.

**Steps:**

1. Push the repo to **GitHub** and import it in [vercel.com](https://vercel.com) → **Add New Project**.
2. **Root Directory**: leave as the repo root (the project has a root `server.js` that exports the backend).
3. **Environment variables** (Project → Settings → Environment Variables):
   - `JWT_SECRET` = a long random string (e.g. from `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`).
4. **Add a database**: In the project, go to **Storage** → **Create Database** → choose **KV** (or **Redis** from the marketplace). Connect it to the project so `KV_REST_API_URL` and `KV_REST_API_TOKEN` are set.
5. Deploy. The API will be at `https://your-project.vercel.app`. Use this URL as `CAFEHOLIC_API_BASE` in the frontend.

**Local dev** is unchanged: run `cd backend && npm start`; it uses the JSON file. On Vercel, when `KV_REST_API_URL` is set, the backend uses KV automatically.

### 2. Railway

1. Push your code to **GitHub** (if not already).
2. Go to [railway.app](https://railway.app) → **Start a New Project** → **Deploy from GitHub**.
3. Select your repo and set **Root Directory** to `backend` (or deploy the whole repo and set it in settings).
4. Add **Variables** in the dashboard:
   - `JWT_SECRET` = a long random string (e.g. from `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`).
5. Railway sets `PORT` automatically. Deploy; it will run `npm install` and `npm start`.
6. Use the generated URL (e.g. `https://your-app.up.railway.app`) as your API base.

**Note:** On Railway’s free tier the filesystem can be ephemeral, so `cafeholic.json` may reset on redeploy. For persistent data, add a **Volume** and point the app to store the DB file there (or move to a real DB later).

### 3. Render

1. [render.com](https://render.com) → **New** → **Web Service**.
2. Connect GitHub and select the repo. Set **Root Directory** to `backend`.
3. **Build:** `npm install`  
   **Start:** `npm start`
4. **Environment:** Add `JWT_SECRET` (long random string).
5. Deploy. Render sets `PORT`; use the service URL as your API base.

Same caveat: free tier has ephemeral disk; data may not persist across deploys unless you use a persistent disk add-on.

### 4. VPS (DigitalOcean, Linode, etc.)

1. Create a small Linux server (e.g. Ubuntu).
2. Install Node.js (e.g. `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -` then `sudo apt install -y nodejs`).
3. Clone your repo and run:
   ```bash
   cd backend
   npm install
   ```
4. Set env and run with **PM2** so it restarts on reboot:
   ```bash
   npm install -g pm2
   export JWT_SECRET="your-long-secret"
   pm2 start server.js --name cafeholic-api
   pm2 save && pm2 startup
   ```
5. Put **Nginx** (or Caddy) in front as reverse proxy and add SSL (e.g. Let’s Encrypt).

Data persists because the server has a real disk; `cafeholic.json` stays in `backend/`.

---

### After deploying the backend

Point the frontend to your deployed API:

- Either set **before** your scripts load:
  ```html
  <script>window.CAFEHOLIC_API_BASE = 'https://your-api-url.up.railway.app';</script>
  ```
- Or change `API_BASE` in `htmlcodes/jscodes/script.js` and in `htmlcodes/online-restaurant-orderjquery/dist/menu.js` to your API URL.

Then deploy the frontend (e.g. **Netlify**, **Vercel**, or **GitHub Pages**) so the site is served over HTTPS and can call your API without CORS issues (if you restrict CORS later, allow your frontend origin).
