# -*- coding:utf-8 -*-
import sys, time

def read(table, **kwargs):
    sql = list()
    sql.append("SELECT * FROM %s " % table)
    if kwargs:
        sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    sql.append(";")
    return "".join(sql)

def insert(table, **kwargs):
    keys = ["%s" % k for k in kwargs]
    values = ["'%s'" % v for v in kwargs.values()]
    sql = list()
    sql.append("INSERT INTO %s (" % table)
    sql.append(", ".join(keys))
    sql.append(") VALUES (")
    sql.append(", ".join(values))
    sql.append(");")
    return "".join(sql)

def delete(table, **kwargs):
    sql = list()
    sql.append("DELETE FROM %s " % table)
    sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    sql.append(";")
    return "".join(sql)

def show_prog(i, tot, last_update):
    prog_update_rate = 1 # time between updates in seconds
    elapsed = time.time() - last_update 
    if elapsed > prog_update_rate or i==tot:
        width = 20
        prog = float(i)/tot
        sys.stdout.write('[{}{}]{}% ({}/{}){}'
                        .format('*' * int(prog*width),
                                '-' * (width-int(prog*width)),
                                int(prog*100),
                                i,
                                tot,
                                '\n' if i==tot else '\r'))
        sys.stdout.flush()
        last_update = time.time()
    return last_update
