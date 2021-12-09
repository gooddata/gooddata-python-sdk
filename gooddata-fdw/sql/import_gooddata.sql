CREATE OR REPLACE PROCEDURE execute_sql(
  sqlStatement VARCHAR,
  debug BOOLEAN DEFAULT FALSE
) LANGUAGE plpgsql AS $$
BEGIN
  IF debug THEN
    RAISE NOTICE '%', sqlStatement;
END IF;
EXECUTE sqlStatement;
END; $$;

CREATE OR REPLACE PROCEDURE import_gooddata(
  workspace VARCHAR,
  object_type VARCHAR,
  foreign_schema VARCHAR = NULL,
  numeric_max_size INT = 18,
  debug BOOLEAN = FALSE
) LANGUAGE plpgsql AS $$
DECLARE
  sql_statement VARCHAR;
  foreign_schema VARCHAR := coalesce(foreign_schema, workspace);
  server VARCHAR := 'multicorn_gooddata';
BEGIN
  -- Recreate schema, where foreign tables will be imported
  sql_statement := format('DROP SCHEMA IF EXISTS "%s" CASCADE', foreign_schema);
  CALL execute_sql(sql_statement, debug);

  sql_statement := format('CREATE SCHEMA "%s"', foreign_schema);
  CALL execute_sql(sql_statement, debug);

  -- Import GoodData objects as foreign tables into the schema created above
  sql_statement := format(
    'IMPORT FOREIGN SCHEMA "%s" FROM SERVER "%s" INTO "%s" OPTIONS (object_type ''%s'', numeric_max_size ''%s'')',
    workspace, server, foreign_schema, object_type, numeric_max_size
  );
  CALL execute_sql(sql_statement, debug);
END; $$;
