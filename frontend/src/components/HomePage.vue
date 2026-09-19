<script>
export default {
    name: 'HomePage',
    data() {
        return {
            activeTab: 0,
            features: [
                {
                    badge: 'Real-Time Occupancy',
                    title: 'Live Bay-Level Tracking & Sensors',
                    description: 'Deploy ultrasonic and magnetic sensors across multi-level structures. Direct drivers to vacant spots instantly and minimize internal congestion.',
                    image: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1200&q=80',
                    stats: '99.4% Sensor Accuracy'
                },
                {
                    badge: 'Automated Access',
                    title: 'ANPR & Frictionless Entry Gates',
                    description: 'Eliminate paper tickets with high-speed Automatic Number Plate Recognition (ANPR) cameras that seamlessly lift barriers for pre-booked and VIP vehicles.',
                    image: 'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1200&q=80',
                    stats: '< 0.8s Gate Latency'
                },
                {
                    badge: 'Dynamic Pricing',
                    title: 'Yield Optimization Engine',
                    description: 'Maximize facility revenue with rule-based surge pricing during peak commuting hours, events, or weekends while offering loyalty discounts for regular visitors.',
                    image: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80',
                    stats: '+32% Average Yield'
                },
                {
                    badge: 'Smart Analytics',
                    title: 'Comprehensive Operations Dashboard',
                    description: 'Gain deep visibility into turnover rates, long-stay violators, peak utilization intervals, and financial reconciliations from a single centralized web console.',
                    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80',
                    stats: 'Real-Time Insights'
                }
            ],
            testimonials: [
                {
                    quote: 'Integrating ParkSync across our commercial plazas reduced morning entry queues by over 70%. It transformed our tenant satisfaction scores.',
                    author: 'Vikram Malhotra',
                    role: 'Director of Real Estate, Apex Towers',
                    image: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
                },
                {
                    quote: 'The ANPR recognition and automated billing platform run completely hands-free. Maintenance tickets dropped dramatically within the first month.',
                    author: 'Ananya Deshmukh',
                    role: 'Operations Head, Metro Spaces',
                    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'
                }
            ],
            faqs: [
                {
                    question: 'How does the hardware integrate with existing boom barriers?',
                    answer: 'ParkSync communicates via standard Wiegand and TCP/IP protocols, making it fully compatible with almost all commercial gate barriers, RFID readers, and loop detectors currently installed.'
                },
                {
                    question: 'Can visitors book parking spaces without downloading a mobile app?',
                    answer: 'Yes! Our progressive web app and instant QR-code gate kiosks allow drivers to check-in, select slots, and complete digital payments seamlessly through their phone browser.'
                },
                {
                    question: 'What happens if internet connectivity drops temporarily at the gate?',
                    answer: 'Our smart controllers feature offline local caching. ANPR matching, whitelist validations, and barrier operations continue smoothly and sync automatically once connectivity is restored.'
                },
                {
                    question: 'How are digital payments processed and secured?',
                    answer: 'All transactions are encrypted and processed through PCI-DSS Level 1 compliant gateways supporting major credit cards, UPI, digital wallets, and corporate billing accounts.'
                }
            ],
            activeFaq: null
        };
    },
    methods: {
        goToLogin() {
            if (this.$router) {
                this.$router.push('/login');
            } else {
                window.location.href = '/login';
            }
        },
        toggleFaq(index) {
            this.activeFaq = this.activeFaq === index ? null : index;
        }
    }
}
</script>

<template>
    <div class="park-landing light-theme">
        <!-- Navigation Bar -->
        <header class="navbar">
            <div class="nav-container">
                <div class="brand">
                    <div class="brand-logo-mark">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
                            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <span class="brand-name">ParkSync</span>
                </div>
                <nav class="nav-menu">
                    <a href="#features">Features</a>
                    <a href="#solutions">Solutions</a>
                    <a href="#pricing">Pricing</a>
                    <a href="#testimonials">Company</a>
                </nav>
                <div class="nav-actions">
                    <button class="btn-login-pill" @click="goToLogin">Secure Portal Login</button>
                </div>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-container">
                <div class="hero-content">
                    <h1 class="hero-title">
                        Effortless Parking Management. <br />
                        <span class="highlight-text">Elevated Experiences.</span>
                    </h1>
                    <p class="hero-subtitle">
                        Smart, real-time solutions for seamless access, dynamic pricing, and intelligent operations. Join the future of mobility.
                    </p>
                    <div class="hero-buttons">
                        <button class="btn-dark-pill" @click="goToLogin">
                            Request a Demo
                        </button>
                        <a href="#features" class="btn-outline-pill">Explore Platform</a>
                    </div>
                </div>
            </div>
            <div class="hero-image-showcase">
                <div class="container">
                    <div class="hero-banner-frame">
                        <img src="https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1600&q=80" alt="Underground Parking Facility" />
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Interactive Tabs Section -->
        <section id="features" class="features-section">
            <div class="container">
                <div class="section-title-wrapper">
                    <h2>Precision & Intelligence</h2>
                </div>

                <div class="feature-tabs-header">
                    <button 
                        v-for="(feat, idx) in features" 
                        :key="idx"
                        :class="['tab-btn-pill', { active: activeTab === idx }]"
                        @click="activeTab = idx"
                    >
                        <span class="tab-number">0{{ idx + 1 }}</span>
                        {{ feat.badge }}
                    </button>
                </div>

                <div class="feature-showcase-box" v-for="(feat, idx) in features" :key="'showcase-' + idx" v-show="activeTab === idx">
                    <div class="feature-text-pane">
                        <span class="sub-badge">{{ feat.badge }}</span>
                        <h3>{{ feat.title }}</h3>
                        <p>{{ feat.description }}</p>
                        <div class="feature-highlight-stat">
                            <i class="fas fa-check-circle"></i>
                            <span>{{ feat.stats }}</span>
                        </div>
                        <button class="btn-dark-pill mt-4" @click="goToLogin">
                            <span>Access Module</span>
                        </button>
                    </div>
                    <div class="feature-image-pane">
                        <img :src="feat.image" :alt="feat.title" />
                    </div>
                </div>
            </div>
        </section>

        <!-- Architecture & Security Callout -->
        <section id="solutions" class="architecture-section">
            <div class="container architecture-container">
                <div class="arch-content">
                    <h2>Enterprise-Grade Security & Cloud Sync</h2>
                    <p>Built on a robust microservices architecture ensuring absolute data privacy, fault tolerance, and rapid integration with existing ERP and billing solutions.</p>
                    <ul class="arch-checklist">
                        <li><i class="fas fa-check"></i> End-to-end encrypted vehicle telemetry and payment rails</li>
                        <li><i class="fas fa-check"></i> Multi-tenant role-based access control (RBAC)</li>
                        <li><i class="fas fa-check"></i> Automated daily backups with instant disaster recovery</li>
                    </ul>
                </div>
                <div class="arch-image-wrapper">
                    <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=80" alt="Analytics Dashboard UI" />
                </div>
            </div>
        </section>

        <!-- Testimonials -->
        <section id="testimonials" class="testimonials-section">
            <div class="container">
                <div class="section-title-wrapper">
                    <h2>Trusted by Industry Leaders</h2>
                    <p>See what property managers and operations executives have to say about ParkSync.</p>
                </div>
                <div class="testimonials-grid">
                    <div class="testimonial-card" v-for="(item, i) in testimonials" :key="i">
                        <p class="quote">"{{ item.quote }}"</p>
                        <div class="client-profile">
                            <img :src="item.image" :alt="item.author" />
                            <div>
                                <h4>{{ item.author }}</h4>
                                <span>{{ item.role }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        <section id="faq" class="faq-section">
            <div class="container">
                <div class="section-title-wrapper">
                    <h2>Frequently Asked Questions</h2>
                    <p>Everything you need to know about implementing and using ParkSync.</p>
                </div>
                <div class="faq-accordion">
                    <div 
                        v-for="(faq, fIdx) in faqs" 
                        :key="fIdx" 
                        :class="['faq-card', { open: activeFaq === fIdx }]"
                        @click="toggleFaq(fIdx)"
                    >
                        <div class="faq-question-row">
                            <h4>{{ faq.question }}</h4>
                            <div class="faq-icon-toggle">
                                <i :class="['fas', activeFaq === fIdx ? 'fa-minus' : 'fa-plus']"></i>
                            </div>
                        </div>
                        <div class="faq-answer-row" v-show="activeFaq === fIdx">
                            <p>{{ faq.answer }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="container footer-container">
                <div class="footer-info">
                    <div class="brand">
                        <div class="brand-logo-mark dark">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <span class="brand-name dark">ParkSync</span>
                    </div>
                    <p>Redefining parking infrastructure through intelligent automation and real-time cloud management.</p>
                </div>
                <div class="footer-links-group">
                    <h4>Platform</h4>
                    <a href="#features">Occupancy Tracking</a>
                    <a href="#features">ANPR Gates</a>
                    <a href="#features">Dynamic Pricing</a>
                </div>
                <div class="footer-links-group">
                    <h4>Solutions</h4>
                    <a href="#solutions">Commercial Malls</a>
                    <a href="#solutions">Corporate Campuses</a>
                    <a href="#solutions">Airports & Hubs</a>
                </div>
                <div class="footer-cta-group">
                    <h4>Ready to Upgrade?</h4>
                    <p>Access the management portal or schedule an enterprise consultation.</p>
                    <button class="btn-dark-pill" @click="goToLogin">Portal Login</button>
                </div>
            </div>
            <div class="footer-bottom">
                <div class="container footer-bottom-flex">
                    <p>&copy; 2026 ParkSync Technologies Inc. All rights reserved.</p>
                    <div class="legal-links">
                        <a href="#">Privacy Policy</a>
                        <a href="#">Terms of Service</a>
                        <a href="#">Security Statement</a>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<style scoped>
.park-landing.light-theme {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
    background-color: #fafbfc;
    min-height: 100vh;
    text-align: left;
    overflow-x: hidden;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
}

/* Navbar matches reference image */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid #edf2f7;
    z-index: 1000;
}

.nav-container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 76px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}

.brand-logo-mark {
    width: 34px;
    height: 34px;
    background: #0f172a;
    color: #ffffff;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.brand-logo-mark.dark {
    background: #ffffff;
    color: #0f172a;
}

.brand-name {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}

.brand-name.dark {
    color: #ffffff;
}

.nav-menu {
    display: flex;
    gap: 2.5rem;
}

.nav-menu a {
    color: #64748b;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}

.nav-menu a:hover {
    color: #0f172a;
}

.btn-login-pill {
    background: #0f172a;
    color: #ffffff;
    border: 1px solid #0f172a;
    padding: 0.55rem 1.35rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

.btn-login-pill:hover {
    background: #1e293b;
}

/* Hero Section */
.hero {
    padding: 130px 0 60px 0;
    background: #fafbfc;
    text-align: center;
}

.hero-container {
    width: 90%;
    max-width: 900px;
    margin: 0 auto;
}

.hero-title {
    font-size: 3.4rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    letter-spacing: -1.5px;
    margin-bottom: 1.25rem;
    font-family: 'Playfair Display', serif, sans-serif;
}

.highlight-text {
    font-family: 'Playfair Display', serif, sans-serif;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 2rem;
    max-width: 640px;
    margin-left: auto;
    margin-right: auto;
}

.hero-buttons {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3.5rem;
}

.btn-dark-pill {
    background: #0f172a;
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.6rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
    transition: transform 0.2s ease;
}

.btn-dark-pill:hover {
    transform: translateY(-2px);
}

.btn-outline-pill {
    background: transparent;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.75rem 1.6rem;
    border-radius: 40px;
    transition: background 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.btn-outline-pill:hover {
    background: #f1f5f9;
}

.hero-image-showcase {
    padding: 0 1rem;
}

.hero-banner-frame {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
    border: 1px solid #e2e8f0;
}

.hero-banner-frame img {
    width: 100%;
    height: 480px;
    object-fit: cover;
    display: block;
}

/* Features Section */
.features-section {
    padding: 100px 0;
    background: #ffffff;
}

.section-title-wrapper {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 50px auto;
}

.section-title-wrapper h2 {
    font-size: 2.4rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    font-family: 'Playfair Display', serif, sans-serif;
}

.section-title-wrapper p {
    color: #64748b;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

.feature-tabs-header {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 40px;
    flex-wrap: wrap;
}

.tab-btn-pill {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #64748b;
    padding: 0.75rem 1.4rem;
    border-radius: 30px;
    font-weight: 650;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
}

.tab-btn-pill .tab-number {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 700;
}

.tab-btn-pill.active {
    background: #fef3c7;
    color: #92400e;
    border-color: #f59e0b;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
}

.tab-btn-pill.active .tab-number {
    color: #b45309;
}

.feature-showcase-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 50px;
    display: flex;
    align-items: center;
    gap: 50px;
}

.feature-text-pane {
    flex: 1;
}

.sub-badge {
    background: #fef3c7;
    color: #92400e;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 1rem;
}

.feature-text-pane h3 {
    font-size: 2rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1rem;
    letter-spacing: -0.5px;
}

.feature-text-pane p {
    color: #64748b;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}

.feature-highlight-stat {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #059669;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

.feature-image-pane {
    flex: 1;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #cbd5e1;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
}

.feature-image-pane img {
    width: 100%;
    height: 340px;
    object-fit: cover;
    display: block;
}

/* Architecture Section */
.architecture-section {
    padding: 90px 0;
    background: #fafbfc;
    border-top: 1px solid #edf2f7;
}

.architecture-container {
    display: flex;
    align-items: center;
    gap: 50px;
}

.arch-content {
    flex: 1;
}

.arch-content h2 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 1rem;
    letter-spacing: -0.5px;
}

.arch-content p {
    color: #64748b;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}

.arch-checklist {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.arch-checklist li {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #334155;
    font-weight: 500;
    font-size: 0.95rem;
}

.arch-checklist li i {
    width: 22px;
    height: 22px;
    background: #d1fae5;
    color: #059669;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
}

.arch-image-wrapper {
    flex: 1;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.06);
}

.arch-image-wrapper img {
    width: 100%;
    height: 350px;
    object-fit: cover;
    display: block;
}

/* Testimonials */
.testimonials-section {
    padding: 100px 0;
    background: #ffffff;
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
}

.testimonial-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 35px;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.testimonial-card .quote {
    font-size: 1.05rem;
    color: #334155;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    font-style: italic;
}

.client-profile {
    display: flex;
    align-items: center;
    gap: 14px;
}

.client-profile img {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
}

.client-profile h4 {
    font-size: 0.98rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 2px 0;
}

.client-profile span {
    font-size: 0.82rem;
    color: #64748b;
}

/* FAQ Section */
.faq-section {
    padding: 100px 0;
    background: #fafbfc;
    border-top: 1px solid #edf2f7;
}

.faq-accordion {
    max-width: 780px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.faq-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.faq-card:hover {
    border-color: #cbd5e1;
}

.faq-question-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.faq-question-row h4 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}

.faq-icon-toggle {
    width: 28px;
    height: 28px;
    background: #f1f5f9;
    color: #475569;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
}

.faq-answer-row {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #edf2f7;
}

.faq-answer-row p {
    color: #64748b;
    line-height: 1.6;
    font-size: 0.95rem;
    margin: 0;
}

/* Footer */
.footer {
    background: #0f172a;
    color: #94a3b8;
    padding-top: 70px;
}

.footer-container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.5fr;
    gap: 3rem;
    padding-bottom: 50px;
}

.footer-info p {
    color: #94a3b8;
    margin-top: 1rem;
    line-height: 1.6;
    font-size: 0.9rem;
    max-width: 300px;
}

.footer-links-group h4 {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.footer-links-group a {
    display: block;
    color: #94a3b8;
    text-decoration: none;
    margin-bottom: 0.7rem;
    font-size: 0.9rem;
    transition: color 0.2s ease;
}

.footer-links-group a:hover {
    color: #ffffff;
}

.footer-cta-group h4 {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.7rem;
}

.footer-cta-group p {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.footer-bottom {
    border-top: 1px solid #1e293b;
    padding: 25px 0;
}

.footer-bottom-flex {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-bottom-flex p {
    color: #64748b;
    font-size: 0.82rem;
    margin: 0;
}

.legal-links {
    display: flex;
    gap: 1.5rem;
}

.legal-links a {
    color: #64748b;
    text-decoration: none;
    font-size: 0.82rem;
    transition: color 0.2s;
}

.legal-links a:hover {
    color: #ffffff;
}

@media (max-width: 968px) {
    .hero-container, .architecture-container, .feature-showcase-box {
        flex-direction: column;
    }
    .hero-title {
        font-size: 2.5rem;
    }
    .nav-menu {
        display: none;
    }
    .footer-container {
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
    .testimonials-grid {
        grid-template-columns: 1fr;
    }
}
</style>