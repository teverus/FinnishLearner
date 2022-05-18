from Code.sentences.grammar_constants import *

"""
CONSTRUCTION_NAME: {
    PART_OF_SENTENCE: {
        STATUS: Status.REQUIRED,
        OPTIONS: [PART_OF_SPEECH, PART_OF_SPEECH]
    }
}
"""

CONSTRUCTIONS = {
    COMPOUND_NOMINAL: {
        DETACHED_WORD: {
            STATUS: Status.OPTIONAL,
            OPTIONS: [INTERJECTION]
        },
        SUBJECT: {
            STATUS: Status.REQUIRED,
            OPTIONS: [PRONOUN_PERSONAL]
        },
        LINK_VERB: {
            STATUS: Status.REQUIRED,
            OPTIONS: [BE_FORM]
        },
        PREDICATE: {
            STATUS: Status.REQUIRED,
            OPTIONS: [ADJECTIVE]
        },
    }
}
