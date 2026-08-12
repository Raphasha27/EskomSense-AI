# EskomSense AI - Supabase Upgrade Guide

This guide details how to integrate your Machine Learning load shedding predictor with a live Supabase PostgreSQL backend.

## 1. Setup Supabase
1. Create a project at [Supabase](https://supabase.com).
2. Obtain your Project URL and Anon Key.

## 2. Apply Schema & Types
1. Run the `schema.sql` script in your Supabase SQL Editor.
2. Run `seed.sql` to populate mock historical data, predictions, and energy tips.

## 3. Integration
1. Add `supabase-client.js` and `analytics.js` to your project folder.
2. Update `supabase-client.js` with your credentials and set `DEMO_MODE = false`.

## 4. Visualizing Data
Ensure you include Chart.js in your `index.html`:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Then hook up the analytics component to show real prediction accuracy vs actual Eskom schedules.
