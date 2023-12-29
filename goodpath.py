import pathlib as pl

def root_path_as_plPath():
    return (pl.Path(__file__).parent.resolve())

def root_path_as_str():
    return str(pl.Path(__file__).parent.resolve())
