"""
This module is a standalone script to generate a pdf report of the test result.

Prerequisite:
- wkhtmltopdf package installation

Usage e.g:
python pipenv run python helpers/report_util.py reports records.csv index.html report_name
first arg(optional): reports directory, defaults to reports/
second arg(optional): name of csv file to be generated, defaults to record.csv
third arg(optional): name of html file to be generated, defaults to index.html
fourth arg(optional): name of report to be generated, defaults to name of reports directory
"""
import csv
import io
import json
import os
import warnings
from datetime import timedelta
from os import listdir
from os.path import join, isfile
from time import ctime

INDENT = 6

# Reformat table_color as dict of tuples

dict_colors = {
    "yellow_light": ("#BF8F00", "2px solid #BF8F00", "#FFF2CC", "#FFFFFF"),
    "grey_light": ("#808080", "2px solid #808080", "#EDEDED", "#FFFFFF"),
    "blue_light": ("#305496", "2px solid #305496", "#D9E1F2", "#FFFFFF"),
    "orange_light": ("#C65911", "2px solid #C65911", "#FCE4D6", "#FFFFFF"),
    "green_light": ("#548235", "2px solid #548235", "#E2EFDA", "#FFFFFF"),
    "red_light": ("#823535", "2px solid #823535", "#efdada", "#FFFFFF"),
    "yellow_dark": ("#FFFFFF", "2px solid #BF8F00", "#FFF2CC", "#BF8F00"),
    "grey_dark": ("#FFFFFF", "2px solid #808080", "#EDEDED", "#808080"),
    "blue_dark": ("#FFFFFF", "2px solid #305496", "#D9E1F2", "#305496"),
    "orange_dark": ("#FFFFFF", "2px solid #C65911", "#FCE4D6", "#C65911"),
    "green_dark": ("#FFFFFF", "2px solid #548235", "#E2EFDA", "#548235"),
    "red_dark": ("#FFFFFF", "2px solid #823535", "#efdada", "#823535"),
}

def build_table(
    df,
    color,
    report_date,
    pass_count,
    fail_count,
    skip_count,
    error_count,
    total_tests,
    font_size="medium",
    font_family="Century Gothic, sans-serif",
    text_align="left",
    width="auto",
    index=False,
    even_color="black",
    even_bg_color="white",
    escape=True,
    width_dict=[],
    conditions={},
    test_info=None,
):
    if df.empty:
        return ""

    # Set color
    padding = "0px 20px 0px 0px"
    color, border_bottom, odd_background_color, header_background_color = dict_colors[
        color
    ]

    a = 0
    while a != len(df):
        if a == 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="", index=index, border=0, escape=escape
            )
            # change format of header
            if index:
                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + header_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";color: "
                    + color
                    + ";text-align: "
                    + text_align
                    + ";border-bottom: "
                    + border_bottom
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                    len(df.columns) + 1,
                )

                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + odd_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";text-align: "
                    + text_align
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                )

            else:
                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + header_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";color: "
                    + color
                    + ";text-align: "
                    + text_align
                    + ";border-bottom: "
                    + border_bottom
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )
            body = """<p>""" + format(df_html_output)

            a = 1

        elif a % 2 == 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="", index=index, header=False, escape=escape
            )

            # change format of index
            df_html_output = df_html_output.replace(
                "<th>",
                '<th style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            body = body + format(df_html_output)

            a += 1

        elif a % 2 != 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="", index=index, header=False, escape=escape
            )

            # change format of index
            df_html_output = df_html_output.replace(
                "<th>",
                '<th style = "background-color: '
                + even_bg_color
                + "; color: "
                + even_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + even_bg_color
                + "; color: "
                + even_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )
            body += format(df_html_output)

            a += 1

    info_body = ""
    if test_info:
        info_body = """<table class="footer-section__label" style="width:100%; color:#fff; background: #332b50; 
        border:2px solid #ccc;"><tbody>"""
        for key, value in test_info.items():
            info_body += (
                """
                        <tr>
                            <td>"""
                + str(key)
                + """</td>
                            <td>"""
                + str(value)
                + """</td>
                        </tr>"""
            )
        info_body += """</tbody></table>"""
    body = (
        """<header style="height: 80px; text-align: left; position: relative; background: #332b50; box-shadow: 0 2px 4px 0 rgb(0 0 0 / 20%);"
        xmlns="http://www.w3.org/1999/html"><img
        src="https://d3egw90877nxc9.cloudfront.net/3.9.731/dist/assets/assets/images/logo-corvin.svg?6d8fbcbe76f3e6ec15638a945efa0c65"
        style="1.8rem 0 0 72px; height: 45px; padding-left: 10px; position: absolute; top: 50%; -ms-transform: translateY(-50%); transform: translateY(-50%);">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); line-height: 3.4rem; text-align: center; font-size: 1.5rem; font-family: 'montserratregular'; color: #fff; letter-spacing: 0.89px;">AUTOMATION TEST REPORT</div>
        </header> 
        <style>
            .card__footer {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                margin-bottom: 5%;
                background: #332b50;
                border: 2px solid #ccc;
                padding: 12px 10px 8px 12px;
            }
            .card__footer-section {
                text-align: center;
                width: 33%;
            }
            .footer-section__data {
                font-size: 2.6rem;
                font-weight: 900;
            }

            .footer-section__label {
                text-transform: uppercase;
                color: #fff;
                font-size: 10pt;

            }
        </style>
        </br>
        <p style="text-align:left; font-weight: bold;">
            Summary:
            <span style="float:right; font-weight: bold;">
                """
        + report_date
        + """
            </span>
        </p>
        <div class="card__footer">"""
        + info_body
        + """
            <div class="card__footer-section">
              <div class="footer-section__data" style="color:#98cc64">"""
        + pass_count
        + """</div>
              <div class="footer-section__label">Passed</div>
            </div>
            <div class="card__footer-section">
              <div class="footer-section__data" style="color:#fc6766">"""
        + fail_count
        + """</div>
              <div class="footer-section__label">Failed</div>
            </div>
            <div class="card__footer-section">
              <div class="footer-section__data" style="color:#ffd050">"""
        + skip_count
        + """</div>
              <div class="footer-section__label">Skipped</div>
            </div>
           <div class="card__footer-section">
              <div class="footer-section__data" style="color:#b13635">"""
        + error_count
        + """</div>
              <div class="footer-section__label">Error</div>
            </div>
            <div class="card__footer-section">
              <div class="footer-section__data" style="color:#fff">"""
        + total_tests
        + """</div>
              <div class="footer-section__label">Total</div>
            </div>
          </div>"""
        + body
        + """</p>"""
    )

    body = body.replace(
        """</td>
    </tr>
  </tbody>
</table>
            <table border="1" class="dataframe">
  <tbody>
    <tr>""",
        """</td>
    </tr>
    <tr>""",
    ).replace(
        """</td>
    </tr>
  </tbody>
</table><table border="1" class="dataframe">
  <tbody>
    <tr>""",
        """</td>
    </tr>
    <tr>""",
    )

    if conditions:
        for k in conditions.keys():
            try:
                conditions[k]["index"] = list(df.columns).index(k)
                width_body = ""
                w = 0
                for line in io.StringIO(body):
                    updated_body = False
                    if w == conditions[k]["index"]:
                        try:
                            if (
                                int(repr(line).split(">")[1].split("<")[0])
                                < conditions[k]["min"]
                            ):
                                if "color: black" in repr(line):
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            "color: black",
                                            "color: " + conditions[k]["min_color"],
                                        )[1:]
                                    )
                                elif "color: white" in repr(line):
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            "color: white",
                                            "color: " + conditions[k]["min_color"],
                                        )[1:]
                                    )
                                else:
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            '">',
                                            "; color: "
                                            + conditions[k]["min_color"]
                                            + '">',
                                        )[1:]
                                    )
                                updated_body = True
                            elif (
                                int(repr(line).split(">")[1].split("<")[0])
                                > conditions[k]["max"]
                            ):
                                if "color: black" in repr(line):
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            "color: black",
                                            "color: " + conditions[k]["max_color"],
                                        )[1:]
                                    )
                                elif "color: white" in repr(line):
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            "color: white",
                                            "color: " + conditions[k]["max_color"],
                                        )[1:]
                                    )
                                else:
                                    width_body = (
                                        width_body
                                        + repr(line).replace(
                                            '">',
                                            "; color: "
                                            + conditions[k]["max_color"]
                                            + '">',
                                        )[1:]
                                    )
                                updated_body = True
                        except:
                            pass
                    if not updated_body:
                        width_body = width_body + repr(line)[1:]

                    if (
                        str(repr(line))[:10] == "'      <td"
                        or str(repr(line))[:10] == "'      <th"
                    ):
                        if w == len(df.columns) - 1:
                            w = 0
                        else:
                            w += 1
                body = width_body[: len(width_body) - 1]
            except:
                pass

    if len(width_dict) == len(df.columns):
        width_body = ""
        w = 0
        if conditions:
            for line in body.split(r"\n'"):
                width_body = (
                    width_body
                    + repr(line).replace("width: auto", "width: " + width_dict[w])[1:]
                )
                if (
                    str(repr(line))[:10] == "'      <td"
                    or str(repr(line))[:10] == "'      <th"
                ):
                    if w == len(df.columns) - 1:
                        w = 0
                    else:
                        w += 1
        else:
            for line in io.StringIO(body):
                width_body = (
                    width_body
                    + repr(line).replace("width: auto", "width: " + width_dict[w])[1:]
                )
                if (
                    str(repr(line))[:10] == "'      <td"
                    or str(repr(line))[:10] == "'      <th"
                ):
                    if w == len(df.columns) - 1:
                        w = 0
                    else:
                        w += 1
        return width_body[: len(width_body) - 1].replace("'", "")
    else:
        return body.replace(r"\n'", "")


def _format_argval(argval):
    """Remove newlines and limit max length

    From Allure-pytest logger (formats argument in the CLI live logs).
    Consider using the same function."""
    MAX_ARG_LENGTH = 100
    argval = argval.replace("\n", " ")
    if len(argval) > MAX_ARG_LENGTH:
        argval = argval[:3] + " ... " + argval[-MAX_ARG_LENGTH:]
    return argval


def build_data(alluredir):
    def _process_steps(session, node):
        if "start" in node:
            if session["start"] is None or node["start"] < session["start"]:
                session["start"] = node["start"]
            if session["stop"] is None or node["stop"] > session["stop"]:
                session["stop"] = node["stop"]

        if "steps" in node:
            for step in node["steps"]:
                _process_steps(session, step)

    json_results = [
        f for f in listdir(alluredir) if isfile(join(alluredir, f)) and "result" in f
    ]
    json_containers = [
        f for f in listdir(alluredir) if isfile(join(alluredir, f)) and "container" in f
    ]
    session = {
        "alluredir": alluredir,
        "start": None,
        "stop": None,
        "results": {
            "broken": 0,
            "failed": 0,
            "skipped": 0,
            "passed": 0,
        },
        "results_relative": {
            "broken": 0,
            "failed": 0,
            "skipped": 0,
            "passed": 0,
        },
        "total": 0,
    }

    data_containers = []
    for file in json_containers:
        with open(join(alluredir, file), encoding="utf-8") as f:
            container = json.load(f)
            data_containers.append(container)

    data_results = []
    rsl_mod = 0
    for file in json_results:
        rsl_mod += 1
        with open(join(alluredir, file), encoding="utf-8") as f:
            result = json.load(f)
            result["_lastmodified"] = os.path.getmtime(join(alluredir, file))

            data_results.append(result)
    for result in data_results:
        _process_steps(session, result)
        session["total"] += 1
        session["results"][result["status"]] += 1

        result["parents"] = []
        for container in data_containers:
            if "children" not in container:
                continue
            if result["uuid"] in container["children"]:
                result["parents"].append(container)
                if "befores" in container:
                    for before in container["befores"]:
                        _process_steps(session, before)
                if "afters" in container:
                    for after in container["afters"]:
                        _process_steps(session, after)

    if session["total"] == 0:
        warnings.warn("No test result files were found!")

    def getsortingkey(d):
        classification = {"broken": 0, "failed": 1, "skipped": 2, "passed": 3}
        return "{}-{}".format(classification[d["status"]], d["name"])

    sorted_results = sorted(data_results, key=getsortingkey)

    if session["start"] is not None:
        session["duration"] = str(
            timedelta(seconds=(session["stop"] - session["start"]) / 1000.0)
        )
        session["start"] = ctime(session["start"] / 1000.0)
        session["stop"] = ctime(session["stop"] / 1000.0)
    else:
        session["duration"] = "Not available"
        session["start"] = "Not available"
        session["stop"] = "Not available"

    for item in session["results"]:
        if session["total"] > 0:
            session["results_relative"][item] = "{:.2f}%".format(
                100 * session["results"][item] / session["total"]
            )
        else:
            session["results_relative"][item] = "Not available"

    return sorted_results, session


def write_to_csv(file_name="records.csv", rows=[]):
    fields = ["#", "Test", "status", "message"]
    # writing to csv file
    with open(file_name, "w") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
