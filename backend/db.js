const { join } = require('path');

const USE_KV = !!process.env.KV_REST_API_URL;
const defaultData = () => ({ users: [], orders: [], wallet_transactions: [] });

let lowdb = null;
let kv = null;
let kvCache = null;

if (!USE_KV) {
  const { Low } = require('lowdb');
  const { JSONFile } = require('lowdb/node');
  const file = join(__dirname, 'cafeholic.json');
  lowdb = new Low(new JSONFile(file), defaultData());
}

async function ensureLoaded() {
  if (USE_KV) {
    if (!kv) {
      const { kv: kvClient } = require('@vercel/kv');
      kv = kvClient;
    }
    if (kvCache === null) {
      kvCache = await kv.get('cafeholic:data');
      if (!kvCache || !Array.isArray(kvCache.users)) kvCache = defaultData();
    }
    return;
  }
  await lowdb.read();
  if (!lowdb.data || !Array.isArray(lowdb.data.users)) {
    lowdb.data = defaultData();
    await lowdb.write();
  }
}

function getData() {
  if (USE_KV) return kvCache;
  return lowdb.data;
}

function getUsers() {
  return getData().users;
}
function getOrders() {
  return getData().orders;
}
function getWalletTransactions() {
  return getData().wallet_transactions;
}

function findUserByEmail(email) {
  return getUsers().find(u => u.email === email.toLowerCase());
}
function findUserById(id) {
  return getUsers().find(u => u.id === id);
}

function createUser({ name, email, college_id, password_hash, wallet_balance }) {
  const users = getUsers();
  const id = users.length ? Math.max(...users.map(u => u.id)) + 1 : 1;
  const user = {
    id,
    name,
    email: email.toLowerCase(),
    college_id,
    password_hash,
    wallet_balance,
    created_at: new Date().toISOString()
  };
  users.push(user);
  return user;
}

function updateUserWallet(userId, balance) {
  const u = findUserById(userId);
  if (u) u.wallet_balance = balance;
  return u;
}

function createOrder({ user_id, total_amount, payment_method, items_json, buyer_name, buyer_phone, buyer_table }) {
  const orders = getOrders();
  const id = orders.length ? Math.max(...orders.map(o => o.id)) + 1 : 1;
  const order = {
    id,
    user_id,
    total_amount,
    payment_method,
    items_json,
    buyer_name: buyer_name || '',
    buyer_phone: buyer_phone || '',
    buyer_table: buyer_table || '',
    created_at: new Date().toISOString()
  };
  orders.push(order);
  return order;
}

function createWalletTransaction({ user_id, amount, type, description }) {
  const tx = getWalletTransactions();
  const id = tx.length ? Math.max(...tx.map(t => t.id)) + 1 : 1;
  const tr = { id, user_id, amount, type, description: description || '', created_at: new Date().toISOString() };
  tx.push(tr);
  return tr;
}

async function write() {
  if (USE_KV) {
    await kv.set('cafeholic:data', kvCache);
    return;
  }
  await lowdb.write();
}

async function init() {
  await ensureLoaded();
}

module.exports = {
  init,
  ensureLoaded,
  findUserByEmail,
  findUserById,
  createUser,
  updateUserWallet,
  createOrder,
  createWalletTransaction,
  write
};
