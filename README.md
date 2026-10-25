
# recover_requirements# Python Requirements Recovery

A small Python utility that scans a directory containing multiple Python projects, finds Windows virtual environments (`venv` or `.venv`), and reconstructs a `requirements.txt` file from the package metadata available in each environment.

## Features

- Recursively searches for virtual environments named `venv` or `.venv`.
- Reads installed package names and versions from `.dist-info` and `.egg-info` metadata.
- Generates a pinned `requirements.txt` (`package==version`) in the parent project directory.
- Writes a `site-packages-folders.txt` inventory inside each virtual environment.
- Skips common irrelevant directories such as `.git`, `node_modules`, and `__pycache__`.
- Handles individual metadata-reading and filesystem errors without immediately stopping the entire scan.

## Requirements

- Python 3.8 or newer (the script uses `pathlib`, `os.walk`, and standard-library modules).
- A **Windows-style virtual environment** containing `Lib/site-packages`.

> Note: This script currently targets Windows virtual environments. It will not find the usual Linux/macOS `lib/pythonX.Y/site-packages` layout without modification.

## Usage

1. Save `recover_requirements.py` to a convenient location.
2. Run it with Python:

   ```bash
   python recover_requirements.py
   ```

3. When prompted, enter the path to the main folder that contains your projects. For example:

   ```text
   D:\Projects\Python
   ```

4. The script searches beneath that folder for `venv` and `.venv` directories.

For each virtual environment found, it creates:

- `requirements.txt` in the project folder (the parent directory of the virtual environment).
- `site-packages-folders.txt` inside the virtual environment directory.

## Example

Suppose your directory structure is:

```text
Projects/
└── MyDjangoProject/
    ├── manage.py
    └── venv/
        └── Lib/
            └── site-packages/
```

After running the script, the project may look like this:

```text
Projects/
└── MyDjangoProject/
    ├── manage.py
    ├── requirements.txt
    └── venv/
        ├── site-packages-folders.txt
        └── Lib/
            └── site-packages/
```

The generated `requirements.txt` contains entries similar to:

```text
Django==5.1.2
requests==2.32.3
```

The versions above are illustrative only; actual versions depend on the packages installed in your environment.

## Important Notes

- The generated `requirements.txt` is based on package metadata found in the virtual environment, not on a source-code dependency analysis.
- The script may include packages that were installed indirectly as dependencies of other packages.
- A package folder without readable `.dist-info` or `.egg-info` metadata may appear in `site-packages-folders.txt` but may not be included in `requirements.txt`.
- The script does not copy packages or rebuild the virtual environment; it only writes inventory files.
- Review the generated `requirements.txt` before using it to recreate an environment.
- Run the script only on folders you trust. It writes files into each discovered project's directory and virtual environment.

## Recreating an Environment

After reviewing the generated file, create and activate a new virtual environment in your project, then install the listed packages:

```bash
python -m venv .venv
```

Windows Command Prompt:

```bat
.venv\Scripts\activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

## Limitations

- Windows virtual environments only, as currently implemented.
- It does not detect packages installed outside the scanned virtual environment.
- It does not guarantee that every listed package is a direct dependency of your project.
- Some packages may require system libraries, environment variables, or other setup steps not captured in `requirements.txt`.

## Author and AI Assistance

This utility was created with assistance from **ChatGPT (OpenAI)**. ChatGPT helped draft the Python script and this README documentation. The project should be reviewed and tested by its maintainer before being used in important environments.

## License

No license has been specified yet. If you want others to use, modify, or distribute this project on GitHub, choose a license (for example, MIT) and add the corresponding `LICENSE` file. Until then, all rights are reserved by default.
