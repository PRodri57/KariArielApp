## KariAriel Web App
For managing clients, work orders and data!

### Base de datos
- Backend usa Supabase via `SUPABASE_URL` y `SUPABASE_SERVICE_KEY`.
- Usar la service key solo en backend (no exponer en frontend).
- No se permite SQLite ni Postgres local; la app asume DB remota.
- No hay sincronizacion ni backups locales (Supabase maneja durabilidad).
- El backend es el unico que accede a la DB (no exponer keys en frontend).

### Hosting en red (LAN / VPN / Internet)
- Backend debe escuchar en `0.0.0.0` y permitir CORS con `CORS_ORIGINS`.
- Frontend necesita `VITE_API_BASE_URL` apuntando al backend.
- Abrir firewall para los puertos `8000` (backend) y `5173` (frontend).

Ejemplo LAN (reemplazar `192.168.1.50` por la IP de la notebook):
```bash
# Backend
CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.50:5173" \
uvicorn App.main:app --host 0.0.0.0 --port 8000

# Frontend
VITE_API_BASE_URL="http://192.168.1.50:8000" \
VITE_USE_MOCKS="false" \
npm run dev -- --host 0.0.0.0 --port 5173
```

Acceso desde otras redes:
- Opcion recomendada: VPN (Tailscale/ZeroTier). Usar la IP del VPN en `CORS_ORIGINS` y `VITE_API_BASE_URL`.
- Opcion publica: tunnel (Cloudflare Tunnel, ngrok) o port-forwarding. Agregar el dominio publico a `CORS_ORIGINS`.

### Scripts de arranque
Se incluyen scripts para levantar ambos servicios desde la raiz del repo (bash):
```bash
# Backend: expone 0.0.0.0:8000 y arma CORS para la IP indicada
./scripts/run-backend.sh 192.168.1.50

# Frontend: expone 0.0.0.0:5173 y apunta al backend
./scripts/run-frontend.sh 192.168.1.50
```

En Windows PowerShell:
```powershell
# Backend
.\scripts\run-backend.ps1 192.168.1.50

# Frontend
.\scripts\run-frontend.ps1 192.168.1.50
```

Si PowerShell bloquea scripts:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Si queres persistir la configuracion del frontend, edita `Frontend/.env`:
```bash
VITE_API_BASE_URL=http://192.168.1.50:8000
VITE_USE_MOCKS=false
```
