# TgUsers

# Installation

```bash
pip3 install tgusers
```

# Create tables:
```sql
CREATE TABLE public."Users"
(
    id SERIAL PRIMARY KEY,
    "telegram_id" integer,
    "user_name" character varying(500),
    "language" character varying(500),
    "role" character varying(500),
    "room" character varying(500) DEFAULT 'start'
)

TABLESPACE pg_default;

ALTER TABLE public."Users"
    OWNER to "postgres"

CREATE INDEX telegram_id_index
ON public."Users" USING btree
(telegram_id ASC NULLS LAST)
TABLESPACE pg_default;


CREATE TABLE public."Messages"
(
    id SERIAL PRIMARY KEY,
    "user_id" integer,
    "message" character varying(1040),
    "message_id" integer,
    "time" integer
)

TABLESPACE pg_default;

ALTER TABLE public."Messages"
    OWNER to "postgres";
    
```
