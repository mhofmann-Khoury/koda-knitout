"""Module containing the Machine Setting Injection class."""
import networkx
from knitout_interpreter.knitout_execution_structures.Carriage_Pass import Carriage_Pass
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import Inhook_Instruction, Releasehook_Instruction, Outhook_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency
from koda_knitout.machine_state_requirements.Machine_State_Requirement import get_requirements


class Machine_Setting_Injection:
    """
        Class to manage injection of knitting machine setting operations to manage required state for carriage passes.
    """

    def __init__(self, carriage_pass_dependencies: networkx.DiGraph):
        self.carriage_pass_dependencies: networkx.DiGraph = carriage_pass_dependencies
        self.knitting_machine: Knitting_Machine = Knitting_Machine()
        self.setting_dependency_graph: networkx.DiGraph = networkx.DiGraph()
        self.last_inhook_by_carrier_id: dict[int, Inhook_Instruction | None] = {cid: None for cid in self.knitting_machine.carrier_system.carrier_ids}
        self.last_release_hook: None | Releasehook_Instruction = None
        self.last_rack: Rack_Instruction = Rack_Instruction(0.0)
        self.last_instruction_at_rack: Needle_Instruction | None = None
        self.add_machine_settings()

    def add_machine_settings(self):
        """
            Injects the required instructions to maintain the knitting machine state for each carriage pass.
        """
        for generation in networkx.topological_generations(self.carriage_pass_dependencies):
            for instruction_set in generation:
                if isinstance(instruction_set, Carriage_Pass):
                    for instruction in instruction_set:
                        self._add_instruction_requirements(instruction, instruction_set.rack, instruction_set.all_needle_rack)
                else:
                    assert isinstance(instruction_set, Knitout_Line)
                    self._add_instruction_requirements(instruction_set)

    def _add_setting_dependency(self, prior_instruction: Knitout_Line, next_instruction: Knitout_Line, dependency: Knitout_Dependency, **kwargs):
        """
        Adds a dependency from the prior_instruction to the next_instruction.
        Marks it with the given dependency type.
        :param prior_instruction: The instruction that must proceed next_instruction.
        :param next_instruction: The instruction that must succeed prior_instruction.
        :param dependency: The type of dependency that connects these instructions.
        """
        if self.setting_dependency_graph.has_edge(prior_instruction, next_instruction):
            self.setting_dependency_graph.edges[(prior_instruction, next_instruction)]['dependencies'].add(dependency)
            for k, v in kwargs.items():
                self.setting_dependency_graph.edges[(prior_instruction, next_instruction)][k] = v
        else:
            self.setting_dependency_graph.add_edge(prior_instruction, next_instruction, dependencies={dependency}, **kwargs)

    def _update_prior_dependencies(self, instruction: Knitout_Line):
        if isinstance(instruction, Inhook_Instruction):
            self.last_inhook_by_carrier_id[instruction.carrier_id] = instruction
        elif isinstance(instruction, Releasehook_Instruction):
            self.last_release_hook = instruction
        elif isinstance(instruction, Rack_Instruction):
            if self.last_instruction_at_rack is not None:
                self._add_setting_dependency(self.last_instruction_at_rack, instruction, Knitout_Dependency.Racking_Alignment)
            self.last_instruction_at_rack = None
            self.last_rack = instruction

    def _add_instruction_requirements(self, instruction: Knitout_Line, rack: int = 0, all_needle_rack: bool = False):
        """
        Identify the required instructions to execute the given instruction at the specified racking.
        :param instruction:
        :param rack: Defaults to 0 but required from a carriage pass.
        :param all_needle_rack: Defaults to False, but required from a carriage pass.
        """
        requirements = get_requirements(instruction, rack, all_needle_rack)
        for requirement in requirements:
            satisfying_instructions = requirement.satisfying_instructions(self.knitting_machine)
            for satisfying_instruction, is_satisfied in satisfying_instructions.items():
                if not is_satisfied:
                    self._add_instruction_requirements(satisfying_instruction)
                    self._add_setting_dependency(satisfying_instruction, instruction, requirement.dependency_type)
                    self._update_prior_dependencies(satisfying_instruction)
                    if isinstance(satisfying_instruction, Rack_Instruction):
                        self.last_instruction_at_rack = instruction
                else:
                    if isinstance(satisfying_instruction, Inhook_Instruction):
                        assert self.last_inhook_by_carrier_id[satisfying_instruction.carrier_id] is not None
                        self._add_setting_dependency(self.last_inhook_by_carrier_id[satisfying_instruction.carrier_id], instruction,
                                                     dependency=requirement.dependency_type)
                    elif isinstance(satisfying_instruction, Releasehook_Instruction) and self.last_release_hook is not None:
                        self._add_setting_dependency(self.last_release_hook, instruction,
                                                     dependency=requirement.dependency_type)
                    elif isinstance(satisfying_instruction, Rack_Instruction):
                        self._add_setting_dependency(self.last_rack, instruction,
                                                     dependency=requirement.dependency_type)
                        self.last_instruction_at_rack = instruction

        instruction.execute(self.knitting_machine)

    def _add_final_outhooks(self):
        for carrier in self.knitting_machine.carrier_system.active_carriers:
            outhook = Outhook_Instruction(carrier)
            self._add_instruction_requirements(outhook)
