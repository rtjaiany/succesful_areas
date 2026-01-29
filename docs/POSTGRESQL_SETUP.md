# PostgreSQL Setup Guide for iGuide Project

## Overview

This guide will help you set up PostgreSQL for storing satellite embedding data.

---

## 1. Install PostgreSQL

### Windows

**Option A: Official Installer (Recommended)**

1. Download PostgreSQL from [official website](https://www.postgresql.org/download/windows/)
2. Run the installer
3. During installation:
    - Choose a password for the `postgres` superuser (remember this!)
    - Default port: `5432`
    - Locale: Default
4. Install pgAdmin 4 (included with installer) for GUI management

**Option B: Using Chocolatey**

```bash
choco install postgresql
```

### Verify Installation

```bash
# Check PostgreSQL version
psql --version

# Should output something like: psql (PostgreSQL) 16.x
```

---

## 2. Create Database and User

### Option A: Using psql Command Line

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# In psql prompt, run:
CREATE DATABASE iguide_db;
CREATE USER iguide_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE iguide_db TO iguide_user;

# Grant schema privileges
\c iguide_db
GRANT ALL ON SCHEMA public TO iguide_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO iguide_user;

# Exit psql
\q
```

### Option B: Using pgAdmin 4

1. Open pgAdmin 4
2. Connect to PostgreSQL server (localhost)
3. Right-click "Databases" → "Create" → "Database"
    - Database name: `iguide_db`
    - Owner: postgres
4. Right-click "Login/Group Roles" → "Create" → "Login/Group Role"
    - Name: `iguide_user`
    - Password: Set a secure password
    - Privileges: Can login
5. Right-click `iguide_db` → "Properties" → "Security"
    - Add `iguide_user` with all privileges

---

## 3. Configure Environment Variables

Edit your `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iguide_db
DB_USER=iguide_user
DB_PASSWORD=your_secure_password
```

**Important**: Never commit the `.env` file to Git! It's already in `.gitignore`.

---

## 4. Install PostgreSQL Extension (Optional but Recommended)

For spatial data support (if you want to store municipality geometries):

```sql
-- Connect to iguide_db
\c iguide_db

-- Install PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify installation
SELECT PostGIS_Version();
```

---

## 5. Create Database Tables

### Option A: Using Python Script (Recommended)

```bash
# Activate virtual environment first
.\venv\Scripts\activate

# Create tables
python src/preprocessing/database_integration.py --create-tables
```

### Option B: Using SQL Script Directly

```bash
# Run the SQL script
psql -U iguide_user -d iguide_db -f sql/create_tables.sql
```

---

## 6. Verify Database Setup

### Check Tables

```bash
# Connect to database
psql -U iguide_user -d iguide_db

# List tables
\dt

# Describe satellite_embeddings table
\d satellite_embeddings

# Exit
\q
```

### Using Python

```bash
python src/preprocessing/database_integration.py --stats
```

---

## 7. Test Connection

Create a test script to verify connection:

```python
# test_db_connection.py
from src.preprocessing.database_integration import DatabaseManager

db = DatabaseManager()
if db.engine:
    print("✅ Database connection successful!")
    stats = db.get_summary_stats()
    print(f"Database stats: {stats}")
else:
    print("❌ Database connection failed!")
```

Run it:

```bash
python test_db_connection.py
```

---

## 8. Common PostgreSQL Commands

### Database Management

```sql
-- List all databases
\l

-- Connect to a database
\c iguide_db

-- List all tables
\dt

-- Describe a table
\d satellite_embeddings

-- List all users
\du

-- Show current database
SELECT current_database();

-- Show current user
SELECT current_user;
```

### Data Queries

```sql
-- Count records
SELECT COUNT(*) FROM satellite_embeddings;

-- View sample data
SELECT * FROM satellite_embeddings LIMIT 5;

-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('satellite_embeddings'));

-- View indexes
\di
```

---

## 9. Performance Tuning (Optional)

For large datasets, consider these PostgreSQL settings:

Edit `postgresql.conf` (location varies by installation):

```conf
# Memory settings
shared_buffers = 256MB          # 25% of RAM
effective_cache_size = 1GB      # 50-75% of RAM
work_mem = 16MB                 # For sorting/joins
maintenance_work_mem = 128MB    # For VACUUM, CREATE INDEX

# Connection settings
max_connections = 100

# Query planner
random_page_cost = 1.1          # For SSD
effective_io_concurrency = 200  # For SSD
```

Restart PostgreSQL after changes:

```bash
# Windows (as Administrator)
net stop postgresql-x64-16
net start postgresql-x64-16
```

---

## 10. Backup and Restore

### Backup Database

```bash
# Full database backup
pg_dump -U iguide_user -d iguide_db -F c -f iguide_db_backup.dump

# SQL format backup
pg_dump -U iguide_user -d iguide_db > iguide_db_backup.sql

# Backup specific table
pg_dump -U iguide_user -d iguide_db -t satellite_embeddings > embeddings_backup.sql
```

### Restore Database

```bash
# From custom format
pg_restore -U iguide_user -d iguide_db iguide_db_backup.dump

# From SQL format
psql -U iguide_user -d iguide_db < iguide_db_backup.sql
```

---

## 11. Security Best Practices

1. **Use Strong Passwords**: At least 16 characters with mixed case, numbers, symbols
2. **Limit Connections**: Configure `pg_hba.conf` to allow only necessary connections
3. **Regular Backups**: Schedule automated backups
4. **Update Regularly**: Keep PostgreSQL updated
5. **Monitor Logs**: Check PostgreSQL logs regularly

### Configure pg_hba.conf

Location: `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   iguide_db       iguide_user                             md5
host    iguide_db       iguide_user     127.0.0.1/32            md5
host    iguide_db       iguide_user     ::1/128                 md5
```

---

## 12. Troubleshooting

### Connection Refused

**Problem**: `psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solutions**:

1. Check if PostgreSQL is running:
    ```bash
    # Windows
    Get-Service postgresql*
    ```
2. Verify port 5432 is not blocked by firewall
3. Check `postgresql.conf` has `listen_addresses = 'localhost'`

### Authentication Failed

**Problem**: `FATAL: password authentication failed for user "iguide_user"`

**Solutions**:

1. Verify password in `.env` file
2. Check user exists: `psql -U postgres -c "\du"`
3. Reset password:
    ```sql
    ALTER USER iguide_user WITH PASSWORD 'new_password';
    ```

### Permission Denied

**Problem**: `ERROR: permission denied for table satellite_embeddings`

**Solutions**:

```sql
-- Grant all privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO iguide_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO iguide_user;
```

### Database Does Not Exist

**Problem**: `FATAL: database "iguide_db" does not exist`

**Solution**:

```bash
psql -U postgres -c "CREATE DATABASE iguide_db;"
```

---

## 13. GUI Tools

### pgAdmin 4 (Included with PostgreSQL)

- Full-featured database management
- Query tool
- Visual schema designer
- Backup/restore tools

### DBeaver (Free, Cross-platform)

- Download: https://dbeaver.io/
- Supports multiple databases
- Great for data exploration

### DataGrip (JetBrains, Paid)

- Professional database IDE
- Advanced query features
- Excellent for development

---

## 14. Next Steps

After setting up PostgreSQL:

1. ✅ Create database and user
2. ✅ Configure `.env` file
3. ✅ Create tables using Python script
4. ✅ Test connection
5. ✅ Run data extraction from GEE
6. ✅ Preprocess data
7. ✅ Ingest data into PostgreSQL
8. ✅ Query and analyze data

---

## Quick Start Commands

```bash
# 1. Create database (run once)
psql -U postgres -c "CREATE DATABASE iguide_db;"
psql -U postgres -c "CREATE USER iguide_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE iguide_db TO iguide_user;"

# 2. Create tables
python src/preprocessing/database_integration.py --create-tables

# 3. Ingest data
python src/preprocessing/database_integration.py --ingest data/processed/your_file.csv

# 4. Check stats
python src/preprocessing/database_integration.py --stats
```

---

## Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [PostGIS Documentation](https://postgis.net/documentation/)

---

**Created**: 2026-01-28  
**Last Updated**: 2026-01-28
