
DROP TABLE IF EXISTS user_tab; 
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS course;

CREATE TABLE user_tab (
  id  INTEGER  PRIMARY KEY,  
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT  NOT NULL,
  email TEXT UNIQUE NOT NULL,
  telephone_number TEXT UNIQUE NOT NULL ,
  birthday TEXT NOT NULL,
  prof_skills TEXT NOT NULL,
  isMentor BOOLEAN NOT NULL

);

CREATE TABLE post (
  id INTEGER  PRIMARY KEY ,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user_tab (id)
);


CREATE TABLE course (
    author_id INTEGER NOT NULL,
    id  INTEGER  PRIMARY KEY,  
    name TEXT NOT NULL, 
    start_date DATE NOT NULL,
    descr TEXT NOT NULL,
    students_id TEXT ,
    volunteers  TEXT NOT NULL,
    min_age INTEGER NOT NULL,
    max_age INTEGER NOT NULL,
    end_date DATE NOT NULL,
    min_people INTEGER NOT NULL,
    max_people INTEGER NOT NULL,
    schedule TEXT NOT NULL,
    min_knowledge TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user_tab (id),
    FOREIGN KEY (students_id) REFERENCES user_tab (id)
);

