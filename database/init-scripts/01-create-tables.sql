CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    temporary BOOLEAN NOT NULL,
    email VARCHAR (64),
    activated BOOLEAN DEFAULT FALSE NOT NULL,
    nickname VARCHAR (64) NOT NULL,
    created_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS heuristics (
    id SERIAL PRIMARY KEY,
    name VARCHAR (32)
);

CREATE TABLE IF NOT EXISTS quizzes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    short_url VARCHAR (64) NOT NULL,
    question VARCHAR (256) NOT NULL,
    heuristic_id INTEGER REFERENCES heuristics(id) NOT NULL,
    answers_target INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS t_options (
    id SERIAL PRIMARY KEY,
    quizz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    text VARCHAR (128) NOT NULL
);

CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    option_id INTEGER NOT NULL REFERENCES t_options(id) ON DELETE CASCADE,
    index_order INTEGER NOT NULL
);
