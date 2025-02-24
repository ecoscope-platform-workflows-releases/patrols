# AUTOGENERATED BY ECOSCOPE-WORKFLOWS; see fingerprint in README.md for details


from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class WorkflowDetails(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str = Field(..., description="The name of your workflow", title="Name")
    description: str = Field(..., description="A description", title="Description")


class ErPatrolTypes(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    patrol_types: List[str] = Field(
        ..., description="list of UUID of patrol types", title="Patrol Types"
    )


class TimeRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    since: AwareDatetime = Field(..., description="The start time", title="Since")
    until: AwareDatetime = Field(..., description="The end time", title="Until")


class StatusEnum(str, Enum):
    active = "active"
    overdue = "overdue"
    done = "done"
    cancelled = "cancelled"


class PatrolObs(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    status: Optional[List[StatusEnum]] = Field(
        None,
        description="list of 'scheduled'/'active'/'overdue'/'done'/'cancelled'",
        title="Status",
    )


class PatrolEvents(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    event_type: List[str] = Field(
        ..., description="list of event types by name", title="Event Type"
    )
    status: Optional[List[str]] = Field(
        None,
        description="list of 'scheduled'/'active'/'overdue'/'done'/'cancelled'",
        title="Status",
    )


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
    name: str = Field(..., title="Connection Name")


class Grouper(BaseModel):
    index_name: str = Field(..., title="Index Name")


class TemporalGrouper(BaseModel):
    temporal_index: str = Field(..., title="Temporal Index")


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
        ...,
        description="Select one of your configured data sources by name.",
        title="Data Source",
    )


class Groupers(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    groupers: Optional[List[Union[Grouper, TemporalGrouper]]] = Field(
        None,
        description="            Temporal index(es) and/or column(s) to group by. This field is optional.\n            If left unfilled, all data will be presented together in a single group.\n            ",
        title="Groupers",
    )


class PatrolTraj(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    trajectory_segment_filter: Optional[TrajectorySegmentFilter] = Field(
        None,
        description="Trajectory Segments outside these bounds will be removed",
        title="Trajectory Segment Filter",
    )


class FetchAndPreprocessPatrolObservations(BaseModel):
    patrol_obs: Optional[PatrolObs] = Field(
        None, title="Get Patrol Observations from EarthRanger"
    )
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
        None, title="Filter Point Coords"
    )


class FetchAndPreprocessPatrolEvents(BaseModel):
    patrol_events: Optional[PatrolEvents] = Field(
        None, title="Get Patrol Events from EarthRanger"
    )
    filter_patrol_events: Optional[FilterPatrolEvents] = Field(
        None, title="Apply Relocation Coordinate Filter"
    )


class FormData(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    workflow_details: Optional[WorkflowDetails] = Field(
        None, title="Set Workflow Details"
    )
    er_client_name: Optional[ErClientName] = Field(
        None, title="Select EarthRanger Data Source"
    )
    er_patrol_types: Optional[ErPatrolTypes] = Field(
        None, title="Set EarthRanger Patrol Types"
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
