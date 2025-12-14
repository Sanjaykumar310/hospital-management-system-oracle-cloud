"""
Simple Oracle DB helper using `oracledb`.
- Reads env vars: ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN
- Provides `get_connection()` and `rows_to_dicts()` helpers
"""
import os

try:
    import oracledb
except Exception as e:
    raise RuntimeError("Install `oracledb` and ensure Oracle Instant Client / Thin mode is available") from e


def get_connection():
    """Return a new Oracle connection using env variables.
    ORACLE_DSN can be: host:port/service_name or a TNS name depending on your environment.
    """
    user = os.environ.get("ORACLE_USER")
    password = os.environ.get("ORACLE_PASSWORD")
    dsn = os.environ.get("ORACLE_DSN")

    if not (user and password and dsn):
        raise RuntimeError("Missing ORACLE_USER/ORACLE_PASSWORD/ORACLE_DSN environment variables")

    # Basic connect; you can replace with pooling in production
    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    return conn


def rows_to_dicts(cursor):
    """Convert cursor results to list of dicts using cursor.description"""
    cols = [c[0].lower() for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]
