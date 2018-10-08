
#' filterOnList
#'
#' @param sc
#' @param df
#' @param targetCol
#' @param values
#'
#' @return
#' @export
#'
#' @examples


filterOnList <- function(sc, df,targetCol,values) {


  # Checks to see if there is spark connection
  stopifnot(inherits(sc, c("spark_connection", "spark_Shell_connection", "DBIConnection")))
  # Checks to see if the dataframe is a spark/shell object
  stopifnot(inherits(df, c("spark_jobj", "shell_jobj")))

  # Here we are checking that the parameters have come in as they should
  # Parameter types are important in R and Scala
  stopifnot(is.character(column_1) & is.character(column_2) & is.character(new_column))



  # Here we invoke the function within the object as the method
  # We also pass the parameters into the method
  # The types need to match in order to get the correct signutre otherwise you will get a no such method found error

  invoke_static(
    sc=sc,
    class="com.example.FilterOnList",
    method="filterOnList",
    df=df,
    targetCol=targetCol,
    values=values
                )
}