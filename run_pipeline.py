import logging
import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DASHBOARD_DATA_DIR = PROJECT_ROOT / "dashboard_data"

REQUIRED_CSV_FILES = [
    "company_metrics.csv",
    "company_intelligence.csv",
    "market_insights.csv",
    "news.csv",
    "prices.csv",
    "sentiment.csv",
]

PYTHON_CANDIDATES = [
    PROJECT_ROOT / "venv" / "Scripts" / "python.exe",
    PROJECT_ROOT / ".venv" / "Scripts" / "python.exe",
    PROJECT_ROOT / "venv" / "bin" / "python",
    PROJECT_ROOT / ".venv" / "bin" / "python",
]


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("insightpulse.pipeline")


def resolve_python_executable() -> str:
    for candidate in PYTHON_CANDIDATES:
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def run_command(label: str, module: str, python_executable: str) -> bool:
    """Run one pipeline module and print captured output only on failure."""
    command = [python_executable, "-m", module]
    logger.info("Running %s...", label)

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        logger.error("%s failed to start: %s", label, exc)
        return False

    if result.returncode == 0:
        return True

    logger.error("%s failed with exit code %s.", label, result.returncode)
    if result.stdout.strip():
        logger.error("\n--- stdout ---\n%s", result.stdout.strip())
    if result.stderr.strip():
        logger.error("\n--- stderr ---\n%s", result.stderr.strip())
    return False


def verify_csv_files() -> tuple[bool, list[str]]:
    missing_files = [
        filename
        for filename in REQUIRED_CSV_FILES
        if not (DASHBOARD_DATA_DIR / filename).is_file()
    ]
    return not missing_files, missing_files


def print_summary(
    bootstrap_passed: bool,
    export_passed: bool,
    csv_passed: bool,
    files_generated: int,
    elapsed_seconds: float,
) -> None:
    pipeline_passed = bootstrap_passed and export_passed and csv_passed

    print("\n========================================")
    print("InsightPulse Pipeline")
    print()
    print(f"Bootstrap ............. {'PASS' if bootstrap_passed else 'FAIL'}")
    print(f"CSV Export ............ {'PASS' if export_passed else 'FAIL'}")
    print(f"CSV Verification ...... {'PASS' if csv_passed else 'FAIL'}")
    print(f"Files Generated ....... {files_generated}/{len(REQUIRED_CSV_FILES)}")
    print(f"Pipeline Status ....... {'SUCCESS' if pipeline_passed else 'FAILED'}")
    print("========================================")
    print(f"Completed in {elapsed_seconds:.2f} seconds.")


def main() -> int:
    start_time = time.perf_counter()
    bootstrap_passed = False
    export_passed = False
    csv_passed = False
    missing_files: list[str] = []
    files_generated = 0
    python_executable = resolve_python_executable()

    try:
        bootstrap_passed = run_command(
            "Bootstrap",
            "scripts.bootstrap",
            python_executable,
        )
        if not bootstrap_passed:
            return_code = 1
            return return_code

        export_passed = run_command(
            "CSV Export",
            "scripts.export_dashboard_data",
            python_executable,
        )
        if not export_passed:
            return_code = 1
            return return_code

        csv_passed, missing_files = verify_csv_files()
        files_generated = len(REQUIRED_CSV_FILES) - len(missing_files)
        if not csv_passed:
            logger.error("Missing CSV files:")
            for filename in missing_files:
                logger.error("- %s", filename)
            return_code = 1
            return return_code

        return 0

    except KeyboardInterrupt:
        logger.error("Pipeline interrupted by user.")
        return 130
    except Exception as exc:
        logger.error("Pipeline failed unexpectedly: %s", exc)
        return 1
    finally:
        elapsed_seconds = time.perf_counter() - start_time
        print_summary(
            bootstrap_passed,
            export_passed,
            csv_passed,
            files_generated,
            elapsed_seconds,
        )


if __name__ == "__main__":
    sys.exit(main())
