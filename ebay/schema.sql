drop table items;

create table items(
id integer primary key autoincrement, 
category char(50), 
title char(50), 
description char(255), 
price float, 
open boolean, 
end_date datetime,
winner char(50));

drop table bids;

create table bids(
id int references items(id), 
buyer char(50), 
price float,
time datetime);

drop table categories;
CREATE TABLE categories(name varchar(20));
insert into categories values('Electronics');
insert into categories values('Toys');
insert into categories values('Books');
insert into categories values('Auto');

drop table systemtime;
CREATE TABLE systemtime(curtime datetime);
insert into systemtime values('2015-04-28 18:00:00');

CREATE TRIGGER timeupdate AFTER UPDATE ON systemtime
FOR EACH ROW
BEGIN
	UPDATE items SET open = false where open = true AND end_date < new.curtime;
	UPDATE items SET winner = (select buyer from bids, items where open = false AND item.id = bids.id AND bids.price = (select max(price) from bids));
END;