# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "80be953de845c95c3cbd1eaf9e3527b2a83b6166f794d9dd3c27d44ce5003da3"
import json
import os

from ecoscope_workflows_core.graph import DependsOn, DependsOnSequence, Graph, Node

from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_ext_ecoscope.tasks.io import get_patrol_observations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import process_relocations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import (
    relocations_to_trajectory,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_core.tasks.groupby import split_groups
from ecoscope_workflows_ext_ecoscope.tasks.results import create_map_layer
from ecoscope_workflows_ext_ecoscope.tasks.io import get_patrol_events
from ecoscope_workflows_ext_ecoscope.tasks.transformation import (
    apply_reloc_coord_filter,
)
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
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
from ecoscope_workflows_core.tasks.results import gather_dashboard

from ..params import Params


def main(params: Params):
    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    dependencies = {
        "groupers": [],
        "patrol_obs": [],
        "patrol_reloc": ["patrol_obs"],
        "patrol_traj": ["patrol_reloc"],
        "traj_add_temporal_index": ["patrol_traj"],
        "split_patrol_traj_groups": ["traj_add_temporal_index", "groupers"],
        "patrol_traj_map_layers": ["split_patrol_traj_groups"],
        "patrol_events": [],
        "filter_patrol_events": ["patrol_events"],
        "pe_add_temporal_index": ["filter_patrol_events"],
        "pe_colormap": ["pe_add_temporal_index"],
        "split_pe_groups": ["pe_colormap", "groupers"],
        "patrol_events_map_layers": ["split_pe_groups"],
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
        "patrol_events_bar_chart": ["filter_patrol_events"],
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
        ],
    }

    nodes = {
        "groupers": Node(
            async_task=set_groupers.validate().set_executor("lithops"),
            partial=params_dict["groupers"],
            method="call",
        ),
        "patrol_obs": Node(
            async_task=get_patrol_observations.validate().set_executor("lithops"),
            partial=params_dict["patrol_obs"],
            method="call",
        ),
        "patrol_reloc": Node(
            async_task=process_relocations.validate().set_executor("lithops"),
            partial={
                "observations": DependsOn("patrol_obs"),
            }
            | params_dict["patrol_reloc"],
            method="call",
        ),
        "patrol_traj": Node(
            async_task=relocations_to_trajectory.validate().set_executor("lithops"),
            partial={
                "relocations": DependsOn("patrol_reloc"),
            }
            | params_dict["patrol_traj"],
            method="call",
        ),
        "traj_add_temporal_index": Node(
            async_task=add_temporal_index.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("patrol_traj"),
            }
            | params_dict["traj_add_temporal_index"],
            method="call",
        ),
        "split_patrol_traj_groups": Node(
            async_task=split_groups.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("traj_add_temporal_index"),
                "groupers": DependsOn("groupers"),
            }
            | params_dict["split_patrol_traj_groups"],
            method="call",
        ),
        "patrol_traj_map_layers": Node(
            async_task=create_map_layer.validate().set_executor("lithops"),
            partial=params_dict["patrol_traj_map_layers"],
            method="mapvalues",
            kwargs={
                "argnames": ["geodataframe"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "patrol_events": Node(
            async_task=get_patrol_events.validate().set_executor("lithops"),
            partial=params_dict["patrol_events"],
            method="call",
        ),
        "filter_patrol_events": Node(
            async_task=apply_reloc_coord_filter.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("patrol_events"),
            }
            | params_dict["filter_patrol_events"],
            method="call",
        ),
        "pe_add_temporal_index": Node(
            async_task=add_temporal_index.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("filter_patrol_events"),
            }
            | params_dict["pe_add_temporal_index"],
            method="call",
        ),
        "pe_colormap": Node(
            async_task=apply_color_map.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("pe_add_temporal_index"),
            }
            | params_dict["pe_colormap"],
            method="call",
        ),
        "split_pe_groups": Node(
            async_task=split_groups.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("pe_colormap"),
                "groupers": DependsOn("groupers"),
            }
            | params_dict["split_pe_groups"],
            method="call",
        ),
        "patrol_events_map_layers": Node(
            async_task=create_map_layer.validate().set_executor("lithops"),
            partial=params_dict["patrol_events_map_layers"],
            method="mapvalues",
            kwargs={
                "argnames": ["geodataframe"],
                "argvalues": DependsOn("split_pe_groups"),
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
            | params_dict["combined_traj_and_pe_map_layers"],
            method="call",
        ),
        "traj_patrol_events_ecomap": Node(
            async_task=draw_ecomap.validate().set_executor("lithops"),
            partial=params_dict["traj_patrol_events_ecomap"],
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
            | params_dict["traj_pe_ecomap_html_urls"],
            method="mapvalues",
            kwargs={
                "argnames": ["text"],
                "argvalues": DependsOn("traj_patrol_events_ecomap"),
            },
        ),
        "traj_pe_map_widgets_single_views": Node(
            async_task=create_map_widget_single_view.validate().set_executor("lithops"),
            partial=params_dict["traj_pe_map_widgets_single_views"],
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
            | params_dict["traj_pe_grouped_map_widget"],
            method="call",
        ),
        "total_patrols": Node(
            async_task=dataframe_column_nunique.validate().set_executor("lithops"),
            partial=params_dict["total_patrols"],
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
            partial=params_dict["total_patrols_sv_widgets"],
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
            | params_dict["total_patrols_grouped_sv_widget"],
            method="call",
        ),
        "total_patrol_time": Node(
            async_task=dataframe_column_sum.validate().set_executor("lithops"),
            partial=params_dict["total_patrol_time"],
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "total_patrol_time_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial=params_dict["total_patrol_time_converted"],
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
            partial=params_dict["total_patrol_time_sv_widgets"],
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
            | params_dict["patrol_time_grouped_widget"],
            method="call",
        ),
        "total_patrol_dist": Node(
            async_task=dataframe_column_sum.validate().set_executor("lithops"),
            partial=params_dict["total_patrol_dist"],
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "total_patrol_dist_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial=params_dict["total_patrol_dist_converted"],
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
            partial=params_dict["total_patrol_dist_sv_widgets"],
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
            | params_dict["patrol_dist_grouped_widget"],
            method="call",
        ),
        "avg_speed": Node(
            async_task=dataframe_column_mean.validate().set_executor("lithops"),
            partial=params_dict["avg_speed"],
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "average_speed_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial=params_dict["average_speed_converted"],
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
            partial=params_dict["avg_speed_sv_widgets"],
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
            | params_dict["avg_speed_grouped_widget"],
            method="call",
        ),
        "max_speed": Node(
            async_task=dataframe_column_max.validate().set_executor("lithops"),
            partial=params_dict["max_speed"],
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_patrol_traj_groups"),
            },
        ),
        "max_speed_converted": Node(
            async_task=with_unit.validate().set_executor("lithops"),
            partial=params_dict["max_speed_converted"],
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
            partial=params_dict["max_speed_sv_widgets"],
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
            | params_dict["max_speed_grouped_widget"],
            method="call",
        ),
        "patrol_events_bar_chart": Node(
            async_task=draw_time_series_bar_chart.validate().set_executor("lithops"),
            partial={
                "dataframe": DependsOn("filter_patrol_events"),
            }
            | params_dict["patrol_events_bar_chart"],
            method="call",
        ),
        "patrol_events_bar_chart_html_url": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "text": DependsOn("patrol_events_bar_chart"),
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | params_dict["patrol_events_bar_chart_html_url"],
            method="call",
        ),
        "patrol_events_bar_chart_widget": Node(
            async_task=create_plot_widget_single_view.validate().set_executor(
                "lithops"
            ),
            partial={
                "data": DependsOn("patrol_events_bar_chart_html_url"),
            }
            | params_dict["patrol_events_bar_chart_widget"],
            method="call",
        ),
        "patrol_events_pie_chart": Node(
            async_task=draw_pie_chart.validate().set_executor("lithops"),
            partial=params_dict["patrol_events_pie_chart"],
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
            | params_dict["pe_pie_chart_html_urls"],
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
            partial=params_dict["patrol_events_pie_chart_widgets"],
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
            | params_dict["patrol_events_pie_widget_grouped"],
            method="call",
        ),
        "td": Node(
            async_task=calculate_time_density.validate().set_executor("lithops"),
            partial={
                "trajectory_gdf": DependsOn("patrol_traj"),
            }
            | params_dict["td"],
            method="call",
        ),
        "td_colormap": Node(
            async_task=apply_color_map.validate().set_executor("lithops"),
            partial={
                "df": DependsOn("td"),
            }
            | params_dict["td_colormap"],
            method="call",
        ),
        "td_map_layer": Node(
            async_task=create_map_layer.validate().set_executor("lithops"),
            partial={
                "geodataframe": DependsOn("td_colormap"),
            }
            | params_dict["td_map_layer"],
            method="call",
        ),
        "td_ecomap": Node(
            async_task=draw_ecomap.validate().set_executor("lithops"),
            partial={
                "geo_layers": DependsOn("td_map_layer"),
            }
            | params_dict["td_ecomap"],
            method="call",
        ),
        "td_ecomap_html_url": Node(
            async_task=persist_text.validate().set_executor("lithops"),
            partial={
                "text": DependsOn("td_ecomap"),
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | params_dict["td_ecomap_html_url"],
            method="call",
        ),
        "td_map_widget": Node(
            async_task=create_map_widget_single_view.validate().set_executor("lithops"),
            partial={
                "data": DependsOn("td_ecomap_html_url"),
            }
            | params_dict["td_map_widget"],
            method="call",
        ),
        "patrol_dashboard": Node(
            async_task=gather_dashboard.validate().set_executor("lithops"),
            partial={
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
            }
            | params_dict["patrol_dashboard"],
            method="call",
        ),
    }
    graph = Graph(dependencies=dependencies, nodes=nodes)
    results = graph.execute()
    return results
