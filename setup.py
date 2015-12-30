from cx_Freeze import setup, Executable

setup(
    name = 'tic-tac-toe',
    version = '1.0.1',
    description = 'Simple Tic-Tac-Toe built in python',
    executables = [Executable(
                      script='tic-tac-toe.py',
                      base='Win32GUI',
                      icon='icons/t3.ico'
                  )]
)
