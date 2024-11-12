# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "ed1d2e93ff19b75dd7db3b34b5cd4b464a1138bca7d7a8c5607da03ddeb385de"


from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, confloat


class WorkflowDetails(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(..., description="The name of your workflow", title="Name")
    description: str = Field(..., description="A description", title="Description")
    image_url: Optional[str] = Field("", description="An image url", title="Image Url")


class ErClientName(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    EcoscopeWorkflowsNamedConnection: str = Field(
        ..., description="A named connection.", title="Name"
    )


class TimeRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    since: AwareDatetime = Field(..., description="The start time", title="Since")
    until: AwareDatetime = Field(..., description="The end time", title="Until")


class PatrolObs(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    patrol_type: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Type"
    )


class PatrolTraj(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    max_length_meters: Optional[float] = Field(10000, title="Max Length Meters")
    max_time_secs: Optional[float] = Field(3600, title="Max Time Secs")
    max_speed_kmhr: Optional[float] = Field(120, title="Max Speed Kmhr")


class PatrolEvents(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    patrol_type: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Type"
    )


class TimeInterval(str, Enum):
    year = "year"
    month = "month"
    week = "week"
    day = "day"
    hour = "hour"


class PatrolEventsBarChart(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    time_interval: TimeInterval = Field(
        ..., description="Sets the time interval of the x axis.", title="Time Interval"
    )


class Grouper(BaseModel):
    index_name: str = Field(..., title="Index Name")


class Directive(str, Enum):
    field_a = "%a"
    field_A = "%A"
    field_b = "%b"
    field_B = "%B"
    field_c = "%c"
    field_d = "%d"
    field_f = "%f"
    field_H = "%H"
    field_I = "%I"
    field_j = "%j"
    field_m = "%m"
    field_M = "%M"
    field_p = "%p"
    field_S = "%S"
    field_U = "%U"
    field_w = "%w"
    field_W = "%W"
    field_x = "%x"
    field_X = "%X"
    field_y = "%y"
    field_Y = "%Y"
    field_z = "%z"
    field__ = "%%"


class TemporalGrouper(BaseModel):
    index_name: str = Field(..., title="Index Name")
    directive: Directive = Field(..., title="Directive")


class TimeRange1(BaseModel):
    since: AwareDatetime = Field(..., title="Since")
    until: AwareDatetime = Field(..., title="Until")
    time_format: Optional[str] = Field("%d %b %Y %H:%M:%S %Z", title="Time Format")


class BarLayoutStyle(BaseModel):
    font_color: Optional[str] = Field(None, title="Font Color")
    font_style: Optional[str] = Field(None, title="Font Style")
    plot_bgcolor: Optional[str] = Field(None, title="Plot Bgcolor")
    showlegend: Optional[bool] = Field(None, title="Showlegend")
    bargap: Optional[confloat(ge=0.0, le=1.0)] = Field(None, title="Bargap")
    bargroupgap: Optional[confloat(ge=0.0, le=1.0)] = Field(None, title="Bargroupgap")


class LineStyle(BaseModel):
    color: Optional[str] = Field(None, title="Color")


class PlotCategoryStyle(BaseModel):
    marker_color: Optional[str] = Field(None, title="Marker Color")


class PlotStyle(BaseModel):
    xperiodalignment: Optional[str] = Field(None, title="Xperiodalignment")
    marker_colors: Optional[List[str]] = Field(None, title="Marker Colors")
    textinfo: Optional[str] = Field(None, title="Textinfo")
    line: Optional[LineStyle] = Field(None, title="Line")


class Groupers(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    groupers: List[Union[Grouper, TemporalGrouper]] = Field(
        ...,
        description="            Index(es) and/or column(s) to group by, along with\n            optional display names and help text.\n            ",
        title="Groupers",
    )


class Params(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    workflow_details: Optional[WorkflowDetails] = Field(
        None, title="Set Workflow Details"
    )
    er_client_name: Optional[ErClientName] = Field(
        None, title="Select EarthRanger Connection"
    )
    groupers: Optional[Groupers] = Field(None, title="Set Groupers")
    time_range: Optional[TimeRange] = Field(None, title="Set Time Range Filter")
    patrol_obs: Optional[PatrolObs] = Field(
        None, title="Get Patrol Observations from EarthRanger"
    )
    patrol_traj: Optional[PatrolTraj] = Field(
        None, title="Transform Relocations to Trajectories"
    )
    patrol_events: Optional[PatrolEvents] = Field(
        None, title="Get Patrol Events from EarthRanger"
    )
    patrol_events_bar_chart: Optional[PatrolEventsBarChart] = Field(
        None, title="Draw Time Series Bar Chart for Patrols Events"
    )


class GroupedPlotStyle(BaseModel):
    category: str = Field(..., title="Category")
    plot_style: PlotCategoryStyle
