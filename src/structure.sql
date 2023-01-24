CREATE TABLE Relayed
(
    time        TIMESTAMP UNIQUE,
    connections INT,
    upload      BIGINT,
    download    BIGINT
);

CREATE TABLE Restart
(
    time        TIMESTAMP
)
