from unittest import TestCase

from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat
from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.run_knitout import run_knitout

from koda_knitout.carriage_pass_dependencies.Carriage_Pass_Dependency_Graph_Generator import Carriage_Pass_Dependency_Graph_Generator
from koda_knitout.knitout_dependencies.Knitout_Dependency_Graph_Generator import Knitout_Dependency_Graph_Generator


class TestCarriage_Pass_Dependency_Graph_Generator(TestCase):
    def test_stst(self):
        cp_generator = self.generate_cp("stst.k")
        optimized_execution = cp_generator.find_execution_order()
        cp_generator.visualize()
        for line in optimized_execution:
            print(line)

    def test_half_rib_half_seed(self):
        knit_script_to_knitout_to_dat("half_rib_half_seed.ks", "half_rib_half_seed.k", "half_rib_half_seed.dat",
                                      pattern_is_filename=True, c=1, width=8, height=4)
        cp_generator = self.generate_cp("half_rib_half_seed.k")
        cp_generator.write_optimized_execution_order("half_rib_half_seed_opt.k")
        compile_knitout("half_rib_half_seed_opt.k", "half_rib_half_seed_opt.dat")

    def test_compile_half_rib_half_seed(self):
        compile_knitout("half_rib_half_seed_opt.k", "half_rib_half_seed_opt.dat")

    def test_tube(self):
        cp_generator = self.generate_cp("tube.k")
        cp_generator.write_optimized_execution_order("tube_opt.k")
        cp_generator.visualize()

    def test_seed(self):
        cp_generator = self.generate_cp("seed.k")
        cp_generator.write_optimized_execution_order("seed_opt.k")
        cp_generator.visualize()

    def test_slow_seed(self):
        #Todo: releasehook not ideally placed, but acceptable.
        cp_generator = self.generate_cp("slow_seed.k")
        cp_generator.write_optimized_execution_order("slow_seed_opt.k")
        cp_generator.visualize()

    def test_lace(self):
        cp_generator = self.generate_cp("lace.k")
        cp_generator.write_optimized_execution_order("lace_opt.k")
        cp_generator.visualize()

    def test_slow_lace(self):
        cp_generator = self.generate_cp("slow_lace.k")
        cp_generator.write_optimized_execution_order("slow_lace_opt.k")
        cp_generator.visualize()

    def test_cable(self):
        cp_generator = self.generate_cp("cable.k")
        cp_generator.write_optimized_execution_order("cable_opt.k")
        cp_generator.visualize()

    def test_slow_cable(self):
        cp_generator = self.generate_cp("slow_cable.k")
        cp_generator.write_optimized_execution_order("slow_cable_opt.k")
        cp_generator.visualize()

    def test_triangle(self):
        cp_generator = self.generate_cp("triangle.k")
        cp_generator.write_optimized_execution_order("triangle_opt.k")
        cp_generator.visualize()

    def test_slow_triangle(self):
        cp_generator = self.generate_cp("slow_triangle.k")
        cp_generator.write_optimized_execution_order("slow_triangle_opt.k")
        cp_generator.visualize()

    @staticmethod
    def generate_cp(knitout_sample: str, visualize=True):
        """
        Run greedy carriage pass generation on the given knitout sample
        :param knitout_sample: The file name for the knitout sample.
        :param visualize: If true, will generate a viewer of the resulting carriage_pass graph.
        """
        executed_program, machine, knit_graph = run_knitout(knitout_sample)
        knitout_dependency_graph_generator = Knitout_Dependency_Graph_Generator(executed_program)
        cp_generator = Carriage_Pass_Dependency_Graph_Generator(knitout_dependency_graph_generator)
        if visualize:
            cp_generator.visualize()
        return cp_generator
