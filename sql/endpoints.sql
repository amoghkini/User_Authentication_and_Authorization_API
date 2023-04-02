CREATE TABLE backtest.endpoints
(
    id serial NOT NULL,
    endpoint character varying(100) NOT NULL,
    method character varying(15) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS backtest.endpoints
    OWNER to postgres;