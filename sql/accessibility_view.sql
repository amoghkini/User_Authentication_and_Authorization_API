CREATE VIEW backtest.accessibility_view
 AS
select 
ep.endpoint, 
ac.roles 
from backtest.endpoints as ep join backtest.accessibility as ac 
on ep.id = ac.endpoint_id;

ALTER TABLE backtest.accessibility_view
    OWNER TO postgres;
