package com.example


import com.example.Maths.{multiply, sum, sumColumns}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.junit.Test


class MathsTest {
  val spark: SparkSession = SparkSession.builder().master("local").getOrCreate()
  spark.sparkContext.setLogLevel("ERROR")

  @Test
  def testSum(): Unit = {
    print(sum("5", "6"))
    //assert(sum("5", "6") == col("5 + 6"))
  }

  @Test
  def testMultiply(): Unit = {
    assert(multiply(5, 6) == 30)
    assert(multiply(5, -6) == -30)
  }

  @Test
  def testSumColumns(): Unit = {
    val input: DataFrame = spark.read.json("./src/test/resources/input/sum_in.json")
    println("Input")
    input.show()
    val expected: DataFrame = spark.read.json("./src/test/resources/expected/sum_out.json")
    println("Expected")
    expected.show()
    val output: DataFrame = sumColumns(input, "col1", "col2", "sum")
    println("Output")
    output.show()

    assert(output.collectAsList() == expected.collectAsList())
  }
}