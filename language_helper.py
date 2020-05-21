from flask import Flask, redirect, url_for, render_template




app = Flask(__name__)


from controllers.Create_deck import create_deck_api
app.register_blueprint(create_deck_api)

from controllers.Flashcards import flashcards_api
app.register_blueprint(flashcards_api)

from controllers.Text_Reader_Helper import text_reader_helper_api
app.register_blueprint(text_reader_helper_api)

from controllers.Text_Getter import text_getter_api
app.register_blueprint(text_getter_api)







@app.route("/")
def index():
    return redirect(url_for('create_deck_api.create_vocabulary'))

@app.route("/flashcards")
def flashcards():
    return redirect(url_for('flashcards_api.flashcards'))

@app.route("/text_read")
def text_read():
    return redirect(url_for('text_reader_helper_api.text_read'))


@app.route("/text_getter")
def text_getter():
    return redirect(url_for('text_getter_api.text_getter'))




if __name__ == "__main__":
    app.run()
