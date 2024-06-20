"""Module containing the Carriage Pass Dependency Graph Generator."""
import networkx
from knitout_interpreter.knitout_execution_structures.Carriage_Pass import Carriage_Pass
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.carrier_instructions import Outhook_Instruction, Releasehook_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction, Loop_Making_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from koda_knitout.carriage_pass_dependencies.Carriage_Pass_Dependency_Viewer import Carriage_Pass_Dependency_Viewer
from koda_knitout.knitout_dependencies.Knitout_Dependency_Graph_Generator import Knitout_Dependency_Graph_Generator
from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency
from koda_knitout.machine_state_requirements.machine_setting_injection import Machine_Setting_Injection


class Carriage_Pass_Dependency_Graph_Generator:
    """
        A class that generates carriage passes from a knitout dependency graph.
    """

    def __init__(self, knitout_dependency_generator: Knitout_Dependency_Graph_Generator):
        self.knitout_dependency_generator: Knitout_Dependency_Graph_Generator = knitout_dependency_generator
        self.carriage_pass_dependency_graph: networkx.DiGraph = networkx.DiGraph()
        self.open_carriage_passes: set[Carriage_Pass] = set()
        self.instructions_to_carriage_pass: dict[Needle_Instruction, Carriage_Pass] = {}
        self.form_carriage_passes()

    @property
    def knitting_machine(self):
        """
        :return: The knitting machine that formed the knitout dependencies. 
        """
        return self.knitout_dependency_generator.knitting_machine

    @property
    def knitout_dependency_graph(self) -> networkx.DiGraph:
        """
        :return: The dependency graph of the original knitout program.
        """
        return self.knitout_dependency_generator.dependency_graph

    def get_instruction_rack(self, instruction: Knitout_Line) -> tuple[int, bool]:
        """
        :param instruction:
        :return: The racking assigned by the original program to the given instruction.
        """
        return self.knitout_dependency_generator.instruction_to_required_rack[instruction]

    def find_mergable_open_carriage_pass(self, instruction: Needle_Instruction) -> None | Carriage_Pass:
        """
        :param instruction: The instruction to find a mergable open carriage pass for.
        :return: Return an open carriage pass by greedy selection that can merge with the given instruction without creating cycles in the carriage pass graph.
        Otherwise, return None if there is no open carriage pass that meets this criteria.
        """
        if isinstance(instruction, Loop_Making_Instruction):
            yarn_order_cp = self._yarn_order_receptive_carriage_pass(instruction)
            if yarn_order_cp is None or not self.carriage_pass_is_open(yarn_order_cp):
                return None
            dep_free_cp = self._receptive_carriage_passes(instruction, {yarn_order_cp})
        else:
            receptive_cp = self._receptive_carriage_passes(instruction, self.open_carriage_passes)
            dep_free_cp = self._dependency_free_carriage_passes(instruction, receptive_cp)
        cycle_free_cp = self.cycle_free_carriage_passes(instruction, dep_free_cp)
        if len(cycle_free_cp) == 0:
            return None
        else:
            for cp in cycle_free_cp:
                return cp

    def carriage_pass_is_open(self, carriage_pass: Carriage_Pass) -> bool:
        """
        :param carriage_pass:
        :return: Return true if the given carriage_pass is in the set of open carriage passes.
        """
        return carriage_pass in self.open_carriage_passes

    def _receptive_carriage_passes(self, instruction: Needle_Instruction, carriage_passes: set[Carriage_Pass]) -> set[Carriage_Pass]:
        rack, all_needle = self.get_instruction_rack(instruction)
        return set(cp for cp in carriage_passes if cp.can_add_instruction(instruction, rack, all_needle))

    def _yarn_order_receptive_carriage_pass(self, instruction: Loop_Making_Instruction) -> Carriage_Pass | None:
        """
        :param instruction: A loop-making instruction that involves a yarn and can only be connect to a carriage pass with the prior loop in the yarn order.
        :return: None if no carriage pass can be extended by this loop forming instruction. Otherwise, return the only carriage pass that it can extend.
        """
        for pred in self.knitout_dependency_graph.predecessors(instruction):
            deps = self.knitout_dependency_generator.get_edge_dependencies(pred, instruction)
            if Knitout_Dependency.Yarn_Order in deps:
                if len(deps) > 1:  # Short-cut. The only allowed dependency within a carriage pass is a yarn-order dependency
                    return None
                else:
                    return self.instructions_to_carriage_pass[pred]  # Note, assumes all predecessors are already included in the carriage pass structure.
        return None

    def _dependency_free_carriage_passes(self, instruction: Needle_Instruction, carriage_passes: set[Carriage_Pass]) -> set[Carriage_Pass]:
        dep_free_cp = set()
        for cp in carriage_passes:
            preds_in_cp = cp.instruction_set().intersection(self.knitout_dependency_graph.predecessors(instruction))
            if len(preds_in_cp) == 0:  # No dependencies within this set.
                dep_free_cp.add(cp)
            elif len(preds_in_cp) == 1:  # Only one dependency, but this must only be a yarn-order dependency
                for pred in preds_in_cp:
                    deps = self.knitout_dependency_generator.get_edge_dependencies(pred, instruction)
                    if len(deps) == 1:
                        for dep in deps:
                            if dep is Knitout_Dependency.Yarn_Order:  # only a yarn-order dependency
                                dep_free_cp.add(cp)
        return dep_free_cp

    def cycle_free_carriage_passes(self, instruction: Needle_Instruction, carriage_passes: set[Carriage_Pass]) -> set[Carriage_Pass]:
        """

        :param instruction: The instruction to search for passes to.
        :param carriage_passes: The carriage passes to consider paths from.
            This operation is expensive per carriage pass. This set should be minimized by more cost-effective criteria.
        :return: The subset of carriage passes that have no path to this instruction.
            These passes will not create a cycle-dependency to this carriage pass
        """
        predecessor_cp = set(self.instructions_to_carriage_pass[pred] for pred in self.knitout_dependency_graph.predecessors(instruction))
        # Note: assumes that predecessors are already assigned to carriage pass
        cycle_free_cp = set()
        for cp in carriage_passes:
            no_paths = True
            for pred_cp in predecessor_cp:
                if cp != pred_cp and networkx.has_path(self.carriage_pass_dependency_graph, cp, pred_cp):
                    no_paths = False
                    break
            if no_paths:
                cycle_free_cp.add(cp)
        return cycle_free_cp

    def add_needle_instruction(self, instruction: Needle_Instruction):
        """
        Add an instruction from the knitout dependency graph to the carriage pass graph.
        This may form a new open carriage pass or be added to an existing open carriage pass.
        :param instruction: The instruction to add to the carriage passes.
        """
        mergable_cp = self.find_mergable_open_carriage_pass(instruction)
        if mergable_cp is None:
            self._new_carriage_pass(instruction)
        else:
            self.merge_into_carriage_pass(instruction, mergable_cp)
        if isinstance(instruction, Loop_Making_Instruction):
            self.close_yarn_order_carriage_passes(instruction)

    def add_outhook_instruction(self, instruction: Outhook_Instruction):
        """
        Add edges from current carriage passes to a given outhook instruction.
         Close any carriage passes that involve this yarn.
        :param instruction: The Outhook instruction to add to the carriage passes graph.
        """
        for predecessor in self.knitout_dependency_graph.predecessors(instruction):
            self.add_cp_dependency_edge(predecessor, instruction, {Knitout_Dependency.Yarn_Order})
            self.close_yarn_order_carriage_passes(instruction)

    def merge_into_carriage_pass(self, instruction: Needle_Instruction, cp: Carriage_Pass):
        """

        :param instruction:
        :param cp:
        """
        rack, all_needle = self.get_instruction_rack(instruction)
        added_to_cp = cp.add_instruction(instruction, rack, all_needle)
        assert added_to_cp, f"Cannot add {instruction} to {cp}."
        self._integrate_instruction_into_carriage_pass(cp, instruction)

    def _new_carriage_pass(self, instruction):
        rack, all_needle = self.get_instruction_rack(instruction)
        cp = Carriage_Pass(instruction, rack, all_needle)
        self.open_carriage_passes.add(cp)
        self.carriage_pass_dependency_graph.add_node(cp)
        self._integrate_instruction_into_carriage_pass(cp, instruction)

    def add_cp_dependency_edge(self, predecessor_instruction: Knitout_Line, successor_instruction: Knitout_Line, dependencies: set[Knitout_Dependency]):
        """
        :param dependencies: The dependencies between the instructions
        :param predecessor_instruction: The instruction that proceeds the successor instruction.
        :param successor_instruction: The successor instruction that follows the predecessor instruction.
        """
        predecessor = predecessor_instruction
        successor = successor_instruction
        if isinstance(predecessor_instruction, Needle_Instruction):
            predecessor = self.instructions_to_carriage_pass[predecessor_instruction]
        if isinstance(successor_instruction, Needle_Instruction):
            successor = self.instructions_to_carriage_pass[successor_instruction]
        if predecessor == successor:
            return
        if not self.carriage_pass_dependency_graph.has_edge(predecessor, successor):
            self.carriage_pass_dependency_graph.add_edge(predecessor, successor, edge_dependencies={(predecessor_instruction, successor_instruction): dependencies})
        else:
            edge_deps = self.carriage_pass_dependency_graph.edges[(predecessor, successor)]['edge_dependencies']
            if (predecessor_instruction, successor_instruction) not in edge_deps:
                edge_deps[(predecessor_instruction, successor_instruction)] = dependencies
            else:
                edge_deps[(predecessor_instruction, successor_instruction)].update(dependencies)

    def _integrate_instruction_into_carriage_pass(self, cp: Carriage_Pass, instruction: Needle_Instruction):
        self.instructions_to_carriage_pass[instruction] = cp
        for predecessor_instruction in self.knitout_dependency_graph.predecessors(instruction):
            dependencies = self.knitout_dependency_generator.get_edge_dependencies(predecessor_instruction, instruction)
            self.add_cp_dependency_edge(predecessor_instruction, instruction, dependencies)

    def close_yarn_order_carriage_passes(self, instruction: Loop_Making_Instruction | Outhook_Instruction):
        """
        Remove any open carriage passes that are completed by a new carriage pass with the same yarn.
        :param instruction: The instruction that would form a new carriage pass.
        """
        prior_yarn_order_instructions = [pred for pred in self.knitout_dependency_graph.predecessors(instruction)
                                         if Knitout_Dependency.Yarn_Order in self.knitout_dependency_generator.get_edge_dependencies(pred, instruction)]
        if instruction in self.instructions_to_carriage_pass:
            instruction_cp = self.instructions_to_carriage_pass[instruction]
            prior_yarn_order_cp = set(self.instructions_to_carriage_pass[pred] for pred in prior_yarn_order_instructions if pred not in instruction_cp)
            self.open_carriage_passes.difference_update(prior_yarn_order_cp)
        else:
            self.open_carriage_passes.difference_update(prior_yarn_order_instructions)

    def form_carriage_passes(self):
        """
            Forme the carriage passes in a greedy fashion from the original instruction set order.
        """
        for instruction in self.knitout_dependency_generator.original_instructions:
            if isinstance(instruction, Needle_Instruction):
                self.add_needle_instruction(instruction)
            elif isinstance(instruction, Outhook_Instruction):
                self.add_outhook_instruction(instruction)

    def add_machine_setting_dependencies_to_carriage_passes(self):
        """
            Evaluates the dependencies of instructions in each carriage pass and
             adds instructions that update the state of the machine to meet their requirements.
        """
        setting_injector: Machine_Setting_Injection = Machine_Setting_Injection(self.carriage_pass_dependency_graph)
        for setting, instruction in setting_injector.setting_dependency_graph.edges:
            dependencies = setting_injector.setting_dependency_graph.edges[(setting, instruction)]['dependencies']
            self.add_cp_dependency_edge(setting, instruction, dependencies)

    def find_execution_order(self, target_release_loop_count: int = 10) -> list[Knitout_Line]:
        """
        :param target_release_loop_count: The number of loops to try to achieve before each releasehook.
        This is a loose constraint and may not be met if other instructions require a release.
        :return: An optimized execution order based on a topological sort of the carriage pass dependencies.
        """
        self.add_machine_setting_dependencies_to_carriage_passes()
        machine_state: Knitting_Machine = Knitting_Machine()
        instructions = []
        next_release: Releasehook_Instruction | None = None

        def _loops_since_inhook() -> int | None:
            if machine_state.carrier_system.hooked_carrier is None:
                return None
            return len(machine_state.carrier_system.hooked_carrier.yarn)

        for instruction_set in networkx.topological_sort(self.carriage_pass_dependency_graph):
            if next_release is not None:
                if self.carriage_pass_dependency_graph.has_edge(next_release, instruction_set):
                    next_release.execute(machine_state)
                    instructions.append(next_release)
                    next_release = None
            if isinstance(instruction_set, Carriage_Pass):
                if (next_release is not None
                        and _loops_since_inhook() >= target_release_loop_count
                        and instruction_set.direction == machine_state.carrier_system.hook_input_direction):
                    next_release.execute(machine_state)
                    instructions.append(next_release)
                    next_release = None
                for instruction in instruction_set:
                    instruction.execute(machine_state)
                instructions.extend(instruction_set)
            elif isinstance(instruction_set, Releasehook_Instruction):
                next_release = instruction_set
            else:
                instruction_set.execute(machine_state)
                instructions.append(instruction_set)
        return instructions

    def write_optimized_execution_order(self, out_name: str, target_release_loop_count: int = 10):
        """

        :param out_name: The name of the output file for the optimized execution order.
        :param target_release_loop_count: The number of loops to try to achieve before each releasehook.
        This is a loose constraint and may not be met if other instructions require a release.
        """
        optimized_instructions = self.find_execution_order(target_release_loop_count)
        with open(out_name, 'w') as f:
            f.writelines([str(ln) for ln in optimized_instructions])

    def visualize(self):
        """
            Open a visualizer of the given carriage pass dependency graph for debugging utility.
        """
        visualizer = Carriage_Pass_Dependency_Viewer(self.carriage_pass_dependency_graph, self.knitout_dependency_graph, self.knitting_machine)
        visualizer.visualize()

    def __len__(self):
        return len(self.carriage_pass_dependency_graph.nodes)

    def __contains__(self, item: Knitout_Line) -> bool:
        return item in self.instructions_to_carriage_pass
