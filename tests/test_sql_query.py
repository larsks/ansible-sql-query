import os
import shutil
import sqlite3
import subprocess
import tempfile
import unittest

testdata = [
    [0, 'testitem1', 1.00],
    [1, 'testitem2', 10.00],
    [2, 'testitem3', 5.00],
    [3, 'testitem4', 2.00],
]

class TestSqlQuery(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.mkdtemp(prefix='ansible')
        self.dbpath = os.path.join(self.workspace,
                                   'test.db')
        self.create_database()
        self.setup_env()

    def setup_env(self):
        os.environ['ANSIBLE_LOCAL_TEMP'] = os.path.join(
            self.workspace, 'ltmp')
        os.environ['ANSIBLE_REMOTE_TEMP'] = os.path.join(
            self.workspace, 'rtmp')

    def create_database(self):
        self.db = sqlite3.connect(self.dbpath)
        self.db.execute('CREATE TABLE testtable ('
                        'id int,'
                        'description varchar(20),'
                        'price float'
                        ')')

        for row in testdata:
            self.db.execute('insert into testtable values (?, ?, ?)',
                            row)

        self.db.commit()

    def run_playbook(self, playbook):
        subprocess.check_call(['ansible-playbook',
                               playbook,
                               '-e', 'testdb=sqlite:///%s' % self.dbpath])

    def test_row_dict(self):
        self.run_playbook('tests/test_row_dict/playbook.yml')

    def test_row_list(self):
        self.run_playbook('tests/test_row_list/playbook.yml')

    def tearDown(self):
        shutil.rmtree(self.workspace)
