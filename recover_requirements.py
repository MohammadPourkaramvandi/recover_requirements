import os
from pathlib import Path
from email.parser import Parser


def get_installed_packages(site_packages):
    """استخراج نام و نسخه پکیج‌ها از فایل‌های متادیتا."""

    packages = {}

    for item in site_packages.iterdir():
        if not item.is_dir():
            continue

        # پوشه‌های مربوط به متادیتای پکیج‌ها
        if item.name.endswith(".dist-info"):
            metadata_file = item / "METADATA"

        elif item.name.endswith(".egg-info"):
            metadata_file = item / "PKG-INFO"

        else:
            continue

        if not metadata_file.is_file():
            continue

        try:
            with metadata_file.open(
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:
                metadata = Parser().parsestr(file.read())

            name = metadata.get("Name")
            version = metadata.get("Version")

            if name and version:
                packages[name.lower()] = (name, version)

        except (OSError, ValueError) as error:
            print(f"Error reading {metadata_file}: {error}")

    return sorted(packages.values(), key=lambda item: item[0].lower())


def get_folder_names(site_packages):
    """استخراج نام پوشه‌های موجود در site-packages."""

    folders = []

    for item in site_packages.iterdir():
        if not item.is_dir():
            continue

        if item.name.endswith((".dist-info", ".egg-info")):
            continue

        if item.name == "__pycache__":
            continue

        folders.append(item.name)

    return sorted(set(folders), key=str.lower)


def recover_project(venv_path):
    """بازیابی اطلاعات یک محیط مجازی."""

    site_packages = venv_path / "Lib" / "site-packages"

    if not site_packages.is_dir():
        return

    project_path = venv_path.parent

    print(f"\nProject: {project_path}")

    packages = get_installed_packages(site_packages)
    folders = get_folder_names(site_packages)

    # فایل requirements.txt در پوشه اصلی پروژه
    requirements_file = project_path / "requirements.txt"

    with requirements_file.open("w", encoding="utf-8") as file:
        for name, version in packages:
            file.write(f"{name}=={version}\n")

    # ثبت نام پوشه‌ها داخل پوشه venv
    folders_file = venv_path / "site-packages-folders.txt"

    with folders_file.open("w", encoding="utf-8") as file:
        for folder in folders:
            file.write(folder + "\n")

    print(f"Packages recovered: {len(packages)}")
    print(f"Requirements: {requirements_file}")
    print(f"Folder list: {folders_file}")


def main():
    print("=" * 50)
    print("Python Requirements Recovery")
    print("=" * 50)

    root_input = input(
        "\nEnter the main folder containing your projects: "
    ).strip().strip('"')

    root = Path(root_input)

    if not root.is_dir():
        print("\nError: The specified folder does not exist.")
        input("Press Enter to exit...")
        return

    found_venvs = []

    # پیدا کردن تمام venvهای موجود در پروژه‌ها
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in {
                ".git",
                "node_modules",
                "__pycache__"
            }
        ]

        current_path = Path(current_root)

        if current_path.name.lower() in {"venv", ".venv"}:
            site_packages = (
                current_path / "Lib" / "site-packages"
            )

            if site_packages.is_dir():
                found_venvs.append(current_path)

            # وارد محیط مجازی نمی‌شویم؛ فقط یک بار بررسی می‌کنیم.
            dirs.clear()

    if not found_venvs:
        print("\nNo virtual environments were found.")
    else:
        print(f"\nFound {len(found_venvs)} virtual environment(s).")

        for venv_path in found_venvs:
            try:
                recover_project(venv_path)
            except OSError as error:
                print(f"Could not process {venv_path}: {error}")

    print("\nRecovery finished.")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
