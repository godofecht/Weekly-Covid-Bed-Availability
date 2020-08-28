from pandas import read_csv, to_datetime
from matplotlib.pyplot import subplots, close
from imageio import get_writer, imread
from io import BytesIO
natest = read_csv('https://www.cdc.gov/nhsn/pdfs/covid19/covid19-NatEst.csv')
natest = natest.drop([0]) # remove column description text
statemap = dict(zip(natest.statename, natest.state)) # store state abbreviations
natest['date'] = to_datetime(natest['collectionDate'], format='%d%b%Y') # code dates
natest = natest[['statename', 'date', 'ICUBedsOccAnyPat__N_ICUBeds_Est'] # ICU bed use
    ].set_index(['date', 'statename']) # index on date, and states temporarily
natest = natest.unstack().astype(float).dropna() # convert states to columns
icus = natest['ICUBedsOccAnyPat__N_ICUBeds_Est'].rolling(window=7).mean().dropna() # weekly moving average

deaths = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
sf = deaths.groupby('Province_State').sum().T # group by state, sum, transpose
sf = sf.drop(sf.index[range(5)]) # remove everything but Population
pops = sf.iloc[[0]].T.astype(int) # Population sum
sf = sf.iloc[1:].astype(int) # remove Population from cumulative deaths
sf['date'] = to_datetime(sf.index, format='%m/%d/%y')
sf = sf.set_index('date')

writer = get_writer('deaths-vs-beds.mp4', mode='I', fps=10)
for d in icus.index:
    icuu = icus.loc[d]
    icuu.name = 'ICUbedUse'
    natest = sf.loc[d].to_frame(name='Deaths' # make Deaths dataframe
        ).merge(pops, left_index=True, right_index=True) # replace Population
    natest['dpc'] = natest['Deaths'] * 100000.0 / natest['Population'] # deaths per 100,000
    natest.index.names = ['statename']
    natest = natest.join(icuu).dropna() # add icu bed use

    fig, ax = subplots()
    natest.plot.scatter(x='dpc', y='ICUbedUse', s=natest.Population/20000, alpha=0.1, ax=ax)
    for k, v in natest.iterrows():
        ax.annotate(statemap[k], (v['dpc'], v['ICUbedUse']), ha='center', va='center')
    ax.set_xlim(0, 180)
    ax.set_ylim(20, 90)
    ax.set_title("US ICU bed use by COVID-19 mortality:")
    ax.xaxis.set_label_text('COVID-19 deaths per 100,000 people')
    ax.yaxis.set_label_text('Hospital ICU bed use 7-day average (percent)')
    img = BytesIO()
    fig.savefig(img, format='png')
    close(fig)
    img.seek(0)
    writer.append_data(imread(img))
    print('.', end='', flush=True)
print('')
