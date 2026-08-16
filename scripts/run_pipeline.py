import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

PROCESS_SCRIPT = BASE_DIR / "scripts" / "process_tickets.py"
REPORT_SCRIPT = BASE_DIR / "scripts" / "generate_reports.py"


def run_script(script_path: Path) -> None:
    print(f"Running {script_path.name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        check=True,
    )

    if result.returncode == 0:
        print(f"Completed {script_path.name}")


def main() -> None:
    print("Starting operational reporting pipeline")

    run_script(PROCESS_SCRIPT)
    run_script(REPORT_SCRIPT)

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()