from typing import Sequence

import numpy as np
from ortools.sat.python.cp_model import CpModel, CpSolver, IntVar


def schedule(job_times: Sequence[int], n_machines: int) -> float:
    """Schedule independent jobs on parallel machines with CP Solver."""
    scheduler = Scheduler(job_times, n_machines)
    return scheduler.schedule()


class Scheduler:
    def __init__(self, job_times: Sequence[int], n_machines: int):
        self.job_times = job_times
        self.n_jobs = len(job_times)
        self.n_machines = n_machines
        self.upper_bound = sum(job_times)

    def schedule(self) -> float:
        model = CpModel()
        jobs = []

        self._add_bool_vars(model, jobs)
        self._add_single_machine_constraints(model, jobs)
        machine_makespans = self._add_machine_makespan_constraints(model, jobs)
        makespan = self._define_objective(model, machine_makespans)
        model.Minimize(makespan)

        solver = CpSolver()
        solver.Solve(model)

        self._print_results(solver, jobs)
        return solver.ObjectiveValue()

    def _add_bool_vars(self, model: CpModel, jobs: list) -> None:
        """Add boolean vars indicating if job j is scheduled on machine i."""
        for i in range(self.n_machines):
            jobs.append([
                model.NewBoolVar(f'Job [{i, j}]')
                for j, job in enumerate(self.job_times)
            ])

    def _add_single_machine_constraints(self, model: CpModel, jobs: list) -> None:
        """Add constraint that job can be scheduled on only one machine."""
        for j in range(self.n_jobs):
            model.Add(sum(jobs[i][j] for i in range(self.n_machines)) == 1)

    def _add_machine_makespan_constraints(self, model: CpModel, jobs: list) -> list:
        """Define that sum of jobs running on a machine is its makespan."""
        machine_makespans = []
        for i in range(self.n_machines):
            machine_makespan = model.NewIntVar(0, self.upper_bound, f'machine_{i}_makespan')
            model.Add(machine_makespan == np.dot(jobs[i], self.job_times))
            machine_makespans.append(machine_makespan)
        return machine_makespans

    def _define_objective(self, model: CpModel, machine_makespans: list) -> IntVar:
        """Define scheduling objective."""
        makespan = model.NewIntVar(0, self.upper_bound, 'makespan')
        model.AddMaxEquality(
            makespan,
            machine_makespans
        )
        return makespan

    @staticmethod
    def _print_results(solver: CpSolver, jobs: list) -> None:
        print("Optimal makespan: ", solver.ObjectiveValue())
        for i, row in enumerate(jobs):
            scheduled = tuple(index for index, job in enumerate(row) if solver.Value(job))
            print(f"Machine {i}: {scheduled}")
