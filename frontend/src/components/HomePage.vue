<script>
import SearchIcon from './icons/SearchIcon.vue';
import ChartIcon from './icons/ChartIcon.vue';
import DownloadIcon from './icons/DownloadIcon.vue';
import UsersIcon from './icons/UsersIcon.vue';
import PlusIcon from './icons/PlusIcon.vue';
import CheckCircleIcon from './icons/CheckCircleIcon.vue';
import CheckIcon from './icons/CheckIcon.vue';
import CarIcon from './icons/CarIcon.vue';

const TOTAL_BAYS = 12;
const INITIALLY_OCCUPIED = [0, 2, 3, 5, 8, 10, 11];
const TARGET_INDEX = 6;

export default {
  name: 'HomePage',

  components: {
    SearchIcon,
    ChartIcon,
    DownloadIcon,
    UsersIcon,
    PlusIcon,
    CheckCircleIcon,
    CheckIcon,
    CarIcon
  },

  data() {
    const occupied = new Set(INITIALLY_OCCUPIED);

    return {
      mobileOpen: false,
      scrolled: false,
      activeFaq: null,
      pulsing: false,
      carVisible: false,
      carCol: 1,
      carRow: 3,
      searchLocation: '',

      spots: Array.from({ length: TOTAL_BAYS }, (_, i) => ({
        id: `A${String(i + 1).padStart(2, '0')}`,
        occupied: occupied.has(i)
      })),

      featuredGarages: [
        {
          id: 1,
          name: 'City Center Garage',
          location: '120 Broadway, Manhattan, NY',
          img: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1400&q=85',
          price: 40,
          avail: '18 / 24 free',
          specs: ['Covered', 'EV charging', 'CCTV']
        },
        {
          id: 2,
          name: 'Riverfront Terminal',
          location: '45 Riverfront Plaza, Chicago, IL',
          img: 'https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=1000&q=85',
          price: 35,
          avail: '12 / 16 free',
          specs: ['Fast access', '24/7 gate', 'Valet']
        },
        {
          id: 3,
          name: 'Metro Mall Underground',
          location: '750 Universal Mall Way, LA',
          img: 'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85',
          price: 25,
          avail: '15 / 16 free',
          specs: ['Underground', 'Mall access', 'Security']
        }
      ],

      faqs: [
        {
          q: 'How does parking allocation work?',
          a: 'You choose a parking lot rather than a specific bay. The application finds the first available spot and creates the reservation for you.'
        },
        {
          q: 'How is the parking cost calculated?',
          a: 'The application calculates the parking duration from the parking and leaving timestamps and applies the lot hourly rate.'
        },
        {
          q: 'What can an operator manage?',
          a: 'Admins can create and manage parking lots, change capacity, inspect bay status, manage users and view operational summaries.'
        },
        {
          q: 'Can I export my parking history?',
          a: 'Yes. Users can request a CSV export of their parking activity. The export is handled asynchronously by the application.'
        }
      ]
    };
  },

  computed: {
    availableCount() {
      return this.spots.filter((s) => !s.occupied).length;
    },

    carStyle() {
      return {
        '--car-col': this.carCol,
        '--car-row': this.carRow,
        opacity: this.carVisible ? 1 : 0
      };
    }
  },

  mounted() {
    this._dead = false;
    this._rafIds = [];
    this.onScroll();
    window.addEventListener('scroll', this.onScroll, { passive: true });
    this.setupReveal();

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduce) this.runLoop();
  },

  beforeUnmount() {
    this._dead = true;
    window.removeEventListener('scroll', this.onScroll);
    if (this._io) this._io.disconnect();
    (this._rafIds || []).forEach((id) => cancelAnimationFrame(id));
  },

  methods: {
    scrollTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    goToLogin() {
      this.mobileOpen = false;
      this.$router.push('/login');
    },

    goToRegister() {
      this.mobileOpen = false;
      this.$router.push('/register');
    },

    goToUser() {
      this.$router.push('/user');
    },

    onScroll() {
      this.scrolled = window.scrollY > 24;
    },

    toggleFaq(index) {
      this.activeFaq = this.activeFaq === index ? null : index;
    },

    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },

    async runLoop() {
      while (!this._dead) {
        try {
          await this.parkCycle();
        } catch (e) {
          break;
        }
      }
    },

    async parkCycle() {
      this.spots.forEach((s, i) => {
        s.occupied = INITIALLY_OCCUPIED.includes(i);
      });

      this.carVisible = false;
      this.carCol = 1;
      this.carRow = 3;

      await this.sleep(900);
      if (this._dead) return;

      this.pulsing = true;
      await this.sleep(1100);
      if (this._dead) return;

      this.pulsing = false;
      this.carVisible = true;

      await this.sleep(650);
      if (this._dead) return;

      this.carCol = TARGET_INDEX % 4;
      this.carRow = Math.floor(TARGET_INDEX / 4);

      await this.sleep(1000);
      if (this._dead) return;

      this.spots[TARGET_INDEX].occupied = true;
      this.carVisible = false;

      await this.sleep(3000);
    },

    setupReveal() {
      const targets = document.querySelectorAll('[data-reveal]');

      this._io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              this._io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12 }
      );

      targets.forEach((el) => this._io.observe(el));
    }
  }
};
</script>

<template>
  <div class="site">
    <!-- NAV -->
    <header class="nav" :class="{ 'nav--scrolled': scrolled }">
      <div class="nav__inner">
        <a href="#" class="brand" @click.prevent="scrollTop">
          <span class="brand__mark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
              <path d="M6 3h7a7 7 0 0 1 0 14h-3v4H6V3Z"/>
              <path d="M10 7h2.5a3.5 3.5 0 1 1 0 7H10V7Z"/>
            </svg>
          </span>
          <span>ParkSync</span>
        </a>

        <nav class="nav__links" :class="{ 'nav__links--open': mobileOpen }">
          <a href="#product" @click="mobileOpen = false">Product</a>
          <a href="#how" @click="mobileOpen = false">How it works</a>
          <a href="#facilities" @click="mobileOpen = false">Facilities</a>
          <a href="#operators" @click="mobileOpen = false">Operators</a>
          <a href="#faq" @click="mobileOpen = false">FAQ</a>

          <div class="nav__mobile-actions">
            <button class="text-btn" @click="goToLogin">Sign in</button>
            <button class="dark-btn" @click="goToRegister">Get started</button>
          </div>
        </nav>

        <div class="nav__actions">
          <button class="text-btn" @click="goToLogin">Sign in</button>
          <button class="dark-btn dark-btn--small" @click="goToRegister">Get started</button>
          <button class="menu-btn" :aria-expanded="mobileOpen" @click="mobileOpen = !mobileOpen">
            <svg v-if="!mobileOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 7h16M4 12h16M4 17h16"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m6 6 12 12M18 6 6 18"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- HERO -->
    <main>
      <section class="hero">
        <div class="container hero__inner">
          <div class="hero__copy" data-reveal>
            <p class="eyebrow"><span></span> Parking management, redesigned</p>

            <h1>
              Find your space.<br>
              <em>Park with confidence.</em>
            </h1>

            <p class="hero__lead">
              A simple parking experience for drivers, backed by a clear control center
              for the people who run every bay.
            </p>

            <div class="hero__actions">
              <button class="blue-btn" @click="goToRegister">
                Get started
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </button>
              <button class="outline-btn" @click="goToLogin">Sign in</button>
            </div>

            <div class="hero__meta">
              <span><i></i> Bay-level availability</span>
              <span><i></i> Automatic allocation</span>
              <span><i></i> CSV reports</span>
            </div>
          </div>

          <div class="hero__visual" data-reveal>
            <div class="hero-photo">
              <img
                src="https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1600&q=90"
                alt="Modern parking facility"
              >
              <div class="hero-photo__veil"></div>

              <div class="hero-photo__caption">
                <span>01 / Parking intelligence</span>
                <strong>See the bay before you arrive.</strong>
              </div>
            </div>

            <div class="live-panel">
              <div class="live-panel__top">
                <div>
                  <span class="live-status"><b></b> Live layout</span>
                  <h3>City Center Garage</h3>
                  <p>Level 02 · East wing</p>
                </div>
                <div class="live-count">
                  <strong>{{ availableCount }}</strong>
                  <span>available</span>
                </div>
              </div>

              <div class="parking-grid" :class="{ 'parking-grid--pulse': pulsing }">
                <div
                  v-for="spot in spots"
                  :key="spot.id"
                  class="parking-bay"
                  :class="{ 'parking-bay--occupied': spot.occupied }"
                >
                  <span>{{ spot.id }}</span>
                  <CarIcon v-if="spot.occupied" />
                </div>

                <div class="moving-car" :style="carStyle">
                  <CarIcon />
                </div>
              </div>

              <div class="live-panel__bottom">
                <span><i class="available-dot"></i> Available</span>
                <span><i class="occupied-dot"></i> Occupied</span>
                <small>allocation updates automatically</small>
              </div>
            </div>
          </div>
        </div>

        <div class="container hero-search" data-reveal>
          <div class="hero-search__field">
            <label>Looking for parking?</label>
            <input v-model="searchLocation" type="text" placeholder="Enter a location, pincode or lot name">
          </div>
          <div class="hero-search__divider"></div>
          <div class="hero-search__info">
            <span>Availability</span>
            <strong>View live parking options</strong>
          </div>
          <button class="hero-search__button" @click="goToUser">
            Search parking
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="7"/>
              <path d="m20 20-4-4"/>
            </svg>
          </button>
        </div>
      </section>

      <!-- PRODUCT STORY -->
      <section id="product" class="story section">
        <div class="container story__grid">
          <div class="story__image" data-reveal>
            <img
              src="https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=1500&q=90"
              alt="Parking facility"
              loading="lazy"
            >
            <div class="story__label">
              <span>ParkSync</span>
              <strong>Built around the bay.</strong>
            </div>
          </div>

          <div class="story__copy" data-reveal>
            <p class="eyebrow">The product</p>
            <h2>Built around the bay, not the spreadsheet.</h2>
            <p>
              Parking becomes much easier when the system understands the actual space.
              ParkSync connects lots, bays, reservations and parking history in one focused
              experience.
            </p>

            <div class="story__points">
              <div><CheckIcon /> Choose a lot and let the system allocate a bay.</div>
              <div><CheckIcon /> See occupied and available spots at a glance.</div>
              <div><CheckIcon /> Track parking time, cost and previous sessions.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- HOW IT WORKS -->
      <section id="how" class="how section section--soft">
        <div class="container">
          <div class="section-heading section-heading--left" data-reveal>
            <p class="eyebrow">How it works</p>
            <h2>From search to parked<br>in a few simple steps.</h2>
          </div>

          <div class="flow">
            <article class="flow__item" data-reveal>
              <span class="flow__number">01</span>
              <div class="flow__icon"><SearchIcon /></div>
              <h3>Find a lot</h3>
              <p>Search by location, pincode or parking lot name and see where space is available.</p>
            </article>

            <div class="flow__line"></div>

            <article class="flow__item" data-reveal>
              <span class="flow__number">02</span>
              <div class="flow__icon"><PlusIcon /></div>
              <h3>Reserve a bay</h3>
              <p>Select the lot, enter your vehicle details and let the system allocate the first free spot.</p>
            </article>

            <div class="flow__line"></div>

            <article class="flow__item" data-reveal>
              <span class="flow__number">03</span>
              <div class="flow__icon"><CheckCircleIcon /></div>
              <h3>Park & check out</h3>
              <p>Park, then release the spot when you leave. Duration and parking cost are recorded automatically.</p>
            </article>
          </div>
        </div>
      </section>

      <!-- FACILITIES / EDITORIAL -->
      <section id="facilities" class="facilities section">
        <div class="container">
          <div class="editorial-heading" data-reveal>
            <div>
              <p class="eyebrow">Parking facilities</p>
              <h2>Every bay has<br>a place in the picture.</h2>
            </div>
            <p>
              Explore parking facilities with clear availability, pricing and useful
              details before choosing where to park.
            </p>
          </div>

          <div class="facility-feature" data-reveal>
            <div class="facility-feature__image">
              <img
                :src="featuredGarages[0].img"
                :alt="featuredGarages[0].name"
                loading="lazy"
              >
              <div class="image-number">01</div>
              <div class="availability-badge">{{ featuredGarages[0].avail }}</div>
            </div>

            <div class="facility-feature__content">
              <span class="facility-feature__index">Featured facility</span>
              <h3>{{ featuredGarages[0].name }}</h3>
              <p>{{ featuredGarages[0].location }}</p>

              <div class="facility-price">
                <strong>₹{{ featuredGarages[0].price }}</strong>
                <span>/ hour</span>
              </div>

              <div class="facility-specs">
                <span v-for="spec in featuredGarages[0].specs" :key="spec">{{ spec }}</span>
              </div>

              <button class="arrow-link" @click="goToUser">
                Find parking here
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="facility-secondary">
            <article
              v-for="(garage, index) in featuredGarages.slice(1)"
              :key="garage.id"
              class="facility-small"
              data-reveal
            >
              <div class="facility-small__image">
                <img :src="garage.img" :alt="garage.name" loading="lazy">
                <span>0{{ index + 2 }}</span>
              </div>
              <div class="facility-small__body">
                <div>
                  <h3>{{ garage.name }}</h3>
                  <p>{{ garage.location }}</p>
                </div>
                <strong>₹{{ garage.price }}<small>/hr</small></strong>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- DARK PRODUCT SHOWCASE -->
      <section id="operators" class="operator section">
        <div class="container operator__inner">
          <div class="operator__intro" data-reveal>
            <p class="eyebrow eyebrow--light">For operators</p>
            <h2>Your parking operation,<br><em>one clear view.</em></h2>
            <p>
              Manage lots, inspect bay status, monitor users and understand parking
              activity without jumping between disconnected screens.
            </p>

            <ul>
              <li><CheckIcon /> Lot and spot management</li>
              <li><CheckIcon /> Occupancy and revenue summaries</li>
              <li><CheckIcon /> User management and CSV export</li>
            </ul>

            <button class="light-btn" @click="goToLogin">
              Open operator console
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M13 6l6 6-6 6"/>
              </svg>
            </button>
          </div>

          <div class="dashboard-stage" data-reveal>
            <div class="dashboard-window">
              <div class="window-bar">
                <div class="window-dots"><i></i><i></i><i></i></div>
                <span>ParkSync / Overview</span>
                <small>Admin</small>
              </div>

              <div class="dashboard-body">
                <div class="dashboard-title">
                  <div>
                    <span>Overview</span>
                    <h3>Parking operations</h3>
                  </div>
                  <button>Today</button>
                </div>

                <div class="dashboard-stats">
                  <div><span>Active lots</span><strong>06</strong></div>
                  <div><span>Total bays</span><strong>86</strong></div>
                  <div><span>Occupied</span><strong>62</strong></div>
                  <div><span>Revenue</span><strong>₹4,820</strong></div>
                </div>

                <div class="dashboard-chart">
                  <div class="chart-head">
                    <span>Weekly occupancy</span>
                    <small>Last 7 days</small>
                  </div>
                  <div class="bars">
                    <div v-for="(height, i) in [48,64,56,82,94,72,58]" :key="i">
                      <span :style="{ height: `${height}%` }"></span>
                      <small>{{ ['M','T','W','T','F','S','S'][i] }}</small>
                    </div>
                  </div>
                </div>

                <div class="dashboard-foot">
                  <span><i></i> 24 spots available now</span>
                  <span>Updated just now</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FEATURES -->
      <section class="features section section--soft">
        <div class="container">
          <div class="editorial-heading editorial-heading--center" data-reveal>
            <div>
              <p class="eyebrow">The essentials</p>
              <h2>Everything the parking loop needs.</h2>
            </div>
            <p>
              No inflated feature list. Just the pieces that make the driver and
              operator experience work together.
            </p>
          </div>

          <div class="feature-grid">
            <article class="feature-card" data-reveal>
              <span><SearchIcon /></span>
              <h3>Find & reserve</h3>
              <p>Search available lots and start a parking session without choosing a bay manually.</p>
            </article>

            <article class="feature-card" data-reveal>
              <span><CarIcon /></span>
              <h3>Bay-level status</h3>
              <p>See which parking spots are occupied and which ones are available.</p>
            </article>

            <article class="feature-card" data-reveal>
              <span><UsersIcon /></span>
              <h3>Role-based access</h3>
              <p>Separate driver and admin experiences with authenticated access.</p>
            </article>

            <article class="feature-card" data-reveal>
              <span><PlusIcon /></span>
              <h3>Lot management</h3>
              <p>Create, edit and manage parking facilities and their capacity.</p>
            </article>

            <article class="feature-card" data-reveal>
              <span><ChartIcon /></span>
              <h3>Operational summaries</h3>
              <p>Understand parking activity, occupancy and revenue through summaries and charts.</p>
            </article>

            <article class="feature-card" data-reveal>
              <span><DownloadIcon /></span>
              <h3>CSV exports</h3>
              <p>Export parking activity without manually copying records into another tool.</p>
            </article>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="faq section">
        <div class="container faq__inner">
          <div class="faq__intro" data-reveal>
            <p class="eyebrow">Questions</p>
            <h2>Good parking software should be easy to understand.</h2>
          </div>

          <div class="faq__list" data-reveal>
            <div
              v-for="(faq, index) in faqs"
              :key="index"
              class="faq-row"
              :class="{ 'faq-row--open': activeFaq === index }"
            >
              <button @click="toggleFaq(index)">
                <span>{{ faq.q }}</span>
                <i>{{ activeFaq === index ? '−' : '+' }}</i>
              </button>
              <div v-if="activeFaq === index" class="faq-row__answer">
                {{ faq.a }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="cta">
        <div class="cta__image"></div>
        <div class="container cta__inner" data-reveal>
          <p class="eyebrow eyebrow--light">ParkSync</p>
          <h2>Less searching.<br><em>More arriving.</em></h2>
          <p>Start with the parking experience, then let the system handle the details.</p>
          <div>
            <button class="blue-btn" @click="goToRegister">Get started</button>
            <button class="outline-btn outline-btn--dark" @click="goToLogin">Sign in</button>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="container footer__grid">
        <div>
          <a href="#" class="brand brand--footer" @click.prevent="scrollTop">
            <span class="brand__mark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
                <path d="M6 3h7a7 7 0 0 1 0 14h-3v4H6V3Z"/>
                <path d="M10 7h2.5a3.5 3.5 0 1 1 0 7H10V7Z"/>
              </svg>
            </span>
            <span>ParkSync</span>
          </a>
          <p>Parking management built around the actual space.</p>
        </div>

        <div>
          <small>Explore</small>
          <a href="#product">Product</a>
          <a href="#how">How it works</a>
          <a href="#facilities">Facilities</a>
        </div>

        <div>
          <small>Access</small>
          <a href="#" @click.prevent="goToLogin">Sign in</a>
          <a href="#" @click.prevent="goToRegister">Create account</a>
          <a href="#" @click.prevent="goToLogin">Admin console</a>
        </div>
      </div>

      <div class="container footer__bottom">
        <span>© 2026 ParkSync</span>
        <span>Vue 3 · Flask · SQLite · Redis · Celery</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.site {
  --ink: #0b1220;
  --text: #111827;
  --muted: #667085;
  --line: #e6e9ee;
  --paper: #ffffff;
  --soft: #f5f7fa;
  --blue: #2563eb;
  --blue-dark: #1d4ed8;
  --blue-soft: #eaf2ff;
  --green: #16a34a;
  --red: #ef4444;
  font-family: var(--font-family-primary, "Manrope", sans-serif);
  color: var(--text);
  background: var(--paper);
  overflow: hidden;
}

* {
  box-sizing: border-box;
}

.container {
  width: min(1240px, calc(100% - 64px));
  margin: 0 auto;
}

button,
input {
  font: inherit;
}

button {
  -webkit-tap-highlight-color: transparent;
}

.nav {
  position: fixed;
  inset: 0 0 auto;
  z-index: 100;
  padding: 18px 0;
  transition: padding .3s ease;
}

.nav__inner {
  width: min(1240px, calc(100% - 64px));
  min-height: 58px;
  margin: auto;
  padding: 0 8px 0 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255,255,255,.9);
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 16px;
  backdrop-filter: blur(18px);
  box-shadow: 0 10px 35px rgba(11,18,32,.06);
  transition: box-shadow .3s ease, border-color .3s ease;
}

.nav--scrolled {
  padding-top: 10px;
}

.nav--scrolled .nav__inner {
  box-shadow: 0 12px 40px rgba(11,18,32,.1);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--ink);
  text-decoration: none;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -.04em;
}

.brand__mark {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  color: #fff;
  background: var(--ink);
  border-radius: 9px;
}

.brand__mark svg {
  width: 17px;
  height: 17px;
}

.nav__links {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav__links > a {
  color: #596273;
  font-size: 12px;
  font-weight: 650;
  text-decoration: none;
  transition: color .2s ease;
}

.nav__links > a:hover {
  color: var(--ink);
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.text-btn,
.dark-btn,
.blue-btn,
.outline-btn,
.light-btn,
.hero-search__button {
  border: 0;
  cursor: pointer;
}

.text-btn {
  padding: 10px 13px;
  color: var(--ink);
  background: transparent;
  font-size: 12px;
  font-weight: 700;
}

.dark-btn {
  padding: 11px 17px;
  color: #fff;
  background: var(--ink);
  border-radius: 10px;
  font-size: 12px;
  font-weight: 750;
  transition: transform .2s ease, background .2s ease;
}

.dark-btn:hover {
  background: var(--blue);
  transform: translateY(-1px);
}

.dark-btn--small {
  padding: 9px 15px;
}

.menu-btn,
.nav__mobile-actions {
  display: none;
}

/* Hero */
.hero {
  position: relative;
  padding: 150px 0 54px;
  background: #f7f9fc;
}

.hero__inner {
  display: grid;
  grid-template-columns: minmax(0, .91fr) minmax(500px, 1.09fr);
  gap: 62px;
  align-items: center;
}

.hero__copy {
  padding-bottom: 25px;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 17px;
  color: var(--blue);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}

.eyebrow > span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--blue);
}

.hero h1 {
  max-width: 660px;
  margin: 0;
  color: var(--ink);
  font-size: clamp(48px, 5.7vw, 78px);
  line-height: .98;
  letter-spacing: -.065em;
  font-weight: 820;
}

.hero h1 em,
.operator h2 em,
.cta h2 em {
  color: var(--blue);
  font-style: normal;
}

.hero__lead {
  max-width: 485px;
  margin: 25px 0 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  gap: 10px;
  margin-top: 29px;
}

.blue-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 46px;
  padding: 0 20px;
  color: #fff;
  background: var(--blue);
  border-radius: 10px;
  font-size: 12px;
  font-weight: 750;
  box-shadow: 0 8px 20px rgba(37,99,235,.2);
  transition: transform .2s ease, background .2s ease;
}

.blue-btn svg {
  width: 15px;
  height: 15px;
}

.blue-btn:hover {
  background: var(--blue-dark);
  transform: translateY(-2px);
}

.outline-btn {
  min-height: 46px;
  padding: 0 20px;
  color: var(--ink);
  background: #fff;
  border: 1px solid #dfe3e8;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 750;
  transition: border-color .2s ease, background .2s ease;
}

.outline-btn:hover {
  border-color: #b8c0cc;
  background: #f9fafb;
}

.hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 28px;
  color: #687386;
  font-size: 10px;
  font-weight: 650;
}

.hero__meta span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.hero__meta i {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--green);
}

.hero__visual {
  position: relative;
  min-height: 520px;
}

.hero-photo {
  position: absolute;
  inset: 0 0 42px 48px;
  overflow: hidden;
  border-radius: 24px;
  background: #dfe5eb;
}

.hero-photo img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  filter: saturate(.85);
}

.hero-photo__veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(5,10,18,.03) 35%, rgba(5,10,18,.6));
}

.hero-photo__caption {
  position: absolute;
  left: 27px;
  right: 27px;
  bottom: 25px;
  color: #fff;
}

.hero-photo__caption span {
  display: block;
  margin-bottom: 6px;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  opacity: .72;
}

.hero-photo__caption strong {
  display: block;
  max-width: 310px;
  font-size: 22px;
  line-height: 1.12;
  letter-spacing: -.035em;
}

.live-panel {
  position: absolute;
  z-index: 2;
  left: 0;
  bottom: 0;
  width: 345px;
  padding: 18px;
  background: rgba(255,255,255,.97);
  border: 1px solid rgba(15,23,42,.09);
  border-radius: 18px;
  box-shadow: 0 22px 55px rgba(11,18,32,.16);
}

.live-panel__top {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 15px;
}

.live-status {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--green);
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .08em;
}

.live-status b {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--green);
}

.live-panel h3 {
  margin: 4px 0 2px;
  font-size: 14px;
  letter-spacing: -.025em;
}

.live-panel p {
  margin: 0;
  color: #8992a1;
  font-size: 9px;
}

.live-count {
  text-align: right;
}

.live-count strong {
  display: block;
  color: var(--blue);
  font-size: 27px;
  line-height: .9;
  letter-spacing: -.05em;
}

.live-count span {
  color: #7c8795;
  font-size: 8px;
  font-weight: 700;
}

.parking-grid {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  padding: 11px;
  background: #f5f7fa;
  border: 1px solid #e5e8ed;
  border-radius: 12px;
}

.parking-grid--pulse .parking-bay:not(.parking-bay--occupied) {
  box-shadow: inset 0 0 0 1px rgba(37,99,235,.28);
}

.parking-bay {
  position: relative;
  height: 54px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 6px;
  color: #a4adba;
  background: #fff;
  border: 1px solid #dfe4ea;
  border-radius: 6px;
  transition: background .35s ease, border-color .35s ease, box-shadow .35s ease;
}

.parking-bay span {
  position: absolute;
  top: 5px;
  left: 6px;
  font-family: var(--font-family-mono, monospace);
  font-size: 7px;
  font-weight: 700;
}

.parking-bay svg,
.moving-car svg {
  width: 20px;
  height: 20px;
}

.parking-bay svg {
  color: var(--red);
}

.parking-bay--occupied {
  background: #fff0f0;
  border-color: #f3b9b9;
}

.moving-car {
  position: absolute;
  left: 16px;
  bottom: 19px;
  width: 20px;
  height: 20px;
  color: var(--blue);
  transition: transform .9s cubic-bezier(.2,.8,.2,1), opacity .25s ease;
  transform: translate(
    calc(var(--car-col, 0) * 68px),
    calc(var(--car-row, 0) * -58px)
  );
}

.live-panel__bottom {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-top: 10px;
  color: #6f7a89;
  font-size: 8px;
  font-weight: 650;
}

.live-panel__bottom span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.live-panel__bottom i {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.available-dot { background: var(--green); }
.occupied-dot { background: var(--red); }

.live-panel__bottom small {
  margin-left: auto;
  color: #a0a8b3;
  font-size: 8px;
}

.hero-search {
  position: relative;
  z-index: 3;
  display: grid;
  grid-template-columns: 1.4fr 1px 1fr auto;
  align-items: center;
  gap: 25px;
  margin-top: 2px;
  padding: 16px 18px 16px 23px;
  background: #fff;
  border: 1px solid #e3e7ec;
  border-radius: 16px;
  box-shadow: 0 17px 40px rgba(11,18,32,.07);
}

.hero-search__field label,
.hero-search__info span {
  display: block;
  margin-bottom: 4px;
  color: #9099a7;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.hero-search__field input {
  width: 100%;
  padding: 0;
  color: var(--ink);
  background: transparent;
  border: 0;
  outline: 0;
  font-size: 13px;
  font-weight: 700;
}

.hero-search__field input::placeholder {
  color: #a5adba;
}

.hero-search__divider {
  width: 1px;
  height: 36px;
  background: #e5e8ed;
}

.hero-search__info strong {
  color: var(--ink);
  font-size: 12px;
}

.hero-search__button {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  min-height: 42px;
  padding: 0 17px;
  color: #fff;
  background: var(--ink);
  border-radius: 9px;
  font-size: 11px;
  font-weight: 750;
  transition: background .2s ease;
}

.hero-search__button:hover {
  background: var(--blue);
}

.hero-search__button svg {
  width: 15px;
}

/* General sections */
.section {
  padding: 112px 0;
}

.section--soft {
  background: var(--soft);
}

.story__grid {
  display: grid;
  grid-template-columns: 1.05fr .8fr;
  gap: 100px;
  align-items: center;
}

.story__image {
  position: relative;
  height: 560px;
}

.story__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 22px;
  filter: saturate(.82);
}

.story__label {
  position: absolute;
  left: 22px;
  bottom: 22px;
  padding: 13px 15px;
  color: #fff;
  background: rgba(11,18,32,.82);
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

.story__label span {
  display: block;
  margin-bottom: 3px;
  color: #b9c3d1;
  font-size: 8px;
  letter-spacing: .12em;
  text-transform: uppercase;
}

.story__label strong {
  font-size: 15px;
  letter-spacing: -.02em;
}

.story__copy h2,
.section-heading h2,
.editorial-heading h2,
.faq__intro h2 {
  margin: 0;
  color: var(--ink);
  font-size: clamp(38px, 4.2vw, 56px);
  line-height: 1.02;
  letter-spacing: -.055em;
}

.story__copy > p:not(.eyebrow) {
  max-width: 470px;
  margin: 23px 0 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.75;
}

.story__points {
  display: grid;
  gap: 13px;
  margin-top: 28px;
  color: #3e4858;
  font-size: 12px;
  font-weight: 650;
}

.story__points div {
  display: flex;
  gap: 10px;
  align-items: center;
}

.story__points svg {
  flex: 0 0 auto;
  width: 16px;
  color: var(--green);
}

/* Flow */
.section-heading {
  max-width: 680px;
}

.section-heading--left {
  margin-bottom: 60px;
}

.flow {
  display: grid;
  grid-template-columns: 1fr 60px 1fr 60px 1fr;
  align-items: center;
}

.flow__item {
  min-height: 245px;
  padding: 30px;
  background: #fff;
  border: 1px solid #e4e8ed;
  border-radius: 16px;
}

.flow__number {
  display: block;
  margin-bottom: 31px;
  color: #a5adba;
  font-family: var(--font-family-mono, monospace);
  font-size: 11px;
  font-weight: 700;
}

.flow__icon {
  width: 39px;
  height: 39px;
  display: grid;
  place-items: center;
  margin-bottom: 25px;
  color: var(--blue);
  background: var(--blue-soft);
  border-radius: 9px;
}

.flow__icon svg {
  width: 17px;
}

.flow h3 {
  margin: 0;
  color: var(--ink);
  font-size: 17px;
  letter-spacing: -.03em;
}

.flow p {
  max-width: 280px;
  margin: 9px 0 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.65;
}

.flow__line {
  height: 1px;
  background: #d7dce3;
}

/* Facilities */
.editorial-heading {
  display: grid;
  grid-template-columns: 1fr .65fr;
  gap: 80px;
  align-items: end;
  margin-bottom: 54px;
}

.editorial-heading > p {
  max-width: 420px;
  margin: 0 0 4px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
}

.editorial-heading--center {
  align-items: end;
}

.facility-feature {
  display: grid;
  grid-template-columns: 1.45fr .75fr;
  min-height: 560px;
  background: #f3f5f7;
  border-radius: 22px;
  overflow: hidden;
}

.facility-feature__image {
  position: relative;
  min-height: 560px;
}

.facility-feature__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  filter: saturate(.82);
}

.image-number {
  position: absolute;
  top: 25px;
  left: 25px;
  color: #fff;
  font-family: var(--font-family-mono, monospace);
  font-size: 11px;
  font-weight: 700;
}

.availability-badge {
  position: absolute;
  right: 24px;
  bottom: 24px;
  padding: 8px 11px;
  color: #fff;
  background: rgba(11,18,32,.78);
  border-radius: 8px;
  font-size: 10px;
  font-weight: 750;
  backdrop-filter: blur(8px);
}

.facility-feature__content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 58px;
}

.facility-feature__index {
  color: var(--blue);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}

.facility-feature h3 {
  max-width: 360px;
  margin: 12px 0 7px;
  color: var(--ink);
  font-size: 31px;
  line-height: 1.03;
  letter-spacing: -.05em;
}

.facility-feature__content > p {
  margin: 0;
  color: #7b8492;
  font-size: 11px;
}

.facility-price {
  display: flex;
  align-items: baseline;
  gap: 5px;
  margin-top: 37px;
}

.facility-price strong {
  color: var(--ink);
  font-size: 28px;
  letter-spacing: -.05em;
}

.facility-price span {
  color: #8b94a1;
  font-size: 10px;
}

.facility-specs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 18px;
}

.facility-specs span {
  padding: 7px 9px;
  color: #626c7b;
  background: #fff;
  border: 1px solid #e0e4e9;
  border-radius: 6px;
  font-size: 9px;
  font-weight: 700;
}

.arrow-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  margin-top: 35px;
  padding: 0 0 8px;
  color: var(--ink);
  background: transparent;
  border: 0;
  border-bottom: 1px solid var(--ink);
  cursor: pointer;
  font-size: 11px;
  font-weight: 800;
}

.arrow-link svg {
  width: 14px;
  transition: transform .2s ease;
}

.arrow-link:hover svg {
  transform: translateX(3px);
}

.facility-secondary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 18px;
}

.facility-small {
  display: grid;
  grid-template-columns: 180px 1fr;
  min-height: 145px;
  background: #fff;
  border: 1px solid #e4e8ed;
  border-radius: 14px;
  overflow: hidden;
}

.facility-small__image {
  position: relative;
}

.facility-small__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(.8);
}

.facility-small__image span {
  position: absolute;
  top: 12px;
  left: 12px;
  color: #fff;
  font-family: var(--font-family-mono, monospace);
  font-size: 9px;
}

.facility-small__body {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  padding: 22px;
}

.facility-small h3 {
  margin: 0;
  color: var(--ink);
  font-size: 14px;
  letter-spacing: -.025em;
}

.facility-small p {
  margin: 7px 0 0;
  color: #8992a0;
  font-size: 10px;
  line-height: 1.5;
}

.facility-small strong {
  white-space: nowrap;
  color: var(--ink);
  font-size: 15px;
}

.facility-small small {
  color: #8d96a2;
  font-size: 8px;
}

/* Operator */
.operator {
  color: #fff;
  background: var(--ink);
}

.operator__inner {
  display: grid;
  grid-template-columns: .78fr 1.22fr;
  gap: 90px;
  align-items: center;
}

.eyebrow--light {
  color: #8eb3ff;
}

.operator h2 {
  margin: 0;
  color: #fff;
  font-size: clamp(42px, 4.6vw, 62px);
  line-height: .99;
  letter-spacing: -.06em;
}

.operator__intro > p:not(.eyebrow) {
  max-width: 440px;
  margin: 24px 0 0;
  color: #9aa5b5;
  font-size: 14px;
  line-height: 1.75;
}

.operator ul {
  display: grid;
  gap: 11px;
  margin: 27px 0 32px;
  padding: 0;
  list-style: none;
  color: #d8dee7;
  font-size: 11px;
  font-weight: 650;
}

.operator li {
  display: flex;
  gap: 9px;
  align-items: center;
}

.operator li svg {
  width: 15px;
  color: #71a2ff;
}

.light-btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  min-height: 43px;
  padding: 0 17px;
  color: var(--ink);
  background: #fff;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 800;
}

.light-btn svg {
  width: 14px;
}

.dashboard-stage {
  padding: 22px;
  background: #121b2a;
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 20px;
  transform: rotate(1deg);
  box-shadow: 0 35px 70px rgba(0,0,0,.28);
}

.dashboard-window {
  overflow: hidden;
  background: #f7f9fb;
  border-radius: 11px;
  color: var(--ink);
}

.window-bar {
  height: 35px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-bottom: 1px solid #e4e7eb;
  background: #fff;
  font-size: 8px;
  color: #7f8997;
}

.window-dots {
  display: flex;
  gap: 4px;
  margin-right: 10px;
}

.window-dots i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #d8dde4;
}

.window-bar small {
  margin-left: auto;
  color: #8c95a1;
}

.dashboard-body {
  padding: 20px;
}

.dashboard-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title span {
  color: #7d8795;
  font-size: 8px;
}

.dashboard-title h3 {
  margin: 3px 0 0;
  font-size: 18px;
  letter-spacing: -.04em;
}

.dashboard-title button {
  padding: 6px 9px;
  color: #667180;
  background: #fff;
  border: 1px solid #e1e5ea;
  border-radius: 6px;
  font-size: 8px;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 7px;
  margin-top: 16px;
}

.dashboard-stats div {
  padding: 10px;
  background: #fff;
  border: 1px solid #e7eaee;
  border-radius: 7px;
}

.dashboard-stats span {
  display: block;
  color: #929aa5;
  font-size: 7px;
}

.dashboard-stats strong {
  display: block;
  margin-top: 5px;
  color: var(--ink);
  font-size: 15px;
  letter-spacing: -.035em;
}

.dashboard-chart {
  margin-top: 8px;
  padding: 14px;
  background: #fff;
  border: 1px solid #e7eaee;
  border-radius: 8px;
}

.chart-head {
  display: flex;
  justify-content: space-between;
  color: #596373;
  font-size: 8px;
  font-weight: 750;
}

.chart-head small {
  color: #9aa2ad;
  font-weight: 500;
}

.bars {
  height: 155px;
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 12px;
  margin-top: 15px;
  padding: 0 4px;
  border-bottom: 1px solid #edf0f3;
}

.bars > div {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: end;
  gap: 7px;
}

.bars span {
  width: min(26px, 80%);
  min-height: 12px;
  background: var(--blue);
  border-radius: 4px 4px 0 0;
}

.bars small {
  padding-bottom: 7px;
  color: #9ca4af;
  font-size: 7px;
}

.dashboard-foot {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  color: #8d96a2;
  font-size: 7px;
}

.dashboard-foot span:first-child {
  color: #3c8c55;
}

.dashboard-foot i {
  display: inline-block;
  width: 5px;
  height: 5px;
  margin-right: 4px;
  border-radius: 50%;
  background: var(--green);
}

/* Features */
.features .editorial-heading {
  margin-bottom: 55px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid #dfe4ea;
  border-left: 1px solid #dfe4ea;
}

.feature-card {
  min-height: 215px;
  padding: 28px;
  background: #fff;
  border-right: 1px solid #dfe4ea;
  border-bottom: 1px solid #dfe4ea;
}

.feature-card > span {
  width: 35px;
  height: 35px;
  display: grid;
  place-items: center;
  color: var(--blue);
  background: var(--blue-soft);
  border-radius: 8px;
}

.feature-card svg {
  width: 16px;
}

.feature-card h3 {
  margin: 29px 0 7px;
  color: var(--ink);
  font-size: 15px;
  letter-spacing: -.025em;
}

.feature-card p {
  max-width: 280px;
  margin: 0;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.65;
}

/* FAQ */
.faq {
  background: #fff;
}

.faq__inner {
  display: grid;
  grid-template-columns: .7fr 1.15fr;
  gap: 120px;
}

.faq__intro h2 {
  font-size: clamp(38px, 4vw, 54px);
}

.faq__list {
  border-top: 1px solid #dfe4ea;
}

.faq-row {
  border-bottom: 1px solid #dfe4ea;
}

.faq-row button {
  width: 100%;
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
  color: var(--ink);
  background: transparent;
  border: 0;
  text-align: left;
  cursor: pointer;
  font-size: 13px;
  font-weight: 750;
}

.faq-row button i {
  display: grid;
  place-items: center;
  width: 25px;
  height: 25px;
  color: #697484;
  border: 1px solid #dfe4ea;
  border-radius: 50%;
  font-style: normal;
  font-size: 15px;
  font-weight: 500;
}

.faq-row__answer {
  max-width: 680px;
  padding: 0 40px 23px 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
}

/* CTA */
.cta {
  position: relative;
  min-height: 470px;
  display: flex;
  align-items: center;
  overflow: hidden;
  color: #fff;
  background: var(--ink);
}

.cta__image {
  position: absolute;
  inset: 0 0 0 48%;
  background:
    linear-gradient(90deg, var(--ink) 0%, rgba(11,18,32,.72) 22%, rgba(11,18,32,.18) 100%),
    url("https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=1800&q=90") center/cover;
  opacity: .8;
}

.cta__inner {
  position: relative;
  z-index: 1;
}

.cta h2 {
  max-width: 620px;
  margin: 0;
  color: #fff;
  font-size: clamp(48px, 6vw, 76px);
  line-height: .95;
  letter-spacing: -.065em;
}

.cta__inner > p:not(.eyebrow) {
  max-width: 440px;
  margin: 20px 0 28px;
  color: #aeb8c7;
  font-size: 13px;
  line-height: 1.7;
}

.cta__inner > div:last-child {
  display: flex;
  gap: 10px;
}

.outline-btn--dark {
  color: #fff;
  background: transparent;
  border-color: rgba(255,255,255,.25);
}

.outline-btn--dark:hover {
  color: var(--ink);
  background: #fff;
}

/* Footer */
.footer {
  padding: 58px 0 22px;
  color: #8e98a7;
  background: #070b13;
}

.footer__grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 70px;
  padding-bottom: 55px;
}

.brand--footer {
  color: #fff;
}

.footer__grid > div:first-child p {
  max-width: 310px;
  margin: 17px 0 0;
  color: #7d8796;
  font-size: 11px;
  line-height: 1.7;
}

.footer__grid > div:not(:first-child) {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.footer small {
  margin-bottom: 5px;
  color: #fff;
  font-size: 9px;
  font-weight: 750;
}

.footer a:not(.brand) {
  color: #7d8796;
  text-decoration: none;
  font-size: 10px;
}

.footer a:not(.brand):hover {
  color: #fff;
}

.footer__bottom {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,.08);
  color: #596271;
  font-size: 9px;
}

/* Reveal */
[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity .75s ease, transform .75s cubic-bezier(.2,.7,.2,1);
}

[data-reveal].is-visible {
  opacity: 1;
  transform: none;
}

/* Responsive */
@media (max-width: 1100px) {
  .hero__inner {
    grid-template-columns: 1fr;
    gap: 45px;
  }

  .hero__copy {
    max-width: 780px;
  }

  .hero__visual {
    min-height: 560px;
  }

  .story__grid {
    gap: 55px;
  }

  .operator__inner {
    gap: 50px;
  }

  .faq__inner {
    gap: 60px;
  }
}

@media (max-width: 850px) {
  .container,
  .nav__inner {
    width: min(100% - 36px, 1240px);
  }

  .nav__links {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    display: none;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: 10px;
    background: #fff;
    border: 1px solid #e1e5ea;
    border-radius: 14px;
    box-shadow: 0 18px 40px rgba(11,18,32,.12);
  }

  .nav__links--open {
    display: flex;
  }

  .nav__links > a {
    padding: 12px;
  }

  .nav__mobile-actions {
    display: flex;
    gap: 7px;
    padding: 8px;
    border-top: 1px solid #edf0f3;
    margin-top: 4px;
  }

  .nav__mobile-actions .dark-btn {
    flex: 1;
  }

  .nav__actions > .text-btn,
  .nav__actions > .dark-btn {
    display: none;
  }

  .menu-btn {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    color: var(--ink);
    background: transparent;
    border: 0;
  }

  .menu-btn svg {
    width: 20px;
  }

  .hero {
    padding-top: 125px;
  }

  .hero h1 {
    font-size: clamp(46px, 10vw, 70px);
  }

  .hero__visual {
    min-height: 500px;
  }

  .story__grid,
  .operator__inner,
  .faq__inner {
    grid-template-columns: 1fr;
  }

  .story__image {
    height: 500px;
  }

  .flow {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .flow__line {
    width: 1px;
    height: 28px;
    margin-left: 30px;
  }

  .editorial-heading {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .facility-feature {
    grid-template-columns: 1fr;
  }

  .facility-feature__image {
    min-height: 400px;
  }

  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .faq__intro {
    max-width: 650px;
  }

  .footer__grid {
    grid-template-columns: 1.5fr 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .container,
  .nav__inner {
    width: calc(100% - 28px);
  }

  .nav {
    padding-top: 10px;
  }

  .nav__inner {
    min-height: 54px;
    padding-left: 12px;
  }

  .hero {
    padding-top: 105px;
    padding-bottom: 30px;
  }

  .hero__inner {
    gap: 35px;
  }

  .hero h1 {
    font-size: 48px;
  }

  .hero__lead {
    font-size: 14px;
  }

  .hero__meta {
    gap: 9px 13px;
  }

  .hero__visual {
    min-height: 410px;
  }

  .hero-photo {
    inset: 0 0 55px 0;
    border-radius: 18px;
  }

  .hero-photo__caption {
    left: 18px;
    bottom: 18px;
  }

  .hero-photo__caption strong {
    font-size: 18px;
  }

  .live-panel {
    width: calc(100% - 28px);
    left: 14px;
    padding: 14px;
    border-radius: 15px;
  }

  .parking-bay {
    height: 44px;
  }

  .moving-car {
    transform: translate(
      calc(var(--car-col, 0) * 22vw),
      calc(var(--car-row, 0) * -48px)
    );
  }

  .live-panel__bottom small {
    display: none;
  }

  .hero-search {
    grid-template-columns: 1fr;
    gap: 12px;
    margin-top: 0;
    padding: 17px;
  }

  .hero-search__divider {
    display: none;
  }

  .hero-search__button {
    justify-content: center;
  }

  .section {
    padding: 78px 0;
  }

  .story__image {
    height: 400px;
  }

  .story__copy h2,
  .section-heading h2,
  .editorial-heading h2,
  .faq__intro h2 {
    font-size: 40px;
  }

  .flow__item {
    min-height: 215px;
  }

  .facility-feature__image {
    min-height: 320px;
  }

  .facility-feature__content {
    padding: 32px 25px 36px;
  }

  .facility-secondary {
    grid-template-columns: 1fr;
  }

  .facility-small {
    grid-template-columns: 130px 1fr;
  }

  .operator h2 {
    font-size: 44px;
  }

  .dashboard-stage {
    padding: 10px;
    transform: none;
  }

  .dashboard-body {
    padding: 12px;
  }

  .dashboard-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .faq__inner {
    gap: 42px;
  }

  .faq-row button {
    min-height: 64px;
  }

  .cta {
    min-height: 440px;
  }

  .cta__image {
    inset: 0;
    opacity: .35;
  }

  .cta h2 {
    font-size: 52px;
  }

  .footer__grid {
    grid-template-columns: 1fr 1fr;
    gap: 35px;
  }

  .footer__grid > div:first-child {
    grid-column: 1 / -1;
  }

  .footer__bottom {
    flex-direction: column;
    gap: 8px;
  }
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .moving-car,
  .parking-bay,
  .blue-btn,
  .dark-btn,
  .arrow-link svg {
    transition: none;
  }
}
</style>
