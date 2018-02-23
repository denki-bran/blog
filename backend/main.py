"""
Main function.
"""

__author__ = "Aaron Tei"
__email__ = "dd7217918@gmail.com"
__name__ = "__main__"

from flask import Flask, jsonify, abort, request
from  flask_restful import Api, Resource,reqparse
import mysql.connector
from time import strftime
from datetime import datetime

app = Flask(__name__)
api = Api(app)
config={
        'user':'root',
        'password':'dd19941130',
        'database':'BLOG',
        'host':'localhost',
        'port':3306,
        'charset':'utf8'
    }
class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_name', type = str, location = 'json')
        self.reqparse.add_argument('user_icon', type = str, location = 'json')
        self.reqparse.add_argument('user_password', type = str, location = 'json')
        super(UserAPI, self).__init__()

    def get(self,user_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM USER WHERE user_id = %s', (user_id,))
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result[0])
        except mysql.connector.Error as e:
            print(e.message)

    def delete(self,user_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('DELETE FROM USER WHERE user_id = %s', (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

    def put(self,user_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            args = self.reqparse.parse_args()
            setSentence=''
            exSentence = 'UPDATE USER SET '
            exEnd = ' WHERE user_id =\'%s\''%(user_id)

            if args.user_name:
                setSentence+='user_name = \'%s\','%(args.user_name)
            elif args.user_icon:
                setSentence+='user_icon = \'%s\','%(args.user_icon)
            elif args.user_password:
                setSentence+='user_password = \'%s\','%(args.user_password)

            if setSentence:
                setSentence=setSentence[:-1]
                exSentence=exSentence+setSentence+exEnd

                print(exSentence)
                cursor.execute(exSentence)
                conn.commit()
            else:
                pass
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

class UserListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_name', type = str, location = 'json',required = True)
        self.reqparse.add_argument('user_icon', type = str, location = 'json')
        self.reqparse.add_argument('user_password', type = str, location = 'json',required = True)
        super(UserListAPI, self).__init__()

    def get(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM USER')
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result)
        except mysql.connector.Error as e:
            print(e.message)

    def post(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            args = self.reqparse.parse_args()

            if not args.user_icon:
                cursor.execute('INSERT INTO USER(user_name,user_created_time,user_password) VALUES(%s,%s,%s)',(args.user_name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),args.user_password,))
            else:
                cursor.execute('INSERT INTO USER(user_name,user_icon,user_created_time,user_password) VALUES(%s,%s,%s,%s)',(args.user_name,args.user_icon,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),args.user_password))
            conn.commit()
            cursor.execute('SELECT * FROM USER')
            result=cursor.fetchall()
            print("Users:")
            for r in result:
                print(r)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

class ArticleAPI(Resource):
    def get(self,article_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM ARTICLE WHERE article_id = %s', (article_id,))
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result[0])
        except mysql.connector.Error as e:
            print(e.message)

    def delete(self,article_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('DELETE FROM ARTICLE WHERE article_id = %s', (article_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

class ArticleListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('article_title', type = str, location = 'json',required = True)
        self.reqparse.add_argument('article_desc', type = str, location = 'json')
        self.reqparse.add_argument('article_detail', type = str, location = 'json')
        super(ArticleListAPI, self).__init__()

    def get(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM ARTICLE')
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result)
        except mysql.connector.Error as e:
            print(e.message)

    def post(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            args = self.reqparse.parse_args()
            cursor.execute('INSERT INTO ARTICLE(article_title,article_created_time,article_desc,article_detail) VALUES(%s,%s,%s,%s)',(args.article_title,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),args.article_desc,args.article_detail))
            conn.commit()
            cursor.execute('SELECT * FROM ARTICLE')
            result=cursor.fetchall()
            print("Articles:")
            for r in result:
                print(r)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

class TagListsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('taglist_name',type=str, location = 'json' ,required = True)
        super(TagListsAPI,self).__init__()

    def get(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM TAGLIST')
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result)
        except mysql.connector.Error as e:
            print(e.message)
    def post(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            args = self.reqparse.parse_args()
            cursor.execute('INSERT INTO TAGLIST(taglist_name) VALUES(%s)',(args.taglist_name))
            conn.commit()
            cursor.execute('SELECT * FROM TAGLIST')
            result=cursor.fetchall()
            print("TAGLISTs:")
            for r in result:
                print(r)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

class TagListNameAPI(Resource):
    def get(self,taglist_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM TAGLIST WHERE taglist_id = %s', (taglist_id,))
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result[0])
        except mysql.connector.Error as e:
            print(e.message)

class TagsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tag_name', type = str, location = 'json',required = True)
        self.reqparse.add_argument('article_id', type = int, location = 'json',required = True)
        super(UserAPI, self).__init__()

    def get(self,taglist_name):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            cursor.execute('SELECT * FROM TAG WHERE taglist_name = %s', (taglist_name,))
            columns=cursor.column_names
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            return format(result)
        except mysql.connector.Error as e:
            print(e.message)

    def post(self,taglist_name):
        try:
            conn = mysql.connector.connect(**config)
            cursor=conn.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
            args = self.reqparse.parse_args()
            cursor.execute('INSERT INTO TAG(tag_name,taglist_name,article_id) VALUES(%s,%s,%s)',(args.tag_name,taglist_name,args.article_id))
            conn.commit()
            cursor.execute('SELECT * FROM TAG WHERE taglist_name = %s', (taglist_name,))
            result=cursor.fetchall()
            print("TAGLISTs:")
            for r in result:
                print(r)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e.message)

api.add_resource(UserAPI,'/api/userinfo/<user_id>')
api.add_resource(UserListAPI,'/api/users')

api.add_resource(ArticleAPI,'/api/article/<article_id>')
api.add_resource(ArticleListAPI,'/api/articles')

api.add_resource(TagListsAPI,'/api/taglists')
api.add_resource(TagListNameAPI,'/api/taglist/<taglist_id>')
api.add_resource(TagsAPI,'/api/tags/<taglist_name>')

# api.add_resource(TodoAPI,'/api/todo/<todo_id>')
# api.add_resource(TodoListAPI,'/api/todos')

# api.add_resource(WantbuyAPI,'/api/wantbuy/<wantbuy_id>')
# api.add_resource(WantbuyListAPI,'/api/wantbuys')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
