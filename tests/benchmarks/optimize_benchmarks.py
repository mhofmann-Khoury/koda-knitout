import csv
import time

from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.run_knitout import run_knitout

from koda_knitout.carriage_pass_dependencies.Carriage_Pass_Dependency_Graph_Generator import Carriage_Pass_Dependency_Graph_Generator
from koda_knitout.knitout_dependencies.Knitout_Dependency_Graph_Generator import Knitout_Dependency_Graph_Generator

optimization_data: dict[str, dict] = {}
dependency_calculation_times = {}
optimization_times = {}


def optimize_knitout(k_file_name: str, optimized_filename: str, dat_file: str, get_seed: bool = False):
    seed = 0
    if get_seed:
        seed = k_file_name[k_file_name.index('_s') + 2:]
        seed = seed[:seed.index('.')]
        seed = int(seed)
        size = k_file_name[k_file_name.index('_w') + 2:]
        size = size[:size.rindex('_')]
        size = int(size)
    else:
        size = k_file_name[k_file_name.rindex('_') + 1:]
        size = size[:size.index('.')]
        size = int(size)

    global optimization_data, dependency_calculation_times, optimization_times
    executed_program, machine, knit_graph = run_knitout(k_file_name)
    start_dependency_time = time.time()
    knitout_dependency_graph_generator = Knitout_Dependency_Graph_Generator(executed_program)
    cp_generator = Carriage_Pass_Dependency_Graph_Generator(knitout_dependency_graph_generator)
    end_dependency_time = time.time()
    dependency_duration = end_dependency_time - start_dependency_time
    dependency_calculation_times[k_file_name] = dependency_duration
    optimization_start_time = time.time()
    optimized_execution = cp_generator.find_execution_order()
    optimization_end_time = time.time()
    optimization_duration = optimization_end_time - optimization_start_time
    optimization_times[k_file_name] = optimization_duration

    time_data_entry = {"Knitout": k_file_name, "Size": size,
                       "Dependency Calculation": dependency_duration * 1000, "Optimization Time": optimization_duration * 1000,
                       "Total Optimization Time": (optimization_duration + dependency_duration) * 1000}
    if get_seed:
        time_data_entry["Seed"] = seed
    optimization_data[k_file_name] = time_data_entry

    with open(optimized_filename, "w") as optimized_file:
        optimized_file.writelines([";!knitout-2\n",
                                   ";;Machine: SWG091N2\n",
                                   ";;Gauge: 15\n",
                                   ";;Position: Right\n",
                                   ";;Carriers: 1 2 3 4 5 6 7 8 9 10\n"])
        execution_strings = [str(l) for l in optimized_execution]
        optimized_file.writelines(execution_strings)
    compile_knitout(optimized_filename, dat_file)


def write_timing_data(csv_file: str, get_seed: bool = False):
    """
    :param get_seed:
    :param csv_file: File to write the timing data to.
    """
    global optimization_data
    fields = ["Knitout", "Size", "Dependency Calculation", "Optimization Time", "Total Optimization Time"]
    if get_seed:
        fields.append("Seed")
    data = list(optimization_data.values())
    with open(csv_file, "w") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(data)


def optimize_lace():
    for i in range(10, 85, 8):
        optimize_knitout(f"no_opt_lace_{i}.k", f"opt_lace_{i}.k", f"opt_lace_{i}.dat")
    write_timing_data("lace_optimization_times.csv")


def optimize_cable():
    for i in range(10, 85, 8):
        optimize_knitout(f"no_opt_cable_{i}.k", f"opt_cable_{i}.k", f"opt_cable_{i}.dat")
    write_timing_data("cable_optimization_times.csv")


def optimize_color_rib():
    for i in range(10, 85, 8):
        optimize_knitout(f"no_opt_color_rib_{i}.k", f"opt_color_rib_{i}.k", f"opt_color_rib_{i}.dat")
    write_timing_data("color_rib_optimization_times.csv")


def optimize_random_lace(size=82):
    for i in range(1, 11):
        optimize_knitout(f"randomized_noopt_lace_w{size}_s{i}.k", f"rand_opt_lace_s{i}.k", f"rand_opt_lace_s{i}.dat", get_seed=True)
    write_timing_data("randomized_lace_timing_data.csv", get_seed=True)


def optimize_random_cable(size=82):
    for i in range(1, 11):
        optimize_knitout(f"randomized_noopt_cable_w{size}_s{i}.k", f"rand_opt_cable_s{i}.k", f"rand_opt_cable_s{i}.dat", get_seed=True)
    write_timing_data("randomized_cable_timing_data.csv", get_seed=True)


def optimize_random_color_rib(size=82):
    for i in range(1, 11):
        optimize_knitout(f"randomized_noopt_color_rib_w{size}_s{i}.k", f"rand_opt_color_s{i}.k", f"rand_opt_color_s{i}.dat", get_seed=True)
    write_timing_data("randomized_color_timing_data.csv", get_seed=True)


def optimize_random(size=82):
    for i in range(1, 11):
        optimize_knitout(f"randomized_noopt_w{size}_s{i}.k", f"rand_opt_s{i}.k", f"rand_opt_s{i}.dat", get_seed=True)
    write_timing_data("randomized_all_timing_data.csv", get_seed=True)


# optimize_lace()
# optimize_cable()
# optimize_color_rib()

# optimize_random_lace()
optimize_random_cable()
# optimize_random_color_rib()
# optimize_random()
# optimize_knitout("no_opt_lace.k", "optimized_lace.k", "optimized_lace.dat")
# optimize_knitout("no_opt_cable.k", "optimized_cable.k", "optimized_cable.dat")
# optimize_knitout("no_opt_color_rib.k", "optimized_color_rib.k", "optimized_color_rib.dat")
