use timeinv_db;

ALTER TABLE product
ADD COLUMN threshold int AFTER price;

UPDATE product SET threshold = 0;