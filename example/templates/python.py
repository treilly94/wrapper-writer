{% import "macros.jinja" as macros %}

{%- set params = method.get("params") -%}
{%- set returns = method.get("returns") -%}
{%- set docs = method.get("docs") -%}
from pyspark.sql import DataFrame


def {{ name }}({{ macros.show_params(params) }}):
	{% if docs != None -%}
    """ {{ docs }}"""
    {%- endif %}

    # Get the Scala API
    api = df._sc._jvm.com.example.api.SumColumnsAPI

    return DataFrame(api.{{ name }}(df._jdf, {{ macros.show_params(params) }}, df.sql_ctx)
