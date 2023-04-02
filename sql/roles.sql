CREATE TABLE backtest.roles
(
    id serial NOT NULL,
    title character varying(45),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS backtest.roles
    OWNER to postgres;