CREATE TABLE Courses (
	code_module VARCHAR(50) NOT NULL,
	code_presentation VARCHAR(50) NOT NULL,
	module_presentation_length INT,
	PRIMARY KEY(code_module, code_presentation)
);

CREATE TABLE Assessments (
	code_module VARCHAR(50),
	code_presentation VARCHAR(50),
	id_assessment INT PRIMARY KEY NOT NULL UNIQUE,
	assessment_type VARCHAR(50),
	assessments_date INT,
	weight FLOAT, 
	FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE Vle (
	id_site INT PRIMARY KEY NOT NULL UNIQUE,
	code_module VARCHAR(50),
	code_presentation VARCHAR(50),
	activity_type VARCHAR(40),
	week_from INT,
	week_to INT,
	FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE Students (
	id_student INT PRIMARY KEY NOT NULL UNIQUE
);

CREATE TABLE StudentInfo (
	code_module VARCHAR(50),
	code_presentation VARCHAR(50),
	id_student INT REFERENCES Students(id_student),
	gender VARCHAR(3),
	region VARCHAR(50),
	highest_education VARCHAR(50),
	imd_band VARCHAR(16),
	age_band VARCHAR(16),
	num_of_prev_attempts INT,
	studied_credits INT,
	disability VARCHAR(3),
	final_result VARCHAR(50),
	FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE StudentRegistration (
	code_module VARCHAR(50),
	code_presentation VARCHAR(50),
	id_student INT,
	date_registration INT,
	date_unregistration INT,
	FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE StudentAssessment (
	id_student INT REFERENCES Students(id_student),
	id_assessment INT REFERENCES Assessments(id_assessment),
	date_submitted INT,
	is_banked INT,
	score INT
);

CREATE TABLE StudentVle (
	id_site INT REFERENCES Vle(id_site),
	id_student INT REFERENCES Students(id_student),
	code_module VARCHAR(50),
	code_presentation VARCHAR(50),
	studentvle_date INT,
	sum_click INT,
	FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);
