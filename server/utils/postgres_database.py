import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

NEON_URI = os.getenv("NEON_URI", "")

class PostgresDB:
	def __init__(self, conn):
		self.conn = conn

	def fetch(self, query, params=None):
		with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
			cur.execute(query, params or ())
			return cur.fetchall()

	def fetch_one(self, query, params=None):
		with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
			cur.execute(query, params or ())
			return cur.fetchone()

	def execute(self, query, params=None):
		with self.conn.cursor() as cur:
			cur.execute(query, params or ())
			self.conn.commit()

def get_postgres_database():
	conn = psycopg2.connect(NEON_URI, sslmode="require")
	return PostgresDB(conn)
