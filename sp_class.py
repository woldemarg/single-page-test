import copy
from typing import Any, Dict, Optional
import plotly.graph_objects as go


# %%


class ScatterPlot:
    def __init__(self,
                 initial_data: Dict[str, Any],
                 style: Dict[str, Any],
                 layout: Dict[str, Any]):
        self.initial_fig = go.Figure(layout=layout)
        self._add_trace(self.initial_fig, initial_data, style)
        self.updated_fig: Optional[go.Figure] = None

    @staticmethod
    def _add_trace(fig: go.Figure,
                   data: Dict[str, Any],
                   style: Dict[str, Any],
                   **kwargs) -> None:
        try:
            scatter_trace = go.Scatter(
                mode='markers',
                x=data['dates'],
                y=data['employee'],
                **style,
                **kwargs
            )
            fig.add_trace(scatter_trace)
        except KeyError as exc:
            raise ValueError("Invalid data input") from exc

    def update_plot(self,
                    data: Dict[str, Any],
                    style: Dict[str, Any],
                    **kwargs) -> None:
        self.updated_fig = copy.deepcopy(self.initial_fig)
        self._add_trace(self.updated_fig, data, style, **kwargs)

    @property
    def initial_figure(self) -> go.Figure:
        return self.initial_fig

    @property
    def updated_figure(self) -> go.Figure:
        return self.updated_fig or self.initial_figure
