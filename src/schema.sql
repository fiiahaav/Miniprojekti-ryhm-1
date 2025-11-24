CREATE TABLE articles (
	id SERIAL PRIMARY KEY,
	author TEXT NOT NULL,
	title TEXT NOT NULL,
	journal TEXT NOT NULL,
	year INTEGER NOT NULL,
	month INTEGER,
	volume TEXT,
	number TEXT,
	pages TEXT,
	notes TEXT
);

CREATE TABLE books (
	id SERIAL PRIMARY KEY,
	author TEXT NOT NULL,
	editor TEXT NOT NULL,
	title TEXT NOT NULL,
	publisher TEXT NOT NULL,
	year INTEGER NOT NULL,
	month INTEGER,
	volume TEXT,
	number TEXT,
	pages TEXT,
	notes TEXT
);

CREATE TABLE inproceedings (
	id SERIAL PRIMARY KEY,
	author TEXT NOT NULL,
	title TEXT NOT NULL,
	booktitle TEXT,
	year INTEGER,
	month INTEGER,
	editor TEXT,
	volume TEXT,
	number TEXT,
	series TEXT,
	pages TEXT,
	address TEXT,
	organization TEXT,
	publisher TEXT,
	notes TEXT
);

CREATE TABLE miscs (
	id SERIAL PRIMARY KEY,
	author TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER NOT NULL,
	month INTEGER,
	url TEXT,
	notes TEXT
);