import http.server
import json
import psycopg2
import os


class HandlerRequest(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/login.html'
        elif self.path == '/teacher':
            self.handle_teacher()
            return

        try:
            file_patch = os.path.join(os.getcwd(), self.path[1:])
            with open(file_patch, 'r', encoding='utf-8') as file:
                file_to_open = file.read()
            self.send_response(200)
        except Exception as e:
            print(f'Error: {e}')
            file_to_open = 'File not found'
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data)

        conn = psycopg2.connect('dbname=Academy user=postgres password=1234')
        cur = conn.cursor()

        if self.path == '/login':
            cur.execute("SELECT * FROM Teachers WHERE login = %s AND password = %s", (user_data['username'], user_data['userpass'],))
            existing_user = cur.fetchone()

            if existing_user:
                role = existing_user[11]
                print(f'ROle {role}') # проверка роли
                if role == 1:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Successful authorization!')
                else:
                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(b'Successful authorization!')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Invalid user name or password')

        cur.close()
        conn.close()

    def handle_teacher(self):
        conn = psycopg2.connect('dbname=Academy user=postgres password=1234')
        cur = conn.cursor()
        # cur.execute("SELECT Name, Surname, Position, Salary, Premium FROM teachers WHERE login = 1")
        cur.execute("SELECT Name, Surname, Position, CAST(Salary AS TEXT) AS Salary, CAST(Premium AS TEXT) AS Premium FROM teachers WHERE login = 5")
        teacher_info = cur.fetchone()
        cur.close()
        conn.close()
        print(f'Что Прочитал запрос в SQL Базе: {teacher_info}')

        if teacher_info:
            teacher_dict = {
                "name": teacher_info[0],
                "surname": teacher_info[1],
                "position": teacher_info[2],
                "salary": teacher_info[3],
                "premium": teacher_info[4],
            }
            print(f'Что записал для отправки в JSON{teacher_dict}')
            teacher_json = json.dumps(teacher_dict, indent=4)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(teacher_json, 'utf-8'))
            print(f'Что отправил сервер в JS: {teacher_json}')
        else:
            print(f'ААААААААААААААААААААААА')
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Teacher not found')


def run(server_class=http.server.HTTPServer, handler_class=HandlerRequest):
    server_adress = ('', 8000)
    httpd = server_class(server_adress, handler_class)
    httpd.serve_forever()

run()