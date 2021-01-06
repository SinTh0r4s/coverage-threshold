from decimal import Decimal

from coverage_threshold.model.coverage_json import (
    JsonReportModel,
    FileCoverageModel,
    CoverageSummaryModel,
    JsonReportMetadata,
)
from coverage_threshold.lib import (
    each_file_line_coverage_metric,
    total_line_coverage_metric,
)
from coverage_threshold.lib.check_result import Pass, Fail

test_report = JsonReportModel(
    meta=JsonReportMetadata(branch_coverage=False),
    files={
        "src/main.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=1,
                num_statements=2,
                percent_covered=Decimal("50.0"),
                missing_lines=0,
                excluded_lines=0,
            )
        ),
        "src/lib.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=2,
                num_statements=2,
                percent_covered=Decimal("100.0"),
                missing_lines=0,
                excluded_lines=0,
            )
        ),
    },
    totals=CoverageSummaryModel(
        covered_lines=3,
        num_statements=4,
        percent_covered=Decimal("75.0"),
        missing_lines=0,
        excluded_lines=0,
    ),
)


def test_all_files_at_or_above_threshold() -> None:
    assert each_file_line_coverage_metric(test_report, Decimal("50.0")) == Pass()
    assert each_file_line_coverage_metric(test_report, Decimal("75.0")) == Fail(
        ['File: "src/main.py" failed line coverage metric, expected: 75.0, was 50.00']
    )


def test_average_line_coverage_at_or_above_threshold() -> None:
    assert total_line_coverage_metric(test_report, Decimal("75.0"))