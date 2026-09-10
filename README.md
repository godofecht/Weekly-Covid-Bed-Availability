# Weekly-Covid-Bed-Availability

Renders an animation of US deaths per 100,000 against ICU bed occupancy, one
frame per day, from two public datasets.

`7dayvis.py` pulls both sources live at run time:

| Source | Used for |
|---|---|
| CDC NHSN `covid19-NatEst.csv` | Estimated ICU beds occupied by any patient, per state. |
| JHU CSSE `time_series_covid19_deaths_US.csv` | Cumulative deaths and state populations. |

ICU occupancy is smoothed with a 7 day rolling mean before plotting, because the
raw series has a strong weekday reporting pattern that otherwise dominates the
animation. Deaths are normalised to population so states are comparable.

Each date becomes a scatter frame, and the frames are written straight to
`deaths-vs-beds.mp4` at 10 fps through `imageio`.

## Run

```bash
pip install pandas matplotlib imageio imageio-ffmpeg
python 7dayvis.py
```

The CDC endpoint is the archived NHSN patient impact report. If it moves, the
first line of the script is the only thing that needs changing.
