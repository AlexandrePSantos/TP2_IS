CREATE TABLE public.imported_documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) UNIQUE NOT NULL,
	xml             XML NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	is_deleted		BOOLEAN NOT NULL DEFAULT FALSE,
	is_migrated	BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.converted_documents (
    id              serial PRIMARY KEY,
    src             VARCHAR(250) NOT NULL,
    file_size       BIGINT NOT NULL,
    dst             VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);
