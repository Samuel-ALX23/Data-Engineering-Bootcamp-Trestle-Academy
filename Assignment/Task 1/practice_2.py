## Create Database
CREATE DATABASE SchoolManagementSystem;

## Create Tables
CREATE TABLE Teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    subject VARCHAR(50) NOT NULL
);

CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    teacher_id INTEGER REFERENCES Teachers(teacher_id)
);

CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INTEGER CHECK (age > 0),
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    class_id INTEGER REFERENCES Classes(class_id)
);

CREATE TABLE Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    class_id INTEGER REFERENCES Classes(class_id)
);

CREATE TABLE Enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Students(student_id),
    subject_id INTEGER REFERENCES Subjects(subject_id),
    enrollment_date DATE NOT NULL
);

## Insert sample data
## Teachers
INSERT INTO Teachers (first_name, last_name, subject) VALUES
('John', 'Smith', 'Mathematics'),
('Sarah', 'Johnson', 'English'),
('Michael', 'Brown', 'Science'),
('Emily', 'Davis', 'History'),
('David', 'Wilson', 'Physics');

## Classes
INSERT INTO Classes (class_name, teacher_id) VALUES
('Class 10A', 1),
('Class 10B', 2),
('Class 11A', 3),
('Class 11B', 4),
('Class 12A', 5);

## Students (20 records)
INSERT INTO Students (first_name, last_name, age, gender, class_id) VALUES
('Alice', 'Anderson', 15, 'F', 1),
('Bob', 'Baker', 16, 'M', 1),
('Charlie', 'Clark', 15, 'M', 1),
('Diana', 'Davis', 16, 'F', 2),
('Edward', 'Evans', 15, 'M', 2),
('Fiona', 'Fisher', 16, 'F', 2),
('George', 'Gray', 17, 'M', 3),
('Hannah', 'Hall', 17, 'F', 3),
('Ian', 'Irving', 17, 'M', 3),
('Jane', 'Jones', 17, 'F', 3),
('Kevin', 'King', 18, 'M', 4),
('Laura', 'Lee', 18, 'F', 4),
('Mark', 'Miller', 18, 'M', 4),
('Nancy', 'Nelson', 18, 'F', 4),
('Oliver', 'Owen', 19, 'M', 5),
('Patricia', 'Parker', 19, 'F', 5),
('Quinn', 'Quinn', 19, 'M', 5),
('Rachel', 'Roberts', 19, 'F', 5),
('Steve', 'Smith', 18, 'M', 5),
('Tara', 'Turner', 18, 'F', 5);

## Subjects
INSERT INTO Subjects (subject_name, class_id) VALUES
('Advanced Mathematics', 1),
('English Literature', 1),
('Physics', 2),
('Chemistry', 2),
('Biology', 3),
('World History', 3),
('Computer Science', 4),
('Economics', 4),
('Statistics', 5),
('Environmental Science', 5);

## Enrollments
INSERT INTO Enrollments (student_id, subject_id, enrollment_date) VALUES
(1, 1, '2024-01-15'),
(1, 2, '2024-01-15'),
(2, 1, '2024-01-15'),
(3, 2, '2024-01-16'),
(4, 3, '2024-01-16'),
(5, 4, '2024-01-17'),
(6, 3, '2024-01-17'),
(7, 5, '2024-01-18'),
(8, 6, '2024-01-18'),
(9, 5, '2024-01-19');

# Query 1: Select all fields from Students table
SELECT * FROM Students;

## Query 2: Filter students above age 18
SELECT first_name, last_name, age 
FROM Students 
WHERE age >= 18;

## Query 3: List of classes ordered alphabetically
SELECT class_name 
FROM Classes 
ORDER BY class_name;

## Query 4: Count of students in each class
SELECT c.class_name, COUNT(s.student_id) as student_count
FROM Classes c
LEFT JOIN Students s ON c.class_id = s.class_id
GROUP BY c.class_name
ORDER BY c.class_name;

## Query 5: Students and their classes
SELECT s.first_name, s.last_name, c.class_name
FROM Students s
JOIN Classes c ON s.class_id = c.class_id
ORDER BY c.class_name, s.last_name;

## Query 6: Students, subjects, and teachers
SELECT 
    s.first_name as student_first_name,
    s.last_name as student_last_name,
    sub.subject_name,
    t.first_name as teacher_first_name,
    t.last_name as teacher_last_name
FROM Students s
JOIN Enrollments e ON s.student_id = e.student_id
JOIN Subjects sub ON e.subject_id = sub.subject_id
JOIN Classes c ON sub.class_id = c.class_id
JOIN Teachers t ON c.teacher_id = t.teacher_id
ORDER BY s.last_name, sub.subject_name;