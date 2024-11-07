# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "f5fbeb4f277bcb0cd0eaeba753d89cec7035a97e2572f641fb667fd95270fb00"
import json
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

from ..params import Params


def main(params: Params):
    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    workflow_details = (
        set_workflow_details.validate()
        .partial(**(params_dict.get("workflow_details") or {}))
        .call()
    )

    er_client_name = (
        set_connection.validate()
        .partial(**(params_dict.get("er_client_name") or {}))
        .call()
    )

    groupers = (
        set_groupers.validate().partial(**(params_dict.get("groupers") or {})).call()
    )

    time_range = (
        set_time_range.validate()
        .partial(**(params_dict.get("time_range") or {}))
        .call()
    )

    patrol_obs = (
        get_patrol_observations.validate()
        .partial(
            client=er_client_name,
            time_range=time_range,
            **(params_dict.get("patrol_obs") or {}),
        )
        .call()
    )

    patrol_reloc = (
        process_relocations.validate()
        .partial(
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
            **(params_dict.get("patrol_reloc") or {}),
        )
        .call()
    )

    patrol_traj = (
        relocations_to_trajectory.validate()
        .partial(relocations=patrol_reloc, **(params_dict.get("patrol_traj") or {}))
        .call()
    )

    traj_add_temporal_index = (
        add_temporal_index.validate()
        .partial(
            df=patrol_traj,
            time_col="extra__patrol_start_time",
            groupers=groupers,
            **(params_dict.get("traj_add_temporal_index") or {}),
        )
        .call()
    )

    patrol_events = (
        get_patrol_events.validate()
        .partial(
            client=er_client_name,
            time_range=time_range,
            **(params_dict.get("patrol_events") or {}),
        )
        .call()
    )

    filter_patrol_events = (
        apply_reloc_coord_filter.validate()
        .partial(df=patrol_events, **(params_dict.get("filter_patrol_events") or {}))
        .call()
    )

    pe_add_temporal_index = (
        add_temporal_index.validate()
        .partial(
            df=filter_patrol_events,
            time_col="time",
            groupers=groupers,
            **(params_dict.get("pe_add_temporal_index") or {}),
        )
        .call()
    )

    pe_colormap = (
        apply_color_map.validate()
        .partial(
            df=pe_add_temporal_index,
            input_column_name="event_type",
            colormap="tab20b",
            output_column_name="event_type_colormap",
            **(params_dict.get("pe_colormap") or {}),
        )
        .call()
    )

    split_pe_groups = (
        split_groups.validate()
        .partial(
            df=pe_colormap,
            groupers=groupers,
            **(params_dict.get("split_pe_groups") or {}),
        )
        .call()
    )

    patrol_events_map_layers = (
        create_point_layer.validate()
        .partial(
            layer_style={"fill_color_column": "event_type_colormap"},
            **(params_dict.get("patrol_events_map_layers") or {}),
        )
        .mapvalues(argnames=["geodataframe"], argvalues=split_pe_groups)
    )

    split_patrol_traj_groups = (
        split_groups.validate()
        .partial(
            df=traj_add_temporal_index,
            groupers=groupers,
            **(params_dict.get("split_patrol_traj_groups") or {}),
        )
        .call()
    )

    patrol_traj_map_layers = (
        create_polyline_layer.validate()
        .partial(**(params_dict.get("patrol_traj_map_layers") or {}))
        .mapvalues(argnames=["geodataframe"], argvalues=split_patrol_traj_groups)
    )

    combined_traj_and_pe_map_layers = (
        groupbykey.validate()
        .partial(
            iterables=[patrol_traj_map_layers, patrol_events_map_layers],
            **(params_dict.get("combined_traj_and_pe_map_layers") or {}),
        )
        .call()
    )

    traj_patrol_events_ecomap = (
        draw_ecomap.validate()
        .partial(
            tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
            north_arrow_style={"placement": "top-left"},
            legend_style={"placement": "bottom-right"},
            static=False,
            **(params_dict.get("traj_patrol_events_ecomap") or {}),
        )
        .mapvalues(argnames=["geo_layers"], argvalues=combined_traj_and_pe_map_layers)
    )

    traj_pe_ecomap_html_urls = (
        persist_text.validate()
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("traj_pe_ecomap_html_urls") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=traj_patrol_events_ecomap)
    )

    traj_pe_map_widgets_single_views = (
        create_map_widget_single_view.validate()
        .partial(
            title="Trajectories & Patrol Events Map",
            **(params_dict.get("traj_pe_map_widgets_single_views") or {}),
        )
        .map(argnames=["view", "data"], argvalues=traj_pe_ecomap_html_urls)
    )

    traj_pe_grouped_map_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=traj_pe_map_widgets_single_views,
            **(params_dict.get("traj_pe_grouped_map_widget") or {}),
        )
        .call()
    )

    total_patrols = (
        dataframe_column_nunique.validate()
        .partial(
            column_name="extra__patrol_id", **(params_dict.get("total_patrols") or {})
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrols_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .partial(
            title="Total Patrols", **(params_dict.get("total_patrols_sv_widgets") or {})
        )
        .map(argnames=["view", "data"], argvalues=total_patrols)
    )

    total_patrols_grouped_sv_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=total_patrols_sv_widgets,
            **(params_dict.get("total_patrols_grouped_sv_widget") or {}),
        )
        .call()
    )

    total_patrol_time = (
        dataframe_column_sum.validate()
        .partial(
            column_name="timespan_seconds",
            **(params_dict.get("total_patrol_time") or {}),
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrol_time_converted = (
        with_unit.validate()
        .partial(
            original_unit="s",
            new_unit="h",
            **(params_dict.get("total_patrol_time_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=total_patrol_time)
    )

    total_patrol_time_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .partial(
            title="Total Time",
            **(params_dict.get("total_patrol_time_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=total_patrol_time_converted)
    )

    patrol_time_grouped_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=total_patrol_time_sv_widgets,
            **(params_dict.get("patrol_time_grouped_widget") or {}),
        )
        .call()
    )

    total_patrol_dist = (
        dataframe_column_sum.validate()
        .partial(
            column_name="dist_meters", **(params_dict.get("total_patrol_dist") or {})
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrol_dist_converted = (
        with_unit.validate()
        .partial(
            original_unit="m",
            new_unit="km",
            **(params_dict.get("total_patrol_dist_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=total_patrol_dist)
    )

    total_patrol_dist_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .partial(
            title="Total Distance",
            **(params_dict.get("total_patrol_dist_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=total_patrol_dist_converted)
    )

    patrol_dist_grouped_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=total_patrol_dist_sv_widgets,
            **(params_dict.get("patrol_dist_grouped_widget") or {}),
        )
        .call()
    )

    avg_speed = (
        dataframe_column_mean.validate()
        .partial(column_name="speed_kmhr", **(params_dict.get("avg_speed") or {}))
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    average_speed_converted = (
        with_unit.validate()
        .partial(
            original_unit="km/h",
            new_unit="km/h",
            **(params_dict.get("average_speed_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=avg_speed)
    )

    avg_speed_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .partial(
            title="Average Speed", **(params_dict.get("avg_speed_sv_widgets") or {})
        )
        .map(argnames=["view", "data"], argvalues=average_speed_converted)
    )

    avg_speed_grouped_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=avg_speed_sv_widgets,
            **(params_dict.get("avg_speed_grouped_widget") or {}),
        )
        .call()
    )

    max_speed = (
        dataframe_column_max.validate()
        .partial(column_name="speed_kmhr", **(params_dict.get("max_speed") or {}))
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    max_speed_converted = (
        with_unit.validate()
        .partial(
            original_unit="km/h",
            new_unit="km/h",
            **(params_dict.get("max_speed_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=max_speed)
    )

    max_speed_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .partial(title="Max Speed", **(params_dict.get("max_speed_sv_widgets") or {}))
        .map(argnames=["view", "data"], argvalues=max_speed_converted)
    )

    max_speed_grouped_widget = (
        merge_widget_views.validate()
        .partial(
            widgets=max_speed_sv_widgets,
            **(params_dict.get("max_speed_grouped_widget") or {}),
        )
        .call()
    )

    patrol_events_bar_chart = (
        draw_time_series_bar_chart.validate()
        .partial(
            dataframe=pe_colormap,
            x_axis="time",
            y_axis="event_type",
            category="event_type",
            agg_function="count",
            color_column="event_type_colormap",
            plot_style={"xperiodalignment": "middle"},
            **(params_dict.get("patrol_events_bar_chart") or {}),
        )
        .call()
    )

    patrol_events_bar_chart_html_url = (
        persist_text.validate()
        .partial(
            text=patrol_events_bar_chart,
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("patrol_events_bar_chart_html_url") or {}),
        )
        .call()
    )

    patrol_events_bar_chart_widget = (
        create_plot_widget_single_view.validate()
        .partial(
            data=patrol_events_bar_chart_html_url,
            title="Patrol Events Bar Chart",
            **(params_dict.get("patrol_events_bar_chart_widget") or {}),
        )
        .call()
    )

    patrol_events_pie_chart = (
        draw_pie_chart.validate()
        .partial(
            value_column="event_type",
            plot_style={"textinfo": "value"},
            **(params_dict.get("patrol_events_pie_chart") or {}),
        )
        .mapvalues(argnames=["dataframe"], argvalues=split_pe_groups)
    )

    pe_pie_chart_html_urls = (
        persist_text.validate()
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("pe_pie_chart_html_urls") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=patrol_events_pie_chart)
    )

    patrol_events_pie_chart_widgets = (
        create_plot_widget_single_view.validate()
        .partial(
            title="Patrol Events Pie Chart",
            **(params_dict.get("patrol_events_pie_chart_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=pe_pie_chart_html_urls)
    )

    patrol_events_pie_widget_grouped = (
        merge_widget_views.validate()
        .partial(
            widgets=patrol_events_pie_chart_widgets,
            **(params_dict.get("patrol_events_pie_widget_grouped") or {}),
        )
        .call()
    )

    td = (
        calculate_time_density.validate()
        .partial(
            trajectory_gdf=patrol_traj,
            pixel_size=250.0,
            crs="ESRI:102022",
            percentiles=[50.0, 60.0, 70.0, 80.0, 90.0, 95.0],
            **(params_dict.get("td") or {}),
        )
        .call()
    )

    td_colormap = (
        apply_color_map.validate()
        .partial(
            df=td,
            input_column_name="percentile",
            colormap="RdYlGn",
            output_column_name="percentile_colormap",
            **(params_dict.get("td_colormap") or {}),
        )
        .call()
    )

    td_map_layer = (
        create_polygon_layer.validate()
        .partial(
            geodataframe=td_colormap,
            layer_style={
                "fill_color_column": "percentile_colormap",
                "opacity": 0.7,
                "get_line_width": 0,
            },
            **(params_dict.get("td_map_layer") or {}),
        )
        .call()
    )

    td_ecomap = (
        draw_ecomap.validate()
        .partial(
            geo_layers=td_map_layer,
            tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
            north_arrow_style={"placement": "top-left"},
            legend_style={"placement": "bottom-right"},
            static=False,
            **(params_dict.get("td_ecomap") or {}),
        )
        .call()
    )

    td_ecomap_html_url = (
        persist_text.validate()
        .partial(
            text=td_ecomap,
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("td_ecomap_html_url") or {}),
        )
        .call()
    )

    td_map_widget = (
        create_map_widget_single_view.validate()
        .partial(
            data=td_ecomap_html_url,
            title="Time Density Map",
            **(params_dict.get("td_map_widget") or {}),
        )
        .call()
    )

    patrol_dashboard = (
        gather_dashboard.validate()
        .partial(
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
            **(params_dict.get("patrol_dashboard") or {}),
        )
        .call()
    )

    return patrol_dashboard
