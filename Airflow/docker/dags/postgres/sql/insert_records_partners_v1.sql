INSERT INTO partners (id, name, status) VALUES (1, 'Partner A', FALSE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;

INSERT INTO partners (id, name, status) VALUES (2, 'Partner B', FALSE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;

INSERT INTO partners (id, name, status) VALUES (3, 'Partner C', FALSE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, status = EXCLUDED.status;
