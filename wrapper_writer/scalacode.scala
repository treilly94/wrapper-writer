DataFramepackage com.example.implicits

import org.apache.spark.sql.DataFrame
import com.example.FilterOnList

object FilterOnList {
	implicit class FilterOnListMethodsImpl(df: DataFrame) {

   def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
     filterFunct(df, targetCol, values)
   }
   def filterFunct(df: DataFrame, listCol: String, values: List[Int]): DataFrame = {
     df.where(!col(targetCol).isin(values: _*))
	 
	def filterOnUltList(targetCol: String,values: List[Int]): DataFrame = {
      FilterOnList.filterOnList(targetCol,values)
    }
   }
 }
 }