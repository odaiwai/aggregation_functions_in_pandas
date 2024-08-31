# Demonstrate Aggregation Functions in Pandas

Based on a couple of blog posts by [Dr. Drang](https://leancrew.com/all-this/):
 - https://leancrew.com/all-this/2024/08/what-i-didn-t-learn-about-the-electoral-college/
 - https://leancrew.com/all-this/2024/08/pandas-and-the-electoral-college/

 where he iterated over a Pandas dataframe to get some results, I tried to do the same thing using an aggregation function, to avoid the iteration step.  (Iterating over a DataFrame is almost always the wrong thing to do - it's fine when it's 50 rows, but the millions of rows datasets I normally work with would be very slow with iteration.)

The key is to supply an aggregation function to the `groupby` operation, so that pandas can take sensible actions with each of the fields.  To have a different action for each columnm, a dictionary of `'<field>': 'operation'` can be passed:

In this case, we have two text fields that we could like to join up as comma separated lists, and two numeric fields we would like to sum.  To aggregate the text fields, we need to define a function to convert the `pd.Series` object to a list, and then `join` the list using the build in `str.join()` function, as shown below.
```python

    ...

    def join_strs(s: pd.Series) -> pd.Series:
        """Aggregate a pd.Series to a Comma Separated List."""
        lst = s.to_list()
        return ', '.join(lst)

    agg_func = {'State': join_strs,
                'Abbrev': join_strs,
                'Population': 'sum',
                'Electors': 'sum'}

    # Aggregate the dataframe by the number of Electors, and aggregate
    # using the aggration function
    df_group = df[agg_func.keys()].groupby(by='Electors').agg(agg_func)

    ...

```

## Other notes

Why separate files for electors and states? That was just the data that I found.  I could have easily put them together in the editor.
