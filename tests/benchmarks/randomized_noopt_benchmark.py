from enum import Enum
import random

from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

yarn = 1
color_yarn = 2
bind = False


class Pattern_Option(Enum):
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


def randomized_lace(reps, height, seed=1):
    random.seed(seed)
    size = (reps * 4) + 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                              f"randomized_noopt_lace_w{size}_s{seed}.k", f"randomized_noopt_lace_w{size}_s{seed}.dat",
                                                              pattern_is_filename=True,
                                                              randomized_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind,
                                                              textures=[
                                                                  Pattern_Option.left_decrease,
                                                                  Pattern_Option.right_decrease
                                                              ])


def randomized_cable(reps, height, seed=1):
    random.seed(seed)
    size = (reps * 4) + 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                              f"randomized_noopt_cable_w{size}_s{seed}.k", f"randomized_noopt_cable_w{size}_s{seed}.dat",
                                                              pattern_is_filename=True,
                                                              randomized_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind,
                                                              textures=[Pattern_Option.left_cable, Pattern_Option.right_cable])


def randomized_color(reps, height, seed=1):
    random.seed(seed)
    size = (reps * 4) + 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                              f"randomized_noopt_color_rib_w{size}_s{seed}.k", f"randomized_noopt_color_rib_w{size}_s{seed}.dat",
                                                              pattern_is_filename=True,
                                                              randomized_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind,
                                                              textures=[
                                                                  Pattern_Option.purl,
                                                                  Pattern_Option.colored_knit
                                                              ])


def randomized_pattern(reps, height, seed=1):
    random.seed(seed)
    size = (reps * 4) + 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("randomized_unoptimized_pattern.ks",
                                                              f"randomized_noopt_w{size}_s{seed}.k", f"randomized_noopt_w{size}_s{seed}.dat",
                                                              pattern_is_filename=True,
                                                              randomized_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind,
                                                              textures=[Pattern_Option.left_decrease, Pattern_Option.right_decrease,
                                                                        Pattern_Option.left_cable, Pattern_Option.right_cable,
                                                                        Pattern_Option.purl, Pattern_Option.colored_knit])


r = 20
w = (r * 4) + 2
h = w
for s in range(1, 11):
    # randomized_lace(r, h, s)
    # randomized_cable(r, h, s)
    # randomized_color(r, h, s)
    randomized_pattern(r, h, s)

# randomized_lace(2, 2)
# randomized_cable(2, 2)
# randomized_color(2, 2)
# randomized_pattern(2, 2)
