# PostgreSQL Quick Reference

## 🚀 Quick Start Commands

### Initial Setup (Run Once)

```bash
# 1. Create database and user
psql -U postgres -c "CREATE DATABASE iguide_db;"
psql -U postgres -c "CREATE USER iguide_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE iguide_db TO iguide_user;"

# 2. Grant schema privileges
psql -U postgres -d iguide_db -c "GRANT ALL ON SCHEMA public TO iguide_user;"
psql -U postgres -d iguide_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO iguide_user;"

# 3. Update .env file with credentials
# Edit: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# 4. Create tables
python src/preprocessing/database_integration.py --create-tables

# 5. Test connection
python test_db_connection.py
```

---

## 📊 Daily Workflow

### 1. Extract Data from GEE

```bash
python src/gee/extract_embeddings.py
```

### 2. Preprocess Data

```bash
python src/preprocessing/process_satellite_data.py data/processed/municipality_embeddings_*.csv
```

### 3. Ingest to Database

```bash
python src/preprocessing/database_integration.py --ingest data/processed/processed_embeddings_*.csv
```

### 4. View Statistics

```bash
python src/preprocessing/database_integration.py --stats
```

---

## 🔍 Common Queries

### Connect to Database

```bash
psql -U iguide_user -d iguide_db
```

### Inside psql:

```sql
-- Count total records
SELECT COUNT(*) FROM satellite_embeddings;

-- View sample data
SELECT municipality_name, state_code, extraction_date
FROM satellite_embeddings
LIMIT 10;

-- Count by state
SELECT state_code, COUNT(*) as count
FROM satellite_embeddings
GROUP BY state_code
ORDER BY count DESC;

-- Get latest embeddings
SELECT * FROM latest_embeddings LIMIT 10;

-- State summary
SELECT * FROM state_summary;

-- Exit
\q
```

---

## 🛠️ Maintenance

### Backup Database

```bash
pg_dump -U iguide_user -d iguide_db -F c -f iguide_db_backup.dump
```

### Restore Database

```bash
pg_restore -U iguide_user -d iguide_db iguide_db_backup.dump
```

### Optimize Performance

```sql
-- Update statistics
ANALYZE satellite_embeddings;

-- Vacuum and analyze
VACUUM ANALYZE satellite_embeddings;
```

### Check Table Size

```sql
SELECT pg_size_pretty(pg_total_relation_size('satellite_embeddings'));
```

---

## 🔧 Troubleshooting

### Check if PostgreSQL is Running

```bash
# Windows
Get-Service postgresql*

# Linux/Mac
sudo systemctl status postgresql
```

### Reset User Password

```sql
ALTER USER iguide_user WITH PASSWORD 'new_password';
```

### Grant All Permissions

```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO iguide_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO iguide_user;
```

---

## 📚 Resources

- **Full Setup Guide**: `docs/POSTGRESQL_SETUP.md`
- **Database Schema**: `docs/database_schema.md`
- **Sample Queries**: `sql/sample_queries.sql`
- **Create Tables**: `sql/create_tables.sql`

---

## 💡 Tips

1. **Always backup** before major operations
2. **Use transactions** for data modifications
3. **Monitor table size** and vacuum regularly
4. **Create indexes** for frequently queried columns
5. **Use views** for complex, repeated queries

---

**Last Updated**: 2026-01-28
