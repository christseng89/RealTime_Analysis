INSERT INTO my_table (id, value) VALUES (1, 'my_value')
ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value;
