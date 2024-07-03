INSERT INTO my_table (id, value) VALUES (%(id)s, %(value)s)
ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value;
