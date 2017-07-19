# sql_query

A module for executing a sql query against a database using
[SqlAlchemy][].

[sqlalchemy]: https://www.sqlalchemy.org/

## Options

- `connection` -- a sqlalchemy database uri
- `query` -- the sql query to execute
- `rows_are_lists` -- if True, return rows as lists.  If False
  (the default), return rows as dictionaries.

## Example playbook

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

## Running tests

    ansible-playbook -i tests/inventory tests/main.yml
