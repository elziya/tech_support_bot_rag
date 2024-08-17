import os

from flask import Flask, render_template, request, g, session, redirect, url_for
from flask_bcrypt import Bcrypt

from web.service import get_unanswered_messages, get_message_by_id, update_chat_info_by_id, sign_in as _sign_in, \
    upload_documentation


app = Flask(__name__)

app.secret_key = os.urandom(42)
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET'])
def main_view():
    if g.user:
        return redirect(url_for('sign_in'))
    return render_template('main.html')


@app.route('/queries/<message_id>', methods=['GET'])
def query_view(message_id):
    if g.user:
        return render_template('query.html', m=get_message_by_id(message_id, g.user))
    return redirect(url_for('sign_in'))


@app.route('/queries/<message_id>', methods=['POST'])
def save_answer(message_id):
    if g.user:
        answer = request.form['answer']
        update_chat_info_by_id(message_id, answer)
        return redirect(url_for('queries_view'))
    return redirect(url_for('sign_in'))


@app.route('/queries', methods=['GET'])
def queries_view():
    if g.user:
        return render_template('queries.html', messages=get_unanswered_messages(g.user))
    return redirect(url_for('sign_in'))


@app.route('/upload', methods=['GET'])
def docs_upload_view():
    if g.user:
        return render_template('docs_upload.html')
    return redirect(url_for('sign_in'))


@app.route('/upload', methods=['POST'])
def upload_docs():
    if g.user:
        docs = request.form['docs']
        upload_documentation(docs.split(','))
        return render_template('docs_upload.html', result=True)
    return redirect(url_for('sign_in'))


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('sign_in.html')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        session.pop('user', None)
        is_signed, session_id = _sign_in(request.form['username'], request.form['password'], bcrypt)
        if is_signed:
            session['user'] = session_id
            return redirect(url_for('queries_view'))
        return render_template('sign_in.html', error=True)

    return render_template('sign_in.html', error=False)


if __name__ == '__main__':
    app.run()
