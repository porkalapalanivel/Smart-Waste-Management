CREATE DATABASE waste_management;

USE waste_management;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    phone VARCHAR(15)
);

CREATE TABLE Complaints (
    complaint_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    location VARCHAR(255),
    complaint_type VARCHAR(100),
    description TEXT,
    status VARCHAR(50),
    complaint_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(255)
);
