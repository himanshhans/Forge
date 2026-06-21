# AI Portfolio Generator - Full Development Plan(working title - "Forge")

## Project Overview

**Product**: AI-powered, multi-niche portfolio & landing page generator
**Tagline**: "Your portfolio live in 3 minutes. No code. Just results."
**Core Value Prop**: 
- Ultra-fast portfolio/landing page creation (3 minutes end-to-end)
- SEO-optimized, deployment-ready pages
- One-click deployment (live immediately on custom subdomain or custom domain)
- Community showcase gallery by niche (network effects + discovery)
- No-code, no technical skills required
- Export-ready (HTML/CSS ownership, no vendor lock-in)
- Niche-optimized generation (questionnaire & design tailored to user type)

**Target Users** (Phased Approach):
- **Phase 1 Launch Focus**: Indie Hackers + Freelancers (designers, developers, writers)
- **Phase 1+ Expansion**: Creators (YouTubers, streamers), Coaches/Consultants, Small Agencies
- **All users**: Non-technical makers who need professional online presence

**Supported Niches**:
1. **Indie Hackers**: Shipped products, revenue, metrics, GitHub/ProductHunt showcase
2. **Freelancers**: Portfolios, case studies, pricing, testimonials, booking integration
3. **Creators**: Social stats, video embeds, Patreon/sponsorship links, community
4. **Coaches/Consultants**: Services, credentials, testimonials, booking/calendar link
5. **Small Agencies**: Team showcase, case studies, services, client list

**Success Metrics**:
- Time to first deployed portfolio: <5 minutes
- Portfolio sites ranking for user's name + "portfolio" in Google within 2 weeks
- Community showcase becomes destination (1000+ portfolios by month 2, high SEO authority)
- User retention: >40% return after 1 month
- Niche diversity: >20% from each of top 3 niches
- NPS > 50

---

---

## Differentiation Strategy

**How we win against Wix, Framer, and other generic tools:**

### 1. Hyper-Speed + Simplicity
- **What**: Go from zero to live in <5 minutes
- **How**: 
  - Minimal questionnaire (5-8 questions, no "advanced settings")
  - One-click generation (no multi-step builders)
  - Automatic deployment (no export/upload steps)
- **Result**: Immediate gratification. Users share it because it's shocking fast.

### 2. Niche-First Approach
- **What**: Tailor everything to user type (indie hacker, freelancer, creator, etc.)
- **How**: 
  - Niche selector upfront (sets tone for entire experience)
  - Different questionnaires per niche (relevant questions only)
  - Niche-specific generation prompts (outputs speak to their buyer)
  - Showcase galleries per niche (indie hacker gallery ≠ freelancer gallery)
- **Result**: Sites feel personal, not generic. "This tool gets me."

### 3. Unique Output (Not Template Remix)
- **What**: AI-generated layouts, not fill-in-the-blank templates
- **How**: 
  - Claude generates custom layouts based on niche + content
  - No shared template pool (each site can be visually distinct)
  - AI makes design decisions (layout, hierarchy, colors)
- **Result**: Sites don't look like "another Wix site"

### 4. Built-In SEO Excellence
- **What**: Sites ranked by Google immediately
- **How**: 
  - Auto-generate optimized meta tags, og tags, structured data (JSON-LD)
  - SEO schema varies by niche (person/portfolio for indie hackers, localBusiness for agencies)
  - All sites indexed by Google within days
  - Showcase gallery itself becomes high-authority destination
- **Result**: Users get organic traffic faster than typical portfolio tools

### 5. Export-First Philosophy
- **What**: Users own their portfolios. Zero vendor lock-in.
- **How**: 
  - Free subdomain via wildcard-serve (`you.forge.app`, instant, zero setup)
  - Support custom domain (CNAME setup, user owns domain)
  - Option to export raw HTML/CSS (future: GitHub repo sync)
  - No proprietary storage format
- **Result**: Trust + power. Users can leave whenever, but won't because of value.

### 6. Smart Iteration Loop
- **What**: Don't regenerate from scratch. Improve incrementally.
- **How**: 
  - "Regenerate this section" instead of full page regenerate
  - "Make it more professional" / "Add social proof" → AI tweaks locally
  - Preserve user customizations between iterations
- **Result**: Faster refinement, less frustration.

### 7. Community + Network Effects
- **What**: Gallery becomes destination for discovery
- **How**: 
  - Per-niche showcases (indie hacker gallery, freelancer gallery, etc.)
  - Featured portfolios (weekly rotation, social proof)
  - User profiles (see all portfolios from one creator)
  - Niche-specific metrics (indie hackers: sort by revenue; creators: sort by subscribers)
  - SEO benefits flow back to us (showcase gets traffic)
- **Result**: Flywheel: more portfolios → bigger gallery → more traffic → more users

### 8. Integration-Ready Foundation
- **What**: Build hooks for integrations from day 1
- **How**: 
  - GitHub API (pull repos, stars, languages)
  - ProductHunt API (pull product ranking, reviews)
  - Social APIs (pull subscriber counts, embeds)
  - Stripe (future: integrated payment on portfolios)
  - Calendly/Stripe integration (future: booking + payments on site)
- **Result**: Portfolios become powerful tools, not just bios.

---

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND - WEB                                 │
│  Next.js 14 + React + Tailwind + Shadcn/UI                  │
│  - Landing page (multi-niche positioning)                   │
│  - Niche selector (user picks their type)                   │
│  - Dynamic questionnaire (tailored to niche)                │
│  - Avatar customization (3D, 2D, AI photo)                  │
│  - Introduction card editor                                 │
│  - Live preview/editor                                      │
│  - Gallery/showcase (filterable by niche)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────┐
│              BACKEND - DJANGO REST API                       │
│  Django 4.2 + DRF + Celery (async)                           │
│                                                              │
│  ├─ Auth (Clerk JWT verify + webhook sync)                   │
│  ├─ Generation API (portfolio + avatar)                      │
│  ├─ Publish API (wildcard-serve; custom domain = Pro)        │
│  ├─ Gallery API (showcase = DB view)                         │
│  ├─ Avatar Generation Service                                │
│  │  ├─ Groq API calls (portfolio text)                       │
│  │  ├─ Replicate integration (image gen)                     │
│  │  └─ ReadyPlayer.me API (3D avatars)                       │
│  └─ File Storage (Cloudflare R2)                             │ 
└──────────────────────────┬───────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Groq API        │ │  Replicate API   │ │ Wildcard-serve   │
│                  │ │  + ReadyPlayer   │ │ + Cloudflare     │
│ - Portfolio Gen  │ │                  │ │ - *.forge.app    │
│ - Llama 3.1      │ │ - Image gen      │ │ - CDN cache      │
│ - Structured     │ │ - Avatar gen     │ │ - Custom domains │
│   output         │ │ - Image upscale  │ │   (Pro, CF SaaS) │
└──────────────────┘ └──────────────────┘ └──────────────────┘
        │                    │                        │
        └────────────────────┼────────────────────────┘
                             │
┌──────────────────────────────────────────────────────────────┐
│              DATABASE - NEON (PostgreSQL)                    │
│                                                              │
│  - Users, Portfolios, Niches, Gallery Index                  │
│  - Avatar metadata, Introduction cards                       │
│  - Deployment history, Analytics                             │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              FRONTEND - MOBILE (React Native)                │
│  Expo + React Native + NativeWind                            │
│  - Questionnaire builder (native UI)                         │
│  - Avatar customization (native)                             │
│  - Live preview (Skia for 3D)                                │
│  - Gallery browsing                                          │
│  - Push notifications                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend - Web
```
Framework:       Next.js 14 (App Router)
UI Library:      React 18
Styling:         Tailwind CSS 4
Component Lib:   Shadcn/ui
Form Handling:   React Hook Form
Validation:      Zod
Styling:         Tailwind CSS 3 (Shadcn-stable)
API Client:      TanStack Query (React Query) + Axios
Auth:            Clerk (Clerk issues JWT; Django verifies)
State:           Zustand (client state) + TanStack Query (server state)
Animations:      Framer Motion (optional, polish phase)
Code Editor:     Monaco Editor (for HTML/CSS editing)
Avatar Preview:  Three.js (for 3D avatars) + Canvas (for 2D)
Hosting:         Vercel (Next.js app) — see Deployment Architecture
```

### Frontend - Mobile
```
Framework:       React Native (Expo)
State Mgmt:      Zustand + TanStack Query (match web; shared api-client)
Navigation:      Expo Router
UI Components:   React Native Paper
Styling:         NativeWind (Tailwind 3 for RN)
API Client:      Axios + Interceptors (shared thin client)
Auth:            Clerk Expo SDK
Avatar Preview:  React Native Skia (3D) + react-native-svg
Deployment:      Expo Go (development) → EAS Build (production)
Platform:        iOS + Android (via EAS)
```

### Backend - API Server
```
Runtime:         Python 3.11+
Framework:       Django 4.2 + Django REST Framework
Database ORM:    Django ORM (NOT Prisma — Prisma is Node-only)
Authentication:  Clerk (verify Clerk JWT via JWKS; PyJWT). Django does NOT issue tokens.
Rate Limiting:   DRF throttling (UserRateThrottle, ScopedRateThrottle) + Redis backend
Async Tasks:     Celery + Redis
File Upload:     django-storages (S3/R2)
Image Processing: Pillow, opencv-python
Validation:      Pydantic + DRF serializers
API Versioning:  /api/v1/
Docs:            drf-spectacular (OpenAPI 3.0)
CORS:            django-cors-headers
Hosting:         Railway, Render, or Fly.io (serverless Python)
```

### Database
```
Primary DB:      Neon (PostgreSQL 15+)
Connection:      psycopg2 + Django ORM
Migrations:      Django migrations
Caching Layer:   Redis (via Neon's Redis add-on or separate service)
Backup:          Neon auto-backups (7-30 days)
```

### AI / Content Generation
```
Portfolio LLM:   Groq API — model via GROQ_MODEL env var (verify live catalog; Llama 3.1 70B likely retired, use current flagship e.g. Llama 3.3 70B)
Fallback LLM:    Together.ai (verify pricing/availability before relying on free tier)
Avatar Gen:      Replicate API (Stable Diffusion)
Avatar 3D:       ReadyPlayer.me API (free, WebGL)
Image Resizing:  Python Pillow (self-hosted)
Prompt Mgmt:     Stored in Django models + env variables
Cost per 1K gens: ~$0.10-0.20 (vs $6 with Claude)
```

### File Storage & CDN
```
Generated Sites: Wildcard-serve from Next.js app (*.forge.app), HTML in DB/R2
                 Custom domains (Pro): Cloudflare for SaaS OR Netlify per-site
User Avatars:    Cloudflare R2 (S3-compatible)
Portfolio Assets: Cloudflare R2 + Cloudflare CDN
DNS/Domains:     Cloudflare (wildcard + custom hostnames)
```

### Deployment Architecture (KEY DECISION)
Two models considered:
- **Model A — per-site deploy**: each portfolio = own Netlify/Vercel site. Doesn't scale
  (10K portfolios = 10K sites, platform limits, slow deploys, global updates require redeploy-all).
- **Model B — wildcard-serve (CHOSEN)**: store generated HTML/CSS in DB/R2, serve all
  portfolios via Next.js catch-all route on wildcard `*.forge.app`. Cloudflare CDN in front.

Decision:
- **Free tier** → wildcard-serve (`you.forge.app`). Instant publish, no deploy wait, infinite scale.
- **Pro custom domain** → Cloudflare for SaaS (custom hostnames + auto SSL); Netlify per-site optional fallback.
- During create flow, ask user: "Free subdomain" (default) or "Connect custom domain" (Pro).

### Development & DevOps
```
Backend Testing:  pytest + pytest-django
Frontend Testing: Vitest + React Testing Library
E2E Testing:     Playwright
Version Control: GitHub
CI/CD:           GitHub Actions (auto-deploy on push)
Monitoring:      Sentry (errors) + DataDog (performance)
Logging:         Python logging + Structured logs (JSON)
Environment:     .env (local), Railway/Render (production)
```

### Niche Configurations

**Niche Config Structure** (stored in `niche_config` JSONB field):
```json
{
  "niche_id": "indie_hacker",
  "display_name": "Indie Hacker",
  "description": "Showcase products you shipped, revenue, and metrics",
  "icon": "rocket",
  "color": "#3b82f6",
  "questionnaire_fields": ["name", "headline", "projects", "revenue", "github", "producthunt"],
  "generation_prompt": "indie_hacker_prompt_v1",
  "showcase_metrics": ["revenue", "users", "projects_shipped"],
  "default_cta": "Get in touch",
  "seo_schema": "Person + Portfolio",
  "example_portfolio": "/showcase/johndoe-indie"
}
```

**Per-Niche Details**:

| Niche | Questionnaire Fields | Generation Focus | Showcase Sort By | Default CTAs |
|-------|-------------------|------------------|-----------------|--------------|
| **Indie Hacker** | Name, projects, revenue, GitHub, ProductHunt, tech stack, "looking for" | Revenue/metrics, GitHub showcase, product traction, investor-ready | Revenue, users, projects | "Let's build together", "Hire me as co-founder" |
| **Freelancer** | Name, services, past work (images), rates, testimonials, booking link, availability | Portfolio grid, case studies, rates/packages, testimonials section | Service category, rating, reviews | "Hire me", "Book a call", "View rates" |
| **Creator** | Name, content type, YouTube/Twitch/TikTok links, subscriber counts, Patreon/Ko-fi | Recent videos embed, subscriber metrics, sponsorship/support links | Followers, engagement rate, video count | "Subscribe", "Join Patreon", "Follow me" |
| **Coach/Consultant** | Name, expertise, credentials, services offered, testimonials, Calendly link | Services grid, credentials/certifications, success stories, booking button | Specialty, rating, testimonial count | "Book a call", "Schedule 1:1", "Get started" |
| **Agency** | Company name, tagline, services, team members, case studies, tech stack, contact | Team showcase, case study portfolio, capabilities matrix, contact form | Specialization, team size, client count | "Get a quote", "Start project", "Schedule consultation" |

**How Niches Work in the System**:
- User selects niche during signup
- Questionnaire form dynamically renders relevant fields
- AI generation prompt adjusts based on niche
- Showcase gallery filters/sorts per niche
- SEO schema (JSON-LD) changes per niche
- CTA buttons and text adapt to niche context

---

### Rate Limiting & Free-Tier Enforcement

**Free-tier limits**: 1 portfolio + 1 contact (intro) card per user.
- Enforced in Django **service layer**, not just UI. On `POST /portfolios/generate/`:
  count user's portfolios → if free plan and count ≥ 1 → reject:
  `403 { "error": "Free plan limit reached. Upgrade to Pro." }`
- Same for contact card: free plan = 1 intro card max.
- NOT a DB unique constraint (Pro needs many) → explicit check in view/service.

**Rate limiting** (DRF throttling, Redis backend — reuse Celery Redis):
```python
# settings.py
REST_FRAMEWORK = {
  "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle",
                               "rest_framework.throttling.AnonRateThrottle"],
  "DEFAULT_THROTTLE_RATES": {
    "anon":       "20/hour",   # gallery browse only
    "user":       "100/hour",  # general authed API
    "generate":   "5/hour",    # ScopedRateThrottle — Groq LLM (cost)
    "avatar_gen": "5/hour",    # ScopedRateThrottle — Replicate (cost)
    "deploy":     "10/hour",   # ScopedRateThrottle
  },
}
```
- `generate`, `avatar_gen`, `deploy` use `ScopedRateThrottle` with `throttle_scope` on the view.

**Input caps** (cost + prompt-injection guard, validate at serializer):
- questionnaire JSON: max ~10 KB
- avatar description: max 500 chars
- intro card bio: max ~1000 chars
- Reject oversized input with `400` at serializer validation.

---

### Database Schema

```sql
-- Users table (identity owned by Clerk; row synced via Clerk webhook user.created)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clerk_user_id VARCHAR(255) UNIQUE NOT NULL, -- maps to Clerk; NO password stored here
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_public BOOLEAN DEFAULT true,
  plan VARCHAR(50) DEFAULT 'free' -- free, pro
);
-- NOTE: Stripe fields (stripe_customer_id, subscription_status) added in Phase 3.

-- Portfolios table
CREATE TABLE portfolios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  slug VARCHAR(100) UNIQUE NOT NULL,
  subdomain VARCHAR(100) UNIQUE NOT NULL,
  custom_domain VARCHAR(255),
  
  -- Niche type
  niche VARCHAR(50) NOT NULL, -- indie_hacker, freelancer, creator, coach, agency
  niche_config JSONB, -- niche-specific settings
  
  -- Generation metadata
  questionnaire JSONB, -- stores user inputs (flexible per niche)
  generated_html TEXT, -- raw HTML output
  generated_css TEXT,  -- inline or separate CSS
  generated_metadata JSONB, -- SEO meta, OG tags, structured data
  
  -- Avatar & Introduction Card
  avatar_type VARCHAR(50), -- 'photo', '3d', '2d_illustrated', 'ai_photo'
  avatar_url VARCHAR(500), -- URL to generated/uploaded avatar
  avatar_generation_data JSONB, -- {provider, model, prompt, timestamp}
  
  intro_card JSONB, -- {name, tagline, bio, socialLinks, features}
  intro_card_features JSONB, -- {animated: bool, interactiveHover: bool, ...}
  
  -- Serving / deployment info (Model B wildcard-serve default)
  published_url VARCHAR(255), -- live URL: https://{subdomain}.forge.app or custom domain
  has_custom_domain BOOLEAN DEFAULT false,
  custom_domain_status VARCHAR(50), -- pending_dns, verified, failed (Pro only)
  netlify_site_id VARCHAR(255), -- only if custom-domain Pro uses Netlify fallback

  -- Granular async status (text + avatar + publish stages)
  generation_status VARCHAR(50) DEFAULT 'text_pending',
    -- text_pending, text_done, avatar_pending, avatar_done, publishing, live, failed
  deployment_status VARCHAR(50) DEFAULT 'pending', -- pending, live, failed
  last_deployed_at TIMESTAMP,
  
  -- Stats
  views INT DEFAULT 0,
  visits INT DEFAULT 0,
  
  -- Showcase
  is_featured BOOLEAN DEFAULT false,
  featured_at TIMESTAMP,
  in_showcase BOOLEAN DEFAULT true,
  showcase_rank INT,
  
  -- LLM Provider tracking
  llm_provider VARCHAR(50) DEFAULT 'groq', -- groq, together
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Avatar generation history (for tracking costs, iterating)
CREATE TABLE avatar_generations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
  avatar_type VARCHAR(50), -- '3d', '2d_illustrated', 'ai_photo'
  provider VARCHAR(50), -- 'readyplayer', 'replicate', 'dalle'
  provider_id VARCHAR(255), -- ID from external provider
  prompt TEXT, -- user's description of physical features
  generated_url VARCHAR(500),
  cost_cents INT, -- cost in cents
  generation_time_ms INT,
  success BOOLEAN,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Metrics/Analytics
CREATE TABLE portfolio_analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
  date DATE,
  views INT DEFAULT 0,
  unique_visitors INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Gallery/Showcase = DB VIEW over portfolios (no separate table; no sync logic)
CREATE VIEW showcase_index AS
SELECT
  p.id AS portfolio_id,
  p.user_id,
  u.username,
  p.title,
  p.niche,
  p.avatar_url AS thumbnail_url,
  p.published_url AS deployed_url,
  p.is_featured AS featured,
  p.featured_at,
  p.views AS view_count,
  p.created_at,
  p.updated_at
FROM portfolios p
JOIN users u ON u.id = p.user_id
WHERE p.in_showcase = true
  AND p.deployment_status = 'live'
  AND u.is_public = true;

-- Niche config: HARDCODED in code (Python/TS constants), NOT a DB table. 5 stable niches.

-- Create indexes for performance
CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX idx_portfolios_niche ON portfolios(niche);
CREATE INDEX idx_portfolios_in_showcase ON portfolios(in_showcase);
CREATE INDEX idx_avatar_generations_portfolio ON avatar_generations(portfolio_id);
CREATE INDEX idx_users_clerk_id ON users(clerk_user_id);
```

---

## Development Phases

### Phase 1: MVP (Weeks 1-4)
**Goal**: Launch a working multi-niche portfolio generator + basic showcase

**Niche Launch Strategy**:
- **Week 1-4**: Launch with 2 niches (Indie Hacker + Freelancer) fully fleshed out
  - These have largest addressable market + most overlap in questionnaire/generation logic
  - Indie Hackers community is tight-knit, early-adopter friendly (easier to go viral)
  - Freelancers have constant demand for portfolios (continuous growth)
- **Week 4+**: Add remaining niches (Creators, Coaches, Agencies) iteratively
  - Each new niche reuses 80% of infrastructure
  - Only new prompts + questionnaire fields + showcase filters needed

#### 1.1 Foundation Setup (Week 1)
- [ ] Project initialization (Next.js 14, Tailwind 3, Shadcn/ui)
- [ ] Database setup (Neon PostgreSQL) + Django migrations
- [ ] Clerk setup (web + Django JWT verification via JWKS) + webhook sync (user.created)
- [ ] Environment configuration (Groq, Replicate, R2, Clerk, Cloudflare keys)
- [ ] DRF throttling config (Redis backend) — see Rate Limiting section
- [ ] Basic file structure & component architecture
- [ ] Landing page (simple, positioning the product)

**Deliverable**: Repo ready, local dev environment working

#### 1.2 Questionnaire Builder & Avatar Customization (Week 1-2)
- [ ] Niche selector (user picks their type: indie hacker, freelancer, creator, coach, agency)
- [ ] Dynamic form component that renders different fields based on niche
- [ ] **Avatar Selection Step**:
  - [ ] User chooses avatar type: photo, 3D, 2D illustrated, AI photo
  - [ ] If photo: upload UI
  - [ ] If 3D: ReadyPlayer.me interactive builder
  - [ ] If 2D illustrated: description form → Replicate generation
  - [ ] If AI photo: physical features description → Replicate/DALL-E generation
- [ ] **Introduction Card Builder**:
  - [ ] Name, tagline, bio
  - [ ] Social links (Twitter, GitHub, LinkedIn, etc.)
  - [ ] Optional: card animation toggle
  - [ ] Optional: interactive hover effects
  - [ ] Preview of intro card with avatar
- [ ] Niche-specific questionnaire fields (see below)
- [ ] Form validation + error handling
- [ ] Live preview pane (shows questionnaire + avatar + intro card)
- [ ] Save as draft option

**Questions by Niche** (with intro card elements):

**Indie Hacker**:
- Avatar + Introduction card (name, "Shipped: X products", bio)
- Projects shipped (with links to GitHub, ProductHunt, etc.)
- Revenue / User count
- Tech stack
- Looking for (investors, collaborators, customers, jobs)

**Freelancer** (Designer/Developer/Writer):
- Avatar + Introduction card (name, services, expertise)
- Portfolio pieces (projects, case studies)
- Client testimonials / Success metrics
- Rates / Availability
- Contact info (email, Calendly link)

**Creator** (YouTuber/Streamer):
- Avatar + Introduction card (name, content type, niche)
- Channel links (YouTube, Twitch, TikTok, etc.)
- Subscriber/follower counts
- Most popular content / recent uploads
- Sponsorship/Patreon links

**Coach/Consultant**:
- Avatar + Introduction card (name, expertise, credentials)
- Services offered / Packages
- Client testimonials / case studies
- Pricing
- Booking link (Calendly, etc.)

**Agency**:
- Team avatar(s) + Introduction card (company name, tagline, team size)
- Services offered
- Team members (names, roles)
- Case studies / client work
- Specializations / tech stack

**Deliverable**: 
- Users select niche → choose avatar → build intro card → answer niche questions → all saved to DB
- Avatar generated if needed (async background job)

#### 1.3 AI Generation Engine (Week 2)
- [ ] Groq API integration (Llama 3.1 70B or Mixtral)
- [ ] Together.ai fallback (for free tier / rate limiting)
- [ ] Niche-aware system prompts (different prompt per niche type)
- [ ] Portfolio HTML/CSS generation via Groq:
  - Hero section (headline, subheading, CTA - tailored to niche)
  - Content sections (varies by niche, see Phase 1.2 above)
  - Introduction card rendering (name, avatar, bio, socials)
  - Social proof / metrics (different per niche)
  - Call-to-action (context-aware: "Hire me", "Invest", "Subscribe", "Book call", etc.)
  - Meta tags, og:image, structured data (JSON-LD schema varies per niche)
- [ ] Generate clean, semantic HTML
- [ ] Generate Tailwind-ready CSS (with niche-specific design)
- [ ] Avatar generation (async background job via Celery):
  - [ ] 3D Avatars: ReadyPlayer.me API integration
    - User's description → ReadyPlayer API → WebGL avatar JSON
  - [ ] 2D Illustrated: Replicate + Stable Diffusion
    - User's description → Replicate API → image URL → save to S3/R2
  - [ ] AI Photo: Replicate DALL-E or Together.ai image generation
    - User's physical features → DALL-E/Stable Diffusion → image → save to storage
- [ ] Image optimization (crop, resize to thumbnails via Pillow)
- [ ] Store generated output + metadata in DB
- [ ] Track LLM provider + cost per portfolio

**Backend Service** (Django):
```python
# backend/services/llm_service.py
- generate_portfolio(niche, questionnaire, avatar_url)
  └─> Try Groq first, fallback to Together.ai

# backend/services/avatar_service.py
- generate_3d_avatar(description) -> ReadyPlayer.me
- generate_2d_avatar(description) -> Replicate
- generate_ai_photo(physical_features) -> Replicate/DALL-E
- optimize_image(image_url) -> thumbnail URLs
```

**Deliverable**: Click "Generate" → AI creates niche-optimized portfolio HTML/CSS/intro card + avatar generation queued

#### 1.4 Publish Pipeline — Wildcard-Serve (Week 2-3)
- [ ] Next.js catch-all route `[subdomain]` → lookup portfolio by subdomain → render stored HTML
- [ ] Store generated HTML/CSS in DB (+ assets in R2); publish = flip status to `live` (instant, no deploy)
- [ ] Cloudflare wildcard `*.forge.app` + CDN cache in front
- [ ] Async status pipeline: text_pending → text_done → avatar_pending → avatar_done → publishing → live
- [ ] Status polling endpoint (frontend polls; progressive UI)
- [ ] Custom domain (Pro, can defer to Phase 3): ask user during flow; Cloudflare for SaaS custom hostnames + auto SSL; Netlify per-site as fallback
- [ ] Error handling + retry logic per stage (avatar fail ≠ lose generated text)

**Deliverable**: Generated portfolio live on `you.forge.app` instantly on publish (no per-site deploy)

#### 1.5 Showcase Gallery (Week 3-4)
- [ ] Gallery page with all live portfolios
- [ ] Niche filtering (user can browse by niche type)
- [ ] Sorting options: by newest, most viewed
- [ ] Niche-specific filtering:
  - **Indie Hacker gallery**: Sort by revenue, users, funding raised (if available)
  - **Freelancer gallery**: Filter by service type, skill
  - **Creator gallery**: Sort by subscriber count
  - **Coach gallery**: Sort by specialty
  - **Agency gallery**: Sort by team size, specialization
- [ ] Portfolio card component (thumbnail, title, niche badge, link)
- [ ] "Built with [YourApp]" badge on each portfolio
- [ ] Link back to app from each portfolio
- [ ] Featured section (rotating weekly, high-quality portfolios)
- [ ] Search functionality (by name, niche, keyword)

**Deliverable**: yourapp.io/showcase shows all portfolios with SEO, niche filtering, and discovery

#### 1.6 Polish & Testing (Week 4)
- [ ] E2E testing (questionnaire → deployed portfolio)
- [ ] Error handling & edge cases
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] SEO basics (meta tags, sitemap for showcase)

**Deliverable**: MVP ready for launch

**Tech Used in Phase 1**:
- Next.js 14 (frontend + wildcard-serve route)
- Django 4.2 + DRF (backend API)
- Neon PostgreSQL (database)
- Clerk (auth)
- Groq API (generation)
- Wildcard-serve + Cloudflare (publishing)
- Shadcn/ui + Tailwind 3 (UI components)

---

### Phase 2: User Accounts & Editing (Weeks 5-8)
**Goal**: Users can create accounts, edit portfolios, own their work

#### 2.1 Authentication (Clerk)
> NOTE: Clerk integrated in Phase 1.1 (needed for authed generate endpoint). Phase 2 = full account UX.
- [ ] Clerk components: signup + login + user profile (email/password + OAuth via Clerk)
- [ ] Protected routes (portfolio dashboard) — Clerk middleware
- [ ] Django: verify Clerk JWT (JWKS) on every authed request
- [ ] Clerk webhooks: user.created → insert users row; user.deleted → cascade cleanup
- [ ] Account deletion (Clerk + cascade DB)

**Deliverable**: Users have accounts (Clerk-managed)

#### 2.2 Portfolio Dashboard
- [ ] List all user's portfolios
- [ ] View live portfolio
- [ ] Edit/regenerate portfolio
- [ ] Delete portfolio
- [ ] View portfolio metrics (views, visits)

**Deliverable**: Users manage their portfolios

#### 2.3 Portfolio Editing
- [ ] Rich text editor for sections (hero, projects, etc.)
- [ ] Regenerate specific sections (not full page)
- [ ] Image upload (profile photo, project screenshots)
- [ ] Color/theme customization (light/dark mode)
- [ ] Custom CTA text

**Deliverable**: Non-technical users can tweak portfolios

#### 2.4 Showcase Enhancements
- [ ] User profiles (all portfolios by one creator)
- [ ] Comments/testimonials on showcased portfolios (optional)
- [ ] Featured portfolios (admin-picked, weekly rotation)
- [ ] Search functionality (by name, keyword)

**Deliverable**: Showcase becomes social + discoverable

**Tech Added**:
- (Auth = Clerk, already in Phase 1)
- django-storages → R2 (image upload)
- Redis (caching for showcase queries)

---

### Phase 3: Custom Domains & Premium Features (Weeks 9-12)
**Goal**: Monetize + improve SEO for power users

#### 3.1 Custom Domain Support
- [ ] UI for adding custom domain
- [ ] CNAME setup instructions
- [ ] SSL certificate auto-provisioning (Cloudflare for SaaS; Netlify fallback)
- [ ] Domain verification + setup wizard

**Deliverable**: Users can use custom domains (paid feature)

#### 3.2 Premium Plan
- [ ] DB: add `stripe_customer_id`, `subscription_status`, `current_period_end` to users (+ optional `subscriptions` table for history)
- [ ] Stripe integration (billing) + Stripe webhooks (checkout.completed, subscription.updated/deleted → flip user.plan)
- [ ] Plan tiers:
  - **Free**: 1 portfolio, subdomain, no analytics
  - **Pro**: 3 portfolios, custom domain, basic analytics, priority regenerations
  - **Pro+**: Unlimited portfolios, multiple custom domains, advanced analytics
- [ ] Upgrade flow + checkout

**Deliverable**: Monetization pathway active

#### 3.3 Analytics Dashboard
- [ ] Portfolio view count + unique visitors
- [ ] Top referrers
- [ ] Geographic breakdown
- [ ] Traffic over time
- [ ] CTA click tracking

**Deliverable**: Users see how their portfolio performs

#### 3.4 SEO Optimization
- [ ] Auto-generate XML sitemap (all showcase portfolios)
- [ ] Implement Open Graph + Twitter cards
- [ ] Structured data (JSON-LD for person + portfolio)
- [ ] robots.txt configuration
- [ ] Submit sitemap to Google Search Console

**Deliverable**: Showcase + individual portfolios rank better

**Tech Added**:
- Stripe (payments)
- Plausible or Vercel Analytics (analytics)
- next-sitemap (sitemap generation)

---

### Phase 4: Integrations & Advanced Features (Weeks 13+)
**Goal**: Make portfolios more powerful with integrations

#### 4.1 GitHub Integration
- [ ] Auto-pull user's GitHub repos
- [ ] Show stars, forks, language
- [ ] Link to live demos (if in repo)
- [ ] Update portfolio when repos change (webhooks)

#### 4.2 ProductHunt Integration
- [ ] Auto-pull ProductHunt products
- [ ] Show ranking, upvotes, reviews
- [ ] Link to ProductHunt page

#### 4.3 Social Integration
- [ ] Twitter card optimization
- [ ] Share portfolio preview (OG image generation)
- [ ] Auto-generate sharing copy

#### 4.4 Email & CRM
- [ ] Simple contact form on portfolios
- [ ] Email notifications to user
- [ ] Export contacts (CSV)

#### 4.5 Advanced Customization
- [ ] Template selection (before AI generation)
- [ ] Font/color picker
- [ ] Custom sections (testimonials, blog, etc.)
- [ ] A/B testing CTAs

**Tech Added**:
- GitHub API
- ProductHunt API
- SendGrid or Mailgun (email)
- Social sharing libraries

---

## Directory Structure

```
portfolio-generator/
├── backend/                       # Django REST API
│   ├── manage.py
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # GROQ_API_KEY, TOGETHER_API_KEY, etc.
│   ├── config/
│   │   ├── settings.py           # Django settings (DB, auth, CORS)
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/                # User model, auth
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── portfolios/           # Portfolio model, CRUD
│   │   │   ├── models.py         # Portfolio, AvatarGeneration
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tasks.py          # Celery tasks (avatar gen)
│   │   ├── gallery/              # Showcase queries
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── niches/               # Niche configs
│   │       ├── models.py
│   │       └── views.py
│   ├── services/                 # Business logic
│   │   ├── llm_service.py        # Groq, Together.ai calls
│   │   ├── avatar_service.py     # ReadyPlayer, Replicate
│   │   ├── portfolio_generator.py # Niche-specific generation
│   │   └── publisher.py          # Wildcard-serve publish + custom-domain (CF SaaS/Netlify)
│   ├── prompts/                  # LLM system prompts
│   │   ├── indie_hacker.txt
│   │   ├── freelancer.txt
│   │   ├── creator.txt
│   │   ├── coach.txt
│   │   └── agency.txt
│   ├── tests/
│   │   ├── test_generation.py
│   │   ├── test_avatars.py
│   │   └── test_auth.py
│   └── utils/
│       ├── celery.py
│       ├── storage.py            # S3/R2 file handling
│       └── validators.py
│
├── web/                           # Next.js 14 frontend
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local
│   ├── public/
│   │   ├── logo.svg
│   │   └── og-image.png
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # Landing page
│   │   │   ├── globals.css
│   │   │   ├── api/               # Next.js API middleware
│   │   │   │   └── proxy/[...path].ts  # Proxy to Django backend
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   ├── signup/
│   │   │   │   └── logout/
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx       # Portfolio list
│   │   │   │   ├── [id]/          # Edit portfolio
│   │   │   │   └── settings/
│   │   │   ├── portfolio/
│   │   │   │   ├── new/           # Create (questionnaire)
│   │   │   │   ├── [slug]/        # Edit/preview
│   │   │   │   └── preview/
│   │   │   ├── gallery/           # Showcase
│   │   │   │   ├── page.tsx
│   │   │   │   └── [slug]/
│   │   │   └── admin/             # Featured management
│   │   ├── components/
│   │   │   ├── questionnaire/     # Form fields, builder
│   │   │   ├── avatar/
│   │   │   │   ├── AvatarSelector.tsx
│   │   │   │   ├── ReadyPlayerEmbed.tsx
│   │   │   │   ├── AvatarPreview.tsx
│   │   │   │   └── AvatarGenerator.tsx
│   │   │   ├── intro-card/        # Intro card builder
│   │   │   │   ├── IntroCardEditor.tsx
│   │   │   │   ├── IntroCardPreview.tsx
│   │   │   │   └── SocialLinksForm.tsx
│   │   │   ├── portfolio/
│   │   │   │   ├── PortfolioPreview.tsx
│   │   │   │   └── PortfolioEditor.tsx
│   │   │   ├── gallery/           # Gallery cards, filters
│   │   │   │   ├── GalleryGrid.tsx
│   │   │   │   ├── NicheFilter.tsx
│   │   │   │   └── PortfolioCard.tsx
│   │   │   ├── ui/                # Shadcn/ui components
│   │   │   └── layout/            # Header, footer, nav
│   │   ├── lib/
│   │   │   ├── api/
│   │   │   │   └── client.ts      # Django API client
│   │   │   ├── utils/
│   │   │   │   ├── validators.ts
│   │   │   │   └── helpers.ts
│   │   │   └── types.ts           # TypeScript types
│   │   ├── hooks/
│   │   │   ├── usePortfolio.ts
│   │   │   ├── useAvatar.ts
│   │   │   └── useGallery.ts
│   │   └── styles/
│   │       └── globals.css
│   └── tests/
│       ├── components/
│       └── integration/
│
├── mobile/                        # React Native (Expo)
│   ├── package.json
│   ├── app.json                  # Expo config
│   ├── eas.json                  # EAS Build config
│   ├── .env
│   ├── app/                       # Expo Router
│   │   ├── _layout.tsx            # Root stack
│   │   ├── (auth)/
│   │   │   ├── _layout.tsx
│   │   │   ├── login.tsx
│   │   │   └── signup.tsx
│   │   ├── (app)/
│   │   │   ├── _layout.tsx        # Bottom tabs
│   │   │   ├── index.tsx          # Home
│   │   │   ├── portfolio/
│   │   │   │   ├── _layout.tsx
│   │   │   │   ├── index.tsx      # List portfolios
│   │   │   │   ├── new.tsx        # Create
│   │   │   │   └── [id].tsx       # Edit
│   │   │   ├── gallery.tsx
│   │   │   └── settings.tsx
│   │   └── (modals)/
│   │       ├── avatar-selector.tsx
│   │       └── intro-card-editor.tsx
│   ├── src/
│   │   ├── components/
│   │   │   ├── QuestionnaireForm.tsx
│   │   │   ├── AvatarCustomizer.tsx
│   │   │   ├── IntroCardBuilder.tsx
│   │   │   ├── PortfolioPreview.tsx
│   │   │   └── GalleryList.tsx
│   │   ├── lib/
│   │   │   ├── api/
│   │   │   │   └── client.ts      # Django API client (shared with web)
│   │   │   ├── store/
│   │   │   │   └── zustand.ts     # client state (matches web)
│   │   │   └── types.ts
│   │   └── hooks/
│   │       ├── useAuth.ts
│   │       └── usePortfolio.ts
│   └── tests/
│       └── components/
│
├── shared/                        # Shared code
│   ├── types.ts                  # Shared TypeScript types
│   ├── api-client.ts             # Shared API client
│   └── prompts/                  # Shared prompt management
│
├── docker-compose.yml            # Local dev: Postgres, Redis
├── .github/
│   └── workflows/
│       ├── backend-test.yml
│       ├── backend-deploy.yml
│       ├── web-deploy.yml
│       └── mobile-build.yml
│
└── README.md
```

---

## API Endpoints (Django REST Framework)

### Authentication
```
POST /api/v1/auth/register/
Body: { email, username, password }
Response: { access_token, refresh_token, user }

POST /api/v1/auth/login/
Body: { email, password }
Response: { access_token, refresh_token, user }

POST /api/v1/auth/refresh/
Body: { refresh_token }
Response: { access_token }

POST /api/v1/auth/logout/
Response: { success: true }
```

### Portfolio Generation (Niche-Aware)
```
POST /api/v1/portfolios/generate/
Headers: Authorization: Bearer {token}
Body: {
  niche: "indie_hacker" | "freelancer" | "creator" | "coach" | "agency",
  questionnaire: {...},
  avatar_type: "photo" | "3d" | "2d_illustrated" | "ai_photo",
  avatar_data: {
    // If photo: { file_url }
    // If 3d: { readyplayer_avatar_json }
    // If 2d/ai: { description: "physical features..." }
  },
  intro_card: {
    name: string,
    tagline: string,
    bio: string,
    socialLinks: [{platform, url}],
    features: {animated: bool, interactiveHover: bool}
  }
}
Response: {
  id: string,
  niche: string,
  html: string,
  css: string,
  metadata: {...},
  avatar_url: string,
  avatar_generation_status: "pending" | "completed" | "failed",
  intro_card: {...}
}
```

### Avatar Generation (Async)
```
POST /api/v1/avatars/generate/
Headers: Authorization: Bearer {token}
Body: {
  portfolio_id: string,
  avatar_type: "3d" | "2d_illustrated" | "ai_photo",
  description: string  -- physical features for user
}
Response: {
  task_id: string,  -- Celery task ID
  status: "queued"
}

GET /api/v1/avatars/generate/{task_id}/
Response: {
  status: "pending" | "completed" | "failed",
  result: {
    url: string,
    provider: string,
    generated_at: timestamp
  },
  error: string (if failed)
}

POST /api/v1/avatars/upload/
Headers: Authorization: Bearer {token}, Content-Type: multipart/form-data
Body: { portfolio_id, file }
Response: {
  avatar_url: string,
  thumbnail_url: string
}
```

### Deployment
```
POST /api/v1/portfolios/{id}/deploy/
Headers: Authorization: Bearer {token}
Body: { html, css, slug }
Response: {
  portfolio_id: string,
  live_url: string,
  deployment_status: "pending" | "deployed" | "failed"
}

GET /api/v1/portfolios/{id}/deployment-status/
Response: {
  status: "pending" | "deployed" | "failed",
  url: string,
  last_deployed_at: timestamp,
  error: string (if failed)
}
```

### Portfolio Management
```
GET /api/v1/portfolios/  (user's portfolios)
Response: [{ id, title, niche, status, url, created_at }]

POST /api/v1/portfolios/
Body: { niche }
Response: { id, niche, questionnaire: {} }

GET /api/v1/portfolios/{id}/
Response: { full portfolio object }

PATCH /api/v1/portfolios/{id}/
Body: { title, intro_card, avatar_url, ... }
Response: { updated portfolio }

DELETE /api/v1/portfolios/{id}/
Response: { success: true }

POST /api/v1/portfolios/{id}/regenerate/
Body: { niche_section: "hero" | "projects" | "all" }
Response: { id, regenerated_section_html, status }
```

### Gallery / Showcase
```
GET /api/v1/gallery/
Query params: ?niche=indie_hacker&sort=newest&limit=20&offset=0&search=
Response: {
  portfolios: [{id, slug, title, url, username, niche, thumbnail, views, created_at}],
  total: number,
  niches: [{id, name, count}]  -- for filter UI
}

GET /api/v1/gallery/{slug}/
Response: { full portfolio object (public fields only) }

POST /api/v1/gallery/{id}/view/
Response: { view_count: number }
```

### Niches Configuration
```
GET /api/v1/niches/
Response: {
  niches: [
    {
      id: "indie_hacker",
      name: "Indie Hacker",
      description: "...",
      icon: "rocket",
      questionnaire_fields: [...],
      intro_card_examples: [...],
      showcase_metrics: ["revenue", "users", "projects"]
    },
    // ... more niches
  ]
}

GET /api/v1/niches/{niche_id}/examples/
Response: {
  examples: [{ portfolio with this niche }]
}
```

### User Dashboard
```
GET /api/v1/users/me/
Response: { id, email, username, plan, created_at }

PATCH /api/v1/users/me/
Body: { username, avatar_url }
Response: { updated user }
```

---

## Claude Code Integration

Since you're using Claude Code for development:

### Build Order (Recommended)

**Phase 1: Backend (Django)**
1. Django project scaffold + models (User, Portfolio, Avatar)
2. Neon database migrations
3. Clerk JWT verification (JWKS) + webhook user sync
4. DRF throttling + free-tier enforcement
5. Portfolio generation service (Groq integration)
6. Avatar generation service (Replicate + ReadyPlayer)
7. Publish service (wildcard-serve; store HTML → flip to live)
8. API endpoints (DRF serializers + views)

**Phase 2: Web Frontend (Next.js)**
1. Landing page + niche selector
2. Authentication UI (signup/login)
3. Questionnaire builder (multi-step form)
4. Avatar customizer (3D, 2D, AI integration)
5. Introduction card editor
6. Portfolio preview
7. Gallery/showcase
8. Dashboard

**Phase 3: Mobile (React Native)**
1. Expo setup + navigation
2. Authentication screens
3. Questionnaire form (native UI)
4. Avatar customizer (Skia for 3D)
5. Gallery
6. Sync with Django backend

### Key Claude Code Tasks

**Backend (Django)**:
- [ ] Create Django project with DRF
- [ ] Define models: User (clerk_user_id), Portfolio, AvatarGeneration (gallery = DB view)
- [ ] Create serializers for CRUD operations + input caps validation
- [ ] Implement Clerk JWT verification (JWKS) + webhook user sync
- [ ] Configure DRF throttling + free-tier (1 portfolio / 1 card) enforcement
- [ ] Create Groq integration service (+ Together.ai fallback)
- [ ] Create Replicate + ReadyPlayer.me avatar service
- [ ] Create wildcard-serve publish service (store HTML, flip to live; custom-domain Pro later)
- [ ] Create API views for all endpoints
- [ ] Write Celery tasks for async avatar generation + status pipeline
- [ ] Create Neon database migrations
- [ ] Add pytest tests for API endpoints

**Frontend - Web (Next.js)**:
- [ ] Setup Next.js 14 with Tailwind + Shadcn/ui
- [ ] Create niche selector component
- [ ] Build multi-step questionnaire form
- [ ] Create ReadyPlayer.me integration for 3D avatars
- [ ] Build avatar image preview/upload
- [ ] Create intro card builder/editor
- [ ] Build portfolio preview component
- [ ] Create gallery grid with filters
- [ ] Implement auth flow (Clerk components + middleware)
- [ ] Add React Query (TanStack) hooks for API calls

**Frontend - Mobile (React Native)**:
- [ ] Setup Expo + Expo Router
- [ ] Create auth navigation
- [ ] Build questionnaire form (native UI)
- [ ] Create avatar customizer
- [ ] Build gallery list
- [ ] Sync state with Zustand + TanStack Query (shared api-client)

### Prompt Ideas for Claude Code

**Backend**:
```
"Create a Django REST API service that:
1. Takes a niche type and questionnaire data
2. Calls Groq API to generate portfolio HTML/CSS with a system prompt
3. Stores the result in Neon PostgreSQL
4. Returns the generated HTML, CSS, and metadata as JSON
Include error handling and rate limiting."

"Build a Django Celery task that:
1. Takes a user's physical feature description
2. Calls Replicate API with Stable Diffusion prompt
3. Downloads the generated image
4. Uploads to R2 cloud storage
5. Updates the database with avatar URL
6. Returns task status"

"Create Django models for User, Portfolio, AvatarGeneration, and Gallery.
Include relationships, indexes for performance, and JSONB fields for flexible data.
Generate migrations for Neon PostgreSQL."
```

**Frontend - Web**:
```
"Build a multi-step React form component using React Hook Form that:
1. Step 1: Niche selector (radio buttons)
2. Step 2: Avatar customization (photo upload, 3D builder button, description form)
3. Step 3: Intro card (name, tagline, bio, social links)
4. Step 4: Niche-specific fields (dynamic based on selected niche)
Include validation, error states, and a preview pane on the right."

"Create a React component that integrates ReadyPlayer.me for 3D avatar creation.
When user clicks 'Create 3D Avatar', open ReadyPlayer iframe.
When they finish, capture the avatar JSON and save to state."

"Build a portfolio preview component that renders generated HTML/CSS
with intro card overlay (avatar + name + tagline + socials)
with animations and responsive design."
```

**Frontend - Mobile**:
```
"Create a React Native form using React Hook Form that matches the web questionnaire.
Use NativeWind for Tailwind styling. Include multi-step navigation with back/next buttons.
Connect to Django API using Axios with Clerk JWT (Clerk Expo SDK); server state via TanStack Query."
```

---

## Environment Variables

### Backend (.env)
```
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (Neon)
DATABASE_URL=postgresql://user:password@host/dbname

# Redis (for Celery + caching)
REDIS_URL=redis://localhost:6379/0

# Auth (Clerk — Django verifies, does not issue)
CLERK_JWKS_URL=https://your-app.clerk.accounts.dev/.well-known/jwks.json
CLERK_ISSUER=https://your-app.clerk.accounts.dev
CLERK_WEBHOOK_SECRET=your-clerk-webhook-secret
CLERK_SECRET_KEY=your-clerk-secret-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# LLM Providers
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile   # verify against live Groq catalog
TOGETHER_AI_API_KEY=your-together-ai-key

# Avatar Generation
REPLICATE_API_KEY=your-replicate-token
READYPLAYER_API_KEY=your-readyplayer-key (optional)

# File Storage
AWS_ACCESS_KEY_ID=your-r2-access-key
AWS_SECRET_ACCESS_KEY=your-r2-secret
AWS_STORAGE_BUCKET_NAME=portfolio-generator
AWS_S3_REGION_NAME=auto
AWS_S3_ENDPOINT_URL=https://your-r2-endpoint.r2.cloudflarestorage.com

# Publishing — wildcard-serve (free) + custom domains (Pro)
PORTFOLIO_WILDCARD_DOMAIN=forge.app          # serves *.forge.app
CLOUDFLARE_API_TOKEN=your-cf-token           # Cloudflare for SaaS custom hostnames
CLOUDFLARE_ZONE_ID=your-zone-id
NETLIFY_TOKEN=your-netlify-token (optional, custom-domain fallback)

# Emails (SendGrid, Mailgun, etc.)
EMAIL_BACKEND=sendgrid
SENDGRID_API_KEY=your-sendgrid-key

# Monitoring
SENTRY_DSN=your-sentry-dsn

# App Config
SITE_URL=https://yourdomain.com
PORTFOLIO_DOMAIN=yourdomain.com
```

### Frontend - Web (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_READYPLAYER_URL=https://preview.readyplayer.me

# Clerk (web)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-pub-key
CLERK_SECRET_KEY=your-clerk-secret-key

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_KEY=your-plausible-key
```

### Frontend - Mobile (.env)
```
EXPO_PUBLIC_API_BASE_URL=https://api.yourdomain.com
EXPO_PUBLIC_APP_NAME=PortfolioAI
EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-pub-key
```

---

## Cost Projections

### Per 1,000 Portfolios Generated

**OLD STACK** (Claude + Next.js):
- Claude API (1000 portfolios × 2000 tokens × $0.003): $6.00
- DALL-E image generation (300 avatars × $0.02): $6.00
- Vercel hosting: $20/month (pro plan)
- Database (Supabase): $25/month
- **Total**: ~$57/month for 1K portfolios

**CHOSEN STACK** (Groq + Django + Neon + Clerk + wildcard-serve):
- Groq API (1000 portfolios × 2000 tokens × $0.00005): $0.10
- Replicate (2D avatars, 200 × $0.001): $0.20
- ReadyPlayer.me (3D avatars): FREE
- AI photos (Replicate SD — verify cost, NOT assume free): ~$0.20-2.00
- Railway/Render (Django hosting): $5-10/month
- Neon database (PostgreSQL): $15/month (pay-as-you-go)
- Clerk: free up to 10K MAU, then paid
- Wildcard-serve via Next.js (Vercel) + Cloudflare CDN: hosting cost only, no per-site fees
- **Total**: ~$20-25/month for 1K portfolios

**SAVINGS**: ~65% vs Claude-based stack (caveat: verify AI-photo + Together.ai/Clerk free tiers)

### Scaling to 10,000 Portfolios/Month

| Component | Claude Stack | Groq Stack | Savings |
|-----------|-------------|-----------|---------|
| Portfolio generation | $60 | $1 | $59 |
| Avatar generation | $60 | $2 | $58 |
| Hosting (backend) | $20 | $10 | $10 |
| Database | $25 | $20 | $5 |
| **Total/Month** | **$165** | **$33** | **$132 (80%)** |

### Monthly Costs at Different Scales

| Portfolios/Month | Groq Stack | Rationale |
|-----------------|-----------|-----------|
| 100 | $18-20 | Minimal fixed costs |
| 1,000 | $20-25 | Avatar generation increases |
| 10,000 | $30-40 | Still within free tiers for most |
| 100,000 | $100-150 | Pay-as-you-go kicks in fully |
| 1,000,000 | $1,000-1,500 | Peak efficiency |

### Revenue Model (Breakeven)

**Free Tier**:
- 1 portfolio
- Subdomain (username.app.com)
- Basic avatar
- No custom domain
- Cost to serve: ~$0.10-0.30

**Pro Tier** ($9.99/month):
- 3 portfolios
- Custom domain
- Advanced avatars
- Analytics
- Margin: ~$8/user (after payment processing 3%)

**Breakeven**: ~25 Pro users at $9.99/month = ~$250/month revenue

---

### Phase 1 Launch
- [ ] Generate time: <5 minutes (across all niches)
- [ ] Deploy time: <30 seconds
- [ ] Error rate: <5%
- [ ] Showcase portfolios: 50+ by end of week 1 (mix of indie hackers + freelancers)
- [ ] Niche split: >30% freelancers, >30% indie hackers by week 2
- [ ] ProductHunt launch (if targeting PH)
- [ ] IH post traction: 100+ upvotes minimum
- [ ] Indie Hackers featured: get at least 50 members to try

### Phase 2
- [ ] User signups: 500+ (goal: 250+ freelancers, 250+ indie hackers)
- [ ] User retention (7-day): >40% (per niche)
- [ ] Portfolios generated: 1000+ (balanced across niches)
- [ ] Gallery views: 5000+ per week
- [ ] Showcase galleries ranking for niche keywords ("freelancer portfolio", "indie hacker showcase")

### Phase 3
- [ ] Conversion to paid: >10% (track per niche)
- [ ] Custom domains: 50+ users
- [ ] MRR: $500+
- [ ] Niche 3-5 (creators, coaches, agencies) launched and generating traction

---

## Launch Checklist (Phase 1)

### Core Features
- [ ] Domain + landing page ready (positions all niches)
- [ ] Niche selector working (indie hacker + freelancer ready)
- [ ] Questionnaires for both niches fully functional
- [ ] All API routes tested (generate, deploy, gallery)
- [ ] Deployment pipeline working (10 test deployments minimum)
- [ ] Gallery page live + indexed by Google
- [ ] Niche filtering on gallery working
- [ ] "Built with [YourApp]" badge on portfolios
- [ ] Error handling for edge cases
- [ ] Mobile responsive
- [ ] Fast: <3s load time for generation + deployment
- [ ] Security: API key handling, rate limiting, user input validation
- [ ] Monitoring: Basic error logging + uptime monitoring

### Pre-Launch Communications (Multi-Niche Strategy)

**For Indie Hackers**:
- [ ] Indie Hackers post: "I built a portfolio generator. Created my own in 3 minutes."
- [ ] Post example: indie hacker showing revenue metrics, GitHub, ProductHunt links
- [ ] HackerNews comment strategy (if launched there)
- [ ] Twitter thread: Show revenue, users, shipped products showcase
- [ ] Communities: IH, ProductHunt, Launch HN, Hacker News

**For Freelancers**:
- [ ] Twitter/LinkedIn posts targeting designers + developers
- [ ] Reddit: r/webdev, r/freelance, r/graphic_design
- [ ] Designer/dev communities (Designer Hangout, Slack groups)
- [ ] Blog post: "How to create a portfolio in 3 minutes (no design skills needed)"
- [ ] Example portfolio: freelancer with case studies, rates, testimonials

**For Both**:
- [ ] ProductHunt launch (if timing makes sense)
- [ ] Email to friends/network (ask them to try and share)
- [ ] Share gallery showcases to relevant communities

---

## Post-Launch Iteration

**Week 1-2 Feedback Loop**:
- Monitor users across both niches, gather feedback separately
- Fix bugs
- Improve generation quality (iterate prompts per niche)
- Highlight best portfolios in showcase (feature indie hacker + freelancer examples)

**Niche-Specific Improvements**:
- **Indie Hackers**: Gather feedback on revenue/metrics display, GitHub integration quality
- **Freelancers**: Gather feedback on portfolio grid layout, testimonial display, rates clarity

**Quick Wins to Implement**:
- Add more questionnaire fields based per-niche feedback
- Improve hero section generation (test with niche-specific copy)
- Better image handling (especially for freelancer portfolio images)
- Test section-based regeneration (faster iteration)
- Add 1-2 example portfolios per niche to gallery for social proof

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Groq API rate limits | Together.ai fallback, queue system, DRF throttling, cache results per niche |
| Wildcard-serve outage | Cloudflare CDN cache, health checks, served HTML cached at edge |
| Custom-domain SSL/DNS issues (Pro) | Cloudflare for SaaS, verification wizard, Netlify fallback |
| Poor portfolio quality | Iterate prompts per niche, A/B test with real users, gather feedback |
| Low adoption | Viral loop via showcase, focus on indie hacker community (tightest), freelancer marketing |
| Niche mismatch | Test questionnaires with real indie hackers + freelancers before launch |
| Gallery becomes messy | Moderation, featured filter, quality scoring, niche-specific curation |
| Publish failures | Per-stage retry, user notifications, wildcard-serve has no deploy step to fail; custom-domain = Netlify fallback |
| Different niches need different features | Start with 2 niches, expand incrementally, reuse 80% of infrastructure |
| Indie hacker vs freelancer audience confusion | Clear landing page per niche, different CTAs, separate showcase galleries |

---

## Next Steps

1. **Validate the idea** (before coding): Post multi-niche + avatar concept on Indie Hackers + freelancer communities
   - "I'm building a 3-minute portfolio generator. What avatar style would you want? (3D, 2D cartoon, AI photo)"
   - Gauge niche interest + avatar preference
   - Collect early user emails for beta

2. **Prepare Groq Account & Keys**:
   - Sign up for Groq (https://console.groq.com)
   - Get free API key + test limits
   - Sign up for Replicate (https://replicate.com) for avatar generation
   - Setup Neon database (https://neon.tech)

3. **Start Phase 1 Week 1 with Claude Code** (Backend first):
   - Django project scaffold + models
   - Neon database setup + migrations
   - Groq integration (test with sample prompts)
   - Replicate + ReadyPlayer.me integration
   - JWT authentication
   - API endpoints (DRF viewsets)
   - Celery for async avatar generation

4. **Week 2: Frontend Web** (Next.js):
   - Landing page + niche selector
   - Questionnaire builder (multi-step)
   - Avatar customizer (3 types)
   - Intro card editor
   - Portfolio preview
   - Connect to Django backend via API

5. **Week 3: Gallery + Polish**:
   - Gallery/showcase implementation (DB view)
   - Wildcard-serve publish pipeline (Cloudflare)
   - Admin dashboard (featured selection)
   - Testing + error handling

6. **Week 4: Mobile** (React Native):
   - Expo setup
   - Mirror web questionnaire as native UI
   - Avatar customization (native version)
   - Gallery browse
   - Push notifications (optional)

7. **Launch Strategy**:
   - Deploy to production on Neon + Railway/Render
   - Launch web first (easier to iterate)
   - Then mobile (EAS Build)
   - Post to Indie Hackers + ProductHunt simultaneously

---

## Notes for Claude Code Sessions

When working with Claude Code, be specific:

✅ **Good**: "Create a Django DRF endpoint POST /api/v1/portfolios/generate/ that takes a portfolio questionnaire object, calls Groq API with this specific system prompt [paste prompt], enforces free-tier limit + throttling, and returns HTML and metadata."

❌ **Vague**: "Make the generation endpoint"

✅ **Good**: "Build a React form with these 8 fields for indie hackers, with validation using Zod, and store the data in state. Include a next/back button between sections."

❌ **Vague**: "Create a questionnaire form"

Always be explicit about:
- What data structure it should handle
- What libraries to use (Next.js, Django/DRF, Neon, Clerk, Groq, etc.)
- What the output/return should be
- Edge cases to handle

---

**Last Updated**: June 2026
**Status**: Ready to build — stack locked: Neon + Groq + Django/DRF + Clerk + wildcard-serve + R2/Cloudflare. Mobile: Zustand + TanStack Query. Tailwind 3. Gallery = DB view. Niches hardcoded.
**Verify before relying on**: Groq model id (`GROQ_MODEL`, live catalog), Together.ai free tier, AI-photo (Replicate SD) real cost, Clerk free-MAU limit, Cloudflare-for-SaaS custom-hostname pricing.
