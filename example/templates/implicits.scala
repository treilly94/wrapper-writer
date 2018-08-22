{%- set params = method.get("params") -%}
{%- set returns = method.get("returns") -%}
{%- set docs = method.get("docs") -%}
package com.example.implicits

import org.apache.spark.sql.DataFrame
import com.example.SumColumns

object SumColumnsImpl {
  implicit class SumColumnMethodsImpl(df: DataFrame) {

  	{%- if docs != None -%}
	/** {{ docs }}*/
	{%- endif %}
    def {{ name }}({% for p in params.keys() %}{{ p }}: {{ params.get(p) }}{% endfor %}): {{ returns }} = {
      SumColumns.{{ name }}({% for p in params.keys() %}{{ p }}{% endfor %})
    }
  }
}
