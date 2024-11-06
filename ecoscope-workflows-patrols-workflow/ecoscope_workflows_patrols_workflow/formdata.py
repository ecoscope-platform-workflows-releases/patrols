# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "07ffd4fc8e89019bbd0086333f0cbead53561801e3c1cd3bba81063c45abdb28"


from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, confloat


class WorkflowDetails(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(..., description="The name of your workflow", title="Name")
    description: str = Field(..., description="A description", title="Description")
    image_url: Optional[str] = Field("", description="An image url", title="Image Url")


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
    client: str = Field(
        ..., description="A named EarthRanger connection.", title="Client"
    )
    patrol_type: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Type"
    )


class PatrolTraj(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    min_length_meters: Optional[float] = Field(0.1, title="Min Length Meters")
    max_length_meters: Optional[float] = Field(10000, title="Max Length Meters")
    max_time_secs: Optional[float] = Field(3600, title="Max Time Secs")
    min_time_secs: Optional[float] = Field(1, title="Min Time Secs")
    max_speed_kmhr: Optional[float] = Field(120, title="Max Speed Kmhr")
    min_speed_kmhr: Optional[float] = Field(0.0, title="Min Speed Kmhr")


class FetchAndPreprocessPatrolObservations(BaseModel):
    patrol_obs: Optional[PatrolObs] = Field(
        None, title="Get Patrol Observations from EarthRanger"
    )
    patrol_traj: Optional[PatrolTraj] = Field(
        None, title="Transform Relocations to Trajectories"
    )


class PatrolEvents(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    client: str = Field(
        ..., description="A named EarthRanger connection.", title="Client"
    )
    patrol_type: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Type"
    )


class FetchAndPreprocessPatrolEvents(BaseModel):
    patrol_events: Optional[PatrolEvents] = Field(
        None, title="Get Patrol Events from EarthRanger"
    )


class TimeInterval(str, Enum):
    year = "year"
    month = "month"
    week = "week"
    day = "day"
    hour = "hour"


class Td(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    max_speed_factor: Optional[float] = Field(1.05, title="Max Speed Factor")
    expansion_factor: Optional[float] = Field(1.3, title="Expansion Factor")


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


class LegendDefinition(BaseModel):
    label_column: Optional[str] = Field(None, title="Label Column")
    color_column: Optional[str] = Field(None, title="Color Column")
    labels: Optional[List[str]] = Field(None, title="Labels")
    colors: Optional[List[str]] = Field(None, title="Colors")


class Placement(str, Enum):
    top_left = "top-left"
    top_right = "top-right"
    bottom_left = "bottom-left"
    bottom_right = "bottom-right"
    fill = "fill"


class LegendStyle(BaseModel):
    placement: Optional[Placement] = Field("bottom-right", title="Placement")


class NorthArrowStyle(BaseModel):
    placement: Optional[Placement] = Field("top-left", title="Placement")
    style: Optional[Dict[str, Any]] = Field({"transform": "scale(0.8)"}, title="Style")


class LineWidthUnits(str, Enum):
    meters = "meters"
    pixels = "pixels"


class RadiusUnits(str, Enum):
    meters = "meters"
    pixels = "pixels"


class PointLayerStyle(BaseModel):
    filled: Optional[bool] = Field(True, title="Filled")
    get_fill_color: Optional[str] = Field(None, title="Get Fill Color")
    get_line_color: Optional[str] = Field(None, title="Get Line Color")
    get_line_width: Optional[float] = Field(1, title="Get Line Width")
    fill_color_column: Optional[str] = Field(None, title="Fill Color Column")
    line_width_units: Optional[LineWidthUnits] = Field(
        "pixels", title="Line Width Units"
    )
    get_radius: Optional[float] = Field(5, title="Get Radius")
    radius_units: Optional[RadiusUnits] = Field("pixels", title="Radius Units")


class PolygonLayerStyle(BaseModel):
    filled: Optional[bool] = Field(True, title="Filled")
    get_fill_color: Optional[str] = Field(None, title="Get Fill Color")
    get_line_color: Optional[str] = Field(None, title="Get Line Color")
    get_line_width: Optional[float] = Field(1, title="Get Line Width")
    fill_color_column: Optional[str] = Field(None, title="Fill Color Column")
    line_width_units: Optional[LineWidthUnits] = Field(
        "pixels", title="Line Width Units"
    )
    extruded: Optional[bool] = Field(False, title="Extruded")
    get_elevation: Optional[float] = Field(1000, title="Get Elevation")


class PolylineLayerStyle(BaseModel):
    pass


class TileLayer(BaseModel):
    name: str = Field(..., title="Name")
    opacity: Optional[float] = Field(1, title="Opacity")


class Unit(str, Enum):
    m = "m"
    km = "km"
    s = "s"
    h = "h"
    d = "d"
    m_s = "m/s"
    km_h = "km/h"


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


class TrajPatrolEventsEcomap(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    tile_layers: Optional[List[TileLayer]] = Field(
        [],
        description="A list of named tile layer with opacity, ie OpenStreetMap.",
        title="Tile Layers",
    )
    north_arrow_style: Optional[NorthArrowStyle] = Field(
        default_factory=lambda: NorthArrowStyle.model_validate(
            {"placement": "top-left", "style": {"transform": "scale(0.8)"}}
        ),
        description="Additional arguments for configuring the North Arrow.",
        title="North Arrow Style",
    )
    legend_style: Optional[LegendStyle] = Field(
        default_factory=lambda: LegendStyle.model_validate(
            {"placement": "bottom-right"}
        ),
        description="Additional arguments for configuring the legend.",
        title="Legend Style",
    )


class PatrolEventsAndTrajectoriesMap(BaseModel):
    traj_patrol_events_ecomap: Optional[TrajPatrolEventsEcomap] = Field(
        None, title="Draw Ecomaps for each combined Trajectory and Patrol Events group"
    )


class TotalPatrolTimeConverted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    original_unit: Optional[Unit] = Field(
        None, description="The original unit of measurement.", title="Original Unit"
    )
    new_unit: Optional[Unit] = Field(
        None, description="The unit to convert to.", title="New Unit"
    )


class TotalPatrolDistConverted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    original_unit: Optional[Unit] = Field(
        None, description="The original unit of measurement.", title="Original Unit"
    )
    new_unit: Optional[Unit] = Field(
        None, description="The unit to convert to.", title="New Unit"
    )


class AverageSpeedConverted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    original_unit: Optional[Unit] = Field(
        None, description="The original unit of measurement.", title="Original Unit"
    )
    new_unit: Optional[Unit] = Field(
        None, description="The unit to convert to.", title="New Unit"
    )


class MaxSpeedConverted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    original_unit: Optional[Unit] = Field(
        None, description="The original unit of measurement.", title="Original Unit"
    )
    new_unit: Optional[Unit] = Field(
        None, description="The unit to convert to.", title="New Unit"
    )


class PatrolSummaryStatistics(BaseModel):
    total_patrol_time_converted: Optional[TotalPatrolTimeConverted] = Field(
        None, title="Convert total patrol time units"
    )
    total_patrol_dist_converted: Optional[TotalPatrolDistConverted] = Field(
        None, title="Convert total patrol distance units"
    )
    average_speed_converted: Optional[AverageSpeedConverted] = Field(
        None, title="Convert Average Speed units"
    )
    max_speed_converted: Optional[MaxSpeedConverted] = Field(
        None, title="Convert Max Speed units"
    )


class TdEcomap(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    north_arrow_style: Optional[NorthArrowStyle] = Field(
        default_factory=lambda: NorthArrowStyle.model_validate(
            {"placement": "top-left", "style": {"transform": "scale(0.8)"}}
        ),
        description="Additional arguments for configuring the North Arrow.",
        title="North Arrow Style",
    )
    legend_style: Optional[LegendStyle] = Field(
        default_factory=lambda: LegendStyle.model_validate(
            {"placement": "bottom-right"}
        ),
        description="Additional arguments for configuring the legend.",
        title="Legend Style",
    )


class TimeDensityMap(BaseModel):
    td: Optional[Td] = Field(None, title="Calculate Time Density from Trajectory")
    td_ecomap: Optional[TdEcomap] = Field(None, title="Draw Ecomap from Time Density")


class LayerDefinition(BaseModel):
    geodataframe: Any = Field(..., title="Geodataframe")
    layer_style: Union[PolylineLayerStyle, PointLayerStyle, PolygonLayerStyle] = Field(
        ..., title="Layer Style"
    )
    legend: LegendDefinition


class GroupedPlotStyle(BaseModel):
    category: str = Field(..., title="Category")
    plot_style: PlotCategoryStyle


class PatrolEventsBarChart1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    time_interval: TimeInterval = Field(
        ..., description="Sets the time interval of the x axis.", title="Time Interval"
    )
    grouped_styles: Optional[List[GroupedPlotStyle]] = Field(
        [],
        description="Style arguments passed to plotly.graph_objects.Bar and applied to individual groups.",
        title="Grouped Styles",
    )


class PatrolEventsBarChart(BaseModel):
    patrol_events_bar_chart: Optional[PatrolEventsBarChart1] = Field(
        None, title="Draw Time Series Bar Chart for Patrols Events"
    )


class FormData(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    workflow_details: Optional[WorkflowDetails] = Field(
        None, title="Set Workflow Details"
    )
    groupers: Optional[Groupers] = Field(None, title="Set Groupers")
    time_range: Optional[TimeRange] = Field(None, title="Set Time Range Filter")
    Fetch_and_preprocess_patrol_observations: Optional[
        FetchAndPreprocessPatrolObservations
    ] = Field(
        None,
        alias="Fetch and preprocess patrol observations",
        description="Fetch patrol observations from EarthRanger, preprocess them into trajectories, and add a temporal index.",
    )
    Fetch_and_preprocess_patrol_events: Optional[FetchAndPreprocessPatrolEvents] = (
        Field(
            None,
            alias="Fetch and preprocess patrol events",
            description="Fetch patrol events from EarthRanger, filter them, and add a temporal index.",
        )
    )
    Patrol_Events_and_Trajectories_Map: Optional[PatrolEventsAndTrajectoriesMap] = (
        Field(
            None,
            alias="Patrol Events and Trajectories Map",
            description="Create a combined patrol trajectories and events map.",
        )
    )
    Patrol_Summary_Statistics: Optional[PatrolSummaryStatistics] = Field(
        None,
        alias="Patrol Summary Statistics",
        description="Create a single value widget for various patrol statistics.",
    )
    Patrol_events_bar_chart: Optional[PatrolEventsBarChart] = Field(
        None,
        alias="Patrol events bar chart",
        description="Create the patrol events bar chart.",
    )
    Time_Density_Map: Optional[TimeDensityMap] = Field(
        None,
        alias="Time Density Map",
        description="Calculate time density from patrol trajectories and display it on a map.",
    )
