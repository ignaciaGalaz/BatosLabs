create table if not exists superheores.cardumen_superhero(
	id serial primary key,
	name varchar(255) not null,
	height integer not null, 
	weight integer not null
);

create table if not exists superheores.cardumen_character(
	superhero_id serial primary key,
	biography_name varchar(255) not null,
	foreign key (superhero_id) references cardumen_superhero(id)
	
);

create table if not exists superheores.cardumen_alterego(
	id serial primary key,
	name varchar(255)
);

create table if not exists superheores.cardumen_workOccupation(
	id serial primary key,
	name varchar(255)
);

create table if not exists superheores.cardumen_superhero_alterego(
    superhero_id bigint not null,
    alterego_id bigint not null,
    primary key (superhero_id, alterego_id),
    foreign key (superhero_id) references cardumen_superhero(id),
    foreign key (alterego_id) references cardumen_alterego(id)
)

create table if not exists superheores.cardumen_superhero_workOccupation(
    superhero_id bigint not null,
    workOccupation_id bigint not null,
    primary key (superhero_id, workOccupation_id),
    foreign key (superhero_id) references cardumen_superhero(id),
    foreign key (workOccupation_id) references cardumen_workOccupation(id)
)