from hn3ttk import __version__


def test_package_version() -> None:
    assert __version__ == "0.1.0"


if __name__ == "__main__":
    test_package_version()
    print("All package metadata tests passed.")
