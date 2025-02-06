from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

yarn = 1
color_yarn = 5
bind = True


def run_pre_optimized_standard_lace(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_lace.ks",
                                                              f"preopt_lace_{width}.k", f"preopt_lace_{width}.dat",
                                                              pattern_is_filename=True,
                                                              lace_reps=reps, height=height,
                                                              yarn=yarn,
                                                              bind=bind)


def run_unoptimized_standard_lace(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_lace.ks",
                                                              f"no_opt_lace_{width}.k", f"no_opt_lace_{width}.dat",
                                                              pattern_is_filename=True,
                                                              lace_reps=reps, height=height,
                                                              yarn=yarn,
                                                              bind=bind)


def run_pre_optimized_standard_cable(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_cable.ks",
                                                              f"preopt_cable_{width}.k", f"preopt_cable_{width}.dat",
                                                              pattern_is_filename=True,
                                                              cable_reps=reps, height=height,
                                                              yarn=yarn,
                                                              bind=bind)


def run_unoptimized_standard_cable(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_cable.ks",
                                                              f"no_opt_cable_{width}.k", f"no_opt_cable_{width}.dat",
                                                              pattern_is_filename=True,
                                                              cable_reps=reps, height=height,
                                                              yarn=yarn,
                                                              bind=bind)


def run_pre_optimized_standard_color_rib(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("pre_optimized_standard_color_rib.ks",
                                                              f"preopt_color_rib_{width}.k", f"preopt_color_rib_{width}.dat",
                                                              pattern_is_filename=True,
                                                              rib_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind)


def run_unoptimized_standard_color_rib(reps: int = 10, height: int = 10):
    width = (reps * 8) + 2
    course = height * 2
    knit_graph, machine_state = knit_script_to_knitout_to_dat("unoptimized_standard_color_rib.ks",
                                                              f"no_opt_color_rib_{width}.k", f"no_opt_color_rib_{width}.dat",
                                                              pattern_is_filename=True,
                                                              rib_reps=reps, height=height,
                                                              yarn=yarn, color_yarn=color_yarn,
                                                              bind=bind)


# for r in range(1, 11):
#     w = (r * 8) + 2
#     h = int(w / 2)
#     # run_pre_optimized_standard_lace(r, h)
#     # run_unoptimized_standard_lace(r, h)
#     # run_pre_optimized_standard_cable(r, h)
#     # run_unoptimized_standard_cable(r, h)
#     run_pre_optimized_standard_color_rib(r, h)
#     run_unoptimized_standard_color_rib(r, h)

# run_pre_optimized_standard_lace(10, 82)
# run_pre_optimized_standard_cable(10, 82)
run_pre_optimized_standard_color_rib(10, 82)
