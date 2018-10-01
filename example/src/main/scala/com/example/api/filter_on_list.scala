package com.example.api

import java.util
import scala.collection.JavaConversions._
import org.apache.spark.sql.{DataFrame, Dataset, Row}
import com.example.FilterOnList

object FilterOnListAPI {
  

  def filterOnList(df: DataFrame,targetCol: String,values: List[Int]): DataFrame = {
    FilterOnList.filterOnList(df,targetCol,values)
  }
}