\c docker;

CREATE SCHEMA sreality;

CREATE TABLE IF NOT EXISTS sreality.property (
    id INT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    locality TEXT NOT NULL,
    price TEXT NOT NULL,
    image_urls TEXT[] NOT NULL
);
