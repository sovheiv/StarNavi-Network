import secrets
from datetime import timedelta

from environs import Env
from flask import Config

env = Env()
env.read_env(override=True)


class CustomConfig(Config):
    def load_config(self):
        with env.prefixed("ADMIN_"):
            self["admin"] = {
                "public_key": env.str("PUBLIC_KEY"),
                "salt": env.str("SALT"),
            }
        with env.prefixed("USER_"):
            self["user"] = {
                "key_salt": env.str("KEY_SALT"),
                "msg_salt": env.str("MSG_SALT"),
            }

        with env.prefixed("FLASK_"):
            self["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=env.int("PERMANENT_SESSION_LIFETIME"))
            self["SECRET_KEY"] = secrets.token_hex(env.int("SECRET_KEY_BYTES"))
            self["SQLALCHEMY_TRACK_MODIFICATIONS"] = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS")

        self["SQLALCHEMY_DATABASE_URI"] = env.str("SQLALCHEMY_DATABASE_URI", default=self.load_db_conf())

    @staticmethod
    def load_db_conf():
        with env.prefixed("DB_"):
            credentials = [
                env.str("USER"),
                env.str("PASSWORD"),
                env.str("HOST"),
                env.int("PORT"),
                env.str("NAME"),
            ]
            return "postgresql+psycopg2://{}:{}@{}:{}/{}".format(*credentials)