# import random
#
# from Code.constants import Statistics, Settings, ALL_WORDS_SENTENCES, PART_OF_SPEECH
# from Code.functions.db import export_constructions
# from Code.functions.high_level import get_all_words
# from Code.functions.ui import show_title_head, show_run_statistics
# from Code.sentences.grammar_functions import get_all_constructions
#
#
# class PracticeSentences:
#     def __init__(self, sentences_per_run):
#         self.sentences_per_run = sentences_per_run
#         self.stats = {Statistics.CORRECT: 0, Statistics.INCORRECT: 0}
#         self.all_words = get_all_words(ALL_WORDS_SENTENCES, sort_by=PART_OF_SPEECH)
#         self.constructions = get_all_constructions()
#         export_constructions(self.constructions)
#         self.run()
#
#     def run(self):
#         print("Work in progress... Please, do not choose this option")
#         exit(1)
#         for index in range(1, self.sentences_per_run + 1):
#             self.show_statistics(index)
#             specific_construction = self.choose_a_construction()
#             self.display_the_sentence(specific_construction)
#             self.get_user_answer()
#             self.evaluate_the_answer()
#
#     def show_statistics(self, index):
#         show_title_head(index, self.sentences_per_run, "SENTENCE", user_tips=False)
#         show_run_statistics(self.stats, Settings.WORD_COMBINATIONS_PER_RUN)
#
#     def choose_a_construction(self):
#         # надо убирать уже выбранные
#         return random.choice(self.constructions)
#
#     def display_the_sentence(self, sentence):
#         print(sentence)
#
#     def get_user_answer(self):
#         a = 1
#
#     def evaluate_the_answer(self):
#         pass
