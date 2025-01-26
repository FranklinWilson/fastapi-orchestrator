'''Utilities to support connecting to and modifying a local datababse'''

import sqlalchemy
import typing

_DEFAULT_DB_FILEPATH: str = 'test.db'


class ConnectionError(Exception):
    '''Exception raised when there is a problem connecting to the database'''
    pass


class QueryError(Exception):
    '''Exception raised when there is a problem with a database query'''
    pass


class EntryNotFoundError(Exception):
    '''Exception raised when an entry is expected, but not found'''
    pass


def create_engine(databse_file_path: str = _DEFAULT_DB_FILEPATH):
    '''Get the connection object and metadata to a local database'''
    try:
        formatted_url: str = f'sqlite:///{databse_file_path}'
        engine = sqlalchemy.create_engine(formatted_url)
        return engine
    except Exception as e:
        raise ConnectionError(e)


def insert_data_to_table(engine: sqlalchemy.Engine,
                         table_name: str,
                         data: typing.List[typing.Dict[str, typing.Union[str, int]]]):
    '''Insert Specified data into the specified table with the provided connection'''
    try:
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(table_name, metadata, autoload_with=engine)

        with engine.connect() as conn:
            conn.execute(sqlalchemy.insert(table), data)
            conn.commit()
        conn.close()
    except Exception as e:
        raise QueryError(e)


def get_rows_from_table(engine: sqlalchemy.Engine,
                        table_name: str) -> typing.List[dict[typing.Any, typing.Any]]:
    '''Get all column data in all rows from the specified table'''
    try:
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(table_name, metadata, autoload_with=engine)
        query = sqlalchemy.select(table)

        with engine.connect() as conn:
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]
            return rows
    except Exception as e:
        raise QueryError(e)


def main():
    '''Use me for testing'''
    return 0


if __name__ == '__main__':
    main()
