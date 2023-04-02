CREATE TABLE backtest.accessibility
(
    id serial NOT NULL,
    endpoint_id integer NOT NULL,
    roles character varying(100) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS backtest.accessibility
    OWNER to postgres;

ALTER TABLE IF EXISTS backtest.accessibility
    ADD CONSTRAINT endpoint_id_fk FOREIGN KEY (endpoint_id)
    REFERENCES backtest.endpoints (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE NO ACTION
    NOT VALID;
