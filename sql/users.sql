CREATE TABLE backtest.users
(
    user_id serial NOT NULL,
    email_id character varying(45) NOT NULL,
    password character varying(100) NOT NULL,
    first_name character varying(40) NOT NULL,
    last_name character varying(40) NOT NULL,
    account_status character varying(20),
    mobile_no character varying(10),
    username character varying(8),
    role_id integer,
    account_creation_date bigint,
    last_login_date bigint,
    last_password_reset_date bigint,
    PRIMARY KEY (user_id),
    CONSTRAINT role_id_fk FOREIGN KEY (role_id)
        REFERENCES backtest.roles (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS backtest.users
    OWNER to postgres;