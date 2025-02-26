# AUTOGENERATED BY ECOSCOPE-WORKFLOWS; see fingerprint in README.md for details

# ruff: noqa: E402

"""WARNING: This file is generated in a testing context and should not be used in production.
Lines specific to the testing context are marked with a test tube emoji (🧪) to indicate
that they would not be included (or would be different) in the production version of this file.
"""

import json
import os
import warnings  # 🧪
from ecoscope_workflows_core.testing import create_task_magicmock  # 🧪


from ecoscope_workflows_core.tasks.config import set_workflow_details
from ecoscope_workflows_core.tasks.io import set_er_connection
from ecoscope_workflows_ext_ecoscope.tasks.io import set_patrol_types
from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_core.tasks.filter import set_time_range

get_patrol_observations = create_task_magicmock(  # 🧪
    anchor="ecoscope_workflows_ext_ecoscope.tasks.io",  # 🧪
    func_name="get_patrol_observations",  # 🧪
)  # 🧪
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import process_relocations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import (
    relocations_to_trajectory,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_core.tasks.transformation import map_columns

get_patrol_events = create_task_magicmock(  # 🧪
    anchor="ecoscope_workflows_ext_ecoscope.tasks.io",  # 🧪
    func_name="get_patrol_events",  # 🧪
)  # 🧪
from ecoscope_workflows_ext_ecoscope.tasks.transformation import (
    apply_reloc_coord_filter,
)
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
from ecoscope_workflows_core.tasks.transformation import convert_column_values_to_string
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
    warnings.warn("This test script should not be used in production!")  # 🧪

    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    workflow_details = (
        set_workflow_details.validate()
        .handle_errors(task_instance_id="workflow_details")
        .partial(**(params_dict.get("workflow_details") or {}))
        .call()
    )

    er_client_name = (
        set_er_connection.validate()
        .handle_errors(task_instance_id="er_client_name")
        .partial(**(params_dict.get("er_client_name") or {}))
        .call()
    )

    er_patrol_types = (
        set_patrol_types.validate()
        .handle_errors(task_instance_id="er_patrol_types")
        .partial(**(params_dict.get("er_patrol_types") or {}))
        .call()
    )

    groupers = (
        set_groupers.validate()
        .handle_errors(task_instance_id="groupers")
        .partial(**(params_dict.get("groupers") or {}))
        .call()
    )

    time_range = (
        set_time_range.validate()
        .handle_errors(task_instance_id="time_range")
        .partial(
            time_format="%d %b %Y %H:%M:%S %Z", **(params_dict.get("time_range") or {})
        )
        .call()
    )

    patrol_obs = (
        get_patrol_observations.validate()
        .handle_errors(task_instance_id="patrol_obs")
        .partial(
            client=er_client_name,
            time_range=time_range,
            patrol_type=er_patrol_types,
            include_patrol_details=True,
            raise_on_empty=True,
            **(params_dict.get("patrol_obs") or {}),
        )
        .call()
    )

    patrol_reloc = (
        process_relocations.validate()
        .handle_errors(task_instance_id="patrol_reloc")
        .partial(
            observations=patrol_obs,
            relocs_columns=[
                "patrol_id",
                "patrol_start_time",
                "patrol_end_time",
                "patrol_type__value",
                "patrol_serial_number",
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
        .handle_errors(task_instance_id="patrol_traj")
        .partial(relocations=patrol_reloc, **(params_dict.get("patrol_traj") or {}))
        .call()
    )

    traj_add_temporal_index = (
        add_temporal_index.validate()
        .handle_errors(task_instance_id="traj_add_temporal_index")
        .partial(
            df=patrol_traj,
            time_col="extra__patrol_start_time",
            groupers=groupers,
            cast_to_datetime=True,
            format="mixed",
            **(params_dict.get("traj_add_temporal_index") or {}),
        )
        .call()
    )

    traj_rename_grouper_columns = (
        map_columns.validate()
        .handle_errors(task_instance_id="traj_rename_grouper_columns")
        .partial(
            df=traj_add_temporal_index,
            drop_columns=[],
            retain_columns=[],
            rename_columns={
                "extra__patrol_type__value": "patrol_type",
                "extra__patrol_serial_number": "patrol_serial_number",
            },
            **(params_dict.get("traj_rename_grouper_columns") or {}),
        )
        .call()
    )

    patrol_events = (
        get_patrol_events.validate()
        .handle_errors(task_instance_id="patrol_events")
        .partial(
            client=er_client_name,
            time_range=time_range,
            patrol_type=er_patrol_types,
            truncate_to_time_range=True,
            raise_on_empty=True,
            **(params_dict.get("patrol_events") or {}),
        )
        .call()
    )

    filter_patrol_events = (
        apply_reloc_coord_filter.validate()
        .handle_errors(task_instance_id="filter_patrol_events")
        .partial(df=patrol_events, **(params_dict.get("filter_patrol_events") or {}))
        .call()
    )

    pe_add_temporal_index = (
        add_temporal_index.validate()
        .handle_errors(task_instance_id="pe_add_temporal_index")
        .partial(
            df=filter_patrol_events,
            time_col="patrol_start_time",
            groupers=groupers,
            cast_to_datetime=True,
            format="mixed",
            **(params_dict.get("pe_add_temporal_index") or {}),
        )
        .call()
    )

    pe_colormap = (
        apply_color_map.validate()
        .handle_errors(task_instance_id="pe_colormap")
        .partial(
            df=pe_add_temporal_index,
            input_column_name="event_type",
            colormap="tab20b",
            output_column_name="event_type_colormap",
            **(params_dict.get("pe_colormap") or {}),
        )
        .call()
    )

    pe_rename_grouper_columns = (
        map_columns.validate()
        .handle_errors(task_instance_id="pe_rename_grouper_columns")
        .partial(
            df=pe_colormap,
            drop_columns=[],
            retain_columns=[],
            rename_columns={"serial_number": "patrol_serial_number"},
            **(params_dict.get("pe_rename_grouper_columns") or {}),
        )
        .call()
    )

    patrol_traj_cols_to_string = (
        convert_column_values_to_string.validate()
        .handle_errors(task_instance_id="patrol_traj_cols_to_string")
        .partial(
            df=traj_rename_grouper_columns,
            columns=["patrol_serial_number", "patrol_type"],
            **(params_dict.get("patrol_traj_cols_to_string") or {}),
        )
        .call()
    )

    pe_cols_to_string = (
        convert_column_values_to_string.validate()
        .handle_errors(task_instance_id="pe_cols_to_string")
        .partial(
            df=pe_rename_grouper_columns,
            columns=["patrol_serial_number", "patrol_type"],
            **(params_dict.get("pe_cols_to_string") or {}),
        )
        .call()
    )

    split_patrol_traj_groups = (
        split_groups.validate()
        .handle_errors(task_instance_id="split_patrol_traj_groups")
        .partial(
            df=patrol_traj_cols_to_string,
            groupers=groupers,
            **(params_dict.get("split_patrol_traj_groups") or {}),
        )
        .call()
    )

    split_pe_groups = (
        split_groups.validate()
        .handle_errors(task_instance_id="split_pe_groups")
        .partial(
            df=pe_cols_to_string,
            groupers=groupers,
            **(params_dict.get("split_pe_groups") or {}),
        )
        .call()
    )

    patrol_events_map_layers = (
        create_point_layer.validate()
        .handle_errors(task_instance_id="patrol_events_map_layers")
        .partial(
            layer_style={"fill_color_column": "event_type_colormap"},
            legend={
                "label_column": "event_type",
                "color_column": "event_type_colormap",
            },
            tooltip_columns=["id", "time", "event_type", "patrol_segment_id"],
            **(params_dict.get("patrol_events_map_layers") or {}),
        )
        .mapvalues(argnames=["geodataframe"], argvalues=split_pe_groups)
    )

    patrol_traj_map_layers = (
        create_polyline_layer.validate()
        .handle_errors(task_instance_id="patrol_traj_map_layers")
        .partial(
            layer_style={
                "auto_highlight": False,
                "opacity": 1.0,
                "pickable": True,
                "get_color": None,
                "get_width": 3.0,
                "color_column": None,
                "width_units": "pixels",
                "cap_rounded": True,
            },
            legend=None,
            tooltip_columns=["extra__patrol_id", "patrol_type", "speed"],
            **(params_dict.get("patrol_traj_map_layers") or {}),
        )
        .mapvalues(argnames=["geodataframe"], argvalues=split_patrol_traj_groups)
    )

    combined_traj_and_pe_map_layers = (
        groupbykey.validate()
        .handle_errors(task_instance_id="combined_traj_and_pe_map_layers")
        .partial(
            iterables=[patrol_traj_map_layers, patrol_events_map_layers],
            **(params_dict.get("combined_traj_and_pe_map_layers") or {}),
        )
        .call()
    )

    traj_patrol_events_ecomap = (
        draw_ecomap.validate()
        .handle_errors(task_instance_id="traj_patrol_events_ecomap")
        .partial(
            tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
            north_arrow_style={"placement": "top-left"},
            legend_style={"placement": "bottom-right"},
            static=False,
            title=None,
            max_zoom=20,
            **(params_dict.get("traj_patrol_events_ecomap") or {}),
        )
        .mapvalues(argnames=["geo_layers"], argvalues=combined_traj_and_pe_map_layers)
    )

    traj_pe_ecomap_html_urls = (
        persist_text.validate()
        .handle_errors(task_instance_id="traj_pe_ecomap_html_urls")
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("traj_pe_ecomap_html_urls") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=traj_patrol_events_ecomap)
    )

    traj_pe_map_widgets_single_views = (
        create_map_widget_single_view.validate()
        .handle_errors(task_instance_id="traj_pe_map_widgets_single_views")
        .partial(
            title="Trajectories & Patrol Events Map",
            **(params_dict.get("traj_pe_map_widgets_single_views") or {}),
        )
        .map(argnames=["view", "data"], argvalues=traj_pe_ecomap_html_urls)
    )

    traj_pe_grouped_map_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="traj_pe_grouped_map_widget")
        .partial(
            widgets=traj_pe_map_widgets_single_views,
            **(params_dict.get("traj_pe_grouped_map_widget") or {}),
        )
        .call()
    )

    total_patrols = (
        dataframe_column_nunique.validate()
        .handle_errors(task_instance_id="total_patrols")
        .partial(
            column_name="extra__patrol_id", **(params_dict.get("total_patrols") or {})
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrols_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .handle_errors(task_instance_id="total_patrols_sv_widgets")
        .partial(
            title="Total Patrols",
            decimal_places=1,
            **(params_dict.get("total_patrols_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=total_patrols)
    )

    total_patrols_grouped_sv_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="total_patrols_grouped_sv_widget")
        .partial(
            widgets=total_patrols_sv_widgets,
            **(params_dict.get("total_patrols_grouped_sv_widget") or {}),
        )
        .call()
    )

    total_patrol_time = (
        dataframe_column_sum.validate()
        .handle_errors(task_instance_id="total_patrol_time")
        .partial(
            column_name="timespan_seconds",
            **(params_dict.get("total_patrol_time") or {}),
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrol_time_converted = (
        with_unit.validate()
        .handle_errors(task_instance_id="total_patrol_time_converted")
        .partial(
            original_unit="s",
            new_unit="h",
            **(params_dict.get("total_patrol_time_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=total_patrol_time)
    )

    total_patrol_time_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .handle_errors(task_instance_id="total_patrol_time_sv_widgets")
        .partial(
            title="Total Time",
            decimal_places=1,
            **(params_dict.get("total_patrol_time_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=total_patrol_time_converted)
    )

    patrol_time_grouped_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="patrol_time_grouped_widget")
        .partial(
            widgets=total_patrol_time_sv_widgets,
            **(params_dict.get("patrol_time_grouped_widget") or {}),
        )
        .call()
    )

    total_patrol_dist = (
        dataframe_column_sum.validate()
        .handle_errors(task_instance_id="total_patrol_dist")
        .partial(
            column_name="dist_meters", **(params_dict.get("total_patrol_dist") or {})
        )
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    total_patrol_dist_converted = (
        with_unit.validate()
        .handle_errors(task_instance_id="total_patrol_dist_converted")
        .partial(
            original_unit="m",
            new_unit="km",
            **(params_dict.get("total_patrol_dist_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=total_patrol_dist)
    )

    total_patrol_dist_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .handle_errors(task_instance_id="total_patrol_dist_sv_widgets")
        .partial(
            title="Total Distance",
            decimal_places=1,
            **(params_dict.get("total_patrol_dist_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=total_patrol_dist_converted)
    )

    patrol_dist_grouped_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="patrol_dist_grouped_widget")
        .partial(
            widgets=total_patrol_dist_sv_widgets,
            **(params_dict.get("patrol_dist_grouped_widget") or {}),
        )
        .call()
    )

    avg_speed = (
        dataframe_column_mean.validate()
        .handle_errors(task_instance_id="avg_speed")
        .partial(column_name="speed_kmhr", **(params_dict.get("avg_speed") or {}))
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    average_speed_converted = (
        with_unit.validate()
        .handle_errors(task_instance_id="average_speed_converted")
        .partial(
            original_unit="km/h",
            new_unit="km/h",
            **(params_dict.get("average_speed_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=avg_speed)
    )

    avg_speed_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .handle_errors(task_instance_id="avg_speed_sv_widgets")
        .partial(
            title="Average Speed",
            decimal_places=1,
            **(params_dict.get("avg_speed_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=average_speed_converted)
    )

    avg_speed_grouped_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="avg_speed_grouped_widget")
        .partial(
            widgets=avg_speed_sv_widgets,
            **(params_dict.get("avg_speed_grouped_widget") or {}),
        )
        .call()
    )

    max_speed = (
        dataframe_column_max.validate()
        .handle_errors(task_instance_id="max_speed")
        .partial(column_name="speed_kmhr", **(params_dict.get("max_speed") or {}))
        .mapvalues(argnames=["df"], argvalues=split_patrol_traj_groups)
    )

    max_speed_converted = (
        with_unit.validate()
        .handle_errors(task_instance_id="max_speed_converted")
        .partial(
            original_unit="km/h",
            new_unit="km/h",
            **(params_dict.get("max_speed_converted") or {}),
        )
        .mapvalues(argnames=["value"], argvalues=max_speed)
    )

    max_speed_sv_widgets = (
        create_single_value_widget_single_view.validate()
        .handle_errors(task_instance_id="max_speed_sv_widgets")
        .partial(
            title="Max Speed",
            decimal_places=1,
            **(params_dict.get("max_speed_sv_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=max_speed_converted)
    )

    max_speed_grouped_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="max_speed_grouped_widget")
        .partial(
            widgets=max_speed_sv_widgets,
            **(params_dict.get("max_speed_grouped_widget") or {}),
        )
        .call()
    )

    patrol_events_bar_chart = (
        draw_time_series_bar_chart.validate()
        .handle_errors(task_instance_id="patrol_events_bar_chart")
        .partial(
            x_axis="time",
            y_axis="event_type",
            category="event_type",
            agg_function="count",
            color_column="event_type_colormap",
            plot_style={"xperiodalignment": "middle"},
            grouped_styles=None,
            layout_style=None,
            **(params_dict.get("patrol_events_bar_chart") or {}),
        )
        .mapvalues(argnames=["dataframe"], argvalues=split_pe_groups)
    )

    patrol_events_bar_chart_html_url = (
        persist_text.validate()
        .handle_errors(task_instance_id="patrol_events_bar_chart_html_url")
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("patrol_events_bar_chart_html_url") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=patrol_events_bar_chart)
    )

    patrol_events_bar_chart_widget = (
        create_plot_widget_single_view.validate()
        .handle_errors(task_instance_id="patrol_events_bar_chart_widget")
        .partial(
            title="Patrol Events Bar Chart",
            **(params_dict.get("patrol_events_bar_chart_widget") or {}),
        )
        .map(argnames=["view", "data"], argvalues=patrol_events_bar_chart_html_url)
    )

    grouped_bar_plot_widget_merge = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="grouped_bar_plot_widget_merge")
        .partial(
            widgets=patrol_events_bar_chart_widget,
            **(params_dict.get("grouped_bar_plot_widget_merge") or {}),
        )
        .call()
    )

    patrol_events_pie_chart = (
        draw_pie_chart.validate()
        .handle_errors(task_instance_id="patrol_events_pie_chart")
        .partial(
            value_column="event_type",
            plot_style={"textinfo": "value"},
            label_column=None,
            color_column="event_type_colormap",
            layout_style=None,
            **(params_dict.get("patrol_events_pie_chart") or {}),
        )
        .mapvalues(argnames=["dataframe"], argvalues=split_pe_groups)
    )

    pe_pie_chart_html_urls = (
        persist_text.validate()
        .handle_errors(task_instance_id="pe_pie_chart_html_urls")
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("pe_pie_chart_html_urls") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=patrol_events_pie_chart)
    )

    patrol_events_pie_chart_widgets = (
        create_plot_widget_single_view.validate()
        .handle_errors(task_instance_id="patrol_events_pie_chart_widgets")
        .partial(
            title="Patrol Events Pie Chart",
            **(params_dict.get("patrol_events_pie_chart_widgets") or {}),
        )
        .map(argnames=["view", "data"], argvalues=pe_pie_chart_html_urls)
    )

    patrol_events_pie_widget_grouped = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="patrol_events_pie_widget_grouped")
        .partial(
            widgets=patrol_events_pie_chart_widgets,
            **(params_dict.get("patrol_events_pie_widget_grouped") or {}),
        )
        .call()
    )

    td = (
        calculate_time_density.validate()
        .handle_errors(task_instance_id="td")
        .partial(
            crs="ESRI:53042",
            percentiles=[50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 99.999],
            nodata_value="nan",
            band_count=1,
            **(params_dict.get("td") or {}),
        )
        .mapvalues(argnames=["trajectory_gdf"], argvalues=split_patrol_traj_groups)
    )

    td_colormap = (
        apply_color_map.validate()
        .handle_errors(task_instance_id="td_colormap")
        .partial(
            df=td,
            input_column_name="percentile",
            colormap="RdYlGn",
            output_column_name="percentile_colormap",
            **(params_dict.get("td_colormap") or {}),
        )
        .mapvalues(argnames=["df"], argvalues=td)
    )

    td_map_layer = (
        create_polygon_layer.validate()
        .handle_errors(task_instance_id="td_map_layer")
        .partial(
            layer_style={
                "fill_color_column": "percentile_colormap",
                "opacity": 0.7,
                "get_line_width": 0,
            },
            legend={
                "label_column": "percentile",
                "color_column": "percentile_colormap",
            },
            tooltip_columns=["percentile"],
            **(params_dict.get("td_map_layer") or {}),
        )
        .mapvalues(argnames=["geodataframe"], argvalues=td_colormap)
    )

    td_ecomap = (
        draw_ecomap.validate()
        .handle_errors(task_instance_id="td_ecomap")
        .partial(
            tile_layers=[{"name": "TERRAIN"}, {"name": "SATELLITE", "opacity": 0.5}],
            north_arrow_style={"placement": "top-left"},
            legend_style={"placement": "bottom-right"},
            static=False,
            title=None,
            max_zoom=20,
            **(params_dict.get("td_ecomap") or {}),
        )
        .mapvalues(argnames=["geo_layers"], argvalues=td_map_layer)
    )

    td_ecomap_html_url = (
        persist_text.validate()
        .handle_errors(task_instance_id="td_ecomap_html_url")
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **(params_dict.get("td_ecomap_html_url") or {}),
        )
        .mapvalues(argnames=["text"], argvalues=td_ecomap)
    )

    td_map_widget = (
        create_map_widget_single_view.validate()
        .handle_errors(task_instance_id="td_map_widget")
        .partial(title="Time Density Map", **(params_dict.get("td_map_widget") or {}))
        .map(argnames=["view", "data"], argvalues=td_ecomap_html_url)
    )

    td_grouped_map_widget = (
        merge_widget_views.validate()
        .handle_errors(task_instance_id="td_grouped_map_widget")
        .partial(
            widgets=td_map_widget, **(params_dict.get("td_grouped_map_widget") or {})
        )
        .call()
    )

    patrol_dashboard = (
        gather_dashboard.validate()
        .handle_errors(task_instance_id="patrol_dashboard")
        .partial(
            details=workflow_details,
            widgets=[
                traj_pe_grouped_map_widget,
                td_grouped_map_widget,
                grouped_bar_plot_widget_merge,
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
