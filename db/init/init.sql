USE appdb;

CREATE TABLE IF NOT EXISTS page_visits (
    id INT PRIMARY KEY,
    visits INT NOT NULL DEFAULT 0
);

INSERT IGNORE INTO page_visits (id, visits) VALUES (1, 0);