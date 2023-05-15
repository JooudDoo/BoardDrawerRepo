try:
    from .GUI.test_debug_window import run_tests as debug_tests
    from .GUI.test_settings_bar import run_tests as settings_bar_tests

    debug_tests()
    settings_bar_tests()
except ImportError as err:
    print(f"Could't run GUI tests:\n {err}")