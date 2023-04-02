CREATE TABLE backtest.blacklisted_tokens
(
    id serial NOT NULL,
    token character varying(500) NOT NULL,
    blacklisted_on integer NOT NULL,
    blacklisting_reason character varying(45) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS backtest.blacklisted_tokens
    OWNER to postgres;
