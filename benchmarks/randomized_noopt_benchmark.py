"""Script to generate randomized patterns for benchmarking Koda."""
from enum import Enum
import random

from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

yarn = 1
color_yarn = 2
bind = False


class Pattern_Option(Enum):
    """Enum of allowed randomized features in a randomized benchmark pattern"""
    left_decrease = "left_decrease"
    right_decrease = "right_decrease"
    left_cable = "left_cable"
    right_cable = "right_cable"
    colored_knit = "colored_knit"
    purl = "purl"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, Pattern_Option):
            return self.value == other.value


def randomized_lace(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized lace pattern without optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                                f"randomized_noopt_lace_w{size}_s{seed}.k", f"randomized_noopt_lace_w{size}_s{seed}.dat",
                                                                pattern_is_filename=True,
                                                                randomized_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind,
                                                                textures=[
                                                                    Pattern_Option.left_decrease,
                                                                    Pattern_Option.right_decrease
                                                                ])


def randomized_cable(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized cable pattern without optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                                f"randomized_noopt_cable_w{size}_s{seed}.k", f"randomized_noopt_cable_w{size}_s{seed}.dat",
                                                                pattern_is_filename=True,
                                                                randomized_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind,
                                                                textures=[Pattern_Option.left_cable, Pattern_Option.right_cable])


def randomized_color(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized color work pattern without optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                                f"randomized_noopt_color_rib_w{size}_s{seed}.k", f"randomized_noopt_color_rib_w{size}_s{seed}.dat",
                                                                pattern_is_filename=True,
                                                                randomized_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind,
                                                                textures=[
                                                                    Pattern_Option.purl,
                                                                    Pattern_Option.colored_knit
                                                                ])


def randomized_pattern(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized pattern with lace, cables, and color work without optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                                f"randomized_noopt_w{size}_s{seed}.k", f"randomized_noopt_w{size}_s{seed}.dat",
                                                                pattern_is_filename=True,
                                                                randomized_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind,
                                                                textures=[Pattern_Option.left_decrease, Pattern_Option.right_decrease,
                                                                          Pattern_Option.left_cable, Pattern_Option.right_cable,
                                                                          Pattern_Option.purl, Pattern_Option.colored_knit])


def generate_randomized_pattern(reps: int):
    """
    Generates 10 randomized patterns with different seeds of the given rep size.
    :param reps: The number of width-wise repetitions to generate.
    """
    w = (reps * 4) + 2
    h = w
    for s in range(1, 11):
        randomized_lace(reps, h, s)
        randomized_cable(reps, h, s)
        randomized_color(reps, h, s)
        randomized_pattern(reps, h, s)

