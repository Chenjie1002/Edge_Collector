INSERT INTO machines (machine_id, machine_name, line_name, plc_name)
VALUES ('LINE_01', 'Demo Line 01', 'Demo Production Line', 'PLC_01')
ON CONFLICT (machine_id) DO UPDATE
SET machine_name = EXCLUDED.machine_name,
    line_name = EXCLUDED.line_name,
    plc_name = EXCLUDED.plc_name;

