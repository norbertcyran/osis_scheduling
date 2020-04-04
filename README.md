## Install

1. Install [poetry](https://python-poetry.org/docs/)
2. Run `poetry install`

To activate shell, run `poetry shell`

## Tests
With activated shell, run `pytest`

## Usage
Use `schedule(job_times, n_machines)` function for scheduling independent jobs
on n machines. `job_times` should be a sequence of execution times of consecutive jobs.
