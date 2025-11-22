CREATE TABLE articles (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER,
	pages TEXT,
	url TEXT,
	notes TEXT
);

CREATE TABLE books (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER NOT NULL,
	publisher TEXT,
	pages TEXT,
	notes TEXT
);


CREATE TABLE inproceedings (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	title TEXT NOT NULL,
	booktitle TEXT,
	year INTEGER NOT NULL,
	publisher TEXT,
	pages TEXT,
	notes TEXT
);


CREATE TABLE miscs (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER NOT NULL,
	url TEXT,
	notes TEXT
);