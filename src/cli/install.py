import logging
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from settings import ASSETS_DIR, BASE_DIR

TEMPLATE_XML = ASSETS_DIR / "munchkin_template.xml"
TASK_NAME = "MunchkinDaemon"
PYTHON_PATH = Path(sys.executable).resolve().parent


def get_user_and_sid():
    try:
        # Run the whoami /user command
        result = subprocess.run(
            ["whoami", "/user"], capture_output=True, text=True, check=True
        )

        # Output will look like:
        # USERNAME SID

        lines = result.stdout.strip().splitlines()
        if len(lines) < 2:
            raise ValueError("Unexpected whoami output format")

        # The second line contains the actual data
        parts = lines[-1].split()

        return parts

    except subprocess.CalledProcessError as e:
        logging.error(f"Error running whoami: {e}")
        return None, None


def generate_task_xml(
    template_path: Path = TEMPLATE_XML, output_path: Path = BASE_DIR / "temp.xml"
):
    full_user, sid = get_user_and_sid()
    python_exe = PYTHON_PATH / "pythonw.exe"
    daemon_py_path = BASE_DIR / "daemon.py"

    with open(template_path, "r", encoding="utf-16") as f:
        xml_content = f.read()

    # Substitute placeholders
    xml_content = (
        xml_content.replace("{{USER}}", full_user)
        .replace("{{PYTHONW_PATH}}", f'"{python_exe}"')
        .replace("{{DAEMON_PATH}}", f'"{daemon_py_path}"')
        .replace("{{SID}}", sid)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)


@click.command()
def install():
    """Run munchkin at logon"""
    if sys.platform == "win32":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
            tmp_path = Path(tmp.name)

        try:
            generate_task_xml(TEMPLATE_XML, tmp_path)

            subprocess.run(
                ["schtasks", "/Create", "/TN", TASK_NAME, "/XML", str(tmp_path), "/F"],
                check=True,
            )
            click.echo("Scheduled task 'MunchkinDaemon' installed.")
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
                click.echo("Temporary XML file deleted.")
    else:
        click.echo("Whoops, this hasn't been implemented yet!")
