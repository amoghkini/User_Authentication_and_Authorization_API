--Load data into roles table
INSERT INTO backtest.roles(id, title) VALUES (1, 'Superadmin');
INSERT INTO backtest.roles(id, title) VALUES (2, 'Admin');
INSERT INTO backtest.roles(id, title) VALUES (3, 'Paid_user');
INSERT INTO backtest.roles(id, title) VALUES (4, 'User');

-- Load endpoints data
INSERT INTO backtest.endpoints(id, endpoint, method) VALUES (1, '/home', 'GET');
INSERT INTO backtest.endpoints(id, endpoint, method) VALUES (2, '/admin', 'GET');
insert into backtest.endpoints values (3,'/password_change','GET')
insert into backtest.endpoints values (4,'/logout','GET')
insert into backtest.endpoints values (5,'/password-change','GET')


-- Load accessibility table data
INSERT INTO backtest.accessibility(id, endpoint_id, roles) VALUES (1, 1, '[4]');
INSERT INTO backtest.accessibility(id, endpoint_id, roles) VALUES (2, 2, '[2,3,4]');
insert into backtest.accessibility values (3,3,'[1,2,3,4]')
insert into backtest.accessibility values (4,4,'[1,2,3,4]')
insert into backtest.accessibility values (5,5,'[1,2,3,4]')