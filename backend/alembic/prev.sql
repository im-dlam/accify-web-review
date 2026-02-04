create table users (
	id serial primary key,
	username varchar(255) unique not null,
	email varchar(100) unique not null,
	password_hash text not null,
	full_name varchar(255) default 'anonymous',
	role char(50) check (role in ('admin','member')) default 'member',
	is_active boolean default true,
	created_at timestamp default now(),
	updated_at timestamp default now()
)

/*
SELECT 
	*
FROM 
	information_schema.table_constraints
where table_name ='users'

alter table users drop constraint users_role_check

alter table users alter column role type varchar(50)
alter table users add constraint users_role_check check(role in ('admin','member'))
alter table users alter column role set default 'member'
*/
create index idx_username on users(username)
create index idx_email on users(email)

/* Product categories */
create table product_categories (
	id serial primary key,
	name varchar(255),
	keyword varchar(255),
	color varchar(255),
	created_at timestamp default now(),
	updated_at timestamp default now()
)

create index idx_product_category_keyword on product_categories(keyword)

/* Product */

create table products (
	id serial primary key,
	category_id int not null,
	name varchar(255) not null,
	price decimal(18, 2) check (price > 0) not null,
	stock int check (stock >= 0) default 0,
	sold int check (sold >= 0) default 0,
	discount int check(discount >= 0) default 0,
	subtitle varchar(255) default null,
	description text default 'no description',
	country varchar(50) default 'random',
	image_url text,
	icons varchar(255),
	time timestamp default now(),
	created_at timestamp default now(),
	updated_at timestamp default now(),
	constraint uk_products_cid_name unique (category_id, name),
	constraint fk_products_cid foreign key (category_id) references product_categories(id)
)

create index idx_products_category_id on products(category_id)
create index idx_products_name on products(name)

/* Product Inventory */

create table product_inventories (
	id serial primary key,
	product_id int not null,
	data text not null,
	status varchar(50) check(status in ('available','sold','locked','refuned')) default 'available',
	created_at timestamp default now(),
	updated_at timestamp default now(),
	constraint uk_product_pid unique (product_id, data),
	constraint fk_product_inventories_pid foreign key (product_id) references products(id)
)

create index idx_product_inventories_pid on product_inventories(product_id)
create index idx_product_inventories_data on product_inventories(data)
create index idx_product_inventories_status on product_inventories(status)

create table user_purchaes (
	id serial primary key,
	user_id int not null references users(id),
	name varchar(255) not null,
	quantity int check (quantity > 0) default 1,
	total_price decimal(18,2) check(total_price > 0),
	data text,
	created_at timestamp default now(),
	updated_at timestamp default now()
)

create index idx_user_purchases_uid on user_purchases(id)
/*
alter table user_purchaes rename to user_purchases;
DROP INDEX IF EXISTS idx_user_purchaes_uid;
*/

/* wallet */

create table wallets (
	id serial primary key,
	user_id int references users(id) not null unique,
	balance decimal(18,2) check(balance >= 0) default 0,
	created_at timestamp default now()
)
create index idx_wallets_uid on wallets(user_id)

/* payments */
create table payments (
	id serial primary key,
	wallet_id int references wallets(id) not null,
	amount decimal(18, 2) not null check (amount > 0),
	status varchar(50) check(status in ('pending','success','failed')) default 'pending',
	description varchar(255),
	created_at timestamp default now()
)

create index idx_payments_wid on payments(wallet_id)

/* New func trigger auto update time */

create or replace function fn_auto_update_time()
returns trigger as $$
begin
	NEW.updated_at := now();
	return NEW;
end;
$$ language plpgsql;

-- trigger users
create trigger trg_auto_update_time_users
before update on users
for each row
execute function fn_auto_update_time();

-- trigger product_categories
create trigger trg_auto_update_time_product_categories
before update on product_categories
for each row
execute function fn_auto_update_time();
-- trigger products
create trigger trg_auto_update_time_products
before update on products
for each row
execute function fn_auto_update_time();
-- trigger product_inventories
create trigger trg_auto_update_time_product_inventories
before update on product_inventories
for each row
execute function fn_auto_update_time();
-- trigger user_purchases 
create trigger trg_auto_update_time_user_purchases
before update on user_purchases
for each row
execute function fn_auto_update_time();
-- trigger wallets 
create trigger trg_auto_update_time_wallets
before update on wallets
for each row
execute function fn_auto_update_time();
-- triiger payments 
create trigger trg_auto_update_time_payments
before update on payments
for each row
execute function fn_auto_update_time();