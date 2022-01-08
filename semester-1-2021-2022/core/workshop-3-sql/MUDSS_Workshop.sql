/*
CREATING A DATABASE 
*/
DROP DATABASE IF EXISTS mudss;

CREATE DATABASE mudss;
USE mudss;

/*
CREATING AND EDITING TABLES
*/

CREATE TABLE students_details (
  student_id INT
, first_name VARCHAR(64)
, date_of_birth DATE
, favourite_cheese VARCHAR(64) DEFAULT 'Blue Cheese'
)
;

INSERT INTO students_details VALUES
  (11111111, 'Jordan', '2000-01-01', 'Cheddar')
, (22222222, 'Julia' , '2000-01-02', 'Mozzarella')
, (33333333, 'Paul'  , '2000-01-03', 'Cheddar')
, (44444444, 'Lake'  , '2000-01-04', 'Wensleydale')
;

INSERT INTO students_details (student_id, first_name, date_of_birth) 
VALUES (55555555, 'Nial', '2000-01-05')
;

DELETE FROM students_details
WHERE first_name = 'Nial'        
;

CREATE TABLE students_cheese_purchases (
  student_id INT
, date_of_purchase DATE
, type_of_cheese VARCHAR(64)
, price DECIMAL(10,2)
)
;

INSERT INTO students_cheese_purchases VALUES
  (11111111, '2021-09-30', 'Cheddar', 2.50)
, (11111111, '2021-10-01', 'Cheddar', 5.00)
, (33333333, '2021-10-01', 'Goat Cheese', 245.10)
, (44444444, '2021-10-02', 'Goat Cheese', 6.99)
, (11111111, '2021-10-03', 'Goat Cheese', 13.98)
;

CREATE TABLE cheese_and_descriptions(
  type_of_cheese VARCHAR(64)
, description VARCHAR(256)
, useless_column VARCHAR(64) DEFAULT 'abc'  
)
;

INSERT INTO cheese_and_descriptions (type_of_cheese, description) 
VALUES
  ('Cheddar', 'Rich English cheese')
, ('Goat Cheese', 'Soft and creamy')
, ('Mozzarella', 'Perfect for pizza')
, ('Wensleydale', 'Nice with cranberries!')
, ('Feta', 'Crumbly')
;

UPDATE cheese_and_descriptions
SET useless_column = NULL
WHERE useless_column = 'abc'
; 

ALTER TABLE cheese_and_descriptions
DROP COLUMN useless_column
;

/*
RETRIEVING DATA FROM TABLES
*/

SELECT * 

FROM students_cheese_purchases

-- WHERE type_of_cheese <> 'Goat Cheese'
;

SELECT first_name
	, favourite_cheese
    
FROM students_details

WHERE first_name <> 'Paul' AND favourite_cheese <> 'Cheddar'
;

SELECT sd.first_name
	, scp.type_of_cheese
    
FROM students_details AS sd
INNER JOIN students_cheese_purchases AS scp
ON sd.student_id = scp.student_id
;

SELECT sd.first_name
	, scp.type_of_cheese
    , SUM(scp.price) AS spending
    
FROM students_details AS sd
INNER JOIN students_cheese_purchases AS scp
ON sd.student_id = scp.student_id

-- WHERE scp.type_of_cheese = 'Goat Cheese'

GROUP BY sd.first_name
	, scp.type_of_cheese
;

/*
DELETING TABLES
*/

DROP TABLE IF EXISTS students_details;
DROP TABLE IF EXISTS students_cheese_purchases;
DROP TABLE IF EXISTS cheese_and_descriptions;