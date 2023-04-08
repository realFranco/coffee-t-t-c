-- CREATE DATABASE coffee_shop;

SELECT 'CREATE DATABASE coffee_shop' 
WHERE NOT EXISTS (
  SELECT 
  FROM pg_database 
  WHERE datname = 'coffee_shop'
);



CREATE TABLE cart (
  id INT PRIMARY KEY,
  name VARCHAR(255)
);
