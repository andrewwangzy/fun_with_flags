import pytest
import tempfile

from funwithflags.entities import (
    generate_update_params,
    read_postgres_config,
)


DATABASE_CONFIG = """[postgresql]
host=dbpostgres
port=5432
dbname=postgres
user=service
password=password
"""


def test_read_postgres_config():
    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".ini") as temp_file:
        # Given
        expected_config = {
            "host": "dbpostgres",
            "port": "5432",
            "dbname": "postgres",
            "user": "service",
            "password": "password",
        }
        temp_file.write(DATABASE_CONFIG)
        temp_file.seek(0)

        # When
        config = read_postgres_config(temp_file.name)

        # Then
        assert expected_config == config


@pytest.mark.parametrize(
    "uid,kwargs,expected",
    [
        (0, dict(), ("", tuple())),
        (
            1,
            {"username": "testname", "randomname": "something"},
            ("username = %s", ("testname", 1)),
        ),
        (
            300,
            {"password": b"k4b67a", "salt": b"h345", "email": "abc@some.com"},
            ("password = %s, email = %s", (b"k4b67a", "abc@some.com", 300)),
        ),
    ],
)
def test_generate_update_params(uid, kwargs, expected):
    # When
    result = generate_update_params(uid, **kwargs)
    # Then
    assert expected == result