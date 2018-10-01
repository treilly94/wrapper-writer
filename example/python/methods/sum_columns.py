from pyspark.sql import DataFrame


def sum_columns(df,col1,col2,newCol):
	""" A cool function"""

    # Get the Scala API
    api = df._sc._jvm.com.example.api.SumColumnsAPI

    return DataFrame(api.sumColumns(df._jdf,col1,col2,newCol), df.sql_ctx)