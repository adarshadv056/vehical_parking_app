# ParkSync — Vehicle Parking & Mobility Management System

> A full-stack, enterprise-grade vehicle parking and mobility platform featuring a bespoke design system, automated bay allocation, real-time driver tracking, and asynchronous operational analytics.

---

## 🌟 Overview

**ParkSync** is an end-to-end vehicle parking platform engineered with a **Vue 3** frontend, **Python Flask** REST API, **SQLite / SQLAlchemy** database, **Redis** caching, and **Celery** background task workers.

Originally conceptualized as an IIT Madras **Modern Application Development II** capstone, ParkSync has been redesigned into a production-grade portfolio project with:
- A custom **Design System** (`DESIGN_SYSTEM.md`) with zero third-party CSS framework bloat.
- **Full responsive design** adapting seamlessly across mobile phones (≤ 640px), tablets (768px–1024px), laptops, and desktop displays.
- **Light & Dark mode** with smooth theme transitions and persistent user preference.
- A **collapsible navigation shell** with desktop rail mode (260px ➔ 68px) and a mobile off-canvas drawer (☰).
- Dedicated, role-based experiences for **Drivers** and **Facility Operators / Admins**.

---

## 🚀 Key Features

### 🚗 Driver Mobility Console
- **Interactive Garage Explorer**: Discover nearby covered, EV-ready, and CCTV-monitored facilities with live occupancy meters, hourly pricing tags, and keyword/zone filtering.
- **Automated Bay Allocation**: Smart allocation engine automatically assigns the first optimal vacant bay (`P-01` to `P-N`) without manual stall guesswork.
- **Digital Boarding-Pass Reservation**: Boarding-pass styled ticket with check-in timestamps, price estimations, and quick demo license plate pills.
- **Active Session Tracker**: Persistent live banner tracking parked status, elapsed parking duration, and one-click instant checkout / park-out.
- **Dedicated Parking History & Receipts**: Isolated receipt center (`/user/history`) with searchable history, status filter chips, payment summary KPIs, and asynchronous CSV export.
- **Personal Analytics**: Graphical parking distribution charts powered by server-side Matplotlib and exportable for personal records.

### 🛡️ Admin Fleet Operations Console
- **Executive Control Center**: Real-time 4-metric KPI row monitoring managed garages, total bay capacity, active vehicle occupancy, and average hourly tariff.
- **Facility Management Studio**: Complete CRUD operations for parking garages. Create facilities with pricing presets (₹15–₹40/hr) and capacity presets (8–24 bays).
- **Automated Stall Layout Diagram**: Dynamic visual diagram rendering all allocated bays (`P-01` to `P-N`) with live status chips and real-time occupancy indicators.
- **Driver Directory & Compliance**: Searchable driver registry with instant toggle between high-density Table View and touch-friendly Grid Cards, plus driver detail inspector modal.
- **Revenue & Utilization Analytics**: Dedicated analytics suite (`/admin/summary`) showing facility yield tables, highest-demand garages, and downloadable Matplotlib revenue charts.

### 🎨 Design System & Visual Architecture
- **Bespoke Design Tokens**: Structured design tokens in `frontend/src/styles/tokens.css` defining typography, spacing, elevations, and palette (`Brand Blue #2563EB`, `Deep Navy #0B1220`, `Status Green #16A34A`, `Warning Amber #F59E0B`, `Error Crimson #EF4444`).
- **22 Handcrafted Vector SVG Icons**: Central icon library in `frontend/src/components/icons/` globally registered with resilient fallback sizing.
- **Light & Dark Mode**: Native CSS custom properties enabling instant theme switching with zero layout shift.
- **Responsive Layout Shell**: Desktop collapse toggle (`PanelLeftClose`/`PanelLeftOpen`), top mobile bar (56px) with hamburger drawer and frosted backdrop.

### ⚡ Background Workers & Performance
- **Redis Cache Layer**: Caches frequently queried facilities and occupancy metrics with automated cache invalidation upon create/update/delete mutations.
- **Celery Task Worker**: Handles long-running and periodic background jobs:
  - Asynchronous CSV parking receipt generation.
  - Scheduled daily parking reminder digests.
  - Monthly operational activity reports.

---

## 🏗️ Architecture

```text
  ┌─────────────────────────────────────────────────────────┐
  │                    Vue 3 Single Page App                │
  │     (Driver Console, Admin Operations, Design System)    │
  └────────────────────────────┬────────────────────────────┘
                               │ JSON / REST via Fetch Client
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │                     Flask REST API                      │
  │    (JWT Authentication, Role Guards, Business Logic)    │
  └──────────────┬───────────────────────────┬──────────────┘
                 │ SQLAlchemy ORM            │
                 ▼                           ▼
  ┌───────────────────────────┐  ┌──────────────────────────┐
  │      SQLite Database      │  │        Redis Store       │
  │ (Users, Lots, Spots,      │  │ (Cache Layer + Celery    │
  │  Reservations, Reports)   │  │  Message Broker)         │
  └───────────────────────────┘  └───────────┬──────────────┘
                                             │
                                             ▼
                                 ┌──────────────────────────┐
                                 │       Celery Workers     │
                                 │ (CSV Exports, Reports,   │
                                 │  Scheduled Reminders)    │
                                 └──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Vue 3, Vue Router 4, Vue CLI, Webpack, Custom CSS Tokens, HTML5 |
| **Backend** | Python 3.10+, Flask 3.1, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-CORS |
| **Data & Cache** | SQLite, Redis 5+, Flask-Caching |
| **Async Processing** | Celery 5.5, Matplotlib (charts), Jinja2 (email templates) |
| **Styling & Assets** | Custom CSS Variables, 22 SVG Vector Icons, Google Inter Font |

---

## 📁 Repository Structure

```text
vehical_parking_app/
│
├── frontend/                     # Vue 3 Frontend Application
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js         # Central API client with JWT interceptor & baseUrl
│   │   ├── components/
│   │   │   ├── icons/            # 22 Vector SVG icons (CarIcon, MapPinIcon, etc.)
│   │   │   ├── layout/           # AppShell, AppSidebar, PageHeader, AppNavbar
│   │   │   ├── ui/               # Button, Card, KpiCard, DataTable, Modal, etc.
│   │   │   ├── feedback/         # ToastHost, ToastItem, Spinner, EmptyState
│   │   │   │
│   │   │   ├── HomePage.vue      # Public landing page with live interactive garage
│   │   │   ├── LoginPage.vue     # Driver & Admin authentication
│   │   │   ├── RegisterPage.vue  # New driver onboarding
│   │   │   ├── UserDashboard.vue # Driver garage finder & live active session hero
│   │   │   ├── UserHistory.vue   # Dedicated driver history & CSV receipt export
│   │   │   ├── UserSummary.vue   # Driver analytics & distribution charts
│   │   │   ├── BookSpot.vue      # Boarding-pass reservation & checkout
│   │   │   ├── AdminDashboard.vue# Admin facility overview & bay occupancy
│   │   │   ├── AllUsers.vue      # Admin driver registry (Table / Cards view)
│   │   │   ├── AddLots.vue       # Split-screen facility creation studio
│   │   │   ├── EditLot.vue       # Split-screen facility edit studio
│   │   │   └── AdminSummary.vue  # Revenue analytics & Matplotlib chart viewer
│   │   ├── routers/
│   │   │   └── router.js         # Navigation routes & authentication guards
│   │   ├── styles/
│   │   │   ├── tokens.css        # Core design system design tokens
│   │   │   └── base.css          # Global typography, resets, scrollbars
│   │   ├── App.vue               # Root application shell wrapper
│   │   └── main.js               # Global component & icon registrations
│   ├── public/
│   ├── DESIGN_SYSTEM.md          # Comprehensive design guidelines & tokens
│   ├── package.json              # Frontend dependencies & build scripts
│   └── vue.config.js             # Webpack aliases & devServer proxy
│
├── backend/                      # Python Flask Backend API
│   ├── applications/
│   │   └── celery_init.py        # Celery application initialization
│   ├── models/
│   │   └── models.py             # SQLAlchemy models (User, ParkingLot, etc.)
│   ├── routes/
│   │   └── routes.py             # REST API endpoints & Celery tasks
│   ├── static/                   # Static charts & export storage
│   ├── app.py                    # Flask application factory & database seeding
│   ├── celery_config.py          # Celery broker & result backend config
│   └── requirements.txt          # Python dependencies
│
├── .env.example                  # Environment configuration template
└── README.md                     # Project documentation
```

---

## ⚡ Getting Started (Local Development)

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Redis Server** (optional for basic auth, required for Celery/caching)
- **Git**

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/adarshadv056/vehical_parking_app.git
cd vehical_parking_app
```

---

### Step 2: Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start Redis (in a separate terminal or service):
   ```bash
   redis-server
   ```
5. Run the Flask application:
   ```bash
   python app.py
   ```
   *The backend starts at `http://127.0.0.1:5000` and automatically initializes `parking.db` with a default seeded administrator.*

---

### Step 3: Celery Workers (Optional for background tasks)
In a separate terminal with the virtual environment activated:
```bash
cd backend
celery -A app.celery worker --loglevel=info
```
To enable scheduled cron digests (daily reminders & monthly reports):
```bash
celery -A app.celery beat --loglevel=info
```

---

### Step 4: Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vue development server:
   ```bash
   npm run serve
   ```
4. Open your browser and navigate to:
   ```text
   http://localhost:8080
   ```

---

### 🔑 Demo Accounts

| Role | Username / Identifier | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `Admin` / `admin@gmail` | `admin123` | Full facility operations, user directory, revenue charts |
| **Driver / User** | Register on `/register` or demo user | As registered | Search lots, reserve spots, park-in/out, view history |

---

## 🌐 How to Host ParkSync (Production Deployment)

ParkSync can be deployed through multiple modern hosting strategies:

### Strategy A: Free / Low-Cost Modern Cloud (Recommended)
This approach separates frontend static hosting (CDN) from the Flask API backend.

```text
┌─────────────────────────┐          ┌─────────────────────────┐
│     Vercel / Netlify    │          │      Render / Railway   │
│   (Vue 3 Static SPA)    │ ───────> │    (Flask REST API)     │
└─────────────────────────┘  HTTPS   └────────────┬────────────┘
                                                  │
                                     ┌────────────┴────────────┐
                                     │ Upstash (Free Redis)    │
                                     └─────────────────────────┘
```

#### 1. Host Backend on [Render](https://render.com) (or [Railway](https://railway.app))
1. Push your repository to GitHub.
2. Sign in to Render and select **New Web Service** ➔ connect your GitHub repo.
3. Configure the service settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt gunicorn`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
4. Set Environment Variables in the Render dashboard:
   ```env
   FLASK_ENV=production
   JWT_SECRET_KEY=generate-a-strong-random-key
   REDIS_URL=rediss://default:your-password@your-upstash-host:6379
   ```
5. Deploy the service and copy your public backend URL (e.g., `https://parksync-api.onrender.com`).

#### 2. Host Redis on [Upstash](https://upstash.com) (Free Cloud Redis)
1. Create a free account at Upstash.
2. Create a new Redis database and copy the `rediss://...` connection URL into your backend's `REDIS_URL`.

#### 3. Host Frontend on [Vercel](https://vercel.com) (or [Netlify](https://netlify.com))
1. Sign in to Vercel and click **Add New Project** ➔ import the GitHub repo.
2. Configure project build settings:
   - **Framework Preset**: `Vue.js`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add Environment Variable:
   ```env
   VUE_APP_API_BASE=https://parksync-api.onrender.com
   ```
4. Click **Deploy**. Vercel will build the frontend and deploy it globally to edge CDNs with automatic SSL.

> **SPA Route Handling (Vercel)**: Create a `frontend/vercel.json` file to support client-side Vue Router refreshes:
> ```json
> {
>   "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
> }
> ```

---

### Strategy B: Single Ubuntu VPS Deployment (DigitalOcean / AWS EC2 / Linode)

For full control on a single virtual server ($4–$6/month):

```text
               Internet (HTTPS:443)
                         │
                         ▼
               ┌───────────────────┐
               │    Nginx Proxy    │
               └────┬─────────┬────┘
      /static & /   │         │ /api, /login, /admin, /user
                    ▼         ▼
        ┌───────────────┐ ┌───────────────────────┐
        │ /var/www/dist │ │ Gunicorn (127.0.0.1)  │
        │  (Built SPA)  │ │      (Flask API)      │
        └───────────────┘ └───────────┬───────────┘
                                      │
                          ┌───────────▼───────────┐
                          │   Local Redis & Celery│
                          └───────────────────────┘
```

1. **Build Frontend for Production**:
   ```bash
   cd frontend
   npm run build
   # Copies the compiled assets into frontend/dist/
   ```
2. **Setup Nginx Configuration** (`/etc/nginx/sites-available/parksync`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       # Serve Vue Single Page App
       location / {
           root /var/www/parksync/frontend/dist;
           index index.html;
           try_files $uri $uri/ /index.html;
       }

       # Reverse proxy API requests to Flask/Gunicorn
       location ~ ^/(login|register|logout|admin|user|export_csv_result|csv_download) {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. **Setup Systemd Service for Flask** (`/etc/systemd/system/parksync.service`):
   ```ini
   [Unit]
   Description=ParkSync Flask Gunicorn Application
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/var/www/parksync/backend
   Environment="PATH=/var/www/parksync/backend/venv/bin"
   ExecStart=/var/www/parksync/backend/venv/bin/gunicorn -w 3 -b 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```
4. **Enable SSL**:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 📡 API Reference Overview

### 🔐 Authentication
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Register driver profile | No |
| `POST` | `/login` | Authenticate driver/admin and receive JWT | No |
| `POST` | `/logout` | Invalidate client session | Yes |

### 🚗 Driver Operations
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/user/search_lot?query=` | Search available facilities | Yes (Driver) |
| `GET` | `/user/get_first_spot/<lot_id>` | Auto-allocate vacant bay | Yes (Driver) |
| `POST` | `/user/book_spot/<spot_id>` | Confirm vehicle reservation | Yes (Driver) |
| `POST` | `/user/park_out/<res_id>` | End session, calculate fee | Yes (Driver) |
| `GET` | `/user/get_history` | Retrieve personal parking receipts | Yes (Driver) |
| `GET` | `/export_csv_result/<user_id>` | Trigger asynchronous CSV export | Yes (Driver) |
| `GET` | `/user/lot_distribution_chart` | Download usage distribution chart | Yes (Driver) |

### 🛡️ Admin Operations
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin/get_lots` | List all managed facilities | Yes (Admin) |
| `POST` | `/admin/add_lot` | Create a new parking garage | Yes (Admin) |
| `PUT` | `/admin/edit_lot/<id>` | Update tariff, address, or capacity | Yes (Admin) |
| `DELETE`| `/admin/delete_lot/<id>` | Remove facility | Yes (Admin) |
| `GET` | `/admin/users` | List all registered drivers & profiles | Yes (Admin) |
| `GET` | `/admin/get_spot/<id>` | Inspect bay occupant details | Yes (Admin) |
| `GET` | `/admin/revenue_chart` | Generate & download revenue Matplotlib chart | Yes (Admin) |

---

## 👨‍💻 Author & Project Context

- **Author**: Adarsh Vishwakarma
- **Program**: BS in Data Science and Applications — **IIT Madras**
- **Coursework Context**: Modern Application Development II (MAD-II) Capstone Redesign
- **Focus Areas**: Full-Stack Architecture, Distributed Caching & Queues, Human-Centered UI/UX Design

---

## 📄 License

This project is licensed for educational and showcase purposes. See individual dependencies for third-party open-source licensing.
