from knit_script.interpret_knit_script import knit_script_to_knitout
from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.knitout_language.Knitout_Context import Knitout_Context
from knitout_interpreter.knitout_operations.Header_Line import get_machine_header
from knitout_interpreter.knitout_operations.carrier_instructions import Outhook_Instruction
from knitout_interpreter.run_knitout import run_knitout

from koda_knitout.carriage_pass_dependencies.Carriage_Pass_Dependency_Graph_Generator import Carriage_Pass_Dependency_Graph_Generator
from koda_knitout.knitout_dependencies.Knitout_Dependency_Graph_Generator import Knitout_Dependency_Graph_Generator


def optimize_knitout_file(knitout_file: str, optimized_knitout_name: str, optimized_dat_name: str | None = None, visualize=False):
    """
    Takes in a knitout file and generates an optimized version of the knitout file.
    :param optimized_dat_name: The name of the dat file for the optimized knitout or None if not DAT file needs to be generated.
    :param knitout_file: The knitout file to be optimized.
    :param optimized_knitout_name: The name of the output file for the optimized instructions.
    :param visualize: If set to true, visualizes the carriage pass dependencies for optimization debugging.
    """
    executed_program, machine, knit_graph = run_knitout(knitout_file)
    knitout_dependency_graph_generator = Knitout_Dependency_Graph_Generator(executed_program)
    cp_generator = Carriage_Pass_Dependency_Graph_Generator(knitout_dependency_graph_generator)
    if visualize:
        cp_generator.visualize()
    optimized_knitout = cp_generator.find_execution_order()
    context = Knitout_Context()
    executed_instructions, execution_machine, _knitgraph = context.execute_knitout_instructions(optimized_knitout)
    optimized_program = get_machine_header(execution_machine)
    optimized_program.extend(executed_instructions)
    for cid in execution_machine.carrier_system.active_carriers:
        optimized_program.append(Outhook_Instruction(cid, f"Take out remaining carriers"))
    with open(optimized_knitout_name, 'w') as knitout_file:
        clean_instructions = [f"{str(i).splitlines()[0]}\n" for i in optimized_program]
        knitout_file.writelines(clean_instructions)
    if optimized_dat_name is not None:
        compile_knitout(optimized_knitout_name, optimized_dat_name)


def optimize_knitscript(ks_file: str, unoptimized_k_name: str, optimized_file_name: str, unoptimized_dat_name: str | None = None, optimized_dat_name: str | None = None, **ks_args):
    """
    Takes in a knitscript file and keyword arguments to generate a new knitout file and then optimize the result.
    :param unoptimized_dat_name:
    :param optimized_dat_name:
    :param ks_file: The knitscript file to be optimized.
    :param unoptimized_k_name:  The name of the unoptimized knitout resulting form the knitscript file.
    :param optimized_file_name: The name of the optimized knitout resulting form the knitscript file.
    :param ks_args: The keyword arguments for the knitscript program.
    """
    knit_script_to_knitout(ks_file, unoptimized_k_name, pattern_is_filename=True, **ks_args)
    if unoptimized_dat_name is not None:
        compile_knitout(unoptimized_k_name, unoptimized_dat_name)
    optimize_knitout_file(unoptimized_k_name, optimized_file_name, optimized_dat_name, visualize=False)
