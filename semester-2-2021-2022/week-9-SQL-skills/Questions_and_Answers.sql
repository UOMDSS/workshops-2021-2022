-- MUDSS SQL Workshop Tasks 27.04.22 --

/*
1) Write a query that returns data for all applicants. Use only the 'applicants' table for now.
*/

SELECT *
FROM applicants
;

/*
2) Write a query that returns the number of applicants.
*/

SELECT COUNT(*)
FROM applicants
;

/*
3) Write a query that returns the number of applicants at a University in Manchester aged 30 or less.
*/

SELECT COUNT(*)
FROM applicants
WHERE 1=1
	AND university LIKE '%Manchester%'
	AND age <= 30
;

/*
4) Write a query that returns data for all applicants alongside their score in the data science survey.
*/

SELECT *
FROM applicants LEFT JOIN survey_scores
USING(student_id)
; 

/*
5) Using your answer in (4), write a query to identify the 5 candidates with the highest score that are at a University in Manchester and aged 30 or less.
*/

SELECT *
FROM applicants AS a
LEFT JOIN survey_scores AS ss
USING(student_id)
WHERE 1=1
	AND university LIKE '%Manchester%'
	AND age <= 30
ORDER BY score DESC
LIMIT 5

/*
6) Write a query to identify the 5 candidates with the highest number of extracurriculars that are NOT in the top 5 candidates you identified for (5).
*/

SELECT *
FROM (
	SELECT *
	FROM applicants AS a
	LEFT JOIN cities AS c
	USING(city)
	LEFT JOIN survey_scores AS ss
	USING(student_id)
	LEFT JOIN extracurriculars AS e
	USING(student_id)
	) 
    
WHERE 1=1
	AND student_id NOT IN (
		SELECT student_id
		FROM applicants AS a
        	LEFT JOIN survey_scores AS ss
        	USING(student_id)
		WHERE university LIKE '%Manchester%'
    		AND age <= 30
		ORDER BY score DESC
		LIMIT 5)

ORDER BY extra_curriculars DESC
LIMIT 5
;

/*
7) Write a query to return the 10 candidates you have identified in (5) and (6). This is your final submission for the brief!
*/

SELECT *
FROM (
	SELECT *
	FROM applicants AS a
	LEFT JOIN cities AS c
	USING(city)
	LEFT JOIN survey_scores AS ss
	USING(student_id)
	LEFT JOIN extracurriculars AS e
	USING(student_id)
    WHERE 1=1 
		AND university LIKE '%Manchester%'
    	AND age <= 30
        ORDER BY score DESC
        LIMIT 5
        ) 

UNION

SELECT *
FROM (
	SELECT *
	FROM applicants AS a
	LEFT JOIN cities AS c
	USING(city)
	LEFT JOIN survey_scores AS ss
	USING(student_id)
	LEFT JOIN extracurriculars AS e
	USING(student_id)
    WHERE 1=1
	AND student_id NOT IN (
		SELECT student_id
		FROM applicants AS a
        	LEFT JOIN survey_scores AS ss
        	USING(student_id)
		WHERE university LIKE '%Manchester%'
    		AND age <= 30
		ORDER BY score DESC
		LIMIT 5)
        ORDER BY extra_curriculars DESC
        LIMIT 5
	) 
    
;
