-- CREATE DATABASE matomo_task_scheduler;

CREATE TABLE api_calls (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
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
    id_visit INT NOT NULL UNIQUE,
    visit_ip VARCHAR,
    visitor_id varchar,
    visit_count integer,
    visit_entry_id_action integer,
    visit_exit_id_action integer,
    device_type varchar,
    visit_duration_seconds integer,
    server_time timestamp,
    created_at timestamp
);

CREATE TABLE action_details (
    id SERIAL PRIMARY KEY,
    daily_visit_id INT NOT NULL,
    type varchar,
    url varchar,
    page_view_identifier varchar,
    page_id_action integer,
    timestamp timestamp,
    page_view_position integer,
    title varchar,
    subtitle varchar,
    -- only for event type action (page views)
    time_spent_seconds integer,
    page_load_time_milliseconds integer,
    -- only for event type event (page views)
    event_category varchar,
    event_action varchar,
    CONSTRAINT fk_daily_visit
        FOREIGN KEY (daily_visit_id)
        REFERENCES daily_visits (id)
        ON DELETE CASCADE
);
