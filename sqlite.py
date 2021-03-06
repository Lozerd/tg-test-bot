import sqlite3


class SQLight:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_users_table(self):
        return self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id integer constraint table_name_pk primary key autoincrement, "
            "user_tg_id varchar, status boolean default true not null)")

    def get_subscriptions(self, status=True):
        self.create_users_table()
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_tg_id):
        self.create_users_table()
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_tg_id` = ?", (user_tg_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_tg_id, status=True):
        self.create_users_table()
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_tg_id`, `status`) VALUES (?,?)",
                                       (user_tg_id, status))

    def update_subscription(self, user_tg_id, status):
        self.create_users_table()
        return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_tg_id` = ?", (status, user_tg_id))

    def close(self):
        return self.connection.close()
