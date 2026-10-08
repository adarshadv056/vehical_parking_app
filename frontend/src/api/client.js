/**
 * Centralised API client.
 * - Base URL comes from VUE_APP_API_BASE (set at build time via .env)
 * - Attaches JWT from localStorage
 * - Normalises error responses
 * - Returns { data, error } tuples so callers don't need try/catch everywhere
 */

// Vue CLI (webpack) injects process.env.VUE_APP_API_BASE at build time from .env files.
const BASE = (
  (typeof window !== 'undefined' && window.__VUE_APP_API_BASE__) ||
  process.env.VUE_APP_API_BASE ||
  ''
).replace(/\/+$/, '');

if (!BASE && typeof window !== 'undefined') {
  console.warn('[ParkSync API] Warning: VUE_APP_API_BASE is not defined in environment variables.');
}

function authHeaders(extra = {}) {
  const token = localStorage.getItem('token');
  return token
    ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', ...extra }
    : { 'Content-Type': 'application/json', ...extra };
}

async function request(path, options = {}) {
  const url = `${BASE}${path}`;
  const res = await fetch(url, { ...options, headers: authHeaders(options.headers) });
  let payload = null;
  const ct = res.headers.get('content-type');
  if (ct?.includes('application/json')) {
    payload = await res.json().catch(() => null);
  } else if (ct?.startsWith('text/') || ct?.startsWith('image/')) {
    payload = await res.blob();
  }
  if (!res.ok) {
    const msg = payload?.message || res.statusText || 'Request failed';
    return { data: null, error: { status: res.status, message: msg, raw: payload } };
  }
  return { data: payload, error: null };
}

export const api = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
  put: (path, body) => request(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (path) => request(path, { method: 'DELETE' }),
  download: (path) => request(path, { method: 'GET' }),
};

export const auth = {
  login: (email, password) => api.post('/login', { email, password }),
  register: (data) => api.post('/register', data),
  logout: () => { localStorage.removeItem('token'); },
  isAuthenticated: () => !!localStorage.getItem('token'),
  getToken: () => localStorage.getItem('token'),
  getPayload: () => {
    const t = localStorage.getItem('token');
    if (!t) return null;
    try {
      return JSON.parse(atob(t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
    } catch { return null; }
  },
};

export const admin = {
  listLots: () => api.get('/admin/get_lots'),
  getLot: (id) => api.get(`/admin/get_lot/${id}`),
  addLot: (data) => api.post('/admin/add_lot', data),
  editLot: (id, data) => api.put(`/admin/edit_lot/${id}`, data),
  deleteLot: (id) => api.delete(`/admin/delete_lot/${id}`),
  listUsers: () => api.get('/admin/users'),
  getSpot: (id) => api.get(`/admin/get_spot/${id}`),
  deleteSpot: (id) => api.delete(`/admin/delete_spot/${id}`),
  getReservation: (spotId) => api.get(`/admin/get_reservations/${spotId}`),
  revenueChart: () => api.download('/admin/revenue_chart'),
};

export const userApi = {
  searchLots: (query) => api.get(`/user/search_lot?query=${encodeURIComponent(query)}`),
  getFirstSpot: (lotId) => api.get(`/user/get_first_spot/${lotId}`),
  bookSpot: (spotId, vehicleNo) => api.post(`/user/book_spot/${spotId}`, { vehicleNo }),
  getHistory: () => api.get('/user/get_history'),
  parkOut: (id) => api.post(`/user/park_out/${id}`),
  exportCSV: (userId) => api.get(`/export_csv_result/${userId}`),
  downloadCSV: (filename) => api.download(`/csv_download/${filename}`),
  lotDistributionChart: () => api.download('/user/lot_distribution_chart'),
};

export default api;