# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "67e050a5f34893bb04f20a0b9d002543d121cd619de7305c3c889e5446d2b502"


# ruff: noqa: E402

# %% [markdown]
# # Patrols
# TODO: top level description

# %% [markdown]
# ## Imports

import os
from ecoscope_workflows_core.tasks.config import set_workflow_details
from ecoscope_workflows_core.tasks.io import set_connection
from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_core.tasks.filter import set_time_range
from ecoscope_workflows_ext_ecoscope.tasks.io import get_patrol_observations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import process_relocations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import (
    relocations_to_trajectory,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_ext_ecoscope.tasks.io import get_patrol_events
from ecoscope_workflows_ext_ecoscope.tasks.transformation import (
    apply_reloc_coord_filter,
)
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
from ecoscope_workflows_core.tasks.groupby import split_groups
from ecoscope_workflows_ext_ecoscope.tasks.results import create_point_layer
from ecoscope_workflows_ext_ecoscope.tasks.results import create_polyline_layer
from ecoscope_workflows_core.tasks.groupby import groupbykey
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_ecomap
from ecoscope_workflows_core.tasks.io import persist_text
from ecoscope_workflows_core.tasks.results import create_map_widget_single_view
from ecoscope_workflows_core.tasks.results import merge_widget_views
from ecoscope_workflows_core.tasks.analysis import dataframe_column_nunique
from ecoscope_workflows_core.tasks.results import create_single_value_widget_single_view
from ecoscope_workflows_core.tasks.analysis import dataframe_column_sum
from ecoscope_workflows_core.tasks.transformation import with_unit
from ecoscope_workflows_core.tasks.analysis import dataframe_column_mean
from ecoscope_workflows_core.tasks.analysis import dataframe_column_max
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_time_series_bar_chart
from ecoscope_workflows_core.tasks.results import create_plot_widget_single_view
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_pie_chart
from ecoscope_workflows_ext_ecoscope.tasks.analysis import calculate_time_density
from ecoscope_workflows_ext_ecoscope.tasks.results import create_polygon_layer
from ecoscope_workflows_core.tasks.results import gather_dashboard

# %% [markdown]
# ## Set Workflow Details

# %%
# parameters

workflow_details_params = dict(
    name=...,
    description=...,
    image_url=...,
)

# %%
# call the task


workflow_details = set_workflow_details.partial(**workflow_details_params).call()


# %% [markdown]
# ## Select EarthRanger Connection

# %%
# parameters

er_client_name_params = dict(
    EcoscopeWorkflowsNamedConnection=...,
)

# %%
# call the task


er_client_name = set_connection.partial(**er_client_name_params).call()


# %% [markdown]
# ## Set Groupers

# %%
# parameters

groupers_params = dict(
    groupers=...,
)

# %%
# call the task


groupers = set_groupers.partial(**groupers_params).call()


# %% [markdown]
# ## Set Time Range Filter

# %%
# parameters

time_range_params = dict(
    since=...,
    until=...,
    time_format=...,
)

# %%
# call the task


time_range = set_time_range.partial(**time_range_params).call()


# %% [markdown]
# ## Get Patrol Observations from EarthRanger

# %%
# parameters

patrol_obs_params = dict(
    patrol_type=...,
    status=...,
    include_patrol_details=...,
)

# %%
# call the task


patrol_obs = get_patrol_observations.partial(
    client=er_client_name, time_range=time_range, **patrol_obs_params
).call()


# %% [markdown]
# ## Transform Observations to Relocations

# %%
# parameters

patrol_reloc_params = dict()

# %%
# call the task


patrol_reloc = process_relocations.partial(
    observations=patrol_obs,
    relocs_columns=[
        "patrol_id",
        "patrol_start_time",
        "patrol_end_time",
        "patrol_type__display",
        "groupby_col",
        "fixtime",
        "junk_status",
        "extra__source",
        "geometry",
    ],
    filter_point_coords=[
        {"x": 180.0, "y": 90.0},
        {"x": 0.0, "y": 0.0},
        {"x": 1.0, "y": 1.0},
    ],
    **patrol_reloc_params,
).call()


# %% [markdown]
# ## Transform Relocations to Trajectories

# %%
# parameters

patrol_traj_params = dict(
    min_length_meters=...,
    max_length_meters=...,
    max_time_secs=...,
    min_time_secs=...,
    max_speed_kmhr=...,
    min_speed_kmhr=...,
)

# %%
# call the task


patrol_traj = relocations_to_trajectory.partial(
    relocations=patrol_reloc, **patrol_traj_params
).call()


# %% [markdown]
# ## Add temporal index to Patrol Trajectories

# %%
# parameters

traj_add_temporal_index_params = dict(
    cast_to_datetime=...,
    format=...,
)

# %%
# call the task


traj_add_temporal_index = add_temporal_index.partial(
    df=patrol_traj,
    time_col="extra__patrol_start_time",
    groupers=groupers,
    **traj_add_temporal_index_params,
).call()


# %% [markdown]
# ## Get Patrol Events from EarthRanger

# %%
# parameters

patrol_events_params = dict(
    patrol_type=...,
    status=...,
)

# %%
# call the task


patrol_events = get_patrol_events.partial(
    client=er_client_name, time_range=time_range, **patrol_events_params
).call()


# %% [markdown]
# ## Apply Relocation Coordinate Filter

# %%
# parameters

filter_patrol_events_params = dict(
    min_x=...,
    max_x=...,
    min_y=...,
    max_y=...,
    filter_point_coords=...,
)

# %%
# call the task


filter_patrol_events = apply_reloc_coord_filter.partial(
    df=patrol_events, **filter_patrol_events_params
).call()


# %% [markdown]
# ## Add temporal index to Patrol Events

# %%
# parameters

pe_add_temporal_index_params = dict(
    cast_to_datetime=...,
    format=...,
)

# %%
# call the task


pe_add_temporal_index = add_temporal_index.partial(
    df=filter_patrol_events,
    time_col="time",
    groupers=groupers,
    **pe_add_temporal_index_params,
).call()


# %% [markdown]
# ## Patrol Events Colormap

# %%
# parameters

pe_colormap_params = dict()

# %%
# call the task


pe_colormap = apply_color_map.partial(
    df=pe_add_temporal_index,
    input_column_name="event_type",
    colormap="tab20b",
    output_column_name="event_type_colormap",
    **pe_colormap_params,
).call()


# %% [markdown]
# ## Split Patrol Events by Group

# %%
# parameters

split_pe_groups_params = dict()

# %%
# call the task


split_pe_groups = split_groups.partial(
    df=pe_colormap, groupers=groupers, **split_pe_groups_params
).call()


# %% [markdown]
# ## Create map layers for each Patrols Events group

# %%
# parameters

patrol_events_map_layers_params = dict(
    legend=...,
)

# %%
# call the task


patrol_events_map_layers = create_point_layer.partial(
    layer_style={"fill_color_column": "event_type_colormap"},
    **patrol_events_map_layers_params,
).mapvalues(argnames=["geodataframe"], argvalues=split_pe_groups)


# %% [markdown]
# ## Split Patrol Trajectories by Group

# %%
# parameters

split_patrol_traj_groups_params = dict()

# %%
# call the task


split_patrol_traj_groups = split_groups.partial(
    df=traj_add_temporal_index, groupers=groupers, **split_patrol_traj_groups_params
).call()


# %% [markdown]
# ## Create map layer for each Patrol Trajectories group

# %%
# parameters

patrol_traj_map_layers_params = dict(
    layer_style=...,
    legend=...,
)

# %%
# call the task


patrol_traj_map_layers = create_polyline_layer.partial(
    **patrol_traj_map_layers_params
).mapvalues(argnames=["geodataframe"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Combine Trajectories and Patrol Events layers

# %%
# parameters

combined_traj_and_pe_map_layers_params = dict()

# %%
# call the task


combined_traj_and_pe_map_layers = groupbykey.partial(
    iterables=[patrol_traj_map_layers, patrol_events_map_layers],
    **combined_traj_and_pe_map_layers_params,
).call()


# %% [markdown]
# ## Draw Ecomaps for each combined Trajectory and Patrol Events group

# %%
# parameters

traj_patrol_events_ecomap_params = dict(
    title=...,
)

# %%
# call the task


traj_patrol_events_ecomap = draw_ecomap.partial(
    tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
    north_arrow_style={"placement": "top-left"},
    legend_style={"placement": "bottom-right"},
    static=False,
    **traj_patrol_events_ecomap_params,
).mapvalues(argnames=["geo_layers"], argvalues=combined_traj_and_pe_map_layers)


# %% [markdown]
# ## Persist Patrols Ecomap as Text

# %%
# parameters

traj_pe_ecomap_html_urls_params = dict(
    filename=...,
)

# %%
# call the task


traj_pe_ecomap_html_urls = persist_text.partial(
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
    **traj_pe_ecomap_html_urls_params,
).mapvalues(argnames=["text"], argvalues=traj_patrol_events_ecomap)


# %% [markdown]
# ## Create Map Widgets for Patrol Events

# %%
# parameters

traj_pe_map_widgets_single_views_params = dict()

# %%
# call the task


traj_pe_map_widgets_single_views = create_map_widget_single_view.partial(
    title="Trajectories & Patrol Events Map", **traj_pe_map_widgets_single_views_params
).map(argnames=["view", "data"], argvalues=traj_pe_ecomap_html_urls)


# %% [markdown]
# ## Merge EcoMap Widget Views

# %%
# parameters

traj_pe_grouped_map_widget_params = dict()

# %%
# call the task


traj_pe_grouped_map_widget = merge_widget_views.partial(
    widgets=traj_pe_map_widgets_single_views, **traj_pe_grouped_map_widget_params
).call()


# %% [markdown]
# ## Calculate Total Patrols Per Group

# %%
# parameters

total_patrols_params = dict()

# %%
# call the task


total_patrols = dataframe_column_nunique.partial(
    column_name="extra__patrol_id", **total_patrols_params
).mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Create Single Value Widgets for Total Patrols Per Group

# %%
# parameters

total_patrols_sv_widgets_params = dict(
    decimal_places=...,
)

# %%
# call the task


total_patrols_sv_widgets = create_single_value_widget_single_view.partial(
    title="Total Patrols", **total_patrols_sv_widgets_params
).map(argnames=["view", "data"], argvalues=total_patrols)


# %% [markdown]
# ## Merge per group Total Patrols SV widgets

# %%
# parameters

total_patrols_grouped_sv_widget_params = dict()

# %%
# call the task


total_patrols_grouped_sv_widget = merge_widget_views.partial(
    widgets=total_patrols_sv_widgets, **total_patrols_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Total Patrol Time Per Group

# %%
# parameters

total_patrol_time_params = dict()

# %%
# call the task


total_patrol_time = dataframe_column_sum.partial(
    column_name="timespan_seconds", **total_patrol_time_params
).mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Convert total patrol time units

# %%
# parameters

total_patrol_time_converted_params = dict()

# %%
# call the task


total_patrol_time_converted = with_unit.partial(
    original_unit="s", new_unit="h", **total_patrol_time_converted_params
).mapvalues(argnames=["value"], argvalues=total_patrol_time)


# %% [markdown]
# ## Create Single Value Widgets for Total Patrol Time Per Group

# %%
# parameters

total_patrol_time_sv_widgets_params = dict(
    decimal_places=...,
)

# %%
# call the task


total_patrol_time_sv_widgets = create_single_value_widget_single_view.partial(
    title="Total Time", **total_patrol_time_sv_widgets_params
).map(argnames=["view", "data"], argvalues=total_patrol_time_converted)


# %% [markdown]
# ## Merge per group Total Patrol Time SV widgets

# %%
# parameters

patrol_time_grouped_widget_params = dict()

# %%
# call the task


patrol_time_grouped_widget = merge_widget_views.partial(
    widgets=total_patrol_time_sv_widgets, **patrol_time_grouped_widget_params
).call()


# %% [markdown]
# ## Calculate Total Distance Per Group

# %%
# parameters

total_patrol_dist_params = dict()

# %%
# call the task


total_patrol_dist = dataframe_column_sum.partial(
    column_name="dist_meters", **total_patrol_dist_params
).mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Convert total patrol distance units

# %%
# parameters

total_patrol_dist_converted_params = dict()

# %%
# call the task


total_patrol_dist_converted = with_unit.partial(
    original_unit="m", new_unit="km", **total_patrol_dist_converted_params
).mapvalues(argnames=["value"], argvalues=total_patrol_dist)


# %% [markdown]
# ## Create Single Value Widgets for Total Distance Per Group

# %%
# parameters

total_patrol_dist_sv_widgets_params = dict(
    decimal_places=...,
)

# %%
# call the task


total_patrol_dist_sv_widgets = create_single_value_widget_single_view.partial(
    title="Total Distance", **total_patrol_dist_sv_widgets_params
).map(argnames=["view", "data"], argvalues=total_patrol_dist_converted)


# %% [markdown]
# ## Merge per group Total Patrol Distance SV widgets

# %%
# parameters

patrol_dist_grouped_widget_params = dict()

# %%
# call the task


patrol_dist_grouped_widget = merge_widget_views.partial(
    widgets=total_patrol_dist_sv_widgets, **patrol_dist_grouped_widget_params
).call()


# %% [markdown]
# ## Calculate Average Speed Per Group

# %%
# parameters

avg_speed_params = dict()

# %%
# call the task


avg_speed = dataframe_column_mean.partial(
    column_name="speed_kmhr", **avg_speed_params
).mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Convert Average Speed units

# %%
# parameters

average_speed_converted_params = dict()

# %%
# call the task


average_speed_converted = with_unit.partial(
    original_unit="km/h", new_unit="km/h", **average_speed_converted_params
).mapvalues(argnames=["value"], argvalues=avg_speed)


# %% [markdown]
# ## Create Single Value Widgets for Avg Speed Per Group

# %%
# parameters

avg_speed_sv_widgets_params = dict(
    decimal_places=...,
)

# %%
# call the task


avg_speed_sv_widgets = create_single_value_widget_single_view.partial(
    title="Average Speed", **avg_speed_sv_widgets_params
).map(argnames=["view", "data"], argvalues=average_speed_converted)


# %% [markdown]
# ## Merge per group Avg Speed SV widgets

# %%
# parameters

avg_speed_grouped_widget_params = dict()

# %%
# call the task


avg_speed_grouped_widget = merge_widget_views.partial(
    widgets=avg_speed_sv_widgets, **avg_speed_grouped_widget_params
).call()


# %% [markdown]
# ## Calculate Max Speed Per Group

# %%
# parameters

max_speed_params = dict()

# %%
# call the task


max_speed = dataframe_column_max.partial(
    column_name="speed_kmhr", **max_speed_params
).mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)


# %% [markdown]
# ## Convert Max Speed units

# %%
# parameters

max_speed_converted_params = dict()

# %%
# call the task


max_speed_converted = with_unit.partial(
    original_unit="km/h", new_unit="km/h", **max_speed_converted_params
).mapvalues(argnames=["value"], argvalues=max_speed)


# %% [markdown]
# ## Create Single Value Widgets for Max Speed Per Group

# %%
# parameters

max_speed_sv_widgets_params = dict(
    decimal_places=...,
)

# %%
# call the task


max_speed_sv_widgets = create_single_value_widget_single_view.partial(
    title="Max Speed", **max_speed_sv_widgets_params
).map(argnames=["view", "data"], argvalues=max_speed_converted)


# %% [markdown]
# ## Merge per group Max Speed SV widgets

# %%
# parameters

max_speed_grouped_widget_params = dict()

# %%
# call the task


max_speed_grouped_widget = merge_widget_views.partial(
    widgets=max_speed_sv_widgets, **max_speed_grouped_widget_params
).call()


# %% [markdown]
# ## Draw Time Series Bar Chart for Patrols Events

# %%
# parameters

patrol_events_bar_chart_params = dict(
    time_interval=...,
    grouped_styles=...,
    layout_style=...,
)

# %%
# call the task


patrol_events_bar_chart = draw_time_series_bar_chart.partial(
    dataframe=pe_colormap,
    x_axis="time",
    y_axis="event_type",
    category="event_type",
    agg_function="count",
    color_column="event_type_colormap",
    plot_style={"xperiodalignment": "middle"},
    **patrol_events_bar_chart_params,
).call()


# %% [markdown]
# ## Persist Patrols Bar Chart as Text

# %%
# parameters

patrol_events_bar_chart_html_url_params = dict(
    filename=...,
)

# %%
# call the task


patrol_events_bar_chart_html_url = persist_text.partial(
    text=patrol_events_bar_chart,
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
    **patrol_events_bar_chart_html_url_params,
).call()


# %% [markdown]
# ## Create Plot Widget for Patrol Events

# %%
# parameters

patrol_events_bar_chart_widget_params = dict(
    view=...,
)

# %%
# call the task


patrol_events_bar_chart_widget = create_plot_widget_single_view.partial(
    data=patrol_events_bar_chart_html_url,
    title="Patrol Events Bar Chart",
    **patrol_events_bar_chart_widget_params,
).call()


# %% [markdown]
# ## Draw Pie Chart for Patrols Events

# %%
# parameters

patrol_events_pie_chart_params = dict(
    label_column=...,
    color_column=...,
    layout_style=...,
)

# %%
# call the task


patrol_events_pie_chart = draw_pie_chart.partial(
    value_column="event_type",
    plot_style={"textinfo": "value"},
    **patrol_events_pie_chart_params,
).mapvalues(argnames=["dataframe"], argvalues=split_pe_groups)


# %% [markdown]
# ## Persist Patrols Pie Chart as Text

# %%
# parameters

pe_pie_chart_html_urls_params = dict(
    filename=...,
)

# %%
# call the task


pe_pie_chart_html_urls = persist_text.partial(
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"], **pe_pie_chart_html_urls_params
).mapvalues(argnames=["text"], argvalues=patrol_events_pie_chart)


# %% [markdown]
# ## Create Plot Widget for Patrol Events

# %%
# parameters

patrol_events_pie_chart_widgets_params = dict()

# %%
# call the task


patrol_events_pie_chart_widgets = create_plot_widget_single_view.partial(
    title="Patrol Events Pie Chart", **patrol_events_pie_chart_widgets_params
).map(argnames=["view", "data"], argvalues=pe_pie_chart_html_urls)


# %% [markdown]
# ## Merge Pie Chart Widget Views

# %%
# parameters

patrol_events_pie_widget_grouped_params = dict()

# %%
# call the task


patrol_events_pie_widget_grouped = merge_widget_views.partial(
    widgets=patrol_events_pie_chart_widgets, **patrol_events_pie_widget_grouped_params
).call()


# %% [markdown]
# ## Calculate Time Density from Trajectory

# %%
# parameters

td_params = dict(
    nodata_value=...,
    band_count=...,
    max_speed_factor=...,
    expansion_factor=...,
)

# %%
# call the task


td = calculate_time_density.partial(
    trajectory_gdf=patrol_traj,
    pixel_size=250.0,
    crs="ESRI:102022",
    percentiles=[50.0, 60.0, 70.0, 80.0, 90.0, 95.0],
    **td_params,
).call()


# %% [markdown]
# ## Time Density Colormap

# %%
# parameters

td_colormap_params = dict()

# %%
# call the task


td_colormap = apply_color_map.partial(
    df=td,
    input_column_name="percentile",
    colormap="RdYlGn",
    output_column_name="percentile_colormap",
    **td_colormap_params,
).call()


# %% [markdown]
# ## Create map layer from Time Density

# %%
# parameters

td_map_layer_params = dict(
    legend=...,
)

# %%
# call the task


td_map_layer = create_polygon_layer.partial(
    geodataframe=td_colormap,
    layer_style={
        "fill_color_column": "percentile_colormap",
        "opacity": 0.7,
        "get_line_width": 0,
    },
    **td_map_layer_params,
).call()


# %% [markdown]
# ## Draw Ecomap from Time Density

# %%
# parameters

td_ecomap_params = dict(
    title=...,
)

# %%
# call the task


td_ecomap = draw_ecomap.partial(
    geo_layers=td_map_layer,
    tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
    north_arrow_style={"placement": "top-left"},
    legend_style={"placement": "bottom-right"},
    static=False,
    **td_ecomap_params,
).call()


# %% [markdown]
# ## Persist Ecomap as Text

# %%
# parameters

td_ecomap_html_url_params = dict(
    filename=...,
)

# %%
# call the task


td_ecomap_html_url = persist_text.partial(
    text=td_ecomap,
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
    **td_ecomap_html_url_params,
).call()


# %% [markdown]
# ## Create Time Density Map Widget

# %%
# parameters

td_map_widget_params = dict(
    view=...,
)

# %%
# call the task


td_map_widget = create_map_widget_single_view.partial(
    data=td_ecomap_html_url, title="Time Density Map", **td_map_widget_params
).call()


# %% [markdown]
# ## Create Dashboard with Patrol Map Widgets

# %%
# parameters

patrol_dashboard_params = dict()

# %%
# call the task


patrol_dashboard = gather_dashboard.partial(
    details=workflow_details,
    widgets=[
        traj_pe_grouped_map_widget,
        td_map_widget,
        patrol_events_bar_chart_widget,
        patrol_events_pie_widget_grouped,
        total_patrols_grouped_sv_widget,
        patrol_time_grouped_widget,
        patrol_dist_grouped_widget,
        avg_speed_grouped_widget,
        max_speed_grouped_widget,
    ],
    groupers=groupers,
    time_range=time_range,
    **patrol_dashboard_params,
).call()
