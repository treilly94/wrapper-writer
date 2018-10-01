from pyspark.sql import DataFrame


def filter_on_list(df,targetCol,values):
	

    # Get the Scala API
    api = df._sc._jvm.com.example.api.FilterOnListAPI

    return DataFrame(api.filterOnList(df._jdf,targetCol,values), df.sql_ctx)