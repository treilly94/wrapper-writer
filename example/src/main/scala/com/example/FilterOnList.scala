package com.example

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.col

object FilterOnList {

  /**
    * This function calls a protected function which filters the data based on where the targetCol doesn't have values
    * that are in the values parameter.
    * @param df DataFrame - Stores all the data.
    * @param targetCol String - Column to be filtered on.
    * @param values List[Int] - List of values to compared.
    * @return DataFrame
    */
  def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    filterFunct(df, targetCol, values)
  }

  /**
    * This function will take in a DataFrame and filter the data based on where the targetCol doesn't have values
    * that are in the values parameter.
    * @param df DataFrame - Stores all the data.
    * @param targetCol String - Column to be filtered on.
    * @param values List[Int] - List of values to compared.
    * @return DataFrame
    */
  protected def filterFunct(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    df.where(!col(targetCol).isin(values: _*))
  }
}
