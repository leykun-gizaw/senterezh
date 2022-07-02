-- Initial setup of database

CREATE DATABASE IF NOT EXISTS senterezh_db;
CREATE USER IF NOT EXISTS 'senterezh_dev'@'localhost' IDENTIFIED BY 'senterezh_dev_pwd';
GRANT ALL PRIVILEGES ON senterezh_db.* TO 'senterezh_dev'@'localhost';
