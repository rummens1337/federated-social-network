CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    email_confirmed int(1) NOT NULL DEFAULT 0,
    password VARCHAR(1000) NOT NULL,
    uploads_id INTEGER DEFAULT NULL,
    location VARCHAR(1000) DEFAULT '-',
    study VARCHAR(1000) DEFAULT '-',
    bio VARCHAR(1000) DEFAULT '-',
    relationship_status VARCHAR(1000) DEFAULT '-',
    phone_number VARCHAR(1000) DEFAULT '-',
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    body VARCHAR(1000) NOT NULL,
    title VARCHAR(1000) DEFAULT NULL,
    username VARCHAR(255) NOT NULL,
    uploads_id INTEGER DEFAULT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    post_id INTEGER NOT NULL,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    comment VARCHAR(1000) NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

-- CREATE TABLE IF NOT EXISTS likes (
--     id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
--     FOREIGN KEY (username) REFERENCES users(username),
--     FOREIGN KEY (id) REFERENCES posts(id)
-- );

CREATE TABLE IF NOT EXISTS friends (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    friend VARCHAR(255) NOT NULL,
    accepted INT NOT NULL DEFAULT 0,
    sender INT NOT NULL DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    filename VARCHAR(1000) NOT NULL,
    location VARCHAR(1000) NOT NULL,
    filesize INTEGER NOT NULL,
    type VARCHAR(1000) NOT NULL,
    sha256 VARCHAR(64) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hobbies (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    title VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    title VARCHAR(255) NOT NULL,
    skill_level INT NOT NULL DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    title VARCHAR(255) NOT NULL,
    skill_level INT NOT NULL DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);