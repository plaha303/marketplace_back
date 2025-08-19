SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

-- Create extensions in the public schema
CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA public;
COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS user_service;
CREATE SCHEMA IF NOT EXISTS order_service;
CREATE SCHEMA IF NOT EXISTS payment_service;
CREATE SCHEMA IF NOT EXISTS product_service;
CREATE SCHEMA IF NOT EXISTS shipping_service;

-- Grant permissions to the user
GRANT ALL ON SCHEMA public TO dev;
GRANT ALL ON SCHEMA user_service TO dev;
GRANT ALL ON SCHEMA order_service TO dev;
GRANT ALL ON SCHEMA payment_service TO dev;
GRANT ALL ON SCHEMA product_service TO dev;
GRANT ALL ON SCHEMA shipping_service TO dev;

-- Set default search_path for the user
ALTER ROLE dev SET search_path TO public,user_service,order_service,payment_service,product_service,shipping_service;

-- Ensure extensions are available in all schemas
GRANT USAGE ON SCHEMA public TO dev;