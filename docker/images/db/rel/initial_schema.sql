CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.Cars (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    maker           VARCHAR(250) NOT NULL,
    model           VARCHAR(250) NOT NULL,
	type            VARCHAR(250) NOT NULL,
    DOL             BIGINT,
    VIN             VARCHAR(250),
    year            INT,
    range           INT,
    location_id     uuid NOT NULL,
    cafv_id         uuid,
    eligibility_id  uuid,
    utility_id      uuid,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.Locations (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    state           VARCHAR(250) NOT NULL,
    city            VARCHAR(250) NOT NULL,
	geom			GEOMETRY,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.CAFV (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name 	   		VARCHAR(250) NOT NULL,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.Utility (
    id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name 	   		VARCHAR(250) NOT NULL,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE Cars
    ADD CONSTRAINT Cars_Locations_id_fk
        FOREIGN KEY (location_id) REFERENCES Locations
            ON DELETE SET NULL;

ALTER TABLE Cars
    ADD CONSTRAINT Cars_CAFV_id_fk
        FOREIGN KEY (cafv_id) REFERENCES CAFV
            ON DELETE SET NULL;

ALTER TABLE Cars
    ADD CONSTRAINT Cars_Utility_id_fk
        FOREIGN KEY (utility_id) REFERENCES Utility
            ON DELETE SET NULL;
