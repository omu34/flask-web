CREATE TABLE students
(
    id bigint NOT NULL,
    fullname character varying(255)  NOT NULL,
   username character varying(255)  NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255)  NOT NULL     
);


INSERT INTO students(id, fullname,username,email, password)
VALUES (1, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');
VALUES (2, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');
VALUES (3, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');

CREATE TABLE signup
(
    id bigint NOT NULL,
    fullname character varying(255)  NOT NULL,
    username character varying(255)  NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255)  NOT NULL     
);


INSERT INTO signup(id, fullname,username,email, password)
VALUES (1, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');
VALUES (2, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');
VALUES (3, 'Bernard omu','Bern', 'bernard@gmail.com', '12345678');
