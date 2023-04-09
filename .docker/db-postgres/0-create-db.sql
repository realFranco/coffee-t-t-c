SELECT 
  'CREATE DATABASE coffee_shop' 
WHERE 
  NOT EXISTS (
    SELECT 
    FROM 
      pg_database 
    WHERE 
      datname = 'coffee_shop'
  );

CREATE TABLE cart (
  id SERIAL NOT NULL, 
  user_id int4 NOT NULL, 
  PRIMARY KEY (id)
);

CREATE TABLE "order" (
  id SERIAL NOT NULL, 
  cart_id int4 NOT NULL, 
  ttl_products float4 DEFAULT 0 NOT NULL, 
  ttl_discounts float4 DEFAULT 0 NOT NULL, 
  ttl_shipping float4 DEFAULT 0 NOT NULL, 
  PRIMARY KEY (id)
);

CREATE TABLE prods_in_cart (
  product_id int4 NOT NULL, 
  cart_id int4 NOT NULL, 
  quantity int4 DEFAULT 0 NOT NULL,
  PRIMARY KEY (cart_id, product_id)
);
COMMENT ON TABLE prods_in_cart IS 'Products in Cart.';

CREATE TYPE product_category AS ENUM ('accessories', 'coffee', 'equipment');

CREATE TABLE product (
  id SERIAL NOT NULL, 
  name varchar(255) NOT NULL, 
  price float4 DEFAULT 0 NOT NULL, 
  category product_category NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE "user" (
  id SERIAL NOT NULL, 
  PRIMARY KEY (id)
);
COMMENT ON TABLE "user" IS 'User, on this context, will be an empty entity.';
COMMENT ON COLUMN "user".id IS 'User ID.';

ALTER TABLE 
  cart 
ADD 
  CONSTRAINT FKcart381905 FOREIGN KEY (user_id) REFERENCES "user" (id);

ALTER TABLE 
  "order" 
ADD 
  CONSTRAINT FKorder534182 FOREIGN KEY (cart_id) REFERENCES cart (id);

ALTER TABLE 
  prods_in_cart 
ADD 
  CONSTRAINT FKprods_in_c227732 FOREIGN KEY (product_id) REFERENCES product (id) ON UPDATE Cascade ON DELETE Cascade;

ALTER TABLE 
  prods_in_cart 
ADD 
  CONSTRAINT FKprods_in_c988850 FOREIGN KEY (cart_id) REFERENCES cart (id) ON UPDATE Cascade ON DELETE Cascade;
