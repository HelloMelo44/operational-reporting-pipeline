from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "service_tickets_clean.csv"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


def load_processed_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


def create_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("department")
        .agg(
            total_tickets=("ticket_id", "count"),
            resolved_tickets=("is_resolved", "sum"),
            sla_breaches=("sla_breached", "sum"),
            reopened_tickets=("reopened_flag", "sum"),
            avg_resolution_hours=("resolution_hours", "mean"),
        )
        .reset_index()
        .sort_values(by="total_tickets", ascending=False)
    )


def create_priority_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("priority")
        .agg(
            total_tickets=("ticket_id", "count"),
            sla_breaches=("sla_breached", "sum"),
            avg_resolution_hours=("resolution_hours", "mean"),
        )
        .reset_index()
        .sort_values(by="sla_breaches", ascending=False)
    )


def create_open_ticket_summary(df: pd.DataFrame) -> pd.DataFrame:
    open_tickets = df[df["is_resolved"] == False]

    return (
        open_tickets.groupby(["department", "assigned_team"])
        .agg(open_tickets=("ticket_id", "count"))
        .reset_index()
        .sort_values(by="open_tickets", ascending=False)
    )


def save_report(report_df: pd.DataFrame, filename: str) -> None:
    output_path = REPORTS_DIR / filename
    report_df.to_csv(output_path, index=False)
    print(f"Saved report: {output_path}")


def main() -> None:
    df = load_processed_data()

    department_summary = create_department_summary(df)
    priority_summary = create_priority_summary(df)
    open_ticket_summary = create_open_ticket_summary(df)

    save_report(department_summary, "department_summary.csv")
    save_report(priority_summary, "priority_summary.csv")
    save_report(open_ticket_summary, "open_ticket_summary.csv")


if __name__ == "__main__":
    main()