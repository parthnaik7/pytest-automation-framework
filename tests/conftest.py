# flake8: noqa
# pylint: skip-file
"""
conftest.py
"""
import os
from datetime import datetime
import logging
import allure
import pandas as pd
import pytest
from utils.report_util import (
    build_table,
    write_to_csv,
    build_data,
)
from utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
log_filename = f"logfile_{timestamp}.log"

def pytest_addoption(parser):
    parser.addoption(
        "--TEST_ENV",
        action="store",
        default="TEST",
        help="TEST | STAGE | PROD",
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "report_" + report.when, report)
    if report.when == "call":
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            try:  # noqa: SIM105
                allure.attach(
                    item.funcargs["driver"].get_screenshot_as_png(),
                    name=f"{item.name}_{timestamp}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:  # noqa: E722, B001
                logger.info(e)

    return report


def pytest_sessionfinish(session, exitstatus):
    try:
        allure_dir = os.path.join(os.getcwd(), "reports")
        print(allure_dir)
        if os.path.isdir(allure_dir):
            results, session = build_data(allure_dir)

            rows = []
            count = 0
            print("####")
            print(results)
            for count, item in enumerate(results):
                count += 1
                message = ""
                if item["status"] == "failed":
                    message = item.get("statusDetails").get("message")
                single_row = [count, item["name"], item["status"], message]
                rows.append(single_row)
            write_to_csv(rows=rows)

            report_date = session["stop"]
            pass_count = str(session["results"]["passed"])
            fail_count = str(session["results"]["failed"])
            skip_count = str(session["results"]["skipped"])
            error_count = str(session["results"]["broken"])
            total_tests = str(session["total"])

            df = pd.read_csv("records.csv")
            env_details = {}
            if os.getenv("VERSION"):
                env_details.update({"Version": os.getenv("VERSION")})
            if os.getenv("URL"):
                env_details.update({"URL": os.getenv("URL")})
            html_table_blue_light = build_table(
                df,
                "blue_light",
                report_date,
                pass_count,
                fail_count,
                skip_count,
                error_count,
                total_tests,
                test_info=env_details,
            )
            with open("index.html", "w") as f:
                f.write(html_table_blue_light)
    except:
        logger.info(f"Failed to generate report")
