from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DepartureDelays").getOrCreate()

# data path
csv_file = "/departuredelays.csv"

# read data into temporary view, infer schema
df = (
    spark.read.format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load(csv_file)
)
df.createOrReplaceTempView("delays_table")


spark.sql(
    """SELECT distance, origin, destination FROM delays_table WHERE distance > 1000 ORDER BY distance DESC"""
).show(10)

spark.sql(
    """SELECT delay, origin, destination,
          CASE
            WHEN delay > 360 THEN 'Very Long Delays'
            WHEN delay > 120 AND delay < 360 THEN 'Long Delays'
            WHEN delay > 60 AND delay < 120 THEN 'Short Delays'
            WHEN delay > 0 AND delay < 60 THEN 'Tolerable Delays'
            WHEN delay = 0 THEN 'No Delays'
            ELSE 'Early'
          END AS delays_length
          FROM delays_table
          ORDER BY origin, delay DESC"""
).show(10)

# this is an alternative to sql above
from pyspark.sql.functions import col, desc

(
    df.select("distance", "origin", "destination")
    .where(col("distance") > 1000)
    .orderBy(desc("distance"))
).show(10)
