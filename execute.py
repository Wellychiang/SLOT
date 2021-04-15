import pytest


if __name__ == '__main__':

    # pytest.main(['-vvsm', 'd'])
    # pytest.main(['-vvs'])

    pytest.main(['-vvs', '--reruns', '3', '--reruns-delay', '2', '--alluredir', 'report'])
