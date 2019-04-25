# coding:utf-8

'''
解析文本文件然后生成导入文件的mysql脚本
使用 mysql -uuser -ppasswd -D db < tmp.sql 注入数据生成table
'''

import sys
from pymysql import connect


class DB(object):
    def __init__(self,
                 username='wheatdb',
                 passwd='wheatdb',
                 hostname='localhost',
                 db='wheatDB'):
        self._con = connect(hostname, username, passwd, db, charset='utf8')

    def _safe_header(self, head):
        return [each.replace('-', '_').replace('.', '_') for each in head]

    def _load_by_file(self, filepath, table, sep, header, debug, enclosed=False):
        cmd_buffer = []
        _head_str = "(" + ','.join([ "`" + each + "`" for each in header]) + ")"
        _load_str = "load data local infile '{filepath}' into table {table}".format(filepath=filepath, table=table)
        _field_str = "fields terminated by '{sep}'".format(sep=sep)
        _line_str = "lines terminated by '\n'"
        if enclosed:
            _enclosed_str = "enclosed by '\"'"
        else:
            _enclosed_str = ""
        cmd = ' '.join([_load_str, _field_str, _enclosed_str, _line_str, "ignore 1 lines", _head_str])

        if debug:
            print(cmd)
        else:
            f = open('tmp.sql', 'w+')
            f.write(cmd)
            f.close()
            print('tmp.sql generated!')

        return None

    def createTable(self,
                    table,
                    filepath,
                    sep="\t",
                    cell_type=("VARCHAR(20)", "VARCHAR(25)"),
                    load_type=None,
                    block_size=1000,
                    add_quote=True,
                    debug=True):
        if not debug:
            self.execute("drop table if exists {0}".format(table))
        headerList = []
        createCmd = "create table {table}(Id INT PRIMARY KEY AUTO_INCREMENT".format(table=table)
        headerList.append(createCmd)
        try:
            with open(filepath, "r+") as info:
                header = self._safe_header(info.readline().strip().split(sep))
                for each in header:
                    if each == header[0]:
                        headerList.append(each + " {0}".format(cell_type[0]))
                    else:
                        headerList.append(each + " {0}".format(cell_type[1]))
                headerStr = ','.join(headerList) + ")Engine=MyISAM DEFAULT CHARSET=utf8;"
                if debug:
                    print(headerStr)
                else:
                    self.execute(headerStr)
                    print("create table: {0}...".format(table))

                if load_type is None:
                    return None

                if load_type not in ("file", "block"):
                    print("load type error: (you can load data by `file` or `block`)")
                    sys.exit(1)

                if load_type == "file":
                    self._load_by_file(filepath=filepath, table=table, sep=sep, header=header, debug=debug, enclosed=True)

                elif load_type == "block":
                    row = info.readline().strip()
                    while row:
                        i = 0
                        blockList = []
                        while row and i < block_size:
                            if add_quote:
                                blockList.append("(" + ','.join(["'" + str(each) + "'" for each in row.split(sep)]) + ")")
                            else:
                                blockList.append("(" + ','.join(row.split(sep)) + ")")
                            row = info.readline().strip()
                            i += 1
                        cmd = "insert into {table} ({head}) VALUES {val};".format(
                                    table=table,
                                    head=','.join(header),
                                    val=','.join(blockList))
                        if debug:
                            print(cmd)
                        else:
                            self.execute(cmd)
                        row = info.readline().strip()
                    if not debug:
                        print("table: {0} had been wrote in mysql!".format(table))
        except IOError as e:
            print('file not find...')
            sys.exit(1)

    @staticmethod
    def Dict2Str(Dict):
        header = Dict.keys()
        # insert data must be include ''
        body = ['"' + Dict[key] + '"' for key in header]
        return header, body

    def execute(self, cmd, get_all=True):
        self._con.ping(True)
        try:
            with self._con.cursor() as cur:
                cur.execute(cmd)
                if get_all:
                    return cur.fetchall()
                else:
                    return cur.fetchone()
        except:
            print("pymysql error on cmd:")
            print(cmd)
            sys.exit(1)


    def insert(self, table, Dict):
        header, body = self.Dict2Str(Dict)
        with self._con.cursor() as cur:
            cmd = "insert into {table} ({head}) VALUES ({val});".format(
                table=table,
                head=u','.join(header).encode('utf-8'),
                val=u','.join(body).encode('utf-8')
            )
            cur.execute(cmd)

    def insert_all(self, table, Dict_list):
        cmd = "insert into {table} ({head}) VALUES ({val});"
        with self._con.cursor() as cur:
            for each in Dict_list:
                header, body = self.Dict2Str(each)
                cur.execute(cmd.format(
                    table=table,
                    head=u','.join(header).encode('utf-8'),
                    val=u','.join(body).encode('utf-8')
                ))

    def update(self, table, Dict, condDict):
        header, body = self.Dict2Str(Dict)
        updateList = []
        for head, val in zip(header, body):
            updateList.append(u'='.join([head, val]).encode('utf-8'))
        with self._con.cursor() as cur:
            cmd = "update {table} set {update} WHERE {key}='{value}';".format(
                table=table,
                update=u','.join(updateList).encode('utf-8'),
                key=condDict.keys()[0].encode('utf-8'),
                value=condDict.values()[0].encode('utf-8')
            )
            cur.execute(cmd)

    def delete(self, table, condDict):
        with self._con.cursor() as cur:
            cmd = "delete from {table} WHERE {key}='{value}';".format(
                table=table,
                key=condDict.keys()[0].encode('utf-8'),
                value=condDict.values()[0].encode('utf-8')
            )
            cur.execute(cmd)


if __name__ == '__main__':
    db = DB()
    db.createTable('tissue_expression', cell_type=("VARCHAR(20)", "VARCHAR(10)"), filepath='/home/data/wheat/public/expression/iwgsc_refseq.tpm.grp.txt', load_type='file', debug=False)
