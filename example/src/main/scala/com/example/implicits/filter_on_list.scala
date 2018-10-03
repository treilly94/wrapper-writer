DataFramepackage com.example.implicits

import org.apache.spark.sql.DataFrame
import com.example.FilterOnList

object FilterOnListImpl {
  implicit class FilterOnListMethodsImpl(df: DataFrame) {
    

    def filterOnList(targetCol: String,values: List[Int]: DataFrame= {
      FilterOnList.filterOnList(targetCol,values)
    }
  }
}