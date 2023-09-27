import typer
from typing_extensions import Annotated

import sys

from rich.status import Status
from rich import print as Print

import graphviz
import platform
import subprocess
import os
import yaml

from install import Installer

##################### INSTALL #####################################


log = open(".createFSM_log", "w")

app = typer.Typer()

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
EP = str.maketrans("E", "ε")


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
            "[red bold]\nDot command could not be found.[/]\nPlease run [bold on black]createFSM install[/] to install GraphViz\nOr view the [link=https://google.com]README[/] for more info."
        )
        return False


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
    g.edge(start, end, label.translate(EP))


def createFSM(fsmFile: str, outputDir: str):
    spin = Status("Creating FSM Diagram", spinner="dots")
    spin.start()
    with open(fsmFile, "r") as f:
        data = yaml.safe_load(f)
        G = graphviz.Digraph(
            data["filename"],
            format="png",
            node_attr={"fontname": "Arial,sans-serif"},
            edge_attr={"fontname": "Arial,sans-serif"},
            directory=sys.argv[2],
        )
        G.graph_attr["rankdir"] = "LR"
        G.graph_attr["size"] = "ideal"
        G.graph_attr["ratio"] = "auto"
        G.graph_attr["fontname"] = "Arial,sans-serif"
        # Initial State
        iS(G, str(data["startstate"]["state"]), data["startstate"]["isfinal"])
        # Setup Nodes
        for state in data["states"]:
            s(G, str(state), state in data["finalstates"])
        # Setup Edges
        for edge in data["edges"]:
            parts = edge.split(";")
            e(G, parts[0], parts[1], parts[2])
        G.filename = data["filename"]
        G.render(directory=outputDir).replace("\\", "/")
        spin.stop()
        Print(f"[bold blue]File output to: {outputDir}/{data['filename']}.png[/]")


@app.command()
def install():
    installer = Installer.getInstaller()


@app.command()
def main(input: str, outputdir: str):
    """
    Generates an image of an FSM, using Graphviz
    """
    if dotSetup():
        createFSM(input, outputdir)


if __name__ == "__main__":
    app()
