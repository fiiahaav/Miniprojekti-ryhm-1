CREATE TABLE refs (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER,
	url TEXT,
	notes TEXT
);

