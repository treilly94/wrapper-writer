
#' sumColumns
#'
#' @param sc
#' @param df
#' @param col1
#' @param col2
#' @param newCol
#'
#' @return
#' @export
#'
#' @examples


sumColumns <- function(sc, df,col1,col2,newCol) {


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
    class="com.example.SumColumns",
    method="sumColumns",
    df=df,
    col1=col1,
    col2=col2,
    newCol=newCol
                )
}