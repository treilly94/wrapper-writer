package com.example.api

import java.util
import scala.collection.JavaConversions._
import org.apache.spark.sql.{DataFrame, Dataset, Row}
import com.example.SumColumns

object SumColumnsAPI {
  /** A cool function*/

  def sumColumns(df: DataFrame,col1: String,col2: String,newCol: String): DataFrame = {
    SumColumns.sumColumns(df,col1,col2,newCol)
  }
}