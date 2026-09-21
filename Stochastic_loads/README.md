# Stochastic Load Study

This example illustrates how to use the time-series solver to run a stochastic load study that estimates voltage sensitivity at each load bus.

## Running analysis

To update the results run the command

    ./run_study.sh

## Viewing results

The results are posted in folders for each feeder model.  To view the results run the command

    gridlabd shell
    marimo run plot_results.py

Note that all voltage angles are plotted with respect the phases' base angle, i.e., 0 for phase A, -120 for phase B, and 120 for phase C.

## Changing the study size

The default study size is about 750 trials (equivalent to about 1 month of hourly trials).  To increase the study size, change the `stoptime` value on line 16 of the file `study_model.glm`.  

## Methodology

The analysis methodology uses an independent random uniform scalar applied to every load every hour. Note that the real and reactive power are scaled by the same value, resulting in the same power factor for each load during each trial.

## Caveats

All the loads are changed every hours. Consequently if any controls respond to the changes, such as regulators changing tap settings, these changes will happen in the minutes following the load change. However, the voltage response at each load is collected immediately after the load is changed. Thus the final voltage after the controls have completed their response is never observed. As a result, the data collected is the initial (i.e., worst case) voltage and not the final (i.e., best case) voltage.
