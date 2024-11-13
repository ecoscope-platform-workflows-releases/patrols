# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "052e86129c795f0113d103f6ff6bd4bf410fafd135cbf3d443f3e5be787c5450"
import json
import os

from ecoscope_workflows_core.graph import DependsOn, DependsOnSequence, Graph, Node

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

from ..params import Params


def main(params: Params):
    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    dependencies = {
        "workflow_details": [],
        "er_client_name": [],
        "groupers": [],
        "time_range": [],
        "patrol_obs": ["er_client_name", "time_range"],
        "patrol_reloc": ["patrol_obs"],
        "patrol_traj": ["patrol_reloc"],
        "traj_add_temporal_index": ["patrol_traj", "groupers"],
        "patrol_events": ["er_client_name", "time_range"],
        "filter_patrol_events": ["patrol_events"],
        "pe_add_temporal_index": ["filter_patrol_events", "groupers"],
        "pe_colormap": ["pe_add_temporal_index"],
        "split_pe_groups": ["pe_colormap", "groupers"],
        "patrol_events_map_layers": ["split_pe_groups"],
        "split_patrol_traj_groups": ["traj_add_temporal_index", "groupers"],
        "patrol_traj_map_layers": ["split_patrol_traj_groups"],
        "combined_traj_and_pe_map_layers": [
            "patrol_traj_map_layers",
            "patrol_events_map_layers",
        ],
        "traj_patrol_events_ecomap": ["combined_traj_and_pe_map_layers"],
        "traj_pe_ecomap_html_urls": ["traj_patrol_events_ecomap"],
        "traj_pe_map_widgets_single_views": ["traj_pe_ecomap_html_urls"],
        "traj_pe_grouped_map_widget": ["traj_pe_map_widgets_single_views"],
        "total_patrols": ["split_patrol_traj_groups"],
        "total_patrols_sv_widgets": ["total_patrols"],
        "total_patrols_grouped_sv_widget": ["total_patrols_sv_widgets"],
        "total_patrol_time": ["split_patrol_traj_groups"],
        "total_patrol_time_converted": ["total_patrol_time"],
        "total_patrol_time_sv_widgets": ["total_patrol_time_converted"],
        "patrol_time_grouped_widget": ["total_patrol_time_sv_widgets"],
        "total_patrol_dist": ["split_patrol_traj_groups"],
        "total_patrol_dist_converted": ["total_patrol_dist"],
        "total_patrol_dist_sv_widgets": ["total_patrol_dist_converted"],
        "patrol_dist_grouped_widget": ["total_patrol_dist_sv_widgets"],
        "avg_speed": ["split_patrol_traj_groups"],
        "average_speed_converted": ["avg_speed"],
        "avg_speed_sv_widgets": ["average_speed_converted"],
        "avg_speed_grouped_widget": ["avg_speed_sv_widgets"],
        "max_speed": ["split_patrol_traj_groups"],
        "max_speed_converted": ["max_speed"],
        "max_speed_sv_widgets": ["max_speed_converted"],
        "max_speed_grouped_widget": ["max_speed_sv_widgets"],
        "patrol_events_bar_chart": ["pe_colormap"],
        "patrol_events_bar_chart_html_url": ["patrol_events_bar_chart"],
        "patrol_events_bar_chart_widget": ["patrol_events_bar_chart_html_url"],
        "patrol_events_pie_chart": ["split_pe_groups"],
        "pe_pie_chart_html_urls": ["patrol_events_pie_chart"],
        "patrol_events_pie_chart_widgets": ["pe_pie_chart_html_urls"],
        "patrol_events_pie_widget_grouped": ["patrol_events_pie_chart_widgets"],
        "td": ["patrol_traj"],
        "td_colormap": ["td"],
        "td_map_layer": ["td_colormap"],
        "td_ecomap": ["td_map_layer"],
        "td_ecomap_html_url": ["td_ecomap"],
        "td_map_widget": ["td_ecomap_html_url"],
        "patrol_dashboard": [
            "workflow_details",
            "traj_pe_grouped_map_widget",
            "td_map_widget",
            "patrol_events_bar_chart_widget",
            "patrol_events_pie_widget_grouped",
            "total_patrols_grouped_sv_widget",
            "patrol_time_grouped_widget",
            "patrol_dist_grouped_widget",
            "avg_speed_grouped_widget",
            "max_speed_grouped_widget",
            "groupers",
            "time_range",
        ],
    }

    nodes = {
        "workflow_details": Node(
            async_task=set_workflow_details.validate().set_executor("lithops"),
            partial=(params_dict.get("workflow_details") or {}),
            method="call",
        ),
        "er_client_name": Node(
            async_task=set_connection.validate().set_executor("lithops"),
            partial=(params_dict.get("er_client_name") or {}),
            method="call",
        ),
        "groupers": Node(
            async_task=set_groupers.validate().set_executor("lithops"),
            partial=(params_dict.get("groupers") or {}),
            method="call",
        ),
        "time_range": Node(
            async_task=set_time_range.validate().set_executor("lithops"),
            partial=(params_dict.get("time_range") or {}),
            method="call",
        ),
        "patrol_obs": Node(
            async_task=get_patrol_observations.validate().set_executor("lithops"),
            partial={
                "client": DependsOn("er_client_name"),
                "time_range": DependsOn("time_range"),
            }
            | (params_dict.get("patrol_obs") or {}),
            method="call",
        ),
        "patrol_reloc": Node(
            async_task=process_relocations.validate().set_executor("lithops"),
            partial={
                "observations": DependsOn("patrol_obs"),
                "relocs_columns": [
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
                "filter_point_coords": [
                    {"x": 180.0, "y": 90.0},
                    {"x": 0.0, "y": 0.0},
                    {"x": 1.0, "y": 1.0},
                ],
            }
            | (params_dict.get("patrol_reloc") or {}),
            method="call",
        ),
        "patrol_traj": Node(
            async_task=relocations_to_trajectory.validate().set_executor("lithops"),
            partial={
                "relocations": DependsOn("patrol_reloc"),
            }
            | (params_dict.get("patrol_traj") or {}),
            method="call",
        ),
        "traj_add_temporal_index": Node(
            async_task=add_temporal_index.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("patrol_traj"),
                "time_col": "extra__patrol_start_time",
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("traj_add_temporal_index") or {}),
            method="call",
        ),
        "patrol_events": Node(
            async_task=get_patrol_events.validate().set_executor("lithops"),
            partial={
                "client": DependsOn("er_client_name"),
                "time_range": DependsOn("time_range"),
            }
            | (params_dict.get("patrol_events") or {}),
            method="call",
        ),
        "filter_patrol_events": Node(
            async_task=apply_reloc_coord_filter.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("patrol_events"),
            }
            | (params_dict.get("filter_patrol_events") or {}),
            method="call",
        ),
        "pe_add_temporal_index": Node(
            async_task=add_temporal_index.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("filter_patrol_events"),
                "time_col": "time",
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("pe_add_temporal_index") or {}),
            method="call",
        ),
        "pe_colormap": Node(
            async_task=apply_color_map.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("pe_add_temporal_index"),
                "input_column_name": "event_type",
                "colormap": "tab20b",
                "output_column_name": "event_type_colormap",
            }
            | (params_dict.get("pe_colormap") or {}),
            method="call",
        ),
        "split_pe_groups": Node(
            async_task=split_groups.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("pe_colormap"),
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("split_pe_groups") or {}),
            method="call",
        ),
        "patrol_events_map_layers": Node(
            async_task=create_point_layer.validate().set_executor("lithops"),
            partial={
                "layer_style": {"fill_color_column": "event_type_colormap"},
            }
            | (params_dict.get("patrol_events_map_layers") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["geodataframe"],
                "argvalues": DependsOn("split_pe_groups"),
            },
        ),
        "split_patrol_traj_groups": Node(
            async_task=split_groups.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("traj_add_temporal_index"),
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("split_patrol_traj_groups") or {}),
            method="call",
        ),
        "patrol_traj_map_layers": Node(
            async_task=create_polyline_layer.validate().set_executor("lithops"),
            partial=(params_dict.get("patrol_traj_map_layers") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["geodataframe"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "combined_traj_and_pe_map_layers": Node(
            async_task=groupbykey.validate().set_executor("lithops"),
            partial={
                "iterables": DependsOnSequence(
                    [
                        DependsOn("patrol_traj_map_layers"),
                        DependsOn("patrol_events_map_layers"),
                    ],
                ),
            }
            | (params_dict.get("combined_traj_and_pe_map_layers") or {}),
            method="call",
        ),
        "traj_patrol_events_ecomap": Node(
            async_task=draw_ecomap.validate().set_executor("lithops"),
            partial={
                "tile_layers": [
                    {"name": "TERRAIN"},
                    {"name": "SATELLITE", "opacity": 0.5},
                ],
                "north_arrow_style": {"placement": "top-left"},
                "legend_style": {"placement": "bottom-right"},
                "static": False,
            }
            | (params_dict.get("traj_patrol_events_ecomap") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["geo_layers"],
                "argvalues": DependsOn("combined_traj_and_pe_map_layers"),
            },
        ),
        "traj_pe_ecomap_html_urls": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | (params_dict.get("traj_pe_ecomap_html_urls") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["text"],
                "argvalues": DependsOn("traj_patrol_events_ecomap"),
            },
        ),
        "traj_pe_map_widgets_single_views": Node(
            async_task=create_map_widget_single_view.validate().set_executor("lithops"),
            partial={
                "title": "Trajectories & Patrol Events Map",
            }
            | (params_dict.get("traj_pe_map_widgets_single_views") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("traj_pe_ecomap_html_urls"),
            },
        ),
        "traj_pe_grouped_map_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("traj_pe_map_widgets_single_views"),
            }
            | (params_dict.get("traj_pe_grouped_map_widget") or {}),
            method="call",
        ),
        "total_patrols": Node(
            async_task=dataframe_column_nunique.validate().set_executor("lithops"),
            partial={
                "column_name": "extra__patrol_id",
            }
            | (params_dict.get("total_patrols") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "total_patrols_sv_widgets": Node(
            async_task=create_single_value_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Total Patrols",
            }
            | (params_dict.get("total_patrols_sv_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("total_patrols"),
            },
        ),
        "total_patrols_grouped_sv_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("total_patrols_sv_widgets"),
            }
            | (params_dict.get("total_patrols_grouped_sv_widget") or {}),
            method="call",
        ),
        "total_patrol_time": Node(
            async_task=dataframe_column_sum.validate().set_executor("lithops"),
            partial={
                "column_name": "timespan_seconds",
            }
            | (params_dict.get("total_patrol_time") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "total_patrol_time_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial={
                "original_unit": "s",
                "new_unit": "h",
            }
            | (params_dict.get("total_patrol_time_converted") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["value"],
                "argvalues": DependsOn("total_patrol_time"),
            },
        ),
        "total_patrol_time_sv_widgets": Node(
            async_task=create_single_value_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Total Time",
            }
            | (params_dict.get("total_patrol_time_sv_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("total_patrol_time_converted"),
            },
        ),
        "patrol_time_grouped_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("total_patrol_time_sv_widgets"),
            }
            | (params_dict.get("patrol_time_grouped_widget") or {}),
            method="call",
        ),
        "total_patrol_dist": Node(
            async_task=dataframe_column_sum.validate().set_executor("lithops"),
            partial={
                "column_name": "dist_meters",
            }
            | (params_dict.get("total_patrol_dist") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "total_patrol_dist_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial={
                "original_unit": "m",
                "new_unit": "km",
            }
            | (params_dict.get("total_patrol_dist_converted") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["value"],
                "argvalues": DependsOn("total_patrol_dist"),
            },
        ),
        "total_patrol_dist_sv_widgets": Node(
            async_task=create_single_value_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Total Distance",
            }
            | (params_dict.get("total_patrol_dist_sv_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("total_patrol_dist_converted"),
            },
        ),
        "patrol_dist_grouped_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("total_patrol_dist_sv_widgets"),
            }
            | (params_dict.get("patrol_dist_grouped_widget") or {}),
            method="call",
        ),
        "avg_speed": Node(
            async_task=dataframe_column_mean.validate().set_executor("lithops"),
            partial={
                "column_name": "speed_kmhr",
            }
            | (params_dict.get("avg_speed") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "average_speed_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial={
                "original_unit": "km/h",
                "new_unit": "km/h",
            }
            | (params_dict.get("average_speed_converted") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["value"],
                "argvalues": DependsOn("avg_speed"),
            },
        ),
        "avg_speed_sv_widgets": Node(
            async_task=create_single_value_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Average Speed",
            }
            | (params_dict.get("avg_speed_sv_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("average_speed_converted"),
            },
        ),
        "avg_speed_grouped_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("avg_speed_sv_widgets"),
            }
            | (params_dict.get("avg_speed_grouped_widget") or {}),
            method="call",
        ),
        "max_speed": Node(
            async_task=dataframe_column_max.validate().set_executor("lithops"),
            partial={
                "column_name": "speed_kmhr",
            }
            | (params_dict.get("max_speed") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "max_speed_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial={
                "original_unit": "km/h",
                "new_unit": "km/h",
            }
            | (params_dict.get("max_speed_converted") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["value"],
                "argvalues": DependsOn("max_speed"),
            },
        ),
        "max_speed_sv_widgets": Node(
            async_task=create_single_value_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Max Speed",
            }
            | (params_dict.get("max_speed_sv_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("max_speed_converted"),
            },
        ),
        "max_speed_grouped_widget": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("max_speed_sv_widgets"),
            }
            | (params_dict.get("max_speed_grouped_widget") or {}),
            method="call",
        ),
        "patrol_events_bar_chart": Node(
            async_task=draw_time_series_bar_chart.validate().set_executor("lithops"),
            partial={
                "dataframe": DependsOn("pe_colormap"),
                "x_axis": "time",
                "y_axis": "event_type",
                "category": "event_type",
                "agg_function": "count",
                "color_column": "event_type_colormap",
                "plot_style": {"xperiodalignment": "middle"},
            }
            | (params_dict.get("patrol_events_bar_chart") or {}),
            method="call",
        ),
        "patrol_events_bar_chart_html_url": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "text": DependsOn("patrol_events_bar_chart"),
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | (params_dict.get("patrol_events_bar_chart_html_url") or {}),
            method="call",
        ),
        "patrol_events_bar_chart_widget": Node(
            async_task=create_plot_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "data": DependsOn("patrol_events_bar_chart_html_url"),
                "title": "Patrol Events Bar Chart",
            }
            | (params_dict.get("patrol_events_bar_chart_widget") or {}),
            method="call",
        ),
        "patrol_events_pie_chart": Node(
            async_task=draw_pie_chart.validate().set_executor("lithops"),
            partial={
                "value_column": "event_type",
                "plot_style": {"textinfo": "value"},
            }
            | (params_dict.get("patrol_events_pie_chart") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["dataframe"],
                "argvalues": DependsOn("split_pe_groups"),
            },
        ),
        "pe_pie_chart_html_urls": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | (params_dict.get("pe_pie_chart_html_urls") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["text"],
                "argvalues": DependsOn("patrol_events_pie_chart"),
            },
        ),
        "patrol_events_pie_chart_widgets": Node(
            async_task=create_plot_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "title": "Patrol Events Pie Chart",
            }
            | (params_dict.get("patrol_events_pie_chart_widgets") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("pe_pie_chart_html_urls"),
            },
        ),
        "patrol_events_pie_widget_grouped": Node(
            async_task=merge_widget_views.validate().set_executor("lithops"),
            partial={
                "widgets": DependsOn("patrol_events_pie_chart_widgets"),
            }
            | (params_dict.get("patrol_events_pie_widget_grouped") or {}),
            method="call",
        ),
        "td": Node(
            async_task=calculate_time_density.validate().set_executor("lithops"),
            partial={
                "trajectory_gdf": DependsOn("patrol_traj"),
                "pixel_size": 250.0,
                "crs": "ESRI:102022",
                "percentiles": [50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 99.999],
            }
            | (params_dict.get("td") or {}),
            method="call",
        ),
        "td_colormap": Node(
            async_task=apply_color_map.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("td"),
                "input_column_name": "percentile",
                "colormap": "RdYlGn",
                "output_column_name": "percentile_colormap",
            }
            | (params_dict.get("td_colormap") or {}),
            method="call",
        ),
        "td_map_layer": Node(
            async_task=create_polygon_layer.validate().set_executor("lithops"),
            partial={
                "geodataframe": DependsOn("td_colormap"),
                "layer_style": {
                    "fill_color_column": "percentile_colormap",
                    "opacity": 0.7,
                    "get_line_width": 0,
                },
            }
            | (params_dict.get("td_map_layer") or {}),
            method="call",
        ),
        "td_ecomap": Node(
            async_task=draw_ecomap.validate().set_executor("lithops"),
            partial={
                "geo_layers": DependsOn("td_map_layer"),
                "tile_layers": [
                    {"name": "TERRAIN"},
                    {"name": "SATELLITE", "opacity": 0.5},
                ],
                "north_arrow_style": {"placement": "top-left"},
                "legend_style": {"placement": "bottom-right"},
                "static": False,
            }
            | (params_dict.get("td_ecomap") or {}),
            method="call",
        ),
        "td_ecomap_html_url": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "text": DependsOn("td_ecomap"),
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | (params_dict.get("td_ecomap_html_url") or {}),
            method="call",
        ),
        "td_map_widget": Node(
            async_task=create_map_widget_single_view.validate().set_executor("lithops"),
            partial={
                "data": DependsOn("td_ecomap_html_url"),
                "title": "Time Density Map",
            }
            | (params_dict.get("td_map_widget") or {}),
            method="call",
        ),
        "patrol_dashboard": Node(
            async_task=gather_dashboard.validate().set_executor("lithops"),
            partial={
                "details": DependsOn("workflow_details"),
                "widgets": DependsOnSequence(
                    [
                        DependsOn("traj_pe_grouped_map_widget"),
                        DependsOn("td_map_widget"),
                        DependsOn("patrol_events_bar_chart_widget"),
                        DependsOn("patrol_events_pie_widget_grouped"),
                        DependsOn("total_patrols_grouped_sv_widget"),
                        DependsOn("patrol_time_grouped_widget"),
                        DependsOn("patrol_dist_grouped_widget"),
                        DependsOn("avg_speed_grouped_widget"),
                        DependsOn("max_speed_grouped_widget"),
                    ],
                ),
                "groupers": DependsOn("groupers"),
                "time_range": DependsOn("time_range"),
            }
            | (params_dict.get("patrol_dashboard") or {}),
            method="call",
        ),
    }
    graph = Graph(dependencies=dependencies, nodes=nodes)
    results = graph.execute()
    return results
