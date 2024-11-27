CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE TaskType (
    type VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    title VARCHAR(255) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    FOREIGN KEY (task_type) REFERENCES TaskType(type),
    status VARCHAR(25) NOT NULL,
    creation_time DATETIME NOT NULL,
    deadline DATETIME,
    completion_time DATETIME,
    description TEXT
);


INSERT INTO User (email, password, username)
VALUES ('ayse@example.com', 'pass789', 'Ayse');

INSERT INTO User (email, password, username)
VALUES ('ahmet@example.com', 'pass456', 'Ahmet');

INSERT INTO User (email, password, username)
VALUES ('ali@example.com', 'pass123', 'Ali');

INSERT INTO TaskType (type) VALUES
('Health'), ('Hobbies'), ('Job'),
('Family'), ('Financial'), ('Lifestyle');

INSERT INTO Task (title, description, status, deadline, creation_time, completion_time, user_id, task_type) VALUES

('Checkup', 'Schedule and attend a checkup', 'Done',
 '2024-10-25 17:00:00', '2024-10-10 10:00:00', '2024-10-25 12:00:00',
 1, 'Health'),

('Register to a cooking course', 'Take a course to improve skills', 'Done',
 '2024-11-01 17:00:00', '2024-10-05 10:00:00', '2024-10-12 11:00:00',
 1, 'Lifestyle'),

('Play guitar', 'Learn new song for an hour', 'Todo',
 '2024-11-05 20:00:00', '2024-10-20 14:00:00', NULL,
 1, 'Hobbies'),

('Grocery shopping', 'Buy groceries for the week', 'Todo',
 '2024-11-05 18:00:00', '2024-10-31 10:00:00', NULL,
 1, 'Family'),

('Read a book', 'Read for personal growth', 'Done',
 '2024-11-01 17:00:00', '2024-10-01 15:00:00', '2024-10-26 12:00:00',
 1, 'Lifestyle'),

('Join yoga classes', 'Signup for a yoga class', 'Done',
 '2024-10-31 17:00:00', '2024-10-20 10:00:00', '2024-11-03 11:00:00',
 1, 'Health'),

('Budget review', 'Review monthly expenses', 'Done',
 '2024-11-10 17:00:00', '2024-10-22 09:00:00', '2024-10-31 14:00:00',
 1, 'Financial'),

('Book flights', 'Book flights for summer vacation', 'Done',
 '2024-10-16 09:00:00', '2024-10-13 13:00:00', '2024-10-16 11:00:00',
 1, 'Lifestyle'),

('Pay bills', 'Ensure all bills are paid', 'Todo',
 '2024-11-30 17:00:00', '2024-11-01 09:00:00', NULL,
 1, 'Financial'),

('Complete project', 'Finish the assigned project', 'Done',
 '2024-10-31 17:00:00', '2024-10-20 10:00:00', '2024-11-03 11:00:00',
 1, 'Job'),

('Painting', 'Paint a landscape for 2 hours', 'Done',
 '2024-10-30 15:00:00', '2024-10-01 08:00:00', '2024-10-25 15:00:00',
 1, 'Hobbies'),

('Networking event', 'Attend the event', 'Todo',
 '2024-11-20 17:00:00', '2024-10-25 09:00:00', NULL,
 1, 'Job'),

('Plan a trip', 'Plan a trip for family', 'Todo',
 '2024-11-15 17:00:00', '2024-10-10 14:00:00', NULL,
 2, 'Family'),

('Gym workout', 'Do weight training for an hour', 'Done',
 '2024-10-19 14:00:00', '2024-10-12 10:00:00', '2024-10-19 11:00:00',
 2, 'Health'),

('Family reunion', 'Host a family gathering', 'Todo',
 '2024-11-25 17:00:00', '2024-10-28 13:00:00', NULL,
 2, 'Family'),

('Car maintenance', 'Take the car for a checkup', 'Done',
 '2024-10-30 17:00:00', '2024-10-20 10:00:00', '2024-10-31 10:00:00',
 2, 'Lifestyle'),

('Go for a walk', 'Walk for at least 30 mins', 'Done',
 '2024-10-20 17:00:00', '2024-10-15 10:00:00', '2024-10-20 10:00:00',
 2, 'Health'),

('Clean the house', 'Clean the whole house', 'Done',
 '2024-10-18 12:00:00', '2024-10-14 09:00:00', '2024-10-18 17:00:00',
 3, 'Lifestyle'),

('Submit report', 'Submit quarterly report', 'Todo',
 '2024-11-12 17:00:00', '2024-10-21 13:00:00', NULL,
 3, 'Job'),

('Call Mom', 'Call Mom and wish her', 'Todo',
 '2024-11-06 11:00:00', '2024-10-23 12:00:00', NULL,
 3, 'Family'),

('Write a blog post', 'Write about recent project', 'Todo',
 '2024-11-11 17:00:00', '2024-10-22 09:00:00', NULL,
 3, 'Job'),

('Donate clothes', 'Donate clothes not in use', 'Done',
 '2024-10-31 17:00:00', '2024-10-15 10:00:00', '2024-11-01 11:00:00',
 3, 'Lifestyle'),

('Garden maintenance', 'Plant new flowers', 'Done',
 '2024-11-15 17:00:00', '2024-10-15 13:00:00', '2024-11-10 15:00:00',
 3, 'Family');
