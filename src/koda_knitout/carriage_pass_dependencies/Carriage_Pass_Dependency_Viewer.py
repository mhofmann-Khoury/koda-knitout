"""Module containing the Carriage Pass Dependency Viewer class."""
import networkx
from knitout_interpreter.knitout_execution_structures.Carriage_Pass import Carriage_Pass
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import Yarn_Carrier_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from koda_knitout.Dependency_Viewer import Dependency_Viewer
from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency


class Carriage_Pass_Dependency_Viewer(Dependency_Viewer):
    """
    Visualize the knitout dependencies structured by a topological sort of the carriage passes they form.
    """

    def __init__(self, carriage_pass_dependency_graph: networkx.DiGraph, knitout_dependency_graph: networkx.DiGraph, knitting_machine: Knitting_Machine):
        super().__init__(knitout_dependency_graph, knitting_machine)
        self.carriage_pass_dependency_graph: networkx.DiGraph = carriage_pass_dependency_graph

    @property
    def knitout_dependency_graph(self) -> networkx.DiGraph:
        """
        :return: clarifies access ot the dependency graph is the original knitout dependencies.
        """
        return self.dependency_graph

    def _plot_instructions(self):

        for y, instruction_set in enumerate(networkx.topological_sort(self.carriage_pass_dependency_graph)):
            if isinstance(instruction_set, Carriage_Pass):
                carriage_pass = instruction_set
                for instruction in carriage_pass:
                    needle_buffer = -.25
                    if instruction.needle.is_back:
                        needle_buffer = .25
                    self.data_graph.add_node(instruction, x=instruction.needle.position, y=y + needle_buffer)
                    self._update_needle_range(instruction)
            elif isinstance(instruction_set, Rack_Instruction):
                self.data_graph.add_node(instruction_set, x=-1, y=y)
            elif isinstance(instruction_set, Yarn_Carrier_Instruction):
                self._add_carrier_op(instruction_set, y)
        self._place_carrier_ops()

    def _plot_dependencies(self):
        self._plot_cp_dependencies()
        self._plot_yarn_order_dependencies()

    def _plot_cp_dependencies(self):
        for u, v in self.carriage_pass_dependency_graph.edges:
            edge_dependencies = self.carriage_pass_dependency_graph.edges[(u, v)]['edge_dependencies']
            for edge, deps in edge_dependencies.items():
                self.data_graph.add_edge(edge[0], edge[1], dependencies=deps)
                for dependency in deps:
                    self.dependencies[dependency].add((edge[0], edge[1]))

    def _plot_yarn_order_dependencies(self):
        for cp in self.carriage_pass_dependency_graph.nodes:
            if isinstance(cp, Carriage_Pass):
                if cp.carrier_set is not None:  # add yarn_order dependencies to graph
                    for instruction in cp:
                        predecessors = self.knitout_dependency_graph.predecessors(instruction)
                        for pred in predecessors:
                            deps = self.knitout_dependency_graph.edges[(pred, instruction)]['dependencies']
                            if Knitout_Dependency.Yarn_Order in deps:
                                self.data_graph.add_edge(pred, instruction, dependencies=deps)
                                self.dependencies[Knitout_Dependency.Yarn_Order].add((pred, instruction))
