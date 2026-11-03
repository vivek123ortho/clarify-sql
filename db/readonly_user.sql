-- Run as a superuser (e.g. postgres) after schema.sql and seed.sql.
-- Change the password, then put it in READONLY_DATABASE_URL in .env.
CREATE USER readonly_user WITH PASSWORD 'change_me';
GRANT CONNECT ON DATABASE shopdb TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;