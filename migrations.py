migrs = ["""
        CREATE TABLE public."Users"
        (
            id SERIAL PRIMARY KEY,
            "telegram_id" integer,
            "first_name" character varying(500),
            "last_name" character varying(500),
            "user_name" character varying(500),
            "phone" character varying(500),
            "language" character varying(500),
            "role" character varying(500),
            "room" character varying(500) DEFAULT 'start'
        )

        TABLESPACE pg_default;

        ALTER TABLE public."Users"
            OWNER to "Admin";
    """,
         """ CREATE TABLE public."Messages"
        (
            id SERIAL PRIMARY KEY,
            "user_id" integer,
            "message" character varying(1040),
            "message_id" integer,
            "time" integer
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE public."Messages"
            OWNER to "Admin";
        """]
