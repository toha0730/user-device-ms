# reset databse for for testing purpose only
from database import database_connect
from os.path import isfile
from sys import exit, argv
import argparse

class Db():
    def __init__(self):
        self.conn = database_connect()
        self.cur = self.conn.cursor()
        print('db connected')
    def reset_db(self, schema_file, data_file):
        if (not isfile(schema_file)) or (not isfile(data_file)):
            print('schema or data not found!')
            return
        ct = []
        for fpath in (schema_file, data_file):
            with open(fpath, 'r') as f:
                ct.append(f.read())
        schema_sql, data_sql = ct
        conn = self.conn
        cur = self.cur
        print('resetting db')
        self._execmulti(schema_sql)
        conn.commit()
        print('schema executed')
        self.print_emp()
        self._execmulti(data_sql)
        conn.commit()
        print('data inserted')
        self.print_emp()
        print('OK')

    def _execmulti(self, multiline_sql):
        cur = self.cur
        # strip out all comments
        msp = multiline_sql.split(';')
        for i, line in enumerate(msp):
            # ignore everything after --
            line = line.strip('\n')
            if not line: continue
            #if len(spl) != 1:
            #    print('ig', line, spl)
            #ignore empty line
            print(i, '/', len(msp), end='\r')
            cur.execute(line)
        print('')

    def print_emp(self):
        c = self.cur
        try:
            c.execute('SELECT * FROM employee')
            print('current employee count:', len(c.fetchall()))
        except Exception as e:
            print('err getting employee count, continuing', e)
            self.close()
            self.conn = database_connect()
            self.cur = self.conn.cursor()
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        self.close()
    def close(self):
        self.conn.close()
        self.cur.close()
        print('db closed')

    def sync_departmentallocation(self):
        """ for each device that is already issue to a department emp ensure the
        device model is also allocated to that department
        """
        cur = self.cur
        s1 = """
            SELECT DISTINCT manufacturer, modelNumber, department
            FROM Device D JOIN EmployeeDepartments ED ON issuedTo=empID
            WHERE NOT EXISTS (
                SELECT *
                FROM ModelAllocations M
                WHERE M.manufacturer = D.manufacturer
                    AND M.modelNumber = D.modelNumber
                    AND M.department = ED.department
            )

        """
        s2 = """
        INSERT INTO ModelAllocations
            (manufacturer, modelNumber, department, maxNumber)
        VALUES (%s, %s, %s, %s)
        """
        print('performing departmentallocation sync')
        cur.execute(s1)
        cur2 = self.conn.cursor()
        c = 0
        while True:
            r = cur.fetchone()
            if not r: break
            mf, mn, dp = r
            cur2.execute(s2, (mf, mn, dp, 414243))
            print('+', end='')
            c += 1
        print('')
        print(c, 'record added')
        self.conn.commit()

if __name__ == '__main__':
    schema_file = 'schema.sql'
    data_file = 'sample_data.sql'
    print('sfile:', schema_file, 'dfile:', data_file)
    parser = argparse.ArgumentParser(description='reset db')
    parser.add_argument('-s', '--syncallocate', dest='salo', action='store_true',
                        help='sync allocate')
    parser.add_argument('-r', '--reset', dest='rs', action='store_true',
                        help='reset db')
    args = parser.parse_args()
    if not (args.salo or args.rs):
        print('nothing to do')
        exit(0)
    with Db() as db:
        if args.rs:
            db.reset_db(schema_file, data_file)
        if args.salo:
            db.sync_departmentallocation()

