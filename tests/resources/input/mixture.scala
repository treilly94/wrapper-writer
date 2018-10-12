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

  def sum(columnA:String, columnB:String): Column = {
    col(columnA)+col(columnB)
  }


  /**
    * This function takes in two integers and multiplies them together and return the outcome.
    *
    * @return Int
    */
  def two(): list[Int] = {
    [2,3]
      }


    /**
    * This function takes in a list of stings and a string.
    *
    * @return Int
    */
  def testing(colb: List[String], cola:String="hello"): = {
    colb.append(cola)
  }

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
