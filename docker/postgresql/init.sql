CREATE TABLE extraction_logs (
    private_id SERIAL PRIMARY KEY,
    public_id VARCHAR(36) NOT NULL,
    timestamp INT NOT NULL,
    status VARCHAR(10) NOT NULL
);