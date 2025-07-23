#!/usr/bin/env bash
# Purpose:  ▸ back‑up Postgres
#           ▸ pull only Django code from GitHub
#           ▸ rebuild & restart the web container (no‑deps)
# Usage:    chmod +x update_webapp.sh && ./update_webapp.sh
# ───────────────────────────────────────────────────────────
set -euo pipefail

# ─── Config ────────────────────────────────────────────────
REPO_URL="https://github.com/millalgo/indexer.git"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$PROJECT_ROOT/db_backups"
TIMESTAMP="$(date +'%Y%m%d_%H%M%S')"
TMP_CLONE="$(mktemp -d)"

# ─── 1/4  Back up Postgres ─────────────────────────────────
echo "🔄 1/4  Backing‑up Postgres…"
mkdir -p "$BACKUP_DIR"

# Discover credentials from the running container
DB_USER="$(docker compose -f "$PROJECT_ROOT/docker-compose.yml" \
            exec -T db printenv POSTGRES_USER 2>/dev/null || true)"
DB_USER="${DB_USER:-postgres}"

DB_PASSWORD="$(docker compose -f "$PROJECT_ROOT/docker-compose.yml" \
               exec -T db printenv POSTGRES_PASSWORD 2>/dev/null || true)"

# Feed password to pg_dumpall only if it exists
if [[ -n "$DB_PASSWORD" ]]; then export PGPASSWORD="$DB_PASSWORD"; fi

docker compose -f "$PROJECT_ROOT/docker-compose.yml" \
  exec -T db pg_dumpall -U "$DB_USER" \
  | gzip > "$BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz"

unset PGPASSWORD
echo "      ➜  $BACKUP_DIR/postgres_${TIMESTAMP}.sql.gz"

# ─── 2/4  Fetch latest Django source ───────────────────────
echo "🔄 2/4  Fetching latest Django source…"
git clone --depth 1 "$REPO_URL" "$TMP_CLONE"

# ─── 3/4  Sync Django files only ───────────────────────────
echo "🔄 3/4  Syncing Django files into project…"
rsync -a --delete \
      --prune-empty-dirs \
      --include='/core/***' \
      --include='/home/***' \
      --include='/manage.py' \
      --include='/requirements.txt' \
      --exclude='*' \
      "$TMP_CLONE"/ "$PROJECT_ROOT"/
rm -rf "$TMP_CLONE"

# ─── 4/4  Rebuild & restart web service ────────────────────
echo "🔄 4/4  Rebuilding & restarting web…"
docker compose -f "$PROJECT_ROOT/docker-compose.yml" build web
docker compose -f "$PROJECT_ROOT/docker-compose.yml" up -d --no-deps web
echo "✅  Update complete."
