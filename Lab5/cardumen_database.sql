create table if not exists superheores.cardumen_superhero(
	id serial primary key,
	name varchar(255) not null,
	height integer,
	weight integer
);

create table if not exists superheores.cardumen_character(
	superhero_id serial primary key,
	biography_name varchar(255),
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

create table if not exists superheores.cardumen_superheroe_alterego(
    superhero_id bigint not null,
    alterego_id bigint not null,
    primary key (superhero_id, alterego_id),
    foreign key (superhero_id) references cardumen_superhero(id),
    foreign key (alterego_id) references cardumen_alterego(id)
)

create table if not exists superheores.cardumen_superheroe_workOcupation(
    superhero_id bigint not null,
    workOcupation_id bigint not null,
    primary key (superhero_id, workOcupation_id),
    foreign key (superhero_id) references cardumen_superhero(id),
    foreign key (workOcupation_id) references cardumen_workOccupation(id)
)