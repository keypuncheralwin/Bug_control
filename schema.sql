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
    title TEXT,
    description TEXT,
    priority TEXT,
    user_id INTEGER
);

INSERT INTO bugs(created_on, title, description, priority, user_id) VALUES ('2021-09-11', 'Testing 1', 'This is sample description to test out the app', 'low', 2);

INSERT INTO reviews (user_id, content) VALUES (1, 'Love the atmosphere!');
INSERT INTO reviews (user_id, content) VALUES (2, 'Very friendly service');
INSERT INTO reviews (user_id, content) VALUES (2, 'Delicious food');
INSERT INTO reviews (user_id, content) VALUES (4, 'Cool truck!');

SELECT reviews.id, reviews.content, reviews.user_id, users.name, users.email FROM reviews INNER JOIN users ON users.id = reviews.user_id;

SELECT bugs.title, users.name FROM reviews INNER JOIN users ON users.id = reviews.user_id;

SELECT b.*, u.name FROM bugs b LEFT JOIN users u ON u.id = b.user_id WHERE u.id=2;

SELECT u.name FROM bugs b LEFT JOIN users u ON u.id = b.user_id WHERE b.id=4;

CREATE TABLE bugs (
    id SERIAL PRIMARY KEY,
    created_on TEXT,
    title TEXT,
    description TEXT,
    priority TEXT,
    user_id INTEGER,
    CONSTRAINT fk_bugs_user
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);

CREATE TABLE archive (
    id SERIAL PRIMARY KEY,
    archived_on TEXT,
    title TEXT,
    description TEXT,
    resolved TEXT,
    user_id INTEGER,
    archived_by TEXT
);



-- SELECT * FROM bugs WHERE title LIKE '%keyword%'

-- count bugs based on user_id
SELECT COUNT(b.id)  FROM bugs b LEFT JOIN users u ON u.id = b.user_id WHERE u.name='Matthew Perry';

SELECT u.name, COUNT(*) AS bug_count FROM bugs b INNER JOIN users u ON u.id = b.user_id GROUP BY b.user_id, u.name;

SELECT COUNT(b.priority)  FROM bugs b WHERE b.priority = 'High';

ALTER TABLE bugs ADD updated_on TEXT;

UPDATE bugs SET created_by WHERE user_id = 4 VALUES 'Matthew Perry';

UPDATE bugs
SET created_by = 'Robert Tucker'
WHERE user_id = 2;