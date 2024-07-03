INSERT INTO partners (id, name, status) VALUES (1, 'Partner A', TRUE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;

INSERT INTO partners (id, name, status) VALUES (2, 'Partner B', TRUE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;

INSERT INTO partners (id, name, status) VALUES (3, 'Partner C', TRUE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;
