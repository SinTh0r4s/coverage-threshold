import argparse
import json
import toml
from decimal import Decimal
from typing import Optional

from coverage_threshold.model.config import Config
from coverage_threshold.model.coverage_json import JsonReportModel
from coverage_threshold.lib import check_all
from coverage_threshold.lib.check_result import fold_check_results


parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--total-line-coverage-threshold",
    type=Decimal,
    required=False,
    help="minimum global average line coverage threshold",
)
parser.add_argument(
    "--line-coverage-threshold-for-every-file",
    type=Decimal,
    required=False,
    help="the coverage threshold",
)
parser.add_argument(
    "--coverage-json",
    type=str,
    default="./coverage.json",
    help="path to coverage json (default: ./coverage.json)",
)


class ArgsNamespace(argparse.Namespace):
    total_line_coverage_threshold: Optional[Decimal]
    line_coverage_threshold_for_every_file: Optional[Decimal]
    coverage_json: str


def bool_to_return_status(x: bool) -> int:
    return 0 if x else 1


def read_report(coverage_json_filename: str) -> JsonReportModel:
    with open(coverage_json_filename) as coverage_json_file:
        return JsonReportModel.parse(json.loads(coverage_json_file.read()))


def read_config(config_file_name: str) -> Config:
    return Config.parse(toml.load(config_file_name).get("coverage-threshold", {}))


def combine_config_with_args(args: ArgsNamespace, config: Config) -> Config:
    return Config(
        total_line_coverage_threshold=(
            args.total_line_coverage_threshold
            or config.total_line_coverage_threshold
        ),
        line_coverage_threshold_for_every_file=(
            args.line_coverage_threshold_for_every_file
            or config.line_coverage_threshold_for_every_file
        ),
        modules=config.modules,
    )


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def main() -> int:
    args = parser.parse_args(namespace=ArgsNamespace())
    report = read_report(args.coverage_json)
    config_from_file = read_config("pyproject.toml")
    config = combine_config_with_args(args, config_from_file)
    all_checks = check_all(report, config)
    if all_checks.result:
        print(bcolors.OKGREEN + "Success!" + bcolors.ENDC)
    else:
        print("Fail!")
        for problem in all_checks.problems:
            print(bcolors.FAIL + problem + bcolors.ENDC)
    return bool_to_return_status(all_checks.result)
