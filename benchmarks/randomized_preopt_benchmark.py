"""Script to generate randomized benchmark swatches that are pre-optimized.
 Used for visual comparison to optimized swatches, but knitgraph structures are not guaranteed to match."""

import random

from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

from benchmarks.randomized_noopt_benchmark import Pattern_Option

yarn = 1
color_yarn = 2
bind = False


def randomized_lace(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized lace pattern with optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_preopt_pattern.ks",
                                                                f"randomized_preopt_lace_w{size}_s{seed}.k", f"randomized_preopt_lace_w{size}_s{seed}.dat",
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
    Generates a randomized cable pattern with optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_preopt_pattern.ks",
                                                                f"randomized_preopt_cable_w{size}_s{seed}.k", f"randomized_preopt_cable_w{size}_s{seed}.dat",
                                                                pattern_is_filename=True,
                                                                randomized_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind,
                                                                textures=[Pattern_Option.left_cable, Pattern_Option.right_cable])


def randomized_color(reps: int, height: int, seed: int = 1):
    """
    Generates a randomized color work pattern with optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_preopt_pattern.ks",
                                                                f"randomized_preopt_color_rib_w{size}_s{seed}.k", f"randomized_preopt_color_rib_w{size}_s{seed}.dat",
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
    Generates a randomized pattern with lace, cables, and color work with optimization.
    :param reps: The number of repetitions of the randomized pattern, width-wise.
    :param height: The height of the randomized pattern.
    :param seed: The seed for the randomization.
    """
    random.seed(seed)
    size = (reps * 4) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("randomized_preopt_pattern.ks",
                                                                f"randomized_preopt_w{size}_s{seed}.k", f"randomized_preopt_w{size}_s{seed}.dat",
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
