import pandas as pd
import matplotlib.pyplot as plt
from tueplots import fonts, figsizes
import numpy as np
from sklearn.linear_model import LinearRegression
from tueplots import figsizes

plt.rcParams.update(fonts.neurips2021())
plt.rcParams.update({"figure.dpi": 150})


colors = {
'Vorfrühling' : '#b8c480',
'Erstfrühling' : '#799555',
'Vollfrühling' : '#3a662a',
'Frühsommer' : '#ff6822',
'Hochsommer' : '#da3411',
'Spätsommer': '#b40000',
'Früherbst': '#F18D00',
'Vollherbst': '#754400',
'Spätherbst': '#4d231d',
'Winter': '#00B5CD'
}

english_names = {
'Vorfrühling' : 'Pre-Spring',
'Erstfrühling' : 'First Spring',
'Vollfrühling' : 'Full Spring',
'Frühsommer' : 'Early Summer',
'Hochsommer' : 'Midsummer',
'Spätsommer': 'Late Summer',
'Früherbst': 'Early Autumn',
'Vollherbst': 'Full Autumn',
'Spätherbst': 'Late Autumn',
'Winter': 'Winter'
}

def make_horizontal_bar_plot(mean):
    data = mean.dropna()
    start = data['Vorfrühling']
    end = data['Spätherbst']
    diff = data.diff(axis=1, periods=-1)
    diff = diff * -1
    diff['Winter'] = 365 - end
    diff.insert(loc=0, column='Winter 1', value=start)
    diff = (diff.T / diff.T.sum()).T * 365
    data = diff[diff.index > 1991]

    fig, ax = plt.subplots(figsize=(figsizes.neurips2021(nrows=2)["figure.figsize"]))
    lefts = 0
    ax.barh(data.index, data.iloc[:,6])
    for idx, c in enumerate(data.columns):
        if c == 'Winter 1':
            ax.barh(data.index, data[c], left=lefts, color = colors['Winter'], edgecolor = colors['Winter'], linewidth=1.5) 
        else:
            ax.barh(data.index, data[c], left=lefts, color = colors[c], edgecolor = colors[c], linewidth=1.5) 
        lefts += data[c]
    plt.margins(x=0, y=0)
    plt.title('Average Start Days of Phenological Seasons')
    plt.xlabel("Day of Year")
    plt.ylabel("Years")
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, english_names.values(), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('./img/hbar_plot.pdf',dpi=300, bbox_inches = "tight")
    
def make_hist_plot(hists):
    fig, axes = plt.subplots(2, 5, sharex=False, sharey=True, figsize=(figsizes.neurips2021(nrows=1.5)["figure.figsize"]))

    for i, ax in enumerate(axes.flatten()):
        if i < len(hists):
            hist = hists[i]
            name = list(hist.keys())[0]
            ax.hist(list(hist.values())[0][0], list(hist.values())[0][1], color = colors[name])
            ax.set_title(str(english_names[name]))
        else:
            ax.remove()

    fig.suptitle('Total Observation per Season')
    fig.text(0.5, -0.02, 'Year', ha='center', va='center')
    fig.text(0.01, 0.5, 'Number of Observations', ha='center', va='center', rotation='vertical')

    plt.tight_layout()
    plt.savefig('./img/hist_plot.pdf',dpi=300, bbox_inches = "tight")

def make_timeseries_plots(data_mean, data_median, data_std, plot_median=False, plot_median_trend=False):
    fig, axs = plt.subplots(4, 3, figsize=(figsizes.neurips2021(nrows=3.)["figure.figsize"]))
    axs = axs.ravel()
    
    fault_cols = ["Spätsommer", "Winter"] # these columns are missing observations 
    
    for c, season in enumerate(data_mean.columns):
            
        if season in fault_cols: # fix starting years
            data_mean[season] = data_mean[season][data_mean[season].index > 1990]
            data_median[season] = data_median[season][data_median[season].index > 1990]
            data_std[season] = data_std[season][data_std[season].index > 1990]
        
        # CI Intervals    
        mean_upper = data_mean[season] + 1.96 * data_std[season] 
        mean_lower = data_mean[season] - 1.96 * data_std[season]

        # trend line mean
        y_mean = data_mean[season].dropna()
        X_mean = np.array(y_mean.index).reshape(-1,1)
        model = LinearRegression(fit_intercept=True)
        model.fit(X_mean, y_mean)
        trend_mean = model.predict(X_mean)

        # trend line median
        if plot_median_trend == True:
            y_median = data_median[season].dropna()
            X_median = np.array(y_median.index).reshape(-1,1)
            model = LinearRegression(fit_intercept=True)
            model.fit(X_median, y_median)
            trend_median = model.predict(X_median)

        # plotting
        axs[c].plot(data_mean[season].index, data_mean[season], '-', color=colors[season], lw=1.5, label='Mean', alpha=.6)
        axs[c].fill_between(data_std.index, mean_lower, mean_upper, color=colors[season], alpha=.1, label='1.96 Std Mean') 
        axs[c].plot(y_mean.index, trend_mean, '--', color='black', lw=1, label="Trend")

        if plot_median == True:
            axs[c].plot(data_median.index, data_median[season], ':', color='tab:orange', alpha=1, lw=2, label='Median')
        if plot_median_trend == True:
            axs[c].plot(y_median.index, trend_median, '-', color='tab:orange', alpha=1, lw=2, label='Trend Median')

        axs[c].margins(x=0, y=0)
        axs[c].set_title(english_names[season])

    for i, ax in enumerate(axs.flatten()):
        if i > 9:
            ax.remove()
            
    lines, labels = fig.axes[-1].get_legend_handles_labels()
    fig.legend(lines, labels, 
                bbox_to_anchor=(0.525,0.060), loc="lower center", 
                bbox_transform=fig.transFigure, ncol=1)
    fig.suptitle('Days since start of year of phenological seasons in Germany', fontsize=12)
    fig.text(0.5, 0.01, 'Year', ha='center', va='center')
    fig.text(-0.0, 0.5, 'Days since start of year', ha='center', va='center', rotation='vertical')
    fig.tight_layout()
    plt.savefig('./img/ts_plot.pdf',dpi=300, bbox_inches = "tight")

    