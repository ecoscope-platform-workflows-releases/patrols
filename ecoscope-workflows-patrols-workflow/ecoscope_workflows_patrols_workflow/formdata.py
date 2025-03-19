# AUTOGENERATED BY ECOSCOPE-WORKFLOWS; see fingerprint in README.md for details


from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class WorkflowDetails(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(..., title="Workflow Name")
    description: Optional[str] = Field("", title="Workflow Description")


class TimeRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    since: AwareDatetime = Field(..., description="The start time", title="Since")
    until: AwareDatetime = Field(..., description="The end time", title="Until")


class ErPatrolTypes(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    patrol_types: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Types"
    )


class StatusEnum(str, Enum):
    active = "active"
    overdue = "overdue"
    done = "done"
    cancelled = "cancelled"


class ErPatrolStatus(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    status: Optional[List[StatusEnum]] = Field(
        None,
        description="List comprised of 'active'/'overdue'/'done'/'cancelled'",
        title="Status",
    )


class PatrolEvents(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    event_type: List[str] = Field(
        ..., description="List of event types by name", title="Event Types"
    )
    drop_null_geometry: Optional[bool] = Field(
        False,
        description="Whether or not to keep events with no geometry data",
        title="Drop Null Geometry",
    )


class PatrolAndEventTypes(BaseModel):
    er_patrol_types: Optional[ErPatrolTypes] = Field(None, title="")
    er_patrol_status: Optional[ErPatrolStatus] = Field(None, title="")
    patrol_events: Optional[PatrolEvents] = Field(None, title="")


class TimeInterval(str, Enum):
    year = "year"
    month = "month"
    week = "week"
    day = "day"
    hour = "hour"


class PatrolEventsBarChart1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    time_interval: TimeInterval = Field(
        ..., description="Sets the time interval of the x axis.", title="Time Interval"
    )


class PatrolEventsBarChart(BaseModel):
    patrol_events_bar_chart: Optional[PatrolEventsBarChart1] = Field(
        None, title="Draw Time Series Bar Chart for Patrols Events"
    )


class Td(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    pixel_size: Optional[float] = Field(
        250.0, description="Raster pixel size in meters.", title="Pixel Size"
    )
    max_speed_factor: Optional[float] = Field(1.05, title="Max Speed Factor")
    expansion_factor: Optional[float] = Field(1.3, title="Expansion Factor")


class TimeDensityMap(BaseModel):
    td: Optional[Td] = Field(None, title="Calculate Time Density from Trajectory")


class EarthRangerConnection(BaseModel):
    name: str = Field(..., title="Data Source")


class TemporalGrouper(RootModel[str]):
    root: str = Field(..., title="Time")


class ValueGrouper(RootModel[str]):
    root: str = Field(..., title="Category")


class TrajectorySegmentFilter(BaseModel):
    min_length_meters: Optional[float] = Field(
        0.001, description="Minimum Segment Length in Meters", title="Min Length Meters"
    )
    max_length_meters: Optional[float] = Field(
        10000, description="Maximum Segment Length in Meters", title="Max Length Meters"
    )
    min_time_secs: Optional[float] = Field(
        1, description="Minimum Segment Duration in Seconds", title="Min Time Secs"
    )
    max_time_secs: Optional[float] = Field(
        3600, description="Maximum Segment Duration in Seconds", title="Max Time Secs"
    )
    min_speed_kmhr: Optional[float] = Field(
        0.0001,
        description="Minimum Segment Speed in Kilometers per Hour",
        title="Min Speed Kmhr",
    )
    max_speed_kmhr: Optional[float] = Field(
        120,
        description="Maximum Segment Speed in Kilometers per Hour",
        title="Max Speed Kmhr",
    )


class Coordinate(BaseModel):
    x: float = Field(..., title="X")
    y: float = Field(..., title="Y")


class ErClientName(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    data_source: EarthRangerConnection = Field(
        ..., description="Select one of your configured data sources.", title=""
    )


class Groupers(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    groupers: Optional[List[Union[ValueGrouper, TemporalGrouper]]] = Field(
        None,
        description="            Specify how the data should be grouped to create the views for your dashboard.\n            This field is optional; if left blank, all the data will appear in a single view.\n            ",
        title=" ",
    )


class PatrolTraj(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    trajectory_segment_filter: Optional[TrajectorySegmentFilter] = Field(
        default_factory=lambda: TrajectorySegmentFilter.model_validate(
            {
                "min_length_meters": 0.001,
                "max_length_meters": 10000,
                "min_time_secs": 1,
                "max_time_secs": 3600,
                "min_speed_kmhr": 0.0001,
                "max_speed_kmhr": 120,
            }
        ),
        description="Trajectory Segments outside these bounds will be removed",
        title="Trajectory Segment Filter",
    )


class PreprocessPatrolObservations(BaseModel):
    patrol_traj: Optional[PatrolTraj] = Field(
        None, title="Transform Relocations to Trajectories"
    )


class FilterPatrolEvents(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    min_x: Optional[float] = Field(-180.0, title="Min X")
    max_x: Optional[float] = Field(180.0, title="Max X")
    min_y: Optional[float] = Field(-90.0, title="Min Y")
    max_y: Optional[float] = Field(90.0, title="Max Y")
    filter_point_coords: Optional[List[Coordinate]] = Field(
        [], title="Filter Point Coords"
    )


class PreprocessPatrolEvents(BaseModel):
    filter_patrol_events: Optional[FilterPatrolEvents] = Field(
        None, title="Apply Coordinate Filter"
    )


class FormData(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    workflow_details: Optional[WorkflowDetails] = Field(
        None,
        description="Add information that will help to differentiate this workflow from another.",
        title="Workflow Details",
    )
    er_client_name: Optional[ErClientName] = Field(None, title="Data Source")
    time_range: Optional[TimeRange] = Field(
        None, description="Choose the period of time to analyze.", title="Time Range"
    )
    Patrol_and_Event_Types: Optional[PatrolAndEventTypes] = Field(
        None,
        alias="Patrol and Event Types",
        description="Select the Patrol and Event types to be analyzed.",
    )
    groupers: Optional[Groupers] = Field(None, title="Group Data")
    Preprocess_patrol_observations: Optional[PreprocessPatrolObservations] = Field(
        None,
        alias="Preprocess patrol observations",
        description="Preprocess patrol observations from EarthRanger.",
    )
    Preprocess_patrol_events: Optional[PreprocessPatrolEvents] = Field(
        None,
        alias="Preprocess patrol events",
        description="Preprocess patrol events from EarthRanger.",
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
