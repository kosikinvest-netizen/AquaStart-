# AquaStart Web App

This is a Next.js 14 web application configured with TypeScript, Tailwind CSS, and ESLint.

## Getting Started

### Installation

With pnpm:
```bash
pnpm install
```

With npm:
```bash
npm install
```

With yarn:
```bash
yarn install
```

### Development Server

Run the development server:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

The application uses Supabase for backend services. Environment variables are located in `.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=your_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key
```

## Building for Production

```bash
pnpm build
pnpm start
```

## Project Structure

```
app/
├── layout.tsx      # Root layout component
├── page.tsx        # Home page
├── globals.css     # Global styles with Tailwind
public/            # Static assets
```

## Technologies Used

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **ESLint** - Code linting
- **Supabase** - Backend services
