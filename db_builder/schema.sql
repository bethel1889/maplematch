DROP TABLE IF EXISTS users;
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT);

CREATE UNIQUE INDEX username ON users (username);

DROP TABLE IF EXISTS occupations;
CREATE TABLE occupations(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    number INTEGER NOT NULL);

DROP TABLE IF EXISTS employers;
CREATE TABLE employers(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    company TEXT NOT NULL);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    address TEXT NOT NULL);

DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    employer_id INTEGER NOT NULL,
    occupation_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    region INTEGER NOT NULL,
    program_stream INTEGER NOT NULL,
    approved_lmia INTEGER NOT NULL,
    approved_position INTEGER NOT NULL,
    FOREIGN KEY(employer_id) REFERENCES employers(id),
    FOREIGN KEY(occupation_id) REFERENCES occupations(id),
    FOREIGN KEY(location_id) REFERENCES locations(id));

DROP TABLE IF EXISTS user_jobs;
CREATE TABLE user_jobs(
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id));

CREATE UNIQUE INDEX company ON employers (company);
CREATE UNIQUE INDEX name ON occupations (name);
CREATE UNIQUE INDEX address ON locations (address);
