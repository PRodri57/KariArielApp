## KariAriel Web App
For managing clients, work orders and data!

### Base de datos
- Backend usa Supabase via `SUPABASE_URL` y `SUPABASE_SERVICE_KEY`.
- Usar la service key solo en backend (no exponer en frontend).
- No se permite SQLite ni Postgres local; la app asume DB remota.
- No hay sincronizacion ni backups locales (Supabase maneja durabilidad).
- El backend es el unico que accede a la DB (no exponer keys en frontend).
