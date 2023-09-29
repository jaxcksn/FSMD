# INSTALLATION SCRIPT
from io import TextIOWrapper
import os
import platform
import shutil
import subprocess
import tempfile

import datetime
from enum import Enum

from rich import print as Print
from rich.prompt import Confirm
from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.status import Status
from rich.progress import Progress

import requests


def normPath(path):
    """
    Helper function to normalize the path.
    """
    return os.path.normpath(path)


def tStamp() -> str:
    return datetime.datetime.now().strftime("%m/%d %H:%M:%S")


class Result(Enum):
    SUCCESS = 1
    ERROR = 2
    WARN = 3
    OTHER = 4


class InstallerException(Exception):
    "An exception raised when installing Graphviz"
    additionalDetails: str

    def __init__(self, message: str, ad: str = "") -> None:
        self.message = message
        self.additionalDetails = ad
        super().__init__(self.message)


class Installer:
    basePath: str
    log: TextIOWrapper or None = None

    @staticmethod
    def printPanel(
        content: str, title: str, subtitle: str or None = None, padding: bool = False
    ):
        if not padding:
            Print(
                Align(
                    Panel(
                        content,
                        border_style="dim",
                        title=title,
                        subtitle=subtitle,
                        title_align="left",
                        subtitle_align="right",
                    ),
                    align="left",
                )
            )
        else:
            Print(
                Align(
                    Panel(
                        Padding(content, (2, 0, 2, 0)),
                        border_style="dim",
                        title=title,
                        subtitle=subtitle,
                        title_align="left",
                        subtitle_align="right",
                    ),
                    align="left",
                )
            )

    @staticmethod
    def promptUser(message: str) -> bool:
        ans = Confirm.ask(message)
        print("\033[A\033[2K\r", end="")
        return ans

    @staticmethod
    def printResult(result: Result, text: str) -> None:
        symbol = ""
        if result == Result.SUCCESS:
            symbol = "[bold green]✔[/]"
        elif result == Result.ERROR:
            symbol = "[bold red]✖[/]"
        elif result == Result.WARN:
            symbol = "[bold yellow]⚠[/]"
        else:
            symbol = "[bold blue]ℹ[/]"
        Print(f"{symbol} [dim]{text}[/]")

    @staticmethod
    def getInstaller():
        """
        Creates an installer for the specific platform.
        """
        sys = platform.system()
        if sys == "Windows":
            return WindowsInstaller()
        elif sys == "Darwin":
            return MacOsInstaller()
        else:
            raise InstallerException(
                "Automatic installation is not support for platform", ad=sys
            )

    @staticmethod
    def makeDir(dir: str):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

    def printInstallerInfo(self) -> None:
        Installer.printPanel(
            "This tool will install GraphViz on your computer",
            "Graphviz Automatic Installer",
            "Version 1.0.0",
            True,
        )
        Print("\n[bold]Starting Installation[/]")
        Print(f"[bold magenta]Platform: [/][reset]{platform.platform()}[/]")
        return

    def prepareLog(self) -> None:
        """
        Prepares the install log file for use, placing it in the temp directory,
        and renaming the old file (if it exists) to something else so a new one
        can be created.
        """
        TEMPDIR = (
            "/tmp" if platform.system() == "Darwin" else normPath(tempfile.gettempdir())
        )
        installFile = normPath(TEMPDIR + "/.CFSM_install_log")
        oldFile = normPath(TEMPDIR + "/.CFSM_install_log_old")

        if os.path.isfile(installFile):
            if os.path.isfile(oldFile):
                os.remove(oldFile)
            os.rename(installFile, oldFile)

        self.log = open(installFile, "w")
        Print(f"SUCCESS: Created new log file - " + tStamp(), file=self.log)

    def FinishInstall(self, statusCode: int):
        try:
            shutil.rmtree(normPath(self.basePath + "/test"))
        except Exception as e:
            print(e, file=self.log)

        if statusCode == 0:
            Print("\n[bold green]Successfully installed Graphviz[/]")
            exit(0)
        elif statusCode == 1:
            Print("\n[bold red]Failed to install Graphviz[/]")
            exit(1)
        elif statusCode == 2:
            Print(
                "\n[bold yellow]Graphviz may have been installed, but it was not on the path. Try manually linking it with homebrew, or adding it to the path. Then rerun the program.[/]"
            )
            exit(1)
        elif statusCode == 3:
            Print("\n[magenta]Graphviz is already installed.[/]")
            exit(0)
        else:
            exit(1)

    def initBasePath(self, base: str):
        Installer.makeDir(base)
        self.basePath = base
        Print(f"INFO: Created {base} - " + tStamp(), file=self.log)

    def __init__(self) -> None:
        self.prepareLog()
        self.printInstallerInfo()


class MacOsInstaller(Installer):
    def TestForDot(self, isFinalCheck: bool = False) -> bool:
        TESTPATH = self.basePath + "/test"

        Print(TESTPATH)
        spin = Status("Checking for Graphviz", spinner="dots")
        spin.start()
        Installer.makeDir(TESTPATH)
        with open(TESTPATH + "/sample.dot", "w") as samp:
            samp.write("digraph G {\n\ta -> b\n}")
            samp.close()
        try:
            subprocess.run(
                [
                    "dot",
                    "-Tpdf",
                    "-o",
                    TESTPATH + "/sample.pdf",
                    TESTPATH + "/sample.dot",
                ],
                stdout=self.log,
                stderr=self.log,
                check=True,
            )
            if os.path.isfile(TESTPATH + "/sample.pdf"):
                spin.stop()
                Installer.printResult(
                    Result.SUCCESS, "Graphviz is installed, and working."
                )
                return True
            else:
                spin.stop()
                if isFinalCheck:
                    Installer.printResult(
                        Result.ERROR,
                        "Graphviz was found, but did not work. Please check the .install_log file for details.",
                    )
                else:
                    Installer.printResult(
                        Result.OTHER,
                        "Graphviz was not found. Continuing with installation.",
                    )
                return False
        except subprocess.CalledProcessError:
            spin.stop()
            if isFinalCheck:
                Installer.printResult(
                    Result.ERROR,
                    "Graphviz was not found. Please check the .install_log file for details.",
                )
            else:
                Installer.printResult(
                    Result.OTHER,
                    "Graphviz was not found. Continuing with installation.",
                )
            return False
        except Exception as e:
            spin.stop()
            Installer.printResult(
                Result.ERROR,
                "There was an error checking for Graphviz, please see .install_log for details.",
            )
            Print(e, file=self.log)

    def CheckForBrew(self):
        spin = Status("Checking for Homebrew", spinner="dots")
        spin.start()
        try:
            subprocess.run(
                ["brew", "--version"], stderr=self.log, stdout=self.log, check=True
            )
            spin.stop()
            Installer.printResult(Result.SUCCESS, "Homebrew was found.")
            return True
        except subprocess.CalledProcessError:
            spin.stop()
            Installer.printResult(Result.ERROR, "Homebrew was not found.")

            Print(
                "\n[red bold]ERROR[/] [link=https://brew.sh/]Homebrew[/link] must be installed to automatically install Graphviz"
            )
            Print(
                "ERROR: Homebrew must be installed to automatically install Graphviz - "
                + tStamp(),
                file=self.log,
            )
            exit(1)

    def InstallGraphviz(self):
        spin = Status("Installing Graphviz (This may take a bit...)")
        spin.start()
        try:
            subprocess.run(
                ["brew", "install", "graphviz"],
                stderr=self.log,
                stdout=self.log,
                check=True,
            )
            spin.stop()
            Installer.printResult(Result.SUCCESS, "Installed Graphviz")
            return True
        except subprocess.CalledProcessError:
            spin.stop()
            Installer.printResult(Result.ERROR, "Failed to Install Graphviz")
            Print(
                "\n[red bold]ERROR[/] Failed to install Graphviz, check .install_log file for details."
            )
            Print(
                "ERROR: Failed to install Graphviz, see above output for details - "
                + tStamp(),
                file=self.log,
            )
            exit(1)

    def LinkGraphviz(self):
        spin = Status("Attempting to link Graphviz manually", spinner="dots")
        spin.start()
        try:
            subprocess.run(
                ["brew", "link", "--overwrite", "graphviz"],
                stderr=self.log,
                stdout=self.log,
                check=True,
            )
            spin.stop()
            Installer.printResult(Result.SUCCESS, "Graphviz was linked by Homebrew.")
            return True
        except subprocess.CalledProcessError:
            spin.stop()
            Installer.printResult(Result.SUCCESS, "Failed to Link")
            Print(
                "\n[red bold]ERROR[/] Failed to link Graphviz, check .install_log file for details.\nYou can also try to add Graphviz to the path yourself, then rerun this command."
            )
            Print(
                "ERROR: Failed to link Graphviz, see above output. - " + tStamp(),
                file=self.log,
            )
            exit(1)

    def StartInstall(self) -> None:
        if not self.TestForDot():
            self.CheckForBrew()
            self.InstallGraphviz()
            if not self.TestForDot():
                if Installer.promptUser(
                    "Would you like to try to manually link Graphviz?"
                ):
                    self.LinkGraphviz()

                    if not self.TestForDot(isFinalCheck=True):
                        self.FinishInstall(1)
                    else:
                        self.FinishInstall(0)
                else:
                    self.FinishInstall(2)
            else:
                self.FinishInstall(0)
        self.FinishInstall(3)

    def __init__(self) -> None:
        base = normPath(
            os.path.join(
                os.environ["HOME"], "Library", "Application Support", "CreateFSM"
            )
        )

        super().__init__()
        self.initBasePath(base)
        self.StartInstall()


class WindowsInstaller(Installer):
    def TestForDot(self, addBase: bool = False):
        if addBase:
            path = os.environ["PATH"]
            os.environ["PATH"] += ";" + str(
                os.path.join(self.basePath, "Graphviz", "bin")
            )

        spin = Status("Checking for Graphviz", spinner="dots")
        spin.start()

        TESTPATH = os.path.join(self.basePath + "test")
        Installer.makeDir(TESTPATH)

        dotPath = os.path.join(TESTPATH, "sample.dot")
        pdfPath = os.path.join(TESTPATH, "sample.pdf")

        with open(normPath(dotPath), "w") as samp:
            samp.write("digraph G {\n\ta -> b\n}")
            samp.close()
        try:
            subprocess.run(
                [
                    "dot",
                    "-Tpdf",
                    "-o",
                    str(pdfPath),
                    str(dotPath),
                ],
                stdout=self.log,
                stderr=self.log,
                check=True,
            )
            if os.path.exists(pdfPath):
                if addBase:
                    os.environ["PATH"] = path

                spin.stop()
                Installer.printResult(
                    Result.SUCCESS, "Graphviz is installed, and working."
                )
                return True
            else:
                spin.stop()
                Installer.printResult(Result.ERROR, "Graphviz is not working properly")
                return False
        except Exception as e:
            spin.stop()
            Installer.printResult(Result.ERROR, "Graphviz is not installed.")
            Print(e, file=self.log)
            return False

    def DownloadGraphviz(self):
        try:
            zipfile = os.path.join(self.basePath, "Graphviz.zip")
            if os.path.isfile(zipfile):
                os.remove(zipfile)

            r = requests.get(
                "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/9.0.0/windows_10_msbuild_Release_graphviz-9.0.0-win32.zip",
                stream=True,
            )

            with Progress() as progress:
                task1 = progress.add_task(
                    "[blue]Downloading Graphviz...",
                    total=int(r.headers.get("Content-Length", 0)),
                )
                if r.status_code != 200:
                    raise InstallerException(
                        f"Request to {r.url} returned status code {r.status_code}"
                    )

                with open((zipfile), "wb") as f:
                    for data in r.iter_content(1024):
                        progress.update(task1, advance=len(data))
                        f.write(data)
                progress.stop()
                print("\033[A\033[2K\r", end="")
                Installer.printResult(
                    Result.SUCCESS, "Successfully downloaded Graphviz"
                )
                return True
        except Exception as e:
            Installer.printResult(Result.ERROR, "Failed to Download Graphviz")
            Print("\n[red bold]ERROR[/] Could not download Graphviz archive.")
            Print(e, file=self.log)
            return False

    def RemoveZip(self):
        zipfile = os.path.join(self.basePath, "Graphviz.zip")
        if os.path.isfile(zipfile):
            os.remove(zipfile)

    def ExtractGraphviz(self):
        spin = Status("Extracting Graphviz")
        spin.start()
        try:
            if os.path.exists(normPath(f"{self.basePath}\Graphviz.zip")):
                shutil.unpack_archive(
                    normPath(f"{self.basePath}\Graphviz.zip"), self.basePath
                )
                spin.stop()
                Installer.printResult(Result.SUCCESS, "Graphviz was extracted")
                self.RemoveZip()
                return True
            else:
                raise InstallerException("Graphviz.zip could not be found.")
        except Exception as e:
            Installer.printResult(Result.ERROR, "Failed to extract Graphviz")
            Print("\n[red bold]ERROR[/] Could not extract Graphviz archive.")
            Print(e, file=self.log)
            return False

    def StartInstall(self):
        if not self.TestForDot(addBase=True):
            self.initBasePath(self.basePath)
            if self.DownloadGraphviz():
                if not self.ExtractGraphviz():
                    self.FinishInstall(1)
                if not self.TestForDot(addBase=True):
                    self.FinishInstall(1)
                else:
                    self.FinishInstall(0)
            else:
                self.FinishInstall(1)
        self.FinishInstall(3)

    def __init__(self) -> None:
        base = normPath(os.getenv("LOCALAPPDATA") + "\CreateFSM")
        super().__init__()

        self.basePath = base
        self.StartInstall()
