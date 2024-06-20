from unittest import TestCase

from knitout_interpreter.run_knitout import run_knitout

from koda_knitout.knitout_dependencies.Knitout_Dependency_Graph_Generator import Knitout_Dependency_Graph_Generator


class TestKnitout_Dependency_Graph_Generator(TestCase):
    def test_cast_on(self):
        self.generate_di_graph("cast_on.k")

    def test_stst(self):
        self.generate_di_graph("stst.k")

    def test_tube(self):
        self.generate_di_graph("tube.k")

    def test_seed(self):
        self.generate_di_graph("seed.k")

    def test_slow_seed(self):
        self.generate_di_graph("slow_seed.k")

    def test_lace(self):
        self.generate_di_graph("lace.k")

    def test_slow_lace(self):
        self.generate_di_graph("slow_lace.k")

    def test_cable(self):
        self.generate_di_graph("cable.k")

    def test_slow_cable(self):
        self.generate_di_graph("slow_cable.k")

    def test_triangle(self):
        self.generate_di_graph("triangle.k")

    def test_slow_triangle(self):
        self.generate_di_graph("slow_triangle.k")

    @staticmethod
    def generate_di_graph(knitout_sample: str, visualize=True):
        """
        Run greedy carriage pass generation on the given knitout sample
        :param knitout_sample: The file name for the knitout sample.
        :param visualize: If true, will generate a viewer of the resulting carriage_pass graph.
        """
        executed_program, machine, knit_graph = run_knitout(knitout_sample)
        knitout_dependency_graph_generator = Knitout_Dependency_Graph_Generator(executed_program)
        if visualize:
            knitout_dependency_graph_generator.visualize()
