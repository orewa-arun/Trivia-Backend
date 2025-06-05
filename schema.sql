CREATE TABLE allowed_users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active CHAR DEFAULT 'A'
);


DROP VIEW IF EXISTS leaderboard;
DROP TABLE IF EXISTS user_answers;
DROP TABLE IF EXISTS game_sessions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS ads;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uid TEXT UNIQUE, -- Firebase UID -> will be "guest" if users are not signed in
    email TEXT,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE game_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    score INTEGER DEFAULT 0
);


CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question TEXT,
    options TEXT[], -- 4 options
    correct_index INTEGER,
    mul_correct_indices INTEGER[], -- for multiple correct answers
    question_type TEXT,   -- 'MCQ' or 'MUL'
    category TEXT,   -- 'history' or 'ad'
    ad_id INTEGER,   -- NULL if not ad-based
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE user_answers (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES game_sessions(id),
    question_id INTEGER REFERENCES questions(id),
    selected_index INTEGER,
    is_correct BOOLEAN,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    duration INTEGER  -- in seconds
);


CREATE OR REPLACE VIEW leaderboard AS
SELECT 
    u.id AS user_id,
    u.name,
    s.score,
    s.started_at,
    s.completed_at
FROM game_sessions s
JOIN users u ON u.id = s.user_id
ORDER BY s.score DESC, s.completed_at ASC;