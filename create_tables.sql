--Create table employees
CREATE OR REPLACE TABLE employees(  
    employee_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    emp_position VARCHAR(50),
    sallary int,
    birth_date DATE,
    e_mail VARCHAR(50),
    phone int
) DEFAULT CHARSET UTF8;

--Create table trainings
CREATE OR REPLACE TABLE trainings(  
    training_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    training_day DATE NOT NULL,
    start_hour TIME NOT NULL,
    end_hour TIME,
    for_who VARCHAR(100),
    free_places int,
    trainer int,
    court VARCHAR(50),
    CONSTRAINT `trainer` FOREIGN KEY (trainer) REFERENCES employees(employee_id) ON UPDATE CASCADE ON DELETE SET NULL
) DEFAULT CHARSET UTF8;
