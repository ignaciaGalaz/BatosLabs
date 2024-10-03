create table if not exists studio(
	id serial primary key,
	name varchar(255) not null
);

create table if not exists anime(
	id serial primary key,
	name varchar(255) not null,
	episodes integer,
	studio_id integer,
	foreign key (studio_id) references studio(id)
);


create table if not exists character(
	id serial primary key,
	name varchar(255) not null
);

create table if not exists voice_actor(
	id serial primary key,
	name varchar(255) not null
);

create table if not exists tag(
	id serial primary key,
	name varchar(255) not null
);

create table if not exists anime_voice_actor_character(
	anime_id bigint not null,
	character_id bigint not null,
	voice_actor_id bigint not null,
	primary key (anime_id, character_id, voice_actor_id),
	foreign key (anime_id) references anime(id),
	foreign key (character_id) references character(id),
	foreign key (voice_actor_id) references voice_actor(id)
);

create table if not exists anime_tag(
	anime_id bigint not null,
	tag_id bigint not null,
	primary key (anime_id, tag_id),
	foreign key (anime_id) references anime(id),
	foreign key (tag_id) references tag(id)
);










