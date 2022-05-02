/*
Add login to app by creating a userpass table containing
user login info
Author: Francisca Moya Jimenez
*/
use timeinv_db;

drop table if exists userpass;

create table userpass(
       username varchar(10) not null primary key,
       hashed char(60),
       foreign key (username) references staff(username)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;