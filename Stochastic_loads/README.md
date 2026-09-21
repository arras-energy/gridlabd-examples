# Stochastic Load Study

This example illustrates how to use the time-series solver to run a stochastic load study that estimates voltage sensitivity at each load bus.

## Running analysis

To update the results run the command

    ./run_study.sh

## Viewing results

The results are posted in folders for each feeder model.  To view the results run the command

    gridlabd shell
    marimo run plot_results.py

