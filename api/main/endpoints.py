from flask import render_template, jsonify, request

from . import main

from api.main.bloom_filter_manager import BloomFilterManager


@main.route("/", methods=["GET"])
def index():
    rendered_template = render_template("index.html.jinja")
    return rendered_template


@main.route("/check", methods=["POST"])
def check():
    bf = BloomFilterManager().read_filter_from_file()
    payload: str = request.form.get("document")

    words = payload.split(" ")
    invalid_words = []
    for word in words:
        if not bf.query(word):
            invalid_words.append(word)

    if len(invalid_words) > 0:
        misspelled = ", ".join(invalid_words)
        response = f"Misspelled words are: {misspelled}"
    else:
        response = "Congrats! All words are spelled correctly!"

    return jsonify(
        message=response
    )
