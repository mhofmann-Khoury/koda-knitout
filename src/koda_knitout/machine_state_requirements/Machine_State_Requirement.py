"""Module defining common requirements to executed a knitout operation."""
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import Yarn_Carrier_Instruction, Releasehook_Instruction, Outhook_Instruction, Inhook_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier

from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency


class Machine_State_Requirement:
    """
    Superclass for a requirement on the machine state needed to execute a given operation.
    """

    def __init__(self, requiring_operation: Knitout_Line, dependency_type: Knitout_Dependency):
        self._dependency_type = dependency_type
        self.requiring_operation: Knitout_Line = requiring_operation

    @property
    def dependency_type(self) -> Knitout_Dependency:
        """
        :return: The type of dependency managed by this Machine_State_Requirement.
        """
        return self._dependency_type

    @property
    def carrier_ids(self) -> list[int]:
        """
        :return: List of carrier ids involved in the required operation.
        """
        if isinstance(self.requiring_operation, Yarn_Carrier_Instruction):
            return [self.requiring_operation.carrier_id]
        elif isinstance(self.requiring_operation, Needle_Instruction):
            if self.requiring_operation.carrier_set is None:
                return []
            return self.requiring_operation.carrier_set.carrier_ids
        return []

    def get_needle(self, machine_state: Knitting_Machine) -> None | Needle:
        """
        :param machine_state:
        :return: The needle in the given machine state that interacts with this operation.
         None if no needle interacts with the requiring operation.
        """
        if isinstance(self.requiring_operation, Needle_Instruction):
            return machine_state[self.requiring_operation.needle]
        else:
            return None

    def receiving_needle(self, machine_state: Knitting_Machine) -> None | Needle:
        """
        :param machine_state:
        :return: The needle that receives a transfer in the given machine state. None if there is no transfer.
        """
        if self.has_second_needle:
            assert isinstance(self.requiring_operation, Needle_Instruction)
            return machine_state[self.requiring_operation.needle_2]
        else:
            return None

    @property
    def has_second_needle(self) -> bool:
        """
        :return: True if this operation has a transfer receiving second needle.
        """
        return isinstance(self.requiring_operation, Needle_Instruction) and self.requiring_operation.has_second_needle

    def get_carriers(self, machine_state: Knitting_Machine) -> list[Yarn_Carrier]:
        """
        :param machine_state:
        :return: The set of carriers required from the given machine state.
        """
        if isinstance(self.requiring_operation, Needle_Instruction):
            return list(self.requiring_operation.get_carriers(machine_state).values())
        else:
            assert isinstance(self.requiring_operation, Yarn_Carrier_Instruction)
            return [self.requiring_operation.get_carrier(machine_state)]

    def is_satisfied(self, machine_state: Knitting_Machine) -> bool:
        """
        :param machine_state:
        :return: True if the Machine State requirement is satisfied for the given machine state.
        """
        return False

    def satisfying_instructions(self, machine_state: Knitting_Machine) -> dict[Knitout_Line, bool]:
        """
        :param machine_state:
        :return: A dictionary of knitout instructions keyed to a boolean
         which is True if the instruction is already satisfied.
        """
        return {}


class Active_Yarn_Requirement(Machine_State_Requirement):

    def __init__(self, requiring_operation: Needle_Instruction | Releasehook_Instruction | Outhook_Instruction):
        super().__init__(requiring_operation, Knitout_Dependency.Active_Carrier)

    def is_satisfied(self, machine_state: Knitting_Machine) -> bool:
        return machine_state.carrier_system.is_active(list(int(c) for c in self.get_carriers(machine_state)))

    def satisfying_instructions(self, machine_state: Knitting_Machine) -> dict[Inhook_Instruction, bool]:
        active_carrier_ids = {c.carrier_id for c in machine_state.carrier_system.active_carriers}
        return {Inhook_Instruction(c, f"Inhook {c} for {self.requiring_operation}"):
                    c in active_carrier_ids
                for c in self.carrier_ids}


class Hooked_Yarn_Requirement(Active_Yarn_Requirement):
    def __init__(self, requiring_operation: Releasehook_Instruction):
        super().__init__(requiring_operation)

    def is_satisfied(self, machine_state: Knitting_Machine) -> bool:
        return machine_state.carrier_system.hooked_carrier == self.get_carriers(machine_state)[0]

    def satisfying_instructions(self, machine_state: Knitting_Machine) -> dict[Inhook_Instruction, bool]:
        return {Inhook_Instruction(c, f"Inhook {c} for {self.requiring_operation}"):
                    c == machine_state.carrier_system.hooked_carrier.carrier_id
                for c in self.carrier_ids}


class Free_Hook_Requirement(Machine_State_Requirement):
    def __init__(self, requiring_operation: Yarn_Carrier_Instruction | Needle_Instruction):
        super().__init__(requiring_operation, Knitout_Dependency.Free_Inserting_Hook)

    def is_satisfied(self, machine_state: Knitting_Machine) -> bool:
        if isinstance(self.requiring_operation, Yarn_Carrier_Instruction) or self.has_second_needle:
            return machine_state.carrier_system.inserting_hook_available
        else:
            assert isinstance(self.requiring_operation, Needle_Instruction)
            if machine_state.carrier_system.searching_for_position:  # this operation will provide an inserting hook location.
                return True
            return not machine_state.carrier_system.conflicts_with_inserting_hook(self.get_needle(machine_state),
                                                                                  self.requiring_operation.direction)

    def satisfying_instructions(self, machine_state: Knitting_Machine) -> dict[Releasehook_Instruction, bool]:
        if machine_state.carrier_system.inserting_hook_available:
            return {Releasehook_Instruction(2, f"Release not required"): True}
        else:
            return {Releasehook_Instruction(machine_state.carrier_system.hooked_carrier,
                                            f"Release required for {self.requiring_operation}"): self.is_satisfied(machine_state)}


class Racking_Requirement(Machine_State_Requirement):

    def __init__(self, requiring_operation: Needle_Instruction, rack_value: int, all_needle_rack: bool):
        super().__init__(requiring_operation, Knitout_Dependency.Racking_Alignment)
        self.all_needle_rack: bool = all_needle_rack
        self.rack_value: int = rack_value

    def is_satisfied(self, machine_state: Knitting_Machine) -> bool:
        return self.rack_value == machine_state.rack and self.all_needle_rack == machine_state.all_needle_rack

    def satisfying_instructions(self, machine_state: Knitting_Machine) -> dict[Rack_Instruction, bool]:
        return {Rack_Instruction.rack_instruction_from_int_specification(self.rack_value,
                                                                         self.all_needle_rack,
                                                                         f"Rack required for {self.requiring_operation}"):
                    self.is_satisfied(machine_state)}


def needle_operation_requirements(needle_op: Needle_Instruction, rack_value: int, all_needle_rack: bool) -> list[Machine_State_Requirement]:
    """

    :param needle_op: The needle operation to be executed.
    :param rack_value: The racking operation will be executed at.
    :param all_needle_rack: The all needle racking condition the operation will be executed at.
    :return: The list of requirements required for the given needle operation.
    """
    return [Active_Yarn_Requirement(needle_op), Free_Hook_Requirement(needle_op),
            Racking_Requirement(needle_op, rack_value, all_needle_rack)]


def inhook_requirements(inhook_op: Inhook_Instruction) -> list[Machine_State_Requirement]:
    """
    :param inhook_op:
    :return: The list of requirements for the given inhook operation.
    """
    return [Free_Hook_Requirement(inhook_op)]


def release_requirements(release_op: Releasehook_Instruction) -> list[Machine_State_Requirement]:
    """

    :param release_op:
    :return: The list of requirements required for the given releasehook operation.
    """
    return [Active_Yarn_Requirement(release_op), Hooked_Yarn_Requirement(release_op)]


def outhook_requirements(outhook_op: Outhook_Instruction) -> list[Machine_State_Requirement]:
    """

    :param outhook_op:
    :return: The list of requirements required for the given outhook operation.
    """
    return [Active_Yarn_Requirement(outhook_op), Free_Hook_Requirement(outhook_op)]


def get_requirements(instruction: Knitout_Line, rack: int = 0, all_needle_rack: bool = False) -> list[Machine_State_Requirement]:
    """
    :param instruction:
    :param rack: Defaults to 0. Must be provided for needle instructions.
    :param all_needle_rack: Defaults to False. Must be provided for needle conditions.
    :return: The set of requirements for a given instruction depending on the instruction type.
    """
    if isinstance(instruction, Needle_Instruction):
        return needle_operation_requirements(instruction, rack, all_needle_rack)
    elif isinstance(instruction, Releasehook_Instruction):
        return release_requirements(instruction)
    elif isinstance(instruction, Outhook_Instruction):
        return outhook_requirements(instruction)
    elif isinstance(instruction, Inhook_Instruction):
        return inhook_requirements(instruction)
    else:
        return []
