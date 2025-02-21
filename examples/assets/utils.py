def get_path(path: str) -> str:
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, path)
