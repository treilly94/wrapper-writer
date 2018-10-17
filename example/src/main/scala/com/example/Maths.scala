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

  /**
    * This function takes in two strings, converts them to Spark columns then adds them together.
    * @param columnA String - Name of column to add.
    * @param columnB String - Name of column to add.
    * @return Column
    */
  protected def sum(columnA:String, columnB:String): Column = {
    col(columnA)+col(columnB)
  }


  /**
    * This function takes in two integers and multiplies them together and return the outcome.
    *
    * @param columnA Int - Integer to multiply.
    * @param columnB Int - Integer to multiply.
    * @return Int
    */
  protected def multiply(columnA:Int, columnB:Int): Int = {
    columnA*columnB
  }

}
