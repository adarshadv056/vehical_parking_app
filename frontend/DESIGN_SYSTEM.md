# Vehicle Parking App — Design System

## 1. Design Direction

The application should feel like a premium modern mobility product.

Visual inspiration:
- premium automotive websites
- modern parking/mobility applications
- editorial product websites
- high-end SaaS interfaces

The reference screenshots are the PRIMARY visual references which are present in design_reference folder.

Do NOT copy any reference literally.

Extract the visual language:
- typography
- spacing
- composition
- whitespace
- image treatment
- card styling
- visual hierarchy
- premium automotive/mobility feeling

The result should NOT look like:
- a generic admin dashboard
- a typical Bootstrap template
- a generic SaaS landing page
- a generic parking-management UI
- an AI-generated gradient website

---

# 2. Brand Personality

The product should feel:

- Premium
- Modern
- Reliable
- Intelligent
- Minimal
- Confident
- Automotive / mobility focused

Avoid:
- childish
- overly colorful
- excessive gradients
- excessive glassmorphism
- neon/futuristic styling
- excessive animations

---

# 3. Color System

Primary brand color:
#2563EB

Deep navy:
#0B1220

Primary text:
#111827

Page background:
#F7F9FC

White:
#FFFFFF

Soft blue:
#EAF2FF

Blue hover:
#1D4ED8

Border:
#E5E7EB

Semantic colors:

Available:
#16A34A

Occupied:
#EF4444

Warning:
#F59E0B

IMPORTANT:

Blue is the brand color.

Green is NOT the brand color.

Green should only communicate availability/success.

Red should communicate occupied/error.

Amber should communicate warning.

Do not make the entire UI blue.

The premium visual language should primarily come from:
white + off-white + navy + black + restrained blue accents.

---

# 4. Typography

Use one primary modern sans-serif typeface throughout the product.

Preferred direction:
Manrope / Geist / Satoshi-like typography.

Typography hierarchy:

12px - metadata / labels
14px - secondary text
16px - body
18px - card titles
24px - component headings
32-40px - page headings
56-80px - landing page hero headings

Landing page typography should be bold and editorial.

Application typography should be cleaner and more compact.

Avoid excessive font weights.

---

# 5. Spacing

Use a consistent spacing system.

Base unit:
4px

Preferred spacing:
4
8
12
16
20
24
32
40
48
64
80
96
120

Marketing pages should use generous whitespace.

Application pages should be more compact.

---

# 6. Border Radius

Small:
8-10px

Medium:
12-16px

Large:
20-24px

Hero / major visual containers:
24-32px

Avoid excessive pill-shaped UI.

Use pills primarily for:
- status
- filters
- small metadata
- tags

---

# 7. Borders & Shadows

Prefer borders over heavy shadows.

Default border:
1px solid #E5E7EB

Shadows should be:
- subtle
- soft
- used mainly for floating cards/modals

Avoid:
- heavy drop shadows
- glowing effects
- excessive neumorphism

---

# 8. Buttons

Primary:

Blue background
White text

Secondary:

White background
Dark text
Subtle border

Dark:

Deep navy background
White text

Buttons should generally have:
- 12-16px radius
- medium/bold typography
- comfortable horizontal padding

Primary CTAs should be visually strong but not oversized.

---

# 9. Landing Page Direction

The landing page should feel closer to a premium automotive/mobility website than a SaaS template.

Structure:

1. Minimal navbar
2. Large editorial hero
3. Animated parking visualization
4. Product story
5. How parking works
6. Product/dashboard showcase
7. Feature section
8. Parking analytics / management story
9. Final CTA
10. Footer

The landing page should use:
- large typography
- generous whitespace
- large visual compositions
- premium parking/automotive imagery
- asymmetric layouts where appropriate
- subtle animation

---

# 10. Hero Concept

The hero should communicate:

Find parking.
Reserve your space.
Park without hassle.

Avoid generic stock-dashboard hero sections.

The hero should contain a visually interesting parking-system visualization.

Preferred concept:

An animated parking grid showing available and occupied spaces.

Example:

A01 A02 A03 A04
A05 A06 A07 A08
A09 A10 A11 A12

A vehicle/marker can move toward an available parking spot.

One spot becomes occupied.

The availability count updates.

Example:

12 available
↓
11 available

This should feel like a product visualization, not a game.

---

# 11. Hero Animation

Build the parking visualization using SVG/CSS/JavaScript where practical.

Do NOT use a video.

Do NOT introduce a heavy 3D engine unless there is a compelling reason.

Animation sequence:

1. Parking lot is displayed.
2. Available spots subtly pulse/highlight.
3. A vehicle/marker enters.
4. It moves toward an available space.
5. The space transitions into occupied state.
6. Availability count updates.
7. UI settles.

Animation should be smooth and restrained.

Use animation primarily to communicate the product.

---

# 12. Scroll Animations

Use subtle scroll-based animation:

- fade-in
- translate-up
- image reveal
- number count-up
- section transitions

Avoid excessive:
- parallax
- floating elements
- particles
- spinning objects
- cursor effects

The site should feel premium, not like an animation showcase.

---

# 13. User Application

The authenticated application should use a different density from the marketing page.

Application style:

- clean
- structured
- data-focused
- premium
- calm

Suggested layout:

Sidebar
+
Top navigation
+
Main content

User dashboard should contain:

- active parking
- available parking
- parking statistics
- recent activity
- quick actions

---

# 14. Parking Lot Cards

Parking lots should be visually strong.

Card information:

Parking lot name
Location
Available spots
Total spots
Price/hour
Availability indicator
Primary action

Example:

City Center Garage

18 / 24 available

₹40 / hour

[ Park here ]

Use parking imagery selectively.

---

# 15. Parking Spot Visualization

Parking spots are a signature UI element.

States:

AVAILABLE
- white / very light blue
- blue outline or subtle blue accent

OCCUPIED
- muted red indicator
- darker visual treatment

SELECTED
- primary blue

The grid should look like actual parking bays rather than simple text labels.

---

# 16. Admin Dashboard

Admin UI should feel like a control center.

Use:

- KPI cards
- occupancy charts
- revenue charts
- parking lot cards
- parking grid
- users table

Prioritize information hierarchy.

The admin should immediately understand:

- number of lots
- total spots
- occupied spots
- available spots
- revenue
- recent activity

---

# 17. Imagery

Use premium automotive / architectural photography.

Preferred subjects:

- modern parking garages
- underground parking
- urban parking
- parking entrances
- premium cars in parking environments
- aerial parking facilities
- architectural parking structures

Avoid generic:
- smiling people
- corporate office stock photos
- random cars on roads
- unrelated technology imagery

Images should have a consistent visual tone.

---

# 18. Important Technical Constraint

This is an EXISTING APPLICATION.

Do NOT rewrite the architecture.

Preserve:

- Vue
- Flask
- Bootstrap
- SQLite
- Redis
- Celery
- JWT authentication
- existing API contracts
- database models
- parking allocation logic
- background jobs

Do NOT migrate to:
- React
- Next.js
- Tailwind
- PostgreSQL
- FastAPI

unless explicitly requested.

The primary goal is a frontend/product redesign.

---

# 19. Component Strategy

Create reusable components before redesigning pages.

Examples:

AppShell
Navbar
Sidebar
PageHeader
Button
Card
StatCard
StatusBadge
ParkingLotCard
ParkingSpot
ParkingGrid
ChartCard
DataTable
Modal
EmptyState
LoadingState
Toast

Pages should compose these components rather than duplicating styles.

---

# 20. Responsive Design

The product must work on:

- desktop
- tablet
- mobile

Marketing:
mobile-first responsive layout.

Application:
desktop sidebar
→ collapsible/mobile navigation on smaller screens.

Never simply shrink the desktop layout.

Reflow components appropriately.

---

# 21. Design Principle

The final product should look like a real mobility product that could be launched commercially.

It should NOT look like:

"college project + prettier Bootstrap."

The underlying functionality is from the college project.

The visual/product presentation should feel production-grade.