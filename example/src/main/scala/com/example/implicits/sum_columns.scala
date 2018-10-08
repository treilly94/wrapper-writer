DataFramepackage com.example.implicits

import org.apache.spark.sql.DataFrame
import com.example.SumColumns

object SumColumnsImpl {
  implicit class SumColumnsMethodsImpl(df: DataFrame) {
    /** A cool function*/

    def sumColumns(col1: String,col2: String,newCol: String: DataFrame = {
      SumColumns.sumColumns(col1,col2,newCol)
    }
  }
}