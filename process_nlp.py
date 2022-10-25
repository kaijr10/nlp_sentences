import stanza
import argparse
import os
import sys
import pandas as pd
import nodebox_linguistics_extended as nle

"""
Get type of sentence
"""
def get_type_of_sentence(sentence):
    negative_question = "negative question"
    tag_question = "tag question"
    question = "question"
    negative = "negative"
    statement = "statement"
    other = "other"

    last_character = sentence[-1]

    negative_words = ["not", "don't", "doesn't", "won't", "wouldn't", "didn't", "can't", "haven't", "hasn't"]

    # check for negative question
    if last_character == '?':
        # check for negative question
        if any(element in sentence.split(" ") for element in negative_words):
            return negative_question
        # check for tag question and question
        if ',' in sentence:
            return tag_question
        else:
            return question
    # check for negative
    if any(element in sentence for element in negative_words):
        return negative
    # check for statement
    if last_character in ['!', '.']:
        return statement
    
    return other

"""
Get grammar tags. return dictionary of {"word": [], "xpos": []}
"""
def get_grammar_tags_of_sentence(sentence):
    words = []
    xpos = []
    for word in sentence.words:
        words.append(word.text)
        xpos.append(word.xpos)
    return {"words": words, "xpos": xpos}


class Tense(object):

    def __init__(self):
        self.name = None
        self.tag_negative_questions = []
        self.tag_questions = []
        self.tag_negative = []
        self.tag_positive = []
        self.condition = {}
        # check condition tag is in
        self.tag_in = True
        # the main verb tag
        self.main_verb = None
    
    def set_name(self, name):
        self.name = name
        return self
    
    def set_tag_negative_questions(self, tag_negative_questions):
        self.tag_negative_questions = tag_negative_questions
        return self
    
    def set_tag_questions(self, tag_questions):
        self.tag_questions = tag_questions
        return self
    
    def set_tag_negative(self, tag_negative):
        self.tag_negative = tag_negative
        return self
    
    def set_tag_positive(self, tag_positive):
        self.tag_positive = tag_positive
        return self
    
    def set_condition(self, condition):
        self.condition.update(condition)
        return self
    
    def set_tag_in(self, is_tag_in):
        self.tag_in = is_tag_in
        return self
    
    def set_main_verb(self, main_verb):
        self.main_verb = main_verb
        return self
    
    def get_name(self):
        return self.name
    
    def get_tag_negative_questions(self):
        return self.tag_negative_questions
    
    def get_tag_questions(self):
        return self.tag_questions
    
    def get_tag_negative(self):
        return self.tag_negative
    
    def get_tag_positive(self):
        return self.tag_positive
    
    def get_condition(self):
        return self.condition
    
    def get_tag_in(self):
        return self.tag_in
    
    def get_main_verb(self):
        return self.main_verb
    
    def get_all_tags(self):
        return [self.tag_negative_questions, self.tag_questions, self.tag_negative, self.tag_positive]
    
    def build_tense(self):
        return self
    
    def add_single_tag_value_condition(self, tag, value):
        if tag in self.condition:
            self.condition[tag].append(value)
        else:
            self.condition.update({tag: value})


"""
Initialize and get tense of sentence
"""
def get_tense_of_sentence(word_xpos):
    future_perfect_continuous = Tense().set_name("Future Perfect Continuous")\
                                    .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB', 'VBN', 'VBG'])\
                                    .set_tag_questions(['MD', 'PRP', 'VB', 'VBN', 'VBG'])\
                                    .set_tag_negative(['MD', 'RB', 'VB', 'VBN', 'VBG'])\
                                    .set_tag_positive(['MD', 'VB', 'VBN', 'VBG'])\
                                    .set_condition({
                                        "MD": ["will", "'ll"],
                                        "VB": ['have'],
                                        "VBN": ['been']
                                    })\
                                    .set_main_verb('VBG')\
                                    .build_tense()
    future_simple_passive = Tense().set_name("Future Simple Passive")\
                                    .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB', 'VBN'])\
                                    .set_tag_questions(['MD', 'PRP', 'VB', 'VBN'])\
                                    .set_tag_negative(['MD', 'RB', 'VB', 'VBN'])\
                                    .set_tag_positive(['MD', 'VB', 'VBN'])\
                                    .set_condition({
                                        "MD": ["will", "'ll"],
                                        "VB": ['am', 'is', 'are']
                                    })\
                                    .set_main_verb('VBN')\
                                    .build_tense()
    present_continuous_passive = Tense().set_name("Present Continuous Passive")\
                                    .set_tag_negative_questions(['VBP', 'RB', 'PRP', 'VBG', 'VBN'])\
                                    .set_tag_questions(['VBP', 'PRP', 'VBG', 'VBN'])\
                                    .set_tag_negative(['VBP', 'RB', 'VBG', 'VBN'])\
                                    .set_tag_positive(['VBP', 'VBG', 'VBN'])\
                                    .set_condition({
                                        "VBP": ["am", "are", "'m", "'re"],
                                        "VBG": ['being']
                                    })\
                                    .set_main_verb('VBN')\
                                    .build_tense()
    present_continuous_passive_3_form = Tense().set_name("Present Continuous Passive 3 Form")\
                                    .set_tag_negative_questions(['VBZ', 'RB', 'PRP', 'VBG', 'VBN'])\
                                    .set_tag_questions(['VBZ', 'PRP', 'VBG', 'VBN'])\
                                    .set_tag_negative(['VBZ', 'RB', 'VBG', 'VBN'])\
                                    .set_tag_positive(['VBZ', 'VBG', 'VBN'])\
                                    .set_condition({
                                        "VBZ": ["is", "'s"],
                                        "VBG": ['being']
                                    })\
                                    .set_main_verb('VBN')\
                                    .build_tense()
    present_perfect_passive = Tense().set_name("Present Perfect Passive")\
                                    .set_tag_negative_questions(['VBP', 'RB', 'PRP', 'VBN', 'VBN'])\
                                    .set_tag_questions(['VBP', 'PRP', 'VBN', 'VBN'])\
                                    .set_tag_negative(['VBP', 'RB', 'VBN', 'VBN'])\
                                    .set_tag_positive(['VBP', 'VBN', 'VBN'])\
                                    .set_condition({
                                        "VBP": ["have", "'ve"]
                                    })\
                                    .set_main_verb('VBN')\
                                    .build_tense()
    present_perfect_passive_3_form = Tense().set_name("Present Perfect Passive 3 Form")\
                                    .set_tag_negative_questions(['VBZ', 'RB', 'PRP', 'VBN', 'VBN'])\
                                    .set_tag_questions(['VBZ', 'PRP', 'VBN', 'VBN'])\
                                    .set_tag_negative(['VBZ', 'RB', 'VBN', 'VBN'])\
                                    .set_tag_positive(['VBZ', 'VBN', 'VBN'])\
                                    .set_condition({
                                        "VBZ": ["has"]
                                    })\
                                    .set_main_verb('VBN')\
                                    .build_tense()
    
    future_perfect = Tense().set_name("Future Perfect")\
                    .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB', 'VBN'])\
                    .set_tag_questions(['MD', 'PRP', 'VB', 'VBN'])\
                    .set_tag_negative(['MD', 'RB', 'VB', 'VBN'])\
                    .set_tag_positive(['MD', 'VB', 'VBN'])\
                    .set_condition({
                        "MD": ["will", "'ll"],
                        "VB": ['have']
                    })\
                    .set_main_verb('VBN')\
                    .build_tense()

    present_perfect_continuous = Tense().set_name("Present Perfect Continuous")\
                                .set_tag_negative_questions(['VBP', 'RB', 'PRP', 'VBN', 'VBG'])\
                                .set_tag_questions(['VBP', 'PRP', 'VBN', 'VBG'])\
                                .set_tag_negative(['VBP', 'RB', 'VBN', 'VBG'])\
                                .set_tag_positive(['VBP', 'VBN', 'VBG'])\
                                .set_condition({
                                    "VBP": ["have", "'ve"],
                                    "VBN": ['been']
                                })\
                                .set_main_verb('VBG')\
                                .build_tense()

    present_perfect_continuous_3_form = Tense().set_name("Present Perfect Continuous 3 Form")\
                                        .set_tag_negative_questions(['VBZ', 'RB', 'PRP', 'VBN', 'VBG'])\
                                        .set_tag_questions(['VBZ', 'PRP', 'VBN', 'VBG'])\
                                        .set_tag_negative(['VBZ', 'RB', 'VBN', 'VBG'])\
                                        .set_tag_positive(['VBZ', 'VBN', 'VBG'])\
                                        .set_condition({
                                            "VBZ": ["has", "'s"],
                                            "VBN": ["been"]
                                        })\
                                        .set_main_verb('VBG')\
                                        .build_tense()

    future_continuous = Tense().set_name("Future Continuous")\
                        .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB', 'VBG'])\
                        .set_tag_questions(['MD', 'PRP', 'VB', 'VBG'])\
                        .set_tag_negative(['MD', 'RB', 'VB', 'VBG'])\
                        .set_tag_positive(['MD', 'VB', 'VBG'])\
                        .set_condition({
                            "MD": ["will", "'ll"],
                            "VB": ["be"]
                        })\
                        .set_main_verb('VBG')\
                        .build_tense()
    
    past_perfect_continuous = Tense().set_name("Past Perfect Continuous")\
                            .set_tag_negative_questions(['VBD', 'RB', 'PRP', 'VBN', 'VBG'])\
                            .set_tag_questions(['VBD', 'PRP', 'VBN', 'VBG'])\
                            .set_tag_negative(['VBD', 'RB', 'VBN', 'VBG'])\
                            .set_tag_positive(['VBD', 'VBN', 'VBG'])\
                            .set_condition({
                                "VBD": ['had'],
                                "VBN": ['been']
                            })\
                            .set_main_verb('VBG')\
                            .build_tense()
    
    used_to = Tense().set_name("Used to")\
            .set_tag_negative(['VBD', 'RB', 'VB', 'TO'])\
            .set_tag_positive(['VBD', 'TO', 'VB'])\
            .set_condition({
                "VBD": ['used', 'use']
            })\
            .set_main_verb('VB')\
            .build_tense()
    
    present_simple_passive = Tense().set_name("Present Simple Passive")\
                            .set_tag_negative(['VBP', 'RB', 'VBN'])\
                            .set_tag_positive(['VBP', 'VBN'])\
                            .set_condition({
                                "VBP": ["are", "am", "'m", "'re"]
                            })\
                            .set_main_verb('VBP')\
                            .build_tense()

    present_simple_passive_3_form = Tense().set_name("Present Simple Passive 3 Form")\
                                    .set_tag_negative(['VBZ', 'RB', 'VBN'])\
                                    .set_tag_positive(['VBZ', 'VBN'])\
                                    .set_condition({
                                        "VBZ": ["is", "'s"]
                                    })\
                                    .set_main_verb('VBZ')\
                                    .build_tense()
    
    future_simple = Tense().set_name("Future Simple")\
                    .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB'])\
                    .set_tag_questions(['MD', 'PRP', 'VB'])\
                    .set_tag_negative(['ND', 'RB', 'VB'])\
                    .set_tag_positive(['MD', 'VB'])\
                    .set_condition({
                        "MD": ["will", "'ll"]
                    })\
                    .set_main_verb('VB')\
                    .build_tense()
    
    present_continuous = Tense().set_name("Present Continuous")\
                        .set_tag_negative_questions(['VBP', 'RB', 'PRP', 'VBG'])\
                        .set_tag_questions(['VBP', 'PRP', 'VBG'])\
                        .set_tag_negative(['VBP', 'RB', 'VBG'])\
                        .set_tag_positive(['VBP', 'VBG'])\
                        .set_condition({
                            "VBP": ["am", "are", "'m", "'re"]
                        })\
                        .set_main_verb('VBG')\
                        .build_tense()
    present_continuous_3_form = Tense().set_name("Present Continuous 3 Form")\
                            .set_tag_negative_questions(['VBZ', 'RB', 'PRP', 'VBG'])\
                            .set_tag_questions(['VBZ', 'PRP', 'VBG'])\
                            .set_tag_negative(['VBZ', 'RB', 'VBG'])\
                            .set_tag_positive(['VBZ', 'VBG'])\
                            .set_condition({
                                "VBZ": ["is", "'s"]
                            })\
                            .set_main_verb('VBG')\
                            .build_tense()
    past_simple_passive = Tense().set_name("Past Simple Passive")\
                        .set_tag_negative_questions(['VBD', 'RB', 'PRP', 'VB'])\
                        .set_tag_questions(['VBD', 'PRP', 'VB'])\
                        .set_tag_negative(['VBD', 'RB', 'VBN'])\
                        .set_tag_positive(['VBD', 'VBN'])\
                        .set_condition({
                            "VBD": ['was', 'were']
                        })\
                        .set_main_verb('VBN')\
                        .build_tense()
    
    present_perfect_base = Tense().set_name("Present Perfect Base")\
                        .set_tag_negative_questions(['VBP', 'RB', 'PRP', 'VBN'])\
                        .set_tag_questions(['VBP', 'PRP', 'VBN'])\
                        .set_tag_negative(['VBP', 'RB', 'VBN'])\
                        .set_tag_positive(['VBP', 'VBN'])\
                        .set_condition({
                            "VBP": ["have", "'ve"]
                        })\
                        .set_main_verb('VBN')\
                        .build_tense()
    
    present_perfect_3_form = Tense().set_name("Present Perfect 3 Form")\
                        .set_tag_negative_questions(['VBZ', 'RB', 'PRP', 'VBN'])\
                        .set_tag_questions(['VBZ', 'PRP', 'VBN'])\
                        .set_tag_negative(['VBZ', 'RB', 'VBN'])\
                        .set_tag_positive(['VBZ', 'VBN'])\
                        .set_condition({
                            "VBZ": ['has']
                        })\
                        .set_main_verb('VBN')\
                        .build_tense()
    
    past_continuous = Tense().set_name("Past Continuous")\
                        .set_tag_negative_questions(['VBD', 'RB', 'PRP', 'VBG'])\
                        .set_tag_questions(['VBD', 'PRP', 'VBG'])\
                        .set_tag_negative(['VBD', 'RB', 'VBG'])\
                        .set_tag_positive(['VBD', 'VBG'])\
                        .set_condition({
                            "VBD": ['was', 'were']
                        })\
                        .set_main_verb('VBG')\
                        .build_tense()
    
    past_perfect = Tense().set_name("Past Perfect")\
                .set_tag_negative_questions(['VBD', 'RB', 'PRP', 'VBN'])\
                .set_tag_questions(['VBD', 'PRP', 'VBN'])\
                .set_tag_negative(['VBD', 'RB', 'VBN'])\
                .set_tag_positive(['VBD', 'VBN'])\
                .set_condition({
                    "VBD": ['had']
                })\
                .set_main_verb('VBN')\
                .build_tense()

    modal = Tense().set_name("Modal")\
            .set_tag_negative_questions(['MD', 'RB', 'PRP', 'VB'])\
            .set_tag_questions(['MD', 'PRP', 'VB'])\
            .set_tag_negative(['MD', 'RB', 'VB'])\
            .set_tag_positive(["MD", 'VB'])\
            .set_condition({
                "MD": ["can't", "can", "might", "may", "could", "must", "should"]
            })\
            .set_main_verb('VB')\
            .build_tense()
    
    there_are = Tense().set_name("There are")\
            .set_tag_negative_questions(['VBP', 'RB', 'EX'])\
            .set_tag_questions(['VBP', 'EX'])\
            .set_tag_negative(['EX', 'VBP', 'RB'])\
            .set_tag_positive(['EX', 'VBP'])\
            .set_condition({
                'VBP': ["are", "'re"]
            })\
            .set_main_verb('VBP')\
            .build_tense()

    there_is = Tense().set_name("There is")\
            .set_tag_negative_questions(['VBZ', 'RB', 'EX'])\
            .set_tag_questions(['VBZ', 'EX'])\
            .set_tag_negative(['EX', 'VBZ', 'RB'])\
            .set_tag_positive(['EX', 'VBZ'])\
            .set_condition({
                'VBZ': ["is", "'s"]
            })\
            .set_main_verb('VBZ')\
            .build_tense()
    
    there_was_were = Tense().set_name("There was/were")\
            .set_tag_negative_questions(['VBD', 'RB', 'EX'])\
            .set_tag_questions(['VBD', 'EX'])\
            .set_tag_negative(['EX', 'VBD', 'RB'])\
            .set_tag_positive(['EX', 'VBD'])\
            .set_condition({
                "VBD": ['was', 'were']
            })\
            .set_main_verb('VBD')\
            .build_tense()
    
    present_simple_base = Tense().set_name("Present Simple Base")\
            .set_tag_negative(['VBP', 'RB', 'VB'])\
            .set_tag_positive(['VBP'])\
            .set_condition({
                "VBP": ["am", "'m", "are", "'re", "have", "'ve"]
            })\
            .set_main_verb('VBP')\
            .set_tag_in(False)\
            .build_tense()
    
    present_simple_base_3_form = Tense().set_name("Present Simple Base 3 Form")\
                                .set_tag_negative(['VBZ', 'RB', 'VB'])\
                                .set_tag_positive(['VBZ'])\
                                .set_condition({
                                    "VBZ": ["is", "has", "'s"]
                                })\
                                .set_tag_in(False)\
                                .set_main_verb('VBZ')\
                                .build_tense()
    
    past_simple = Tense().set_name("Past Simple")\
            .set_tag_negative_questions(['VBD', 'RB', 'PRP', 'VB'])\
            .set_tag_questions(['VBD', 'PRP', 'VB'])\
            .set_tag_negative(['VBD', 'RB', 'VB'])\
            .set_tag_positive(['VBD'])\
            .set_condition({
                "VBD": ['was', 'were']
            })\
            .set_tag_in(False)\
            .set_main_verb('VBD')\
            .build_tense()
    
    to_be = Tense().set_name("To be")\
            .set_tag_negative(['VBP', 'RB'])\
            .set_tag_positive(['VBP'])\
            .set_condition({
                "VBP": ["are", "'re", "am", "'m"]
            })\
            .set_main_verb('VBP')\
            .build_tense()
    
    to_be_3_form = Tense().set_name("To be 3 form")\
            .set_tag_negative(['VBZ', 'RB'])\
            .set_tag_positive(['VBZ'])\
            .set_condition({
                "VBZ": ["is", "'s"]
            })\
            .set_main_verb('VBZ')\
            .build_tense()
    
    would_like = Tense().set_name("Would like")\
            .set_tag_questions(['MD', 'PRP', 'VB'])\
            .set_tag_negative(['MD', 'RB', 'VB'])\
            .set_tag_positive(['MD', 'VB'])\
            .set_condition({
                "MD": ["would", "'d"],
                "VB": ["like"]
            })\
            .set_main_verb('MD')\
            .build_tense()
    
    to_be_past = Tense().set_name("To be past")\
            .set_tag_negative(['VBD', 'RB'])\
            .set_tag_positive(['VBD'])\
            .set_condition({
                "VBD": ["was", "were"]
            })\
            .set_main_verb('VBD')\
            .build_tense()
    
    tenses = [
        future_perfect_continuous,
        future_simple_passive,
        present_continuous_passive,
        present_continuous_passive_3_form,
        present_perfect_passive,
        present_perfect_passive_3_form,
        future_perfect,
        present_perfect_continuous,
        present_perfect_continuous_3_form,
        future_continuous,
        past_perfect_continuous,
        used_to,
        present_simple_passive,
        present_simple_passive_3_form,
        future_simple,
        future_continuous,
        present_continuous,
        present_continuous_3_form,
        past_simple_passive,
        present_perfect_base,
        present_perfect_3_form,
        past_continuous,
        past_perfect,
        modal,
        there_are,
        there_is,
        there_was_were,
        present_simple_base,
        present_simple_base_3_form,
        past_simple,
        to_be,
        to_be_3_form,
        would_like,
        to_be_past
    ]

    return check_tense(word_xpos, tenses)


"""
Check tense of sentence
"""
def check_tense(word_xpos, tenses):
    for tense in tenses:
        for tag in tense.get_all_tags():
            print("Checking tags {0} in tags {1}".format(tag, word_xpos['xpos']))
            sub_word_xpos = get_sub_word_xpos(tag, word_xpos)
            if sub_word_xpos:
                print("Found the tag: {0} of tense {1}".format(tag, tense.get_name()))
                print("Checking extra conditions")

                # update the condition for negative case
                update_for_negative_case(tense, tag)

                print("tag {0} - conditions {1} - tag in {2}".format(tag, tense.get_condition(), tense.get_tag_in()))

                num_of_condition = len(tense.get_condition().keys())
                num_of_condition_matched = 0

                for tag_condition in tense.get_condition().keys():
                    word = sub_word_xpos['words'][sub_word_xpos['xpos'].index(tag_condition) if tag_condition in sub_word_xpos['xpos'] else -1]
                    if word != -1:
                        # convert the word to lower case
                        word = word.lower()
                        print("word {0} - tag condition {1}".format(word, tag_condition))
                        condition = tense.get_condition()
                        
                        if tense.get_tag_in() == False:
                            # check for "is NOT" first
                            if tag != 'RB' and word not in condition[tag_condition]:
                                num_of_condition_matched += 1
                                continue
                        
                        elif word in condition[tag_condition]:
                            # check for other tense
                            num_of_condition_matched += 1
                            continue

                print("num of condition matched {0}".format(num_of_condition_matched))    
                if num_of_condition_matched == num_of_condition:
                    return tense
                    
    if 'VB' in word_xpos['xpos'] and word_xpos['words'][word_xpos['xpos'].index('VB')].lower() == "let":
        return Tense().set_name("Imperative").build_tense()
    return None

"""
Update the condition for specical tenses like: Present Simple Base, Present
Simple Base 3 Form and Past Simple
"""
def update_for_negative_case(tense, tag):
    if 'RB' in tag:
        # add more condition checking RB
        tense.set_condition({'RB': ["not", "n't"]})
        # add "wo" if MD exists
        if 'MD' in tense.get_condition().keys():
            tense.add_single_tag_value_condition('MD', 'wo')
        # update for specical cases of tense
        if tense.get_name() == 'Present Simple Base':
            tense.set_condition({'VBP': ['do']})
            tense.set_tag_in(True)
        elif tense.get_name() == 'Present Simple Base 3 Form':
            tense.set_condition({'VBZ': ['does']})
            tense.set_tag_in(True)
        elif tense.get_name() == 'Past Simple':
            tense.set_condition({'VBD': ['did']})
            tense.set_tag_in(True)


"""
Get main verb of sentence
"""
def get_main_verb(tense, word_xpos):
    if tense:
        tag_main_verb = tense.get_main_verb()
        if tag_main_verb:
            print("Getting main verb tag {0} in tags {1} with words {2}".format(tag_main_verb, word_xpos['xpos'], word_xpos['words']))
            #return word_xpos['words'][word_xpos['xpos'].index(tag_main_verb)] if tag_main_verb in word_xpos['xpos'] else None
            return check_and_get_main_verb(tag_main_verb, word_xpos)
    return None

"""
Check and get the main verb. Check the main verb is in ['s, 'd, 've, 'd, 'm, 're, 'll],
then combine with the previous word to make the meaningful main verb. eg We'd = We + ' + d
@param tag_main_verb: the tag (xpos) of main verb in a sentence
@param word_xpos: the dictionary of words and xposes of words in a sentence
@return the main verb of sentence a if exist, vice versa None
"""
def check_and_get_main_verb(tag_main_verb, word_xpos):
    combined = False
    if tag_main_verb in word_xpos['xpos']:
        # get index of main verb
        index_main_verb = word_xpos['xpos'].index(tag_main_verb)
        # check if main verb is in ['s, 'd, 've, 'd, 'm, 're, 'll]
        main_verb = word_xpos['words'][index_main_verb]
        if main_verb:
            if "’" in main_verb:
                main_verb = main_verb.replace("’", "'")
            if main_verb in ["'s", "'d", "'ve", "'d", "'m", "'re", "'ll"]:
                # combine the previous word
                main_verb = word_xpos['words'][index_main_verb-1] + main_verb
            elif index_main_verb < len(word_xpos['words'])-1 and word_xpos['words'][index_main_verb+1] == "n't":
                # check after main verb is "n't"
                main_verb = main_verb + word_xpos['words'][index_main_verb+1]
            return main_verb
    return None

"""
Wrap the main verb in sentence by parenthesess
"""
def wrap_main_word(sentence, main_verb):
    if main_verb:
        return sentence.replace(main_verb, "{" + main_verb + "}", 1)
    return sentence

"""
Get the verb conjugators in 3 alternatives: infinitive, 3rd singular present and present participle
""" 
def main_verb_conjugate(main_verb):
    if main_verb is not None:
        main_verb = main_verb.lower()
        log_debug("Getting conjugators of main_verb: " + main_verb)
        try:
            tenses = nle.verb.tenses()
            num_of_alter = 3
            result = []
            for tense in tenses:
                if len(result) == num_of_alter:
                    break
                alter = nle.verb.conjugate(word=main_verb, tense=tense)
                log_debug("alter word: {0}, main verb: {1}".format(alter, main_verb))
                if alter and alter != 'be' and alter != main_verb and alter not in result:
                    result.append(alter)

            if len(result) < num_of_alter:
                len_result = len(result)
                for _ in range(0, 3-len_result):
                    result.append('')
            return result
        except Exception:
            log_debug("The main verb {0} vocalbulary does not exist".format(main_verb))
            # debug to log main verb does not exists, then update the main verb vocalbulary.
            # comment this line if all main verb is updated
            log_main_verb(main_verb)
    return ('','','')

"""
Log the missing main verb in nodebox_linguistics_extended main verb volcabulary.
Using this file to update nodebox_linguistics_extended later 
"""
def log_main_verb(main_verb):
    log_file = "main_verb.log"
    if os.path.isfile(log_file):
        try:
            os.remove(log_file)
        except:
            pass
        with open(log_file, 'a+') as f_a:
            f_a.write(main_verb + " \n")

"""
Check a list is sublist of other list
"""
def check_sublist(l1, l2):
    if len(l1) == 0 or len(l1) > len(l2):
        return False
    for i in range(0, len(l2)-len(l1)+1):
        if l2[i:i+len(l1)] == l1:
            return True
    return False

"""
Get sub dictionary from list of keys
"""
def get_sub_word_xpos(xposes, word_xpos):
    len_xposes = len(xposes)
    len_word_xpos = len(word_xpos['xpos'])
    if len_xposes > 0 and len_xposes <= len_word_xpos:
        for i in range(0, len_word_xpos-len_xposes+1):
            if word_xpos['xpos'][i:i+len_xposes] == xposes:
                return {
                    "words": word_xpos['words'][i:i+len_xposes],
                    "xpos": word_xpos['xpos'][i:i+len_xposes]
                }
    return {}
        

"""
Generate NLP model with necessary processors
"""
def generate_nlp_model():
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
    return nlp

"""
Remove the special character of end character of sentence
"""
def remove_special_character_end_of_sentence(sentence):
    special_characters = "!@#$%^&*()-+?_=,<>/."
    try:
        if sentence[-1] in special_characters:
            return sentence[:-1]
    except:
        return sentence
    return sentence


"""
Log message error and exit the program with status code -1
"""
def log_error(msg):
    print("ERROR: {msg}".format(msg=msg))
    sys.exit(1)

"""
Log message debug
"""
def log_debug(msg):
    print("DEBUG: {msg}".format(msg=msg))

"""
Get arguments from command line
"""
def get_args():
    parser = argparse.ArgumentParser(description="The progam to proess sentences using stanford NLP to get sentences's characteristic")
    parser.add_argument('-i', '--input', required=True, type=str, help="The input excel file")
    args = parser.parse_args()

    return args

"""
Read excel file to dataframe
"""
def read_excel_file():
    args = get_args()
    excel_file = args.input
    log_debug("Reading input excel file {excel_file}".format(excel_file=excel_file))
    # check excel file
    if not os.path.isfile(excel_file):
        log_error("File {excel_file} not found".format(excel_file=excel_file))
    if os.path.splitext(excel_file)[1] != '.xlsx':
        log_error("File {excel_file} is not excel file. Must be excel file with format xlsx".format(excel_file=excel_file))
    df = pd.read_excel(excel_file, index_col=None, engine="openpyxl")

    return df, excel_file
    

"""
The main function to take responsible for the whole of program process
"""
def main():
    # read excel file
    df, excel_file = read_excel_file()
    nlp = generate_nlp_model()
    for i in range(0, len(df)):
        sentence = df.iloc[i]["sentences"]
        
        if isinstance(sentence, int) or pd.isna(sentence):
            log_debug("No supported format!. Sentence: {0} - Skipping".format(sentence))
            continue
        df.loc[i, "sentences"] = sentence.replace("’", "'")
        # get type of sentence
        df.loc[i, "sentence_type"] = get_type_of_sentence(sentence)
        
        sentence_processed = remove_special_character_end_of_sentence(sentence)
        doc = nlp(sentence_processed)
        sent = doc.sentences[0]

        # get grammar tags of sentence
        word_xpos = get_grammar_tags_of_sentence(sent)
        log_debug("Process sentence: {0} - pos_tags: {1}".format(sentence_processed, word_xpos["xpos"]))
        df.loc[i, "grammar_tags"] = " ".join(word_xpos["xpos"])

        # get tense and main verb of sentence
        tense = get_tense_of_sentence(word_xpos)
        ## get tense of sentence
        df.loc[i, "tense"] = tense.get_name() if tense else None
        ## get main verb of sentence
        main_verb = get_main_verb(tense, word_xpos)
        df.loc[i, "main_verb"] = main_verb
        ## format sentence by wrapping main verb by parenthesess
        df.loc[i, "formatted"] = wrap_main_word(sentence, main_verb)
        ## main verb conjugation
        (alter_1, alter_2, alter_3) = main_verb_conjugate(main_verb)
        df.loc[i, "alter_1"] = alter_1
        df.loc[i, "alter_2"] = alter_2
        df.loc[i, "alter_3"] = alter_3
        log_debug("Processed sentence {0}".format(sentence))
    
    # save excel file to output
    output_file = excel_file.split('.')[0] + "-output.xlsx"
    log_debug("Save the result to output file {0}!".format(output_file))
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    main()