https://classroom.emeritus.org/courses/8898/pages/spark?module_item_id=1486497

# download the docker compose file for spark

`curl https://raw.githubusercontent.com/bitnami/containers/main/bitnami/spark/docker-compose.yml -o docker-compose.yaml`

then run

`docker-compose up`

copy txt file from local to container
`docker cp ./SampleFile/SampleFile.txt bitnami-spark-1:/SampleFile.txt`
in docker hub, spark-1 will be in bitnami.

# To fix Pyspark error

when trying to open pyspark shell in container, it says
Error: pyspark does not support any application options.
try editing a file like how it says here
https://github.com/bitnami/containers/issues/38139
`docker cp bitnami-spark-1:/opt/bitnami/spark/bin/pyspark ./pyspark`
on the last line, change with
exec "${SPARK_HOME}"/bin/spark-submit pyspark-shell-main "$@"
copy back to container
`docker cp ./pyspark bitnami-spark-1:/opt/bitnami/spark/bin/pyspark`
now it works when doing `pyspark` in container

# creating and manipulating dataframes

in pyspark shell
`textFile = spark.read.text("SampleFile.txt")`

count lines
`textFile.count()`

capture first row
`textFile.first()`

transform dataframe
`linesWithSpark = textFile.filter(textFile.value.contains("Spark"))`

I think this line in the instructions
from pyspark.sql.functions import
should be
from pyspark.sql.functions import *
because without *, it is invalid syntax
Now can run 
`textFile.select(size(split(textFile.value,"\s+")).name("numWords")).agg(max(col("numWords"))).collect()`

# to cache a dataframe
`linesWithSpark.cache()`

# Running python applications
copy MLKSpeech.txt from local to container
`docker cp ./MLKSpeech/MLKSpeech.txt bitnami-spark-1:/MLKSpeech.txt`

copy SimpleApp.py from local to container
`docker cp ./SimpleApp/SimpleApp.py bitnami-spark-1:/SimpleApp.py`

Run the python app
`pyspark < SimpleApp.py`

# CSV analysis
transfer departure csv from local to container. in local cmd,
`docker cp ./departuredelays.csv bitnami-spark-1:/departuredelays.csv`

transfer departure python file
`docker cp ./departuredelays.py bitnami-spark-1:/departuredelays.py`

run python script in container
`pyspark < departuredelays.py`