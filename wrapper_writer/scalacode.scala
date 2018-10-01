object FilterOnList {

   def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
     filterFunct(df, targetCol, values)
   }
   def filterFunct(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
     df.where(!col(targetCol).isin(values: _*))
   }
 }