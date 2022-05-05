from dataclasses import dataclass

from helpers import SecretManager
import psycopg2
from psycopg2 import sql


@dataclass
class PostgresCredentials:
    username: str
    password: str
    host: str
    port: int
    database: str


class Postgres:
    def __enter__(self):
        return self

    def __init__(self, secret_name, region_name="us-east-1"):
        self._secret_name = secret_name
        self._connection = self._create_connection()

    def execute_query(self, query: str, identifiers: dict = {}, parameters: dict = {}):
        with self._connection:
            with self._connection.cursor() as curs:
                curs.execute(
                    sql.SQL(query).format(**self._get_sql_identifiers(identifiers)),
                    parameters,
                )
                if curs.description:
                    return curs.fetchall()

    def _create_connection(self):
        credentials = self._postgres_credentials()

        self._connection = psycopg2.connect(
            user=credentials.username,
            password=credentials.password,
            host=credentials.host,
            port=credentials.port,
            database=credentials.database,
            connect_timeout=3,
            sslmode="require",
        )
        self._connection.autocommit = True

        return self._connection

    def _postgres_credentials(self) -> PostgresCredentials:
        with SecretManager(self._secret_name) as client:
            secret = client.retrieve_secret_string()

        postgres_credentials = PostgresCredentials(
            username=secret["username"],
            password=secret["password"],
            host=secret["host"],
            port=secret["port"],
            database=secret["engine"],
        )

        return postgres_credentials

    def _get_sql_identifiers(self, identifiers: dict = {}) -> dict:
        return {name: sql.Identifier(value) for name, value in identifiers.items()}

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self._connection.close()
