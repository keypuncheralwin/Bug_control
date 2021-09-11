CREATE TABLE food(
    id SERIAL PRIMARY KEY,
    name TEXT,
    price INTEGER
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    password_hash TEXT
);

INSERT INTO food (name, price) VALUES ('Schnitzel burger', 1000);
INSERT INTO food (name, price) VALUES ('Veggie burger', 1000);
INSERT INTO food (name, price) VALUES ('Hot Dog', 700);


INSERT INTO users (email, name) VALUES ('tony@smallpp.com', 'Tiny Tony');

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    content TEXT
);

CREATE TABLE bugs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    created
);

INSERT INTO reviews (user_id, content) VALUES (1, 'Love the atmosphere!');
INSERT INTO reviews (user_id, content) VALUES (2, 'Very friendly service');
INSERT INTO reviews (user_id, content) VALUES (2, 'Delicious food');
INSERT INTO reviews (user_id, content) VALUES (4, 'Cool truck!');

SELECT reviews.id, reviews.content, reviews.user_id, users.name, users.email FROM reviews INNER JOIN users ON users.id = reviews.user_id;

SELECT reviews.content, users.name FROM reviews INNER JOIN users ON users.id = reviews.user_id;