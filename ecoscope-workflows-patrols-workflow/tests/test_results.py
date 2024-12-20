# AUTOGENERATED BY ECOSCOPE-WORKFLOWS; see fingerprint in README.md for details

import asyncio
from typing import Any, Coroutine

import pytest
import pytest_check.context_manager
from syrupy import SnapshotAssertion
from syrupy.matchers import path_type


def test_dashboard_json(dashboard_json: dict, snapshot_json: SnapshotAssertion):
    exclude_results_data = {
        f"result.views.{key}.{i}.data": (str,)
        for key in dashboard_json["result"]["views"]
        for i, _ in enumerate(dashboard_json["result"]["views"][key])
    }
    matcher = path_type(exclude_results_data)
    assert dashboard_json == snapshot_json(matcher=matcher)


@pytest.mark.asyncio
async def test_iframes(
    snapshot_png: SnapshotAssertion,
    screenshot_coros: list[Coroutine[Any, Any, tuple[str, bytes]]],
    check: pytest_check.context_manager.CheckContextManager,
):
    screenshots = await asyncio.gather(*screenshot_coros)
    assert len(screenshots) >= 1, "No screenshots taken"
    for widget_title, actual_png in screenshots:
        with check:
            assert actual_png == snapshot_png(name=widget_title.replace(" ", "_"))
