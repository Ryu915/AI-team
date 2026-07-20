from pathlib import Path
import shutil

def apply_node(state):
    print(f"\n=========Apply Node=========")

    project_path = Path(state["project_path"])

    changes = state["code_output"].changes

    for change in changes:

        file_path = project_path / change.file_path
        # make sure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if change.action == "create":
            file_path.write_text(change.code, encoding="utf-8")
            print(f"\nCreated: {change.file_path}")

        if change.action == "update":
            # Backup the existing file
            if file_path.exists():
                backup = file_path.with_suffix(file_path.suffix + ".bak")
                shutil.copy(file_path, backup)

            file_path.write_text(change.code, encoding="utf-8")
            print(f"Updated: {change.file_path}")

        if change.action == "delete":
            if file_path.exists():
                file_path.unlink()
                print(f"Deleted: {change.file_path}")

    return state