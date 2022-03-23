-- Creates product, staff, transaction, supplier and supplyTerm tables.

use timeinv_db; 

drop table if exists supplierTerm;
drop table if exists supplier;
drop table if exists transaction;
drop table if exists product;
drop table if exists staff;

create table staff(
    username varchar(10),
    name varchar(50),
    role varchar(30), -- Maybe role and permission can be narrowed down  
    permission set('product','transaction','staff','supplier','supplierTerm'),
    primary key(username)
)
ENGINE = InnoDB;

create table product (
    sku int unsigned not null primary key,
    title varchar(50),
    price decimal(10,2),
    image_file_name varchar(100),
    last_modified_by varchar(10), -- staff username
    foreign key (last_modified_by) references staff(username)
        on update restrict
        on delete restrict
)
ENGINE = InnoDB;


create table transaction(
    timestamp datetime,
    tid int unsigned auto_increment,
    sku int unsigned,
    amount int, -- can be positive or negative (positive for increase in inventory aka. purchase, negative for decrease aka. sales)
    last_modified_by varchar(10), -- staff username
    primary key (tid,sku),
    index(timestamp), 
    foreign key (sku) references product(sku)
        on update restrict
        on delete restrict,
    foreign key (last_modified_by) references staff(username)
        on update restrict
        on delete restrict
)
ENGINE = InnoDB;

create table supplier(
    sid int unsigned,
    company_name varchar(50),
    last_modified_by varchar(10), -- staff username
    primary key(sid),
    foreign key (last_modified_by) references staff(username)
        on update restrict
        on delete restrict
)
ENGINE = InnoDB;

create table supplierTerm(
    sid int unsigned,
    sku int unsigned,
    cost decimal(10,2),
    last_modified_by varchar(10), -- staff username
    primary key(sid,sku),
    foreign key (last_modified_by) references staff(username)
        on update restrict
        on delete restrict,
    foreign key (sku) references product(sku)
        on update restrict
        on delete restrict
)
ENGINE = InnoDB;