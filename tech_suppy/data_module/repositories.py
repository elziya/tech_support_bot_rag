import os
from datetime import datetime
import psycopg2

from .models import MessageInfo, MailingMessage, Operator

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)


def get_operator_by_username(username):
    with conn.cursor() as curs:
        curs.execute("select id, username, password FROM operator where username=%s", (username,))
        r = curs.fetchone()
        return Operator(id=r[0], username=r[1], password=r[2])


def get_unanswered_messages(operator_id):
    with conn.cursor() as curs:
        curs.execute("select id, user_id, question, sending_date FROM chat_info where answered=false and "
                     "operator_answered=false and operator_id=%s;", (operator_id,))
        res = curs.fetchall()
        return [MessageInfo(id=r[0], user_id=r[1], query=r[2], date=datetime.strptime(str(r[3]), "%Y-%m-%d %H:%M:%S"))
                for r in res]


def get_mailing_messages():
    with conn.cursor() as curs:
        curs.execute("select id, user_id, question, operator_answer FROM chat_info where answered=false and "
                     "operator_answered=true;")
        res = curs.fetchall()
        return [MailingMessage(id=r[0], user_id=r[1], query=r[2], operator_answer=r[3])
                for r in res]


def update_chat_info_by_id(id, answer):
    with conn.cursor() as curs:
        curs.execute(
            "update chat_info set operator_answer=%s, operator_answered=true, operator_answer_date=%s where id=%s",
            (answer, datetime.now(), id))
    conn.commit()


def update_mailing_message_by_id(id):
    with conn.cursor() as curs:
        curs.execute("update chat_info set answered=true where id=%s", (id,))
    conn.commit()


def get_message_by_id(id, operator_id) -> MessageInfo:
    with conn.cursor() as curs:
        curs.execute("select id, user_id, question, sending_date FROM chat_info WHERE id=%s and operator_id=%s",
                     (id, operator_id))
        r = curs.fetchone()
    return MessageInfo(id=r[0], user_id=r[1], query=r[2], date=datetime.strptime(str(r[3]), "%Y-%m-%d %H:%M:%S"))


def save_chat_info(chat_info, operator_id):
    with conn.cursor() as curs:
        curs.execute("insert into chat_info(user_id, question, sending_date, bot_answer, source, operator_answered, "
                     "answered, operator_id) values (%s, %s, %s, %s, %s, %s, %s, %s);",
                     (chat_info.user_id, chat_info.query,
                      chat_info.date, chat_info.answer,
                      chat_info.source, chat_info.operator_answered,
                      chat_info.answered, operator_id))
    conn.commit()


def get_operator_for_query():
    with conn.cursor() as curs:
        curs.execute("with c1 as (select operator_id, count(id) num from chat_info where operator_answered=false "
                     "and answered=false group by operator_id), c2 as (select min(c1.num) m from c1) select "
                     "operator_id from c1 cross join c2 where num=m;")
        res = curs.fetchone()
        return res[0]


def save_sources(names, type):
    type = type.name
    values = [(name, type) for name in names]
    with conn.cursor() as curs:
        curs.executemany("insert into source(name, type) values (%s, %s);", values)
    conn.commit()


def get_source_id_by_name(name):
    with conn.cursor() as curs:
        curs.execute("select id FROM source where name=%s", (name,))
        r = curs.fetchone()
        return r[0]
