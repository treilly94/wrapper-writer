package com.example


import org.apache.spark.sql.{Column, DataFrame}
import org.apache.spark.sql.functions.col

object Maths {

  /**
    * This function takes in a DataFrame and then adds a new column to it which holds the values of columnA + columnB.
    * This is calculated by calling the sumColumns function when adding the new column.
    *
    * @param df DataFrame - Stores all the data.
    * @param columnA String - Name of column to add.
    * @param columnB String - Name of column to add.
    * @param newCol String - Name of new column being added to to data set, holds the values of columnA + columnB.
    * @return DataFrame
    */
  def sumColumns(df: DataFrame, columnA: String, columnB: String, newCol: String): DataFrame = {
    df.withColumn(newCol, sum(columnA, columnB))
  }