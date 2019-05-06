CREATE TABLE Students (
	student_id INT NOT NULL UNIQUE PRIMARY KEY
);

CREATE TABLE Sessions (
	session_id INT NOT NULL UNIQUE PRIMARY KEY
);

CREATE TABLE InterGrade (
	student_id INT REFERENCES Students(student_id),
	session_id INT REFERENCES Sessions(session_id),
	grade FLOAT
);

CREATE TABLE FinalGrade (
	student_id INT REFERENCES Students(student_id),
	session_id INT REFERENCES Sessions(session_id),
	question_no INT,
	max_grade FLOAT,
	grade FLOAT,
	passage_no INT
);

CREATE TABLE Presence (
	student_id INT REFERENCES Students(student_id),
	session_id INT REFERENCES Sessions(session_id),
	present BOOLEAN
);

CREATE TABLE Epm (
	student_id INT REFERENCES Students(student_id),
	session_id INT REFERENCES Sessions(session_id),
	exercice VARCHAR(50),
	activity VARCHAR(50),
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	idle_time INT,
	mouse_wheel INT,
	mouse_wheel_click INT,
	mouse_click_left INT,
	mouse_click_right INT,
	mouse_movement INT,
	keystroke INT
);
#CREATE TABLE join_result(student_id INT, session_id INT, i_grade FLOAT, question_no INT, max_grade FLOAT, grade FLOAT, passage_no INT, exercice VARCHAR(50), activity VARCHAR(50), start_time TIMESTAMP, end_time TIMESTAMP, idle_time INT, mouse_wheel INT, mouse_wheel_click INT, mouse_click_left INT, mouse_click_right INT, mouse_movement INT, keystroke INT);

