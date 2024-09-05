CREATE TABLE api_calls (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    status_code INT,
    status VARCHAR(50),
    total_rows_found INT,
    error_message TEXT
);


CREATE TABLE visits (
    idSite INTEGER,
    idVisit INTEGER,
    visitIp TEXT,
    visitorId TEXT,
    fingerprint TEXT,
    type TEXT,
    url TEXT,
    pageTitle TEXT,
    pageIdAction INTEGER,
    idpageview INTEGER,
    serverTimePretty TEXT,
    pageId INTEGER,
    timeSpent INTEGER,
    timeSpentPretty TEXT,
    pageviewPosition INTEGER,
    title TEXT,
    subtitle TEXT,
    icon TEXT,
    iconSVG TEXT,
    timestamp TIMESTAMP,
    PRIMARY KEY (idVisit, idSite, timestamp) -- Composite primary key for uniqueness
);
