#!/usr/bin/env python3
"""Demonstrate the use of aggregation functions in Pandas."""
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
    df_group = df[agg_func.keys()].groupby(by='Electors').agg(agg_func)

    # Calculate the proportions of the total
    df_group['PopPct'] = df_group.Population/pop_sum
    df_group['ECPct'] = df_group.Electors/ec_sum
    df_group = df_group.drop('State', axis=1)

    # formatting and alignment
    colaligns = ['center'] * 2 + ['right'] * 4
    floatfmts = [None] * 2 + ['0.0:,d'] * 2 + ['0.2%'] * 2

    print(df_group.to_markdown(tablefmt='pipe',
                               colalign=colaligns,
                               floatfmt=floatfmts))


if __name__ == '__main__':
    main()
