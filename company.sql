-- Hashed passsword is: $2b$12$V/cXqWN/M2vTnYUcXMB9oODcNBX/QorJekmaDkq1Z7aeD3I5ZAjfu

DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_pk                 TEXT,
    user_username           TEXT,
    user_first_name         TEXT,
    user_last_name          TEXT,
    user_email              TEXT UNIQUE,
    user_password           TEXT,
    user_role               TEXT,
    user_created_at         INTEGER,
    user_updated_at         INTEGER,
    user_is_verified        INTEGER,
    user_blocked_at         INTEGER,
    user_deleted_at         INTEGER,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

INSERT INTO users VALUES(
    "d11854217ecc42b2bb17367fe33dc8f4",
    "johndoe",
    "Jhon",
    "Doe",
    "admin@company.com",
    "$2b$12$V/cXqWN/M2vTnYUcXMB9oODcNBX/QorJekmaDkq1Z7aeD3I5ZAjfu",
    "admin",
    1712674758,
    0,
    1,
    0,
    0
);

SELECT * FROM users

DELETE FROM users WHERE user_username != 'johndoe';

DELETE FROM users WHERE user_email== 'samu1493@stud.kea.dk';

UPDATE users SET user_deleted_at = 0 WHERE user_pk = '2132b02480194efe9d20096682d823b2'

###############################################################################################################

DROP TABLE IF EXISTS items;

CREATE TABLE items(
    item_pk                 TEXT,
    item_name               TEXT,
    item_lat                TEXT,
    item_lon                TEXT,
    item_stars              REAL,
    item_price_per_night    REAL,
    item_created_at         INTEGER,
    item_updated_at         INTEGER,
    item_owner_fk           TEXT,
    item_blocked_at         INTEGER,
    item_booked_at         INTEGER,
    PRIMARY KEY(item_pk)
) WITHOUT ROWID;

INSERT INTO items VALUES
("5dbce622fa2b4f22a6f6957d07ff4951", "Christiansborg Palace", 55.6761, 12.5770, 5, 2541, 1, 0,"01ad74495a114c28b80fd73be024aa7d",0,0),

("5dbce622fa2b4f22a6f6957d07ff4952", "Tivoli Gardens", 55.6736, 12.5681, 4.97, 985, 2, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4953", "Nyhavn", 55.6794, 12.5918, 3.45, 429, 3, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4954", "The Little Mermaid statue", 55.6929, 12.5998, 4, 862, 4, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4955", "Amalienborg Palace", 55.6846, 12.5949, 2.67, 1200, 5, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4956", "Copenhagen Opera House",  55.6796, 12.6021, 4.57, 1965, 6,0 ,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4957", "Rosenborg Castle", 55.6867, 12.5734, 4, 1700, 7, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4958", "The National Museum of Denmark", 55.6772, 12.5784, 5, 2100, 8, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4959", "Church of Our Saviour", 55.6732, 12.5986, 4.3, 985, 9, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0),
("5dbce622fa2b4f22a6f6957d07ff4910", "Round Tower",  55.6813, 12.5759, 4.8, 1200, 10, 0,"d11854217ecc42b2bb17367fe33dc8f4",0,0);

-- (page_number - 1) * items_per_page
-- (1 - 1) * 3 = 10 1 2
-- (2 - 1) * 3 = 3 4 5
-- (3 - 1) * 3 = 6 7 8


-- Page 4
-- 0 3 6 9
SELECT * FROM items 
ORDER BY item_created_at
LIMIT 9,3;


-- offset = (currentPage - 1) * itemsPerPage
-- page 1 = 1 2 3+
-- page 2 = 4 5 6
-- page 3 = 7 8 9
-- page 4 = 10
SELECT * FROM items 
ORDER BY item_created_at
LIMIT 3 OFFSET 9;





###############################################################################################################


DROP TABLE IF EXISTS items_images;

CREATE TABLE items_images(
    image_pk                TEXT,
    image_url               TEXT,
    item_fk                 TEXT, 
    image_created_at        INTEGER,
    PRIMARY KEY(image_pk)
) WITHOUT ROWID;

INSERT INTO items_images VALUES 
("213test","5dbce622fa2b4f22a6f6957d07ff4951.webp","5dbce622fa2b4f22a6f6957d07ff4951", 1),
("213test1","5dbce622fa2b4f22a6f6957d07ff4952.webp","5dbce622fa2b4f22a6f6957d07ff4952",0),
("213test2","5dbce622fa2b4f22a6f6957d07ff4953.webp","5dbce622fa2b4f22a6f6957d07ff4953",0),
("213test3","5dbce622fa2b4f22a6f6957d07ff4954.webp","5dbce622fa2b4f22a6f6957d07ff4954",0),
("213test4","5dbce622fa2b4f22a6f6957d07ff4955.webp","5dbce622fa2b4f22a6f6957d07ff4955",0),
("213test5","5dbce622fa2b4f22a6f6957d07ff4956.webp","5dbce622fa2b4f22a6f6957d07ff4956",0),
("213test6","5dbce622fa2b4f22a6f6957d07ff4957.webp","5dbce622fa2b4f22a6f6957d07ff4957",0),
("213test7","5dbce622fa2b4f22a6f6957d07ff4958.webp","5dbce622fa2b4f22a6f6957d07ff4958",0),
("213test8","5dbce622fa2b4f22a6f6957d07ff4959.webp","5dbce622fa2b4f22a6f6957d07ff4959",0),
("213test9","5dbce622fa2b4f22a6f6957d07ff4910.webp","5dbce622fa2b4f22a6f6957d07ff4910",0);


SELECT * FROM items_images

SELECT * FROM items_images INNER JOIN items ON items_images.item_fk  = items.item_pk;

SELECT * FROM items_images JOIN items ON items_images.item_fk  = items.item_pk WHERE item_blocked_at = 0;