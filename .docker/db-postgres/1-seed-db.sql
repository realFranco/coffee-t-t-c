INSERT INTO product(id, name, price, category) 
    VALUES (11, 'Coffee aa', 1.0, 'coffee'),
    (12, 'Coffee bb', 2.0, 'coffee'),
    (21, 'Accessory aa', 4.0, 'accessories'),
    (22, 'Accessory bb', 5.0, 'accessories'),
    (31, 'Equipment aa', 7.0, 'equipment'),
    (32, 'Equipment bb', 8.0, 'equipment');

INSERT INTO "user"(id) 
    VALUES (11);

INSERT INTO cart(id, user_id) 
    VALUES (1, 11);
