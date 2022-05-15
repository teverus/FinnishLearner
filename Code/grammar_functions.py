import random

from Code.Constructions import CONSTRUCTIONS
from Code.grammar_constants import *


def get_all_constructions():
    skeletons = [get_skeleton() for _ in range(4)]
    unique_skeletons = []
    for skeleton in skeletons:
        if skeleton not in unique_skeletons:
            unique_skeletons.append(skeleton)

    return unique_skeletons


def get_skeleton():
    skeleton = []
    skeleton_name = random.choice(list(CONSTRUCTIONS.keys()))

    for bone, bone_info in CONSTRUCTIONS[skeleton_name].items():
        is_optional = bone_info[STATUS] == Status.OPTIONAL
        is_processed = random.choice([True, False]) if is_optional else True
        bone_options = bone_info[OPTIONS]

        if is_processed:
            option = random.choice(bone_options)
            skeleton.append(option)
        else:
            skeleton.append("X")

    return skeleton
