"""Module containing the KnitoutDependencyViewer class."""
import networkx
from knitout_interpreter.knitout_operations.carrier_instructions import Yarn_Carrier_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from koda_knitout.Dependency_Viewer import Dependency_Viewer


class Knitout_Dependency_Viewer(Dependency_Viewer):
    """A Class that generates a viewer of a knitout dependency graph."""

    def __init__(self, dependency_graph: networkx.DiGraph, knitting_machine: Knitting_Machine):
        super().__init__(dependency_graph, knitting_machine)

    def _plot_instructions(self):
        for y, generation in enumerate(networkx.topological_generations(self.dependency_graph)):
            for instruction in generation:
                if isinstance(instruction, Needle_Instruction):
                    needle_buffer = -.25
                    if instruction.needle.is_back:
                        needle_buffer = .25
                    self.data_graph.add_node(instruction, x=instruction.needle.position, y=y + needle_buffer, carriers=instruction.carrier_set)
                    self._update_needle_range(instruction)
                elif isinstance(instruction, Yarn_Carrier_Instruction):
                    self._add_carrier_op(instruction, y)
        self._place_carrier_ops()

    def _plot_dependencies(self):
        for u, v in self.dependency_graph.edges:
            self.data_graph.add_edge(u, v, dependencies=self.dependency_graph.edges[(u, v)]['dependencies'])
            for dependency in self.dependency_graph.edges[(u, v)]['dependencies']:
                self.dependencies[dependency].add((u, v))
