CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    body VARCHAR(1000) NOT NULL,
    title VARCHAR(1000) DEFAULT NULL,
    users_id INTEGER NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS friends (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    users_id INTEGER NOT NULL,
    friend VARCHAR(1000) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(1000) NOT NULL,
    password VARCHAR(1000) NOT NULL,
    name VARCHAR(1000) NOT NULL,
    uploads_id INTEGER DEFAULT NULL,
    location VARCHAR(1000) DEFAULT NULL,
    study VARCHAR(1000) DEFAULT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(1000) NOT NULL,
    location VARCHAR(1000) NOT NULL,
    filesize INTEGER NOT NULL,
    type VARCHAR(1000) NOT NULL,
    sha256 VARCHAR(64) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);
