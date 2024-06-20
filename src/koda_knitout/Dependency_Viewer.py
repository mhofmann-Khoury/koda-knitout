"""Module containing the Dependency Viewer class."""
import math

import networkx
import plotly.graph_objects as go
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.carrier_instructions import Yarn_Carrier_Instruction
from knitout_interpreter.knitout_operations.needle_instructions import Needle_Instruction, Loop_Making_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_constructed_knit_graph.Machine_Knit_Yarn import Machine_Knit_Yarn

from koda_knitout.knitout_dependencies.knitout_depenendencies import Knitout_Dependency


class Dependency_Viewer:
    """
    A class that manages a viewer of the dependencies between knitting instructions.
    """

    def __init__(self, dependency_graph: networkx.DiGraph, knitting_machine: Knitting_Machine):
        self.knitting_machine: Knitting_Machine = knitting_machine
        self.dependency_graph: networkx.DiGraph = dependency_graph
        self.data_graph: networkx.DiGraph = networkx.DiGraph()
        self.dependencies: dict[Knitout_Dependency, set[tuple[Knitout_Line, Knitout_Line]]] = {dep: set() for dep in Knitout_Dependency}
        self._min_needle_position: float = math.inf
        self._max_needle_position: float = 0.0
        self._carrier_ops_to_place: dict[int, dict[Knitout_Line, float]] = {cid: {} for cid in self.knitting_machine.carrier_system.carrier_ids}

    def _update_needle_range(self, instruction: Needle_Instruction):
        self._max_needle_position = max(self._max_needle_position, instruction.needle.position)
        self._min_needle_position = min(self._min_needle_position, instruction.needle.position)

    def _add_carrier_op(self, carrier_op: Yarn_Carrier_Instruction, y: float):
        self._carrier_ops_to_place[carrier_op.carrier_id][carrier_op] = y

    def _place_carrier_ops(self):
        for cid, instruction_map in self._carrier_ops_to_place.items():
            for instruction, y in instruction_map.items():
                self.data_graph.add_node(instruction, x=self._max_needle_position + cid, y=y)

    def _plot_instructions(self):
        pass

    def _plot_dependencies(self):
        pass

    def _trace_instruction_nodes(self):
        def _node_trace():
            return dict(x=[], y=[], instruction=[])

        instruction_data = _node_trace()

        carrier_instruction_data: dict[Machine_Knit_Yarn, dict] = {}

        def _add_by_yarn(y: Machine_Knit_Yarn, op: Knitout_Line):
            if y not in carrier_instruction_data:
                carrier_instruction_data[y] = _node_trace()
            carrier_instruction_data[y]['x'].append(self.data_graph.nodes[op]['x'])
            carrier_instruction_data[y]['y'].append(self.data_graph.nodes[op]['y'])
            carrier_instruction_data[y]['instruction'].append(str(op))

        for instruction in self.data_graph.nodes:
            if isinstance(instruction, Loop_Making_Instruction):
                for yarn in instruction.get_yarns(self.knitting_machine).values():
                    _add_by_yarn(yarn, instruction)
            elif isinstance(instruction, Yarn_Carrier_Instruction):
                _add_by_yarn(instruction.get_yarn(self.knitting_machine), instruction)
            else:
                instruction_data['x'].append(self.data_graph.nodes[instruction]['x'])
                instruction_data['y'].append(self.data_graph.nodes[instruction]['y'])
                instruction_data['instruction'].append(str(instruction))

        instruction_traces = [
            go.Scatter(name=f"Instructions", x=instruction_data['x'],
                       y=instruction_data['y'],
                       text=instruction_data['instruction'],
                       textposition='top center',
                       mode='markers+text',
                       marker=dict(
                           # size=90,
                           symbol=101,  # square-open
                           color='black',
                           line=dict(color='black', width=3)
                       ))]
        for yarn, data in carrier_instruction_data.items():
            instruction_traces.append(
                go.Scatter(name=f"Carrier {yarn} Instructions", x=data['x'],
                           y=data['y'],
                           text=data['instruction'],
                           textposition='top center',
                           mode='markers+text',
                           marker=dict(
                               # size=90,
                               symbol=101,  # square-open
                               color=yarn.properties.color,
                               line=dict(color=yarn.properties.color, width=3)
                           )))
        return instruction_traces

    def _trace_dependencies(self):
        traces = []

        def _new_edge_data():
            return {'x': [], 'y': [], 'edge': [], 'is_start': []}

        def _add_edge_data(e_data: dict[str, list], prior_instruction: Knitout_Line, next_instruction: Knitout_Line):
            e_data['x'].append(self.data_graph.nodes[prior_instruction]['x'])
            e_data['y'].append(self.data_graph.nodes[prior_instruction]['y'])
            e_data['edge'].append((prior_instruction, next_instruction))
            e_data['is_start'].append(True)
            e_data['x'].append(self.data_graph.nodes[next_instruction]['x'])
            e_data['y'].append(self.data_graph.nodes[next_instruction]['y'])
            e_data['edge'].append((prior_instruction, next_instruction))
            e_data['is_start'].append(False)
            e_data['x'].append(None)
            e_data['y'].append(None)

        def _add_trace(dependency_edges, color='black'):
            edge_data = _new_edge_data()
            for prior, follower in dependency_edges:
                _add_edge_data(edge_data, prior, follower)
            traces.append(go.Scatter(name=dependency.name,
                                     x=edge_data['x'], y=edge_data['y'],
                                     line=dict(width=2, color=color, dash='solid'),
                                     mode='lines+markers',
                                     marker=dict(
                                         size=15,
                                         symbol='arrow-bar-up',
                                         angleref='previous'
                                     )
                                     )
                          )

        for dependency, edges in self.dependencies.items():
            if len(edges) == 0:
                continue
            if dependency is Knitout_Dependency.Yarn_Order:
                yarns_to_edges: dict[Machine_Knit_Yarn, list] = {}
                for u, v in edges:
                    assert isinstance(u, Loop_Making_Instruction), f"Yarn order edges should start with loop creation but got {u}->{v}."
                    for yarn in u.get_yarns(self.knitting_machine).values():
                        if yarn not in yarns_to_edges:
                            yarns_to_edges[yarn] = []
                        yarns_to_edges[yarn].append((u, v))
                for yarn, yarn_edges in yarns_to_edges.items():
                    _add_trace(yarn_edges, color=yarn.properties.color)
            else:
                _add_trace(edges)
        return traces

    def visualize(self):
        """
            Open a visualizer of the given dependency graph for debugging utility.
        """
        self._plot_instructions()
        self._plot_dependencies()
        figure_traces = self._trace_instruction_nodes()
        figure_traces.extend(self._trace_dependencies())
        go_layout = go.Layout(title="Knitout Process Visualization",
                              showlegend=True,
                              hovermode='closest',
                              margin=dict(b=20, l=5, r=5, t=40)
                              )
        fig = go.Figure(data=figure_traces, layout=go_layout)
        fig.show()
