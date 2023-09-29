import re
from typing_extensions import Annotated
import typer

import sys

from rich.status import Status
from rich import print as Print

import graphviz
import platform
import subprocess
import os
import yaml
import tempfile

from FSMD.install import Installer

TEMPDIR = (
    "/tmp" if platform.system() == "Darwin" else os.path.normpath(tempfile.gettempdir())
)

doEps = False


log = open(TEMPDIR + "/.createFSM_log", "w+")

app = typer.Typer()
create_app = typer.Typer()
app.add_typer(
    create_app,
    name="create",
    help="Creates a diagram, run 'FSMD create --help' for details",
)

EP = str.maketrans("E", "ε")
SUB_TRANS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def dotSetup():
    if platform.system() == "Windows":
        os.environ["Path"] += ";" + os.join.path(
            os.getenv("LOCALAPPDATA"), "CreateFSM", "Graphviz", "bin"
        )
    try:
        subprocess.run(["dot", "--version"], stderr=log, stdout=log, check=True)
        return True
    except Exception as e:
        Print(
            "[red bold]\nDot command could not be found.[/]\nPlease run [bold on black]FSMD install[/] to install GraphViz\nOr view the [link=https://github.com/jaxcksn/FSMD]README[/] for more info."
        )
        return False


def toSub(match):
    digit = str(match.group(1))
    subscripted_digit = digit.translate(SUB_TRANS)
    return subscripted_digit


def addSubscripts(name):
    pattern = r"_(\d)"
    result = re.sub(pattern, toSub, name)
    return result


# Adds the inital state.
def iS(g: graphviz.Digraph, startingState: str, acceptsEmpty: bool = False):
    g.node("none", None, shape="point", style="invis")
    if acceptsEmpty:
        shapeType = "doubleCircle"
    else:
        shapeType = "circle"

    g.node(startingState, shape=shapeType)
    g.edge("none", startingState)


# Adds a state
def s(g: graphviz.Digraph, name: str, accepted: bool = False):
    g.node(name, shape="doublecircle" if accepted else "circle")


# Adds an edge
def e(g: graphviz.Digraph, start: str, end: str, label: str):
    g.edge(start, end, label.translate(EP) if doEps else label)


def createDiagram(data, outputDir, format):
    spin = Status("Creating FSM Diagram", spinner="dots")
    spin.start()
    G = graphviz.Digraph(
        data["filename"],
        format=format,
        node_attr={"fontname": "Arial,sans-serif"},
        edge_attr={"fontname": "Arial,sans-serif"},
        directory=sys.argv[2],
    )
    G.graph_attr["rankdir"] = "LR"
    G.graph_attr["size"] = "ideal"
    G.graph_attr["ratio"] = "auto"
    G.graph_attr["fontname"] = "Arial,sans-serif"
    # Initial State
    iS(
        G,
        addSubscripts(str(data["startstate"])),
        data["startstate"] in data["finalstates"],
    )
    # Setup Nodes
    for state in data["states"]:
        s(G, addSubscripts(str(state)), state in data["finalstates"])
    # Setup Edges
    for edge in data["transitions"]:
        parts = edge.split(";")
        e(G, addSubscripts(parts[0]), addSubscripts(parts[1]), parts[2])
    G.filename = data["filename"]
    G.render(directory=outputDir).replace("\\", "/")
    spin.stop()
    Print(f"[bold blue]File output to: {outputDir}/{data['filename']}.{format}[/]")


def createFSM(fsmFile: str, outputDir: str, format: str):
    with open(fsmFile, "r") as f:
        data = yaml.safe_load(f)
        createDiagram(data, outputDir, format)


@app.command()
def install():
    """
    Runs the automatic installer, only supported by Windows and MacOS
    """
    installer = Installer.getInstaller()


@create_app.command("svg")
def svg(
    input: str,
    outputdir: str,
    epsilon: Annotated[
        bool,
        typer.Option(
            "--epsilon",
            "-E",
            help="Turns 'E' into epsilon for non-deterministic automata.",
        ),
    ] = False,
):
    """
    Generates an SVG diagram of an FSM from an input file.
    """
    doEps = epsilon
    if dotSetup():
        createFSM(input, outputdir, "svg")


@create_app.command("png")
def png(
    input: str,
    outputdir: str,
    epsilon: Annotated[
        bool,
        typer.Option(
            "--epsilon",
            "-E",
            help="Turns 'E' into epsilon for non-deterministic automata.",
        ),
    ] = False,
):
    """
    Generates an PNG diagram of an FSM from an input file.
    """
    doEps = epsilon
    if dotSetup():
        createFSM(input, outputdir, "png")


def run():
    app()


if __name__ == "__main__":
    app()
