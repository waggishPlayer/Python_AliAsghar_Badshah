import subprocess
import sys
from pathlib import Path
from typing import List

def run_command(cmd: List[str], description: str) -> bool:
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error while {description}:")
        print((e.stderr or str(e)).strip())
        return False
    except FileNotFoundError:
        print(f"Error while {description}: command not found")
        return False

#To set up the development environment and install all the dependencies
def main() -> None:
    root_dir = Path(__file__).parent.parent
    venv_dir = root_dir / "venv"
    requirements_file = root_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"Error: {requirements_file} not found")
        sys.exit(1)
    
    success = True
    
    success &= run_command(
        [sys.executable, "-m", "venv", str(venv_dir)],
        "Creating virtual environment"
    )
    
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python"
    else:
        python_exe = venv_dir / "bin" / "python"
    
    success &= run_command(
        [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrading pip"
    )
    
    success &= run_command(
        [str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)],
        "Installing dependencies"
    )
    
    if success:
        if sys.platform == "win32":
            print(f"Activate with: {venv_dir}\\Scripts\\activate")
        else:
            print(f"Activate with: source {venv_dir}/bin/activate")
    else:
        print("Setup failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
