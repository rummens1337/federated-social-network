CREATE TABLE IF NOT EXISTS posts (
    post_id INTEGER NOT NULL AUTO_INCREMENT,
    body VARCHAR NOT NULL,
    title VARCHAR DEFAULT 0,
    profile_id INTEGER NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS friends (
    profile_id INTEGER NOT NULL,
    friend VARCHAR NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    profile_id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    image_location VARCHAR DEFAULT 0,
    location VARCHAR DEFAULT 0,
    study VARCHAR DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edit_date TIMESTAMP DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP
);

