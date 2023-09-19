import os

from typing import Dict


def get_project_level() -> str:

    current_path = os.getcwd().split('/')

    for i in range(1, len(current_path)):
        candidate_path = '/'.join(current_path[:-i])

        candidate_path_dirs = os.listdir(candidate_path)
        if '.git' in candidate_path_dirs:
            return i * '../'

    raise EOFError('No parent project directory found')


PROJECT_LEVEL = get_project_level()


paths: Dict[str, str] = {
    'data': os.path.join(PROJECT_LEVEL, 'data'),
}
