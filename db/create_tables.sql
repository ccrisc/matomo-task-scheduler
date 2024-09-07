-- CREATE DATABASE matomo_task_scheduler;

CREATE TABLE api_calls (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    status_code INT,
    status varchar,
    total_rows_found INT,
    error_message TEXT DEFAULT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    encrypted_password varchar default ''::character varying not null,
    sign_in_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE daily_visits (
    id SERIAL PRIMARY KEY,
    idVisit INT NOT NULL,
    visitIp VARCHAR(45) NOT NULL,
    PRIMARY KEY (idVisit)
);

