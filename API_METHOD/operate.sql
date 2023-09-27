
-- query how many people from illinois (state_id = 13) attended the session '103rd General Assembly'
SELECT COUNT(*) AS total_attendees
FROM people AS p
INNER JOIN sessions AS s ON p.session_id = s.session_id
WHERE s.session_name = '103rd General Assembly' AND p.state_id=13;

-- query adopted amendments in 2013
SELECT * FROM amendments WHERE adopted=1 AND YEAR(date) > 2012 AND YEAR(date) < 2014;

-- query all enacted bills in Alabama (state_id = 1)
SELECT bill_id, title, description
FROM bills b
JOIN sessions AS s ON b.session_id = s.session_id
WHERE last_action='Enacted' AND state_id = 1;