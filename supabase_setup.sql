-- Create table for IP logs in Supabase
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS ip_logs (
    id BIGSERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    referer TEXT,
    hostname VARCHAR(255),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_ip_logs_timestamp ON ip_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_ip_logs_ip_address ON ip_logs(ip_address);

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE ip_logs ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows inserts from your service role key
-- This allows the app to insert data but keeps it secure from public access
CREATE POLICY "Enable insert for service role" ON ip_logs
    FOR INSERT
    TO authenticated, anon
    WITH CHECK (true);

-- Create a policy for reading (only for authenticated users)
CREATE POLICY "Enable read for authenticated users" ON ip_logs
    FOR SELECT
    TO authenticated
    USING (true);

-- Add a comment
COMMENT ON TABLE ip_logs IS 'Logs of IP addresses and visitor information';
