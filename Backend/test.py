
from sqlalchemy import text
from App.db.session import get_connection

with get_connection() as conn:
    print(conn.execute(text("select 1")).scalar())
