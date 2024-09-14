-- CREATE DATABASE matomo_task_scheduler;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    encrypted_password varchar default ''::character varying not null,
    admin boolean DEFAULT false,
    sign_in_count INT DEFAULT 0,
    last_sign_in_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- INSERT INTO users (id, username, encrypted_password, admin, sign_in_count, created_at, updated_at, last_sign_in_at) VALUES (1, 'demo', 'pbkdf2:sha256:600000$PzxlSZY9TADyOQ88$004ba5f704d7c18cd96a61e870b335fe357d87ba2d414e4040429dbfe3ed8719', true, 0, '2024-09-08 18:53:42.938455 +00:00', '2024-09-08 18:53:42.938455 +00:00', null);

CREATE TABLE api_calls (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status_code INT,
    status varchar,
    total_rows_found INT,
    error_message TEXT DEFAULT NULL
);

CREATE TABLE daily_visits (
    id SERIAL PRIMARY KEY,
    id_visit INT NOT NULL UNIQUE,
    visit_ip VARCHAR,
    visitor_id VARCHAR,
    user_id VARCHAR,
    visitor_type VARCHAR,
    visit_count INTEGER,
    visit_duration INTEGER,
    number_of_actions INTEGER,
    number_of_interactions INTEGER,
    number_of_events INTEGER,
    device_type VARCHAR,
    device_brand VARCHAR,
    operating_system VARCHAR,
    device_model VARCHAR,
    browser_name VARCHAR,
    country VARCHAR,
    latitude VARCHAR,
    longitude VARCHAR,
    seconds_since_first_visit INTEGER,
    seconds_since_last_visit INTEGER,
    resolution VARCHAR,
    server_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE action_details (
    id SERIAL PRIMARY KEY,
    daily_visit_id INT NOT NULL,
    type varchar,
    url varchar,
    page_view_identifier varchar NOT NULL UNIQUE,
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

CREATE TABLE course_contents (
    id SERIAL PRIMARY KEY,
    lecture_no varchar,
    lecture_title varchar,
    youtube_link varchar,
    type_of varchar,
    language varchar,
    ex_number varchar,
    ex_instruction varchar,
    hint varchar,
    slides_link varchar,
    teams_link varchar,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);