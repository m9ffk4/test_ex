CREATE DATABASE IF NOT EXISTS data;

CREATE TABLE data.data
(
    timestamp DateTime,
    message String
)
ENGINE = MergeTree
ORDER BY timestamp;
