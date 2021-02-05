# sql_query

A module for executing a sql query against a database using
[SqlAlchemy][].

[sqlalchemy]: https://www.sqlalchemy.org/

## Requirements

You must install the [sqlalchemy][] Python module on hosts that will be
running this role.

[sqlalchemy]: https://www.sqlalchemy.org/

## Installation

Install the contents of this repository into `roles/sql_query`, where
`roles` is in your playbook directory. For example:

```
git clone https://github.com/larsks/ansible-sql-query roles/sql_query
```

Then import this role by specifying it in the `roles` key of your
play, like this:

```
- hosts: localhost
  roles:
    - sql_query
```

You may then use the `sql_query` module in tasks in that play.

## Options

This module supports the following options:

- `connection` -- a sqlalchemy [database uri][]

   For example:

   - `sqlite:///airports.sqlite`, for a sqlite database named
     `airports.sqlite` in the current directory.

   - `mysql://someuser:somepassword@host.example.com/airports`, for a
     MySQL or MariaDB database named `airports` on host
     `host.example.com`, authenticating with username `someuser` and
     password `somepassword`.

  - `postgresql://someuser:somepassword@host.example.com/airports`,
    for the same thing using PostgreSQL.

- `query` -- the sql query to execute

- `rows_are_lists` -- if True, return rows as lists.  If False
  (the default), return rows as dictionaries.

[database uri]: https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases

## Example playbook

```
- hosts: localhost
  roles:
    - sql_query

  tasks:
    - sql_query:
        connection: sqlite:///airports.sqlite
        query: >
          select name, city from airports
          where timezone = -5 and country = 'United States'
      register: result

    - debug:
        var: result

    - debug:
        msg: "{{ item.name }} is located in {{ item.city }}"
      with_items: "{{ result.results }}"
```

## Running tests

If you run `pytest` in the top level of this repository, that will run
some simple tests described in `tests/test_sql_query.py`. The
playbooks in `tests/test_row_dict` and `tests/test_row_list` may also
be interesting as examples.
