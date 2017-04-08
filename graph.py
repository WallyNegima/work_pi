#!/usr/bin/pythonCGI
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import MySQLdb
import datetime

def mychart(environ, start_response):

  env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
  tpl = env.get_template('template.html')

  #テンプレートへ挿入するデータの作成
  title = u"Tmperature Chart"

  temp_list = []

  connector = MySQLdb.connect(host="localhost", db="pi_sensor", user="root", passwd="", charset="utf8")
  cursor = connector.cursor()

  #sql = "select * from temperature"
  sql = "select * from temp_values where DATE_ADD(date, INTERVAL 24 HOUR) > NOW()"
  cursor.execute(sql)
  records = cursor.fetchall()
  for record in records:
    temp_list.append({'date':record[0].strftime("%Y-%m-%d %H:%M"), 'temp':record[1]})
  cursor.close()
  connector.close()

  #テンプレートへ挿入するデータの作成
  title = u"Tmperature Chart"

  #テンプレートへの挿入
  html = tpl.render({'title':title, 'temp_list':temp_list})

  start_response('200 OK', [('Content-Type', 'text/html')])
  return [html.encode('utf-8')]

if __name__ == '__main__':
  from flup.server.fcgi import WSGIServer
  WSGIServer(mychart).run()
