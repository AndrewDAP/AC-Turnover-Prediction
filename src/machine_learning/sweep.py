"""
Hyperparameter sweeps module
"""
from wandb import agent


def run_sweep(train: callable, sweep_id: str):
    """
    Run a sweep using a training method
    Args:
        train : The training method to run for the sweep
        sweep_id : ID of the sweep
    """

    agent(
        sweep_id,
        project="alayacare",
        function=train,
        count=6,
    )
