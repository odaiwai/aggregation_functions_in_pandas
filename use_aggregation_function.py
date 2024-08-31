#!/usr/bin/env python3
"""Demonstrate the use of aggregation functions in Pandas."""
import matplotlib.pyplot as plt
import pandas as pd


def join_strs(s: pd.Series) -> pd.Series:
    """Aggregate a pd.Series to a Comma Separated List."""
    lst = s.to_list()
    return ', '.join(lst)


def main() -> None:
    """Build and aggregate the dataframe."""
    # build the combined dataframes
    df1 = pd.read_csv('states.csv', delimiter=';')
    df2 = pd.read_csv('electors.csv', delimiter=';')
    df = pd.merge(df1, df2, how='left', on='State')
    pop_sum = df.Population.sum()
    ec_sum = df.Electors.sum()

    # Make a dictionary of how to aggregate the fields:
    agg_func = {'State': join_strs,
                'Abbrev': join_strs,
                'Population': 'sum',
                'Electors': 'sum'}

    # Aggregate the dataframe by the number of Electors, and aggregate
    # using the aggration function
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
    df_group = df[agg_func.keys()].groupby(by='Electors').agg(agg_func)

    # Calculate the proportions of the total
    df['PopPct'] = df.Population/pop_sum
    df['ECPct'] = df.Electors/ec_sum
    df_group['PopPct'] = df_group.Population/pop_sum
    df_group['ECPct'] = df_group.Electors/ec_sum
    df_group = df_group.drop('State', axis=1)

    # formatting and alignment for .to_markdown():
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html
    # https://pypi.org/project/tabulate/
    colaligns = ['center'] * 2 + ['right'] * 4
    floatfmts = [None] * 2 + ['0.0d'] * 2 + ['0.2%'] * 2

    print(df_group.to_markdown(tablefmt='pipe',
                               colalign=colaligns,
                               floatfmt=floatfmts))

    # Just for fun, make a bubble plot
    fig, ax = plt.subplots(figsize=(9, 9), layout='constrained')
    fig.suptitle('Compare EC representation against Popular Representation.',
                 fontsize=18)

    df.plot.scatter(ax=ax, x='ECPct', y='ECPct', c='gray',
                    label='Line of Equality')
    df.plot.scatter(ax=ax,
                    x='PopPct', y='ECPct',
                    s=df['Electors'] * 20,
                    c='Electors',
                    cmap='viridis')
    # Annotate the states
    def annotate_df(row):
        ax.annotate(xy=(row.PopPct, row.ECPct), text=row.Abbrev,
                    xytext=(10, -5),
                    textcoords='offset points',
                    size=10,
                    color='darkslategrey')

    _ = df.apply(annotate_df, axis=1)

    fig.savefig(f'ec_representation.png', format='png', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
