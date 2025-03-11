"""Benchmarks for Koda."""

from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

yarn = 1
color_yarn = 5
bind = True


def run_pre_optimized_standard_lace(reps: int = 10, height: int = 10):
    """
    Generates a pre-optimized standardized lace pattern of the given size.
    Pre-optimized patterns are used for comparison to how KODA optimizes the same knit-graph structure.
    :param reps: The number of repetitions of the lace pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_lace.ks",
                                                                f"preopt_lace_{width}.k", f"preopt_lace_{width}.dat",
                                                                pattern_is_filename=True,
                                                                lace_reps=reps, height=height,
                                                                yarn=yarn,
                                                                bind=bind)


def run_unoptimized_standard_lace(reps: int = 10, height: int = 10):
    """
    Generates an un-optimized standardized lace pattern of the given size.
    The un-optimized program makes use of hand-knitting intuitive decrease functions.
    :param reps: The number of repetitions of the lace pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_lace.ks",
                                                                f"no_opt_lace_{width}.k", f"no_opt_lace_{width}.dat",
                                                                pattern_is_filename=True,
                                                                lace_reps=reps, height=height,
                                                                yarn=yarn,
                                                                bind=bind)


def run_pre_optimized_standard_cable(reps: int = 10, height: int = 10):
    """
    Generates a pre-optimized standardized cable pattern of the given size.
    Pre-optimized patterns are used for comparison to how KODA optimizes the same knit-graph structure.
    :param reps: The number of repetitions of the pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_cable.ks",
                                                                f"preopt_cable_{width}.k", f"preopt_cable_{width}.dat",
                                                                pattern_is_filename=True,
                                                                cable_reps=reps, height=height,
                                                                yarn=yarn,
                                                                bind=bind)


def run_unoptimized_standard_cable(reps: int = 10, height: int = 10):
    """
    Generates an un-optimized standardized cable pattern of the given size.
    The un-optimized program makes use of hand-knitting intuitive decrease functions.
    :param reps: The number of repetitions of the pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_cable.ks",
                                                                f"no_opt_cable_{width}.k", f"no_opt_cable_{width}.dat",
                                                                pattern_is_filename=True,
                                                                cable_reps=reps, height=height,
                                                                yarn=yarn,
                                                                bind=bind)


def run_pre_optimized_standard_color_rib(reps: int = 10, height: int = 10):
    """
    Generates a pre-optimized standardized color-rib pattern of the given size.
    Pre-optimized patterns are used for comparison to how KODA optimizes the same knit-graph structure.
    :param reps: The number of repetitions of the pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_color_rib.ks",
                                                                f"preopt_color_rib_{width}.k", f"preopt_color_rib_{width}.dat",
                                                                pattern_is_filename=True,
                                                                rib_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind)


def run_unoptimized_standard_color_rib(reps: int = 10, height: int = 10):
    """
    Generates an un-optimized standardized color-rib pattern of the given size.
    The un-optimized program makes use of hand-knitting intuitive decrease functions.
    :param reps: The number of repetitions of the pattern, width-wise.
    :param height: The height of the pattern.
    """
    width = (reps * 8) + 2
    _knit_graph, _machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_color_rib.ks",
                                                                f"no_opt_color_rib_{width}.k", f"no_opt_color_rib_{width}.dat",
                                                                pattern_is_filename=True,
                                                                rib_reps=reps, height=height,
                                                                yarn=yarn, color_yarn=color_yarn,
                                                                bind=bind)


def generate_benchmarks(max_reps: int = 10):
    """
    Generates all the benchmark knitout files from 1 to max_reps repetitions, width-wise.
    The height of each swatch will create a square based on the width resulting from the width-wise repetitions.
    :param max_reps: The maximum number of repetitions to generate.
    """
    for r in range(1, max_reps+1):
        w = (r * 8) + 2
        h = int(w / 2)
        run_pre_optimized_standard_lace(r, h)
        run_unoptimized_standard_lace(r, h)
        run_pre_optimized_standard_cable(r, h)
        run_unoptimized_standard_cable(r, h)
        run_pre_optimized_standard_color_rib(r, h)
        run_unoptimized_standard_color_rib(r, h)
