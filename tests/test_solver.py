from scheduling.solver import schedule

test_jobs = (3, 4, 6, 2, 2, 8)
n_machines = 3


def test_scheduling():
    assert schedule(test_jobs, n_machines) == 9.0
