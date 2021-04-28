CREATE TABLE accounts (
    qq INTEGER PRIMARY KEY,
    code CHAR(9),
    created_time TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    is_active BOOL DEFAULT true,
    recent_type CHAR(10) DEFAULT 'pic',
    b30_type CHAR(10) DEFAULT 'pic'
);