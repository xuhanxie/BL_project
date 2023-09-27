CREATE DATABASE bridge_legal;

USE bridge_legal;

CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT UNIQUE,
    state_id INT,
    year_start INT,
    year_end INT,
    prefile INT,
    sine_die INT,
    prior INT,
    special INT,
    session_tag VARCHAR(255),
    session_title VARCHAR(255),
    session_name VARCHAR(255)
);


CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    people_id INT,
    party_id INT,
    state_id INT NOT NULL,
    party VARCHAR(1),
    role_id INT,
    role VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    suffix VARCHAR(10),
    nickname VARCHAR(50),
    district VARCHAR(20),
    ftm_eid INT,
    votesmart_id INT,
    opensecrets_id VARCHAR(50),
    knowwho_pid INT,
    ballotpedia VARCHAR(255),
    bioguide_id VARCHAR(50),
    committee_sponsor INT,
    committee_id INT,
    state_federal INT,
    session_id INT,
    UNIQUE KEY unique_people_session (people_id, session_id)
);

CREATE TABLE bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    number VARCHAR(255),
    url VARCHAR(255),
    status_date DATE,
    status INT,
    last_action_date DATE,
    last_action TEXT,
    title TEXT,
    description TEXT,
    session_id INT,
    UNIQUE KEY unique_bill_session (bill_id, session_id)
);

CREATE TABLE amendments (
    amendment_id INT PRIMARY KEY,
    bill_id INT,
    adopted INT,
    date DATE,
    title VARCHAR(255),
    description TEXT,
    url VARCHAR(255),
    state_link VARCHAR(255)
);
