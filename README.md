# Weekly-Covid-Bed-Availability

Weekly US hospital bed availability, pulled from the CDC NHSN patient impact report.

## What this is

A short Python script that makes a video from two public COVID-19 datasets from 2020. Each frame is one day. Each US state is a circle: across, its COVID-19 deaths per 100,000 people so far; up, the share of its hospital intensive care unit (ICU) beds in use, averaged over 7 days. Bigger circles are states with more people. Played in order, the frames show states moving as the first wave of the pandemic spread.

The original CDC data link no longer works. "Run it" below shows how to point the script at an archived copy, which was tested and works.

## What you can learn from it

- Statistics: moving averages. ICU use is smoothed with a 7 day rolling mean because hospitals report less at weekends, and that weekly pattern would otherwise dominate the picture.
- Statistics: rates. Deaths are divided by population and multiplied by 100,000, so a small state and a large state can be compared fairly.
- Statistics: scatter plots and correlation, and why a pattern between two variables does not prove one causes the other.
- Geography: how one event affects places differently, for example the early peak in New York and New Jersey.
- Computer Science: loading data from the web, reshaping tables with pandas, and making a video one frame at a time.

## Run it

### On your own computer

**You will need:**

- [Python](https://www.python.org/downloads/) 3.11. Newer versions of Python cannot install the older pandas the script needs.
- An internet connection. The script downloads about 12 MB of data.

Tested on macOS with Python 3.11 and pandas 1.5.3.

1. Download the code:

   ```sh
   git clone https://github.com/godofecht/Weekly-Covid-Bed-Availability.git
   cd Weekly-Covid-Bed-Availability
   ```

2. Install the libraries. pandas must be older than version 2, because the script relies on how pandas 1 added up tables that contain text.

   ```sh
   python3.11 -m pip install "pandas<2" "numpy<2" matplotlib imageio imageio-ffmpeg
   ```

3. Open **7dayvis.py** and replace the web address on line 5 with an archived copy of the CDC file. Line 5 should read:

   ```python
   natest = read_csv('https://web.archive.org/web/20220604130041id_/https://www.cdc.gov/nhsn/pdfs/covid19/covid19-NatEst.csv')
   ```

4. Run it:

   ```sh
   python3.11 7dayvis.py
   ```

It prints one dot per frame, about 70 in all. When it finishes there is a file called `deaths-vs-beds.mp4` in the folder. It is a 640 by 480 video, about 7 seconds long at 10 frames per second. You may also see warnings about `imread`; they do not stop the script.

## How it works

1. Read the CDC National Healthcare Safety Network (NHSN) estimates. Keep the ICU column, turn the table so each state is a column, and take a 7 day rolling mean.
2. Read the Johns Hopkins University (JHU) deaths table. Add up its counties to get one row per state, and take each state's population from it.
3. For each date with ICU data, work out deaths per 100,000 for every state, join the ICU figure, and draw a scatter plot with the state's two-letter code on each circle.
4. Save each plot as an image and append it to the video.

| File or folder | What is in it |
| --- | --- |
| `7dayvis.py` | the whole program |
| `CITATION.cff` | how to cite this repository |
| `LICENSE` | the MIT licence |

## Ideas to try

1. In `7dayvis.py`, change `fps=10` to `fps=5` to slow the video down.
2. In `7dayvis.py`, change `window=7` to `window=1` to turn off smoothing. Watch the weekly reporting pattern appear.
3. In `7dayvis.py`, change `ax.set_title` so each frame shows its date. The loop variable `d` holds the date.
4. The archived CDC file has other columns, such as `InBedsOccAnyPat__Numbeds_Est` (all hospital beds in use, as a percent). Plot that in place of ICU use.
5. Ambitious: work out the correlation between deaths per 100,000 and ICU use for each day with pandas `corr`, and plot how it changes over time.

## Technical details

`7dayvis.py` pulls both sources at run time:

| Source | Used for |
| --- | --- |
| CDC NHSN `covid19-NatEst.csv` | Estimated ICU beds occupied by any patient, per state (`ICUBedsOccAnyPat__N_ICUBeds_Est`). |
| JHU CSSE `time_series_covid19_deaths_US.csv` | Cumulative deaths and state populations. |

ICU occupancy is smoothed with a 7 day rolling mean before plotting, because the raw series has a strong weekday reporting pattern that otherwise dominates the animation. Deaths are normalised to population so states are comparable.

Each date becomes a scatter frame, and the frames are written straight to `deaths-vs-beds.mp4` at 10 fps through `imageio`. Circle size is population divided by 20,000. The axes are fixed at 0 to 180 deaths per 100,000 and 20 to 90 percent ICU use.

The archived CDC file (snapshot of 4 June 2022) covers 1 April 2020 to 7 July 2020, for 50 states, Washington DC, Puerto Rico and the US total. The first row under the header describes each column, which is why the script drops row 0.

## Project status

The script does not run as committed, for two reasons:

- The CDC address on line 5 returns "Page Not Found". Use the archived copy shown in "Run it".
- With pandas 2 or newer, the line that reads population fails with `ValueError: invalid literal for int()`, because pandas 2 joins text columns when it adds up a table. Use `pandas<2`.

The JHU repository it reads from was archived in 2023 and no longer updates. Its address still works.

## Licence

You can use, copy and change this code for any purpose, as long as you keep the copyright notice. See [LICENSE](LICENSE) (MIT).

## Credits

- Written by Abhishek Shivakumar. Citation details are in [CITATION.cff](CITATION.cff).
- ICU data: CDC National Healthcare Safety Network, COVID-19 patient impact and hospital capacity estimates (`covid19-NatEst.csv`), read from the [Internet Archive copy](https://web.archive.org/web/20220604130041/https://www.cdc.gov/nhsn/pdfs/covid19/covid19-NatEst.csv).
- Deaths and population: [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).
- Libraries: [pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/), [imageio](https://imageio.readthedocs.io/).
