import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _(feeder_dir, mo):
    get_feeders,set_feeders = mo.state(feeder_dir())
    return get_feeders, set_feeders


@app.cell
def _(get_feeders, mo):
    model_ui = mo.ui.dropdown(options=get_feeders(),value=get_feeders()[0],label="**Feeder**:")
    return (model_ui,)


@app.cell
def _(os):
    def feeder_dir(*args):
        return sorted([x for x in os.listdir(".") if os.path.exists(f"{x}/results.csv.gz")])

    return (feeder_dir,)


@app.cell
def _(feeder_dir, mo, set_feeders):
    refresh_ui = mo.ui.button(label="Refresh",on_click=lambda x:set_feeders(feeder_dir()))
    return (refresh_ui,)


@app.cell
def _(mo, model_ui, refresh_ui):
    mo.hstack([model_ui,refresh_ui],justify='start')
    return


@app.cell
def _(df, mo):
    loads = sorted(set([x.split()[0] for x in df.columns]))
    load_ui = mo.ui.dropdown(options=loads,value=loads[0],label="**Load**:")
    complex_ui = mo.ui.radio(options=["Real","Reactive"],value="Real",inline=True)
    voltage_ui = mo.ui.radio(options=["Magnitude","Angle"],value="Magnitude",inline=True,label="**Voltage**:")
    return complex_ui, load_ui, voltage_ui


@app.cell
def _(complex_ui, load_ui, mo, voltage_ui):
    mo.hstack([mo.hstack([load_ui,complex_ui],justify='start'),voltage_ui])
    return


@app.cell
def _(complex_ui, df, load_ui, np, plt, scipy, voltage_ui):
    _options = [
        x
        for x in df.columns
        if x.startswith(load_ui.value) and "Voltage" not in x
    ]
    _options
    fig, _ax = plt.subplots(3, 3, figsize=(16, 16))
    _units = {"Power":"kW", "Current":"A", "Admittance":"mS"}
    _zip = {"Power":"P", "Current": "I", "Admittance": "1/Z"}
    _base = {"A":0, "B":-120, "C":120}
    for _col, _channel in enumerate(_units):
        for _row, _phase in enumerate("ABC"):
            _column = f"{load_ui.value} {_channel} {_phase}"
            _voltage = f"{load_ui.value} Voltage {_phase}"
            if _column in df.columns and _voltage in df.columns:
                match complex_ui.value:
                    case "Real":
                        _X = np.array(df[_column]).real
                        _xlabel = f"Real {_channel}"
                    case "Reactive":
                        _X = np.array(df[_column]).imag
                        _xlabel = f"Reactive {_channel}"
                    case _:
                        raise ValueError(f"{complex_ui.value} is invalid")
                match voltage_ui.value:
                    case "Magnitude":
                        _Y = np.abs(df[_voltage]) / 1000
                        _ylabel = "Voltage magnitude (kV)"
                    case "Angle":
                        _Y = np.angle(df[_voltage]) * 180 / np.pi - _base[_phase]
                        _ylabel = "Voltage angle (deg)"
                    case _:
                        raise ValueError(f"{voltage_ui.value} is invalid")
                _ax[_row, _col].plot(_X, _Y, ".")
                if np.var(_X) > 0:
                    _fit = scipy.stats.linregress(_X, _Y)
                    _X = np.array([_X.min(), _X.max()])
                    _Y = _fit.slope * _X + _fit.intercept
                    _ax[_row, _col].plot(_X, _Y, "k", linewidth=2)
                    _ax[_row, _col].legend(
                        ["Data", f"$V.{_phase}$ = {_fit.slope*1000:.3f} x ${_zip[_channel]}.{_phase}$ {_fit.intercept*1000:+.1f}"]
                    )                
                _ax[_row, _col].set_title(f"{_channel} {_phase}")
                _ax[_row, _col].grid()
                _ax[_row, _col].set_xlabel(f"{_xlabel} ({_units[_channel]})")
                _ax[_row, _col].set_ylabel(_ylabel)
            else:
                _ax[_row, _col].set_axis_off()
                _ax[_row, _col].text(
                    0.5,
                    0.5,
                    f"No data for {_channel} {_phase}",
                    verticalalignment="center",
                    horizontalalignment="center",
                )
    return (fig,)


@app.cell
def _(df, load_ui):
    data = df.loc[
        :, [x for x in df.columns if x.split()[0] == load_ui.value]
    ].round(1)
    return (data,)


@app.cell
def _(data, fig, mo):
    mo.ui.tabs(
        {
            "Plots": fig,
            "Data": data,
        }
    )
    return


@app.cell
def _(mo, model_ui, pd):
    with mo.status.spinner("Loading data"):
        df = pd.read_csv(f"{model_ui.value}/results.csv.gz",parse_dates=[0],converters={"value":complex})
        df.columns = ["Timestamp","channel","value"]
        df["load"] = [x.split(".")[0] for x in df["channel"]]
        df["channel"] = [x.split(".")[1] for x in df["channel"]]
        df.set_index(["Timestamp","load","channel"],inplace=True)

        df = df.unstack(level=[1,2])
        df.columns = [f"{x[1]} {x[2].replace('constant_','').replace('_',' ')}".title() for x in df.columns]
        for _col in [x for x in df.columns if "Impedance" in x]:
            df[_col] = 1 / df[_col] * 1000
            df.rename({_col:_col.replace("Impedance","Admittance")},inplace=True,axis=1)
        for _col in [x for x in df.columns if "Power" in x]:
            df[_col] /= 1000
        df = df[sorted(df.columns)]
    return (df,)


@app.cell
def _():
    import os
    import math
    import re
    import scipy
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, os, pd, plt, scipy


if __name__ == "__main__":
    app.run()
