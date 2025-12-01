CREATE TABLE IF NOT EXISTS tasks (
    title VARCHAR(255) PRIMARY KEY,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, status) VALUES 
    ('Sample Task 1', 'completed'),
    ('Sample Task 2', 'pending');