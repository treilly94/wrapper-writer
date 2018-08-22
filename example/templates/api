{%- set params = method.get("params") -%}
{%- set returns = method.get("returns") -%}
{%- set docs = method.get("docs") -%}
package com.example.api

import java.util
import scala.collection.JavaConversions._
import org.apache.spark.sql.{DataFrame, Dataset, Row}
import com.example.SumColumns

object SumColumnsAPI {

  {%- if docs != None -%}
  /** {{ docs }}*/
  {%- endif %}	
  def {{ name }}({% for p in params.keys() %}{{ p }}: {{ params.get(p) }}{% endfor %}): {{ returns }} = {
    SumColumns.{{ name }}({% for p in params.keys() %}{{ p }}{% endfor %})
  }
}
