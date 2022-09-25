CREATE DATABASE IF NOT EXISTS logs;

CREATE TABLE IF NOT EXISTS logs.logs (
    message String
)
ENGINE = MergeTree()
ORDER BY tuple()

