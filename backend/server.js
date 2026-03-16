const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'cafeholic-secret-change-in-production';
const INITIAL_WALLET = 1000;

app.use(cors({ origin: true, credentials: true }));
app.use(express.json());

// Load DB into memory on each request (required for Vercel KV / serverless)
app.use(async (req, res, next) => {
  try {
    await db.ensureLoaded();
    next();
  } catch (e) {
    next(e);
  }
});

app.get('/', (req, res) => {
  res.json({
    name: 'Cafeholic API',
    message: 'Backend is running. Open the frontend: htmlcodes/index.html (or menu.html) in your browser.',
    endpoints: ['POST /api/auth/register', 'POST /api/auth/login', 'GET /api/user/me', 'GET /api/wallet', 'POST /api/wallet/add', 'POST /api/orders']
  });
});

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  const token = authHeader.slice(7);
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    req.userEmail = decoded.email;
    next();
  } catch (e) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// ----- Auth -----

app.post('/api/auth/register', async (req, res) => {
  const { name, email, collegeId, password } = req.body || {};
  if (!name || !email || !collegeId || !password) {
    return res.status(400).json({ error: 'Name, email, college ID and password are required' });
  }
  if (db.findUserByEmail(email.trim())) {
    return res.status(400).json({ error: 'Email already registered' });
  }
  const password_hash = bcrypt.hashSync(password, 10);
  const user = db.createUser({
    name: name.trim(),
    email: email.trim(),
    college_id: String(collegeId).trim(),
    password_hash,
    wallet_balance: INITIAL_WALLET
  });
  await db.write();
  const token = jwt.sign({ userId: user.id, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
  res.json({
    token,
    user: { id: user.id, name: user.name, email: user.email, collegeId: user.college_id, walletBalance: user.wallet_balance }
  });
});

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }
  const row = db.findUserByEmail(email.trim());
  if (!row || !bcrypt.compareSync(password, row.password_hash)) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }
  const token = jwt.sign({ userId: row.id, email: row.email }, JWT_SECRET, { expiresIn: '7d' });
  res.json({
    token,
    user: {
      id: row.id,
      name: row.name,
      email: row.email,
      collegeId: row.college_id,
      walletBalance: row.wallet_balance
    }
  });
});

app.get('/api/user/me', authMiddleware, (req, res) => {
  const row = db.findUserById(req.userId);
  if (!row) return res.status(404).json({ error: 'User not found' });
  res.json({
    user: {
      id: row.id,
      name: row.name,
      email: row.email,
      collegeId: row.college_id,
      walletBalance: row.wallet_balance
    }
  });
});

// ----- Wallet -----

app.get('/api/wallet', authMiddleware, (req, res) => {
  const row = db.findUserById(req.userId);
  if (!row) return res.status(404).json({ error: 'User not found' });
  res.json({ balance: row.wallet_balance });
});

app.post('/api/wallet/add', authMiddleware, async (req, res) => {
  const amount = parseFloat(req.body.amount);
  if (!Number.isFinite(amount) || amount <= 0) {
    return res.status(400).json({ error: 'Valid positive amount required' });
  }
  const user = db.findUserById(req.userId);
  if (!user) return res.status(404).json({ error: 'User not found' });
  const newBalance = user.wallet_balance + amount;
  db.updateUserWallet(req.userId, newBalance);
  db.createWalletTransaction({ user_id: req.userId, amount, type: 'credit', description: 'Add money' });
  await db.write();
  res.json({ balance: newBalance });
});

// ----- Orders -----

app.post('/api/orders', authMiddleware, async (req, res) => {
  const { items, total, paymentMethod, buyerName, buyerPhone, buyerTable } = req.body || {};
  const totalAmount = parseFloat(total);
  if (!Number.isFinite(totalAmount) || totalAmount <= 0) {
    return res.status(400).json({ error: 'Invalid order total' });
  }
  const user = db.findUserById(req.userId);
  if (!user) return res.status(404).json({ error: 'User not found' });

  if (paymentMethod === 'wallet') {
    if (user.wallet_balance < totalAmount) {
      return res.status(400).json({ error: 'Insufficient wallet balance', balance: user.wallet_balance });
    }
    const newBalance = user.wallet_balance - totalAmount;
    db.updateUserWallet(req.userId, newBalance);
    db.createWalletTransaction({ user_id: req.userId, amount: -totalAmount, type: 'debit', description: 'Order payment' });
  }

  const itemsJson = typeof items === 'string' ? items : JSON.stringify(items || []);
  db.createOrder({
    user_id: req.userId,
    total_amount: totalAmount,
    payment_method: paymentMethod || 'cash',
    items_json: itemsJson,
    buyer_name: buyerName,
    buyer_phone: buyerPhone,
    buyer_table: buyerTable
  });
  await db.write();

  const updated = db.findUserById(req.userId);
  res.json({ success: true, walletBalance: updated.wallet_balance });
});

async function start() {
  await db.init();
  app.listen(PORT, () => {
    console.log('Cafeholic backend running on http://localhost:' + PORT);
  });
}

// Export app for Vercel serverless; run server locally otherwise
if (process.env.VERCEL) {
  module.exports = app;
} else {
  start().catch(err => {
    console.error(err);
    process.exit(1);
  });
}
