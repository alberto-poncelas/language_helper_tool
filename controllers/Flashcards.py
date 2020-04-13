# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for


import controllers.modules.deck.Deck as Deck

from flask import Blueprint

flashcards_api = Blueprint('flashcards_api', __name__)



import random
import difflib


current_deck=Deck.Deck.getInstance()


@flashcards_api.route('/_getQA')
def getQA():
    global current_deck
    num_candidates = request.args.get('num_candidates', type=int)
    [q,a,answ_candidates]=current_deck.get_QandA(0)
    return jsonify(q=q,a=a,candidates=answ_candidates)






@flashcards_api.route('/flashcards')
def flashcards():
    global current_deck
    num_candidates=0
    automatic_answer=False
    opt = {'num_candidates': num_candidates , 'automatic_answer':automatic_answer}
    #print("checkpoint1")
    return render_template('flashcards/flashcards.html', opt=opt)


