"""Enumeration of knitout Dependencies."""
from enum import Enum


class Knitout_Dependency(Enum):
    """
    An enumeration of the dependency types between instructions that from a knitgraph on a virtual knitting machine.
    """
    Yarn_Order = "Order that loops are knit with carrier."
    Float_Position = "Order that creates an alignment of loops and floats"
    Stitch_Order = "Order that loops are stitched."
    Loop_Position = "Order that loops are positioned on needle bed."
    Wale_Crossing = "Order that crosses loops to form wale-braids."
    Active_Carrier = "Order requires active carrier."
    Free_Inserting_Hook = "Order requires free inserting hook."
    Racking_Alignment = "Order requires specified racking alignment."

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
