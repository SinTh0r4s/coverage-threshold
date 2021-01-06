from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List, Mapping, Optional

from .util import parse_option_field

# replace these dataclass models with pydantic
# if this gets too complex


@dataclass(frozen=True)
class CoverageSummaryModel:
    covered_lines: int
    num_statements: int
    percent_covered: Decimal
    missing_lines: int
    excluded_lines: int
    num_branches: Optional[int] = None
    num_partial_branches: Optional[int] = None
    covered_branches: Optional[int] = None
    missing_branches: Optional[int] = None

    @staticmethod
    def parse(obj: Any) -> CoverageSummaryModel:
        return CoverageSummaryModel(
            covered_lines=int(obj["covered_lines"]),
            num_statements=int(obj["num_statements"]),
            percent_covered=Decimal(obj["percent_covered"]),
            missing_lines=int(obj["missing_lines"]),
            excluded_lines=int(obj["excluded_lines"]),
            num_branches=parse_option_field(obj, int, "num_branches"),
            num_partial_branches=parse_option_field(obj, int, "num_partial_branches"),
            covered_branches=parse_option_field(obj, int, "covered_branches"),
            missing_branches=parse_option_field(obj, int, "missing_branches"),
        )


@dataclass(frozen=True)
class FileCoverageModel:
    summary: CoverageSummaryModel

    @staticmethod
    def parse(obj: Any) -> FileCoverageModel:
        return FileCoverageModel(summary=CoverageSummaryModel.parse(obj["summary"]))


@dataclass(frozen=True)
class JsonReportMetadata:
    branch_coverage: bool

    @staticmethod
    def parse(obj: Any) -> JsonReportMetadata:
        return JsonReportMetadata(branch_coverage=bool(obj["branch_coverage"]))


@dataclass(frozen=True)
class JsonReportModel:
    files: Mapping[str, FileCoverageModel]
    totals: CoverageSummaryModel
    meta: JsonReportMetadata

    @staticmethod
    def parse(obj: Any) -> JsonReportModel:
        return JsonReportModel(
            files={
                filename: FileCoverageModel.parse(value)
                for filename, value in obj["files"].items()
            },
            totals=CoverageSummaryModel.parse(obj["totals"]),
            meta=JsonReportMetadata.parse(obj["meta"]),
        )
