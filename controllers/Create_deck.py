# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for


#import modules.Deck as Deck
#import modules.Vocabulary as Vocabulary

import controllers.modules.deck.Vocabulary as Vocabulary
import controllers.modules.deck.Deck as Deck


from flask import Blueprint

create_deck_api = Blueprint('create_deck_api', __name__)




current_deck=Deck.Deck.getInstance()
current_vocab=Vocabulary.Vocabulary.getInstance()

############################
####### VOCABULARY #########
############################




@create_deck_api.route('/create_vocabulary')
def create_vocabulary():
    global current_vocab
    #vocab_data=dbmodel.get_vocabulary_db()
    vocab_data=current_vocab.get_vocabulary()
    vocab_list=[x[1]+" - "+x[2] for x in vocab_data]
    params={
        "vocab_list":vocab_list,
        "num_vocab": len(vocab_list)  
    }
    return render_template('deck/create_vocabulary.html',params=params)



@create_deck_api.route('/_load_vocab_file', methods=[ 'POST'])
def load_vocab_file():
    global current_vocab
    vocab_text = request.form.get('vocab_text', type=str)
    if request.files:
        f = request.files['vocab_file']
        vocab_file_text=f.read().decode('utf-8')
        if len(vocab_file_text)>0:
            vocab_text=vocab_file_text
    #load_from_file_content(vocab_text)
    vocab=vocab_text.strip().split("\n")
    loaded_pairs = [x.strip().split("\t")[0:2] for x in vocab if len(x.split("\t"))>=2]
    #res=dbmodel.add_vocabulary_db(loaded_pairs)
    vocab_data=current_vocab.set_vocabulary(loaded_pairs)
    return redirect('create_vocabulary')




############################
######### DECK #############
############################






def filter_vocabulary(num_cards,subdeck):
    #pairs=dbmodel.get_vocabulary_db()
    global current_vocab
    pairs=current_vocab.get_vocabulary()
    if len(pairs)==0:
        return []
    sublist=[pairs[x:x+num_cards] for x in range(0, len(pairs), num_cards)]
    pairs_sublist=list(sublist[min(len(sublist)-1,subdeck-1)])
    return pairs_sublist




@create_deck_api.route('/create_deck', methods=[ 'GET','POST'])
def create_deck():
    global current_deck
    DEFAULT_DECK_SIZE=8
    SUBDECK=1
    split_in = request.form.get('split_in',DEFAULT_DECK_SIZE, type=int)
    subdeck_number = request.form.get('subdeck_number',SUBDECK, type=int)
    vocab_data=filter_vocabulary(num_cards=split_in,subdeck=subdeck_number)
    vocab_id=[]
    vocab_src=[]
    vocab_trg=[]
    for elem in vocab_data:
        vocab_id.append(elem[0])
        vocab_src.append(elem[1])
        vocab_trg.append(elem[2])
    params={
        "current_deck": current_deck.get_cards(),
        "vocab_id":vocab_id,
        "vocab_src":vocab_src,
        "vocab_trg":vocab_trg,
        "num_vocab": len(vocab_id),
        "split_in": split_in,
        "subdeck_number": subdeck_number,
    }
    return render_template('deck/build_deck.html',params=params)





@create_deck_api.route('/_submit_deck', methods=[ 'POST'])
def submit_deck():
    global current_deck
    selected_cards=request.form.getlist('card')
    selected_cards_idx=[x.strip() for x in selected_cards]
    current_deck.set_cards(selected_cards_idx)
    return redirect('/create_deck')

