# Accify Web (This is the source code under development)
A full-stack e-commerce platform for selling digital products. Built with FastAPI on the backend and React on the frontend.

## What it does

Accify Web lets users browse, purchase, and manage digital product accounts through a clean web interface. Sellers can manage inventory, track orders, and handle payments — all from one place.

**Key highlights:**
- JWT-based authentication with role-based access control (admin, member, distributor, collaborator)
- Built-in wallet & payment system
- Inventory management with automatic stock tracking
- Dark / Light theme toggle
- Order data auto-deletes after 24 hours for privacy

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python, FastAPI, SQLAlchemy (async), Pydantic v2 |
| Frontend | TypeScript, React, Vite, TanStack Query |
| Database | PostgreSQL (asyncpg) |
| Migrations | Alembic |
| Auth | JWT (HttpOnly cookies), pwdlib |

## Project Structure

```
accify-web/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── login.py        # Login & password recovery
│   │   │   │   ├── users.py        # Signup, logout, user profile
│   │   │   │   ├── products.py     # CRUD for products
│   │   │   │   ├── categories.py   # Product categories
│   │   │   │   └── inventories.py  # Inventory management
│   │   │   ├── deps.py             # Auth dependencies (get_current_user, get_current_admin)
│   │   │   ├── exception.py        # Custom API exceptions
│   │   │   └── main.py             # Router aggregation
│   │   ├── core/
│   │   │   ├── config.py           # Database URL & settings
│   │   │   ├── db.py               # Async session factory
│   │   │   └── security.py         # JWT creation, password hashing
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── crud.py                 # Database operations
│   │   └── main.py                 # FastAPI app entry point
│   ├── alembic/                    # Database migrations
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── hooks/
│   │   │   ├── useAuth.ts          # Login, register, logout mutations
│   │   │   └── useUser.ts          # Current user query
│   │   ├── services/
│   │   │   ├── auth.ts             # Auth API calls
│   │   │   └── user.ts             # User API calls
│   │   ├── App.tsx                 # Routes & providers
│   │   ├── Header.tsx              # Navbar with theme toggle
│   │   ├── Home.tsx                # Landing page
│   │   ├── HeroSection.tsx         # Hero banner
│   │   ├── Product.tsx             # Product listing table
│   │   ├── Login.tsx               # Login form
│   │   ├── Signup.tsx              # Registration form
│   │   └── UserInfo.tsx            # User context provider
│   └── index.html
```

## Database Schema

The app uses 7 tables:

```
users ──────────┐
                ├── wallets ──── payments
                └── user_purchases

product_categories ──── products ──── product_inventories
```

- **users** — accounts with roles (`admin`, `member`, `distributor`, `collaborator`)
- **wallets** — one per user, tracks balance (with non-negative constraint)
- **payments** — deposit/withdrawal records with status tracking (`pending` → `success` / `failed`)
- **user_purchases** — order history with quantity, total price, and raw data
- **product_categories** — groups like "Facebook", "BM", etc.
- **products** — items with price, stock count, discount, country, and description
- **product_inventories** — individual account entries per product (`available` → `sold` / `refunded` / `locked`)

## API Endpoints

```
POST   /api/login              # Log in (supports username or email)
POST   /api/recover-password   # Password recovery (WIP)

GET    /api/users/me            # Get current user profile
POST   /api/users/signup        # Register a new account
POST   /api/users/logout        # Log out (clears cookie)

GET    /api/products/           # List all products
POST   /api/products/           # Create a product (auth required)
DELETE /api/products/:id        # Delete a product (admin only)

GET    /api/categories/         # List categories
POST   /api/categories/         # Create a category

GET    /api/inventories/        # List all inventory (admin only)
GET    /api/inventories/:id     # Get single inventory item (admin only)
POST   /api/inventories/        # Bulk insert inventory items (admin only)
DELETE /api/inventories/:id     # Delete inventory item (admin only)
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### Backend

```bash
cd backend
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and talks to the backend at `http://localhost:8000`.

## How Auth Works

1. User logs in with username/email + password
2. Backend verifies credentials and issues a JWT
3. JWT is stored in an **HttpOnly cookie** (not localStorage — more secure)
4. Every protected request reads the cookie automatically
5. Admin-only routes check the `role` field in the token payload

## Inventory System

Adding inventory uses an **atomic SQL transaction** (CTE) to insert items and update the product stock count in a single query — no race conditions, no inconsistent data:

```sql
WITH insert_inventory AS (
    INSERT INTO product_inventories (product_id, data)
    SELECT :product_id, unnest(:items)
    RETURNING 1
)
UPDATE products
SET stock = stock + (SELECT COUNT(*) FROM insert_inventory)
WHERE id = :product_id
RETURNING stock
```

## License

MIT
