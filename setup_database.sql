-- Create database
CREATE DATABASE IF NOT EXISTS `moneta_db`;
USE `moneta_db`;

-- creating user for the database
CREATE USER IF NOT EXISTS 'moneta_user'@'localhost' IDENTIFIED BY 'Moneta_User_PWD';

-- Granting all privileges to the user
GRANT ALL PRIVILEGES ON `moneta_db`.* TO 'moneta_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'moneta_user'@'localhost';

-- Flush the privileges
FLUSH PRIVILEGES;