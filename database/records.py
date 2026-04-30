import sqlite3

from schema import Record, RecordNew


def select_records(
    search: str | None,
    cursor: sqlite3.Cursor
) -> list[Record]:
    statement_where = f"where user like '%{search}%'" if search else ''
    statement = f'select * from records {statement_where}'

    record_rows = cursor.execute(statement).fetchall()

    return [
        Record(id=id, course_id=course_id, user=user, payment_id=payment_id)
        for id, course_id, payment_id, user in record_rows
    ]


def select_record(
        record_id: int,
        cursor: sqlite3.Cursor
) -> Record | None:
    statement = f'select * from records where id = ?'
    row = cursor.execute(statement, (record_id,)).fetchone()

    if not row:
        return None

    return Record(id=row[0], course_id=row[1], user=row[3], payment_id=row[2])


def insert_record(
        new_record: RecordNew,
        cursor: sqlite3.Cursor
) -> int:
    statement = '''insert into records 
        (course_id, payment_id, user) values
        (?, ?, ?)
    '''

    cursor.execute(
        statement,
        (new_record.course_id, new_record.payment_id, new_record.user)
    )

    return cursor.lastrowid


if __name__ == "__main__":
    def create_table_records(cursor: sqlite3.Cursor):
        cursor.execute('''
            create table if not exists records (
                id integer primary key,
                course_id integer not null,
                payment_id integer not null,
                user varchar(50) not null
            )
        ''')

    def seed_table_records(cursor: sqlite3.Cursor):
        data = [
            (1, 2, 1, "Карпов А.У."),
            (2, 1, 1, "Меньшов У.И.")
        ]

        statement = 'insert into records values (?, ?, ?, ?)'
        cursor.executemany(statement, data)


    connection = sqlite3.connect('records.sqlite3')
    cursor = connection.cursor()

    create_table_records(cursor)
    connection.commit()

    try:
        seed_table_records(cursor)
        connection.commit()
    except Exception:
        connection.rollback()
