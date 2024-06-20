"""Module containign Knitout Dependency Graph Generator"""
import networkx
from knit_graphs.Knit_Graph import Knit_Graph
from knit_graphs.Loop import Loop
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.carrier_instructions import Outhook_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Loop_Making_Instruction, Needle_Instruction, Knit_Instruction, Split_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from koda_knitout.knitout_dependencies.Knitout_Dependency_Viewer import Knitout_Dependency_Viewer
from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency


class Knitout_Dependency_Graph_Generator:
    """
    A class that generates a dependency graph from knitout instructions by executing the input knitout program.
    """

    def __init__(self, instructions: list[Knitout_Line]):
        self.dependency_graph: networkx.DiGraph = networkx.DiGraph()
        self.dependencies: dict[Knitout_Dependency: list[tuple[Knitout_Line, Knitout_Line]]] = {d: [] for d in Knitout_Dependency}
        self.instruction_to_required_rack: dict[Knitout_Line, tuple[int, bool]] = {}
        self.loop_to_creation_instruction: dict[Loop, Loop_Making_Instruction] = {}
        self.loop_to_last_instruction: dict[Loop, Needle_Instruction] = {}
        self.stitch_to_creation_instruction: dict[tuple[Loop, Loop], Loop_Making_Instruction] = {}
        self.crossing_to_creation_instruction: dict[tuple[Loop, Loop], Needle_Instruction] = {}
        self.original_instructions: list[Knitout_Line] = instructions
        self.knitting_machine: Knitting_Machine = Knitting_Machine()
        self.generate_dependency_graph()

    @property
    def knit_graph(self) -> Knit_Graph:
        """
        :return: The Knit_Graph formed by the execution of the original instructions.
        """
        return self.knitting_machine.knit_graph

    def get_edge_dependencies(self, prior_instruction: Knitout_Line, next_instruction: Knitout_Line) -> set[Knitout_Dependency]:
        """
        :param prior_instruction:
        :param next_instruction:
        :return: The dependencies between the prior and next instructions.
         If the set is empty, then there is no dependency between these instructions.
        """
        if not self.dependency_graph.has_edge(prior_instruction, next_instruction):
            return set()
        else:
            return self.dependency_graph.edges[(prior_instruction, next_instruction)]['dependencies']

    def add_dependency(self, prior_instruction: Knitout_Line, next_instruction: Knitout_Line, dependency: Knitout_Dependency, **kwargs):
        """
        Adds a dependency from the prior_instruction to the next_instruction.
        Marks it with the given dependency type.
        :param prior_instruction: The instruction that must proceed next_instruction.
        :param next_instruction: The instruction that must succeed prior_instruction.
        :param dependency: The type of dependency that connects these instructions.
        """
        if self.dependency_graph.has_edge(prior_instruction, next_instruction):
            self.dependency_graph.edges[(prior_instruction, next_instruction)]['dependencies'].add(dependency)
            for k, v in kwargs.items():
                self.dependency_graph.edges[(prior_instruction, next_instruction)][k] = v
        else:
            self.dependency_graph.add_edge(prior_instruction, next_instruction, dependencies={dependency}, **kwargs)

    def add_instruction(self, instruction: Knitout_Line):
        """
        Execute and add the given instruction to the dependency graph.
        :param instruction: The instruction to execute and form dependencies from.
        """
        prior_n1_loops: list[Loop] = []
        if isinstance(instruction, Needle_Instruction):
            prior_n1_loops = self.knitting_machine[instruction.needle].held_loops
        updated_kg = instruction.execute(self.knitting_machine)
        if updated_kg:
            self.instruction_to_required_rack[instruction] = self.knitting_machine.rack, self.knitting_machine.all_needle_rack
            if isinstance(instruction, Needle_Instruction):
                involved_floats = set()
                if isinstance(instruction, Loop_Making_Instruction):
                    made_loops = instruction.made_loops
                    for l in made_loops:
                        yarn_prior_loop = l.prior_loop_on_yarn()
                        if yarn_prior_loop is not None:
                            involved_floats.add((yarn_prior_loop, l))
                            self.add_dependency(self.loop_to_creation_instruction[yarn_prior_loop], instruction, Knitout_Dependency.Yarn_Order,
                                                yarn=l.yarn)
                        self.loop_to_creation_instruction[l] = instruction
                        self.loop_to_last_instruction[l] = instruction
                    if isinstance(instruction, (Knit_Instruction, Split_Instruction)):
                        for v in made_loops:
                            for u in prior_n1_loops:
                                last_instruction = self.loop_to_last_instruction[u]
                                self.add_dependency(last_instruction, instruction, Knitout_Dependency.Stitch_Order)
                                self.stitch_to_creation_instruction[(u, v)] = instruction
                if instruction.has_second_needle:
                    for l in prior_n1_loops:
                        yarn_prior_loop = l.prior_loop_on_yarn()
                        if yarn_prior_loop is not None:
                            involved_floats.add((yarn_prior_loop, l))
                        yarn_next_loop = l.next_loop_on_yarn()
                        if yarn_next_loop is not None:
                            involved_floats.add((l, yarn_next_loop))
                        last_instruction = self.loop_to_last_instruction[l]
                        self.add_dependency(last_instruction, instruction, Knitout_Dependency.Loop_Position)
                        self.loop_to_last_instruction[l] = instruction
                        for right_loop in self.knit_graph.braid_graph.left_crossing_loops(l):
                            right_instruction = self.loop_to_last_instruction[right_loop]
                            self.add_dependency(right_instruction, instruction, Knitout_Dependency.Wale_Crossing,
                                                crossing=self.knit_graph.braid_graph.get_crossing(l, right_loop))
                        for left_loop in self.knit_graph.braid_graph.right_crossing_loops(l):
                            left_instruction = self.loop_to_last_instruction[left_loop]
                            self.add_dependency(left_instruction, instruction, Knitout_Dependency.Wale_Crossing,
                                                crossing=self.knit_graph.braid_graph.get_crossing(left_loop, l))
                for u, v in involved_floats:
                    for l in u.yarn.get_loops_in_front_of_float(u, v):
                        l_instruction = self.loop_to_last_instruction[l]
                        self.add_dependency(l_instruction, instruction, Knitout_Dependency.Float_Position,
                                            in_front_of_float=True, behind_float=False)
                    for l in u.yarn.get_loops_behind_float(u, v):
                        l_instruction = self.loop_to_last_instruction[l]
                        self.add_dependency(l_instruction, instruction, Knitout_Dependency.Float_Position,
                                            in_front_of_float=False, behind_float=True)
            elif isinstance(instruction, Outhook_Instruction):
                yarn = instruction.get_yarn(self.knitting_machine)
                last_instruction = self.loop_to_creation_instruction[yarn.last_loop]
                self.add_dependency(last_instruction, instruction, Knitout_Dependency.Yarn_Order, yarn=yarn)

    def generate_dependency_graph(self):
        """
            Executes and forms the dependency graph from the input instruction set.
        """
        for instruction in self.original_instructions:
            self.add_instruction(instruction)

    def visualize(self):
        """
            Open a visualizer of the given dependency graph for debugging utility.
        """
        visualizer = Knitout_Dependency_Viewer(self.dependency_graph, self.knitting_machine)
        visualizer.visualize()

    def __len__(self):
        return len(self.original_instructions)
