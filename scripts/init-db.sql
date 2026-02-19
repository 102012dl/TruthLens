-- TruthLens Database Initialization
-- =================================
-- Author: 102012dl

-- Create extension for UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE,
    email VARCHAR(255) UNIQUE,
    username VARCHAR(100),
    password_hash VARCHAR(255),
    plan VARCHAR(50) DEFAULT 'free',
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analysis requests table
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    text_content TEXT NOT NULL,
    url VARCHAR(2048),
    credibility_score INTEGER NOT NULL,
    verdict VARCHAR(50) NOT NULL,
    sentiment VARCHAR(50),
    sentiment_score FLOAT,
    bias_level VARCHAR(50),
    bias_score FLOAT,
    manipulation_score FLOAT,
    source_credibility FLOAT,
    source_name VARCHAR(255),
    key_findings JSONB DEFAULT '[]',
    recommendations JSONB DEFAULT '[]',
    manipulative_techniques JSONB DEFAULT '[]',
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sources table
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    credibility_score FLOAT NOT NULL,
    category VARCHAR(100),
    country VARCHAR(100),
    language VARCHAR(10),
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Trends table
CREATE TABLE IF NOT EXISTS trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    count INTEGER DEFAULT 0,
    average_credibility FLOAT,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    is_correct BOOLEAN,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at);
CREATE INDEX IF NOT EXISTS idx_analyses_credibility ON analyses(credibility_score);
CREATE INDEX IF NOT EXISTS idx_sources_domain ON sources(domain);
CREATE INDEX IF NOT EXISTS idx_trends_date ON trends(date);
CREATE INDEX IF NOT EXISTS idx_trends_topic ON trends(topic);

-- Insert default sources
INSERT INTO sources (domain, name, credibility_score, category, is_verified) VALUES
('reuters.com', 'Reuters', 0.95, 'news', true),
('apnews.com', 'Associated Press', 0.95, 'news', true),
('bbc.com', 'BBC News', 0.90, 'news', true),
('nytimes.com', 'The New York Times', 0.85, 'news', true),
('theguardian.com', 'The Guardian', 0.85, 'news', true),
('nature.com', 'Nature', 0.95, 'science', true),
('science.org', 'Science', 0.95, 'science', true),
('who.int', 'World Health Organization', 0.95, 'health', true)
ON CONFLICT (domain) DO NOTHING;
