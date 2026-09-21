"""Execute DATA_REVIEW.ipynb with IPython and save its real outputs in place.

Uses the existing Python environment, without requiring a Jupyter server.
The notebook can also be opened and Run All in a normal Jupyter frontend.
"""
import json
import os
from pathlib import Path
import sys
import tempfile

from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
from traitlets.config import Config


def main():
    lab = Path(__file__).resolve().parents[1]
    path = lab / "DATA_REVIEW.ipynb"
    notebook = json.loads(path.read_text())
    os.chdir(lab)
    with tempfile.TemporaryDirectory(prefix="election-mpl-") as cache:
        os.environ.setdefault("MPLCONFIGDIR", cache)
        os.environ.setdefault("IPYTHONDIR", str(Path(cache) / "ipython"))
        config = Config()
        config.HistoryManager.hist_file = ":memory:"
        shell = InteractiveShell.instance(config=config)
        count = 0
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            count += 1
            with capture_output() as captured:
                result = shell.run_cell("".join(cell["source"]), store_history=True)
            cell["execution_count"] = count
            outputs = []
            for channel in ("stdout", "stderr"):
                value = getattr(captured, channel)
                if value:
                    outputs.append(dict(output_type="stream", name=channel, text=value))
            for output in captured.outputs:
                outputs.append(dict(output_type="display_data", data=output.data, metadata=output.metadata))
            cell["outputs"] = outputs
            error = result.error_before_exec or result.error_in_exec
            if error:
                cell["outputs"].append(dict(output_type="error", ename=type(error).__name__,
                                            evalue=str(error), traceback=[]))
                path.write_text(json.dumps(notebook, indent=1) + "\n")
                raise RuntimeError(f"Notebook cell {count} failed") from error
            print(f"Executed cell {count}: {len(outputs)} output blocks")
    notebook["metadata"]["language_info"]["version"] = sys.version.split()[0]
    path.write_text(json.dumps(notebook, indent=1) + "\n")
    print(f"Saved executed notebook: {path}")


if __name__ == "__main__":
    main()
