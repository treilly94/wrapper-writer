package com.example


import org.apache.spark.sql.{Column, DataFrame}
import org.apache.spark.sql.functions.col

object Maths {

  def sumColumns(df: DataFrame, columnA: String, columnB: String, newCol: String): DataFrame = {
    df.withColumn(newCol, sum(columnA, columnB))
  }

  def sum(columnA:String, columnB:String): Column = {
    col(columnA)+col(columnB)
  }


  def multiply(columnA:Int, columnB:Int): Int = {
    columnA*columnB
  }

}
