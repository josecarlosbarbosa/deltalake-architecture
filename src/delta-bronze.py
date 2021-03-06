import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import DataFrame

if __name__ == '__main__':

    spark = pyspark.sql.SparkSession.builder.appName("Pyspark - Deltalake")\
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .getOrCreate()

    spark.sparkContext.setLogLevel("INFO")
   
    def read_data(path: str, format: str) -> DataFrame:
        """[Read data on local path]

        Args:
            path (str): [data location path]

        Returns:
            DataFrame: [Dataframe with data]
        """        
        df = spark.read.format(format)\
            .option("inferSchema", "true")\
            .option("header", "true")\
            .load(path)

        return df

    def write_data(df: DataFrame, path: str, write_delta_mode: str) -> str:
        """[Write data on format delta]

        Args:
            df (DataFrame): [Dataframe with data]
            path (str): [data location path]
            write_delta_mode (str): [append, overwrite]

        Returns:
            str: [Message after write]
        """        
        df.write.mode(write_delta_mode)\
        .format("delta")\
        .save(path)

        return "Data saved successfully"

    # Array of tables
    table_names = ["vehicle", "subscription", "movies" , "user"]
    
    for table_name in table_names:
        data = f"/Users/carlosbarbosa/Desktop/work/de-apache-spark/files/landing-zone/{table_name}/*.json"
        
        df = read_data(data, "json")
        print(f"Schema of the {table_name} is: \n")
        df.printSchema()

        delta_processing_store_zone = f"/Users/carlosbarbosa/Desktop/work/challenge-ows/delta/bronze/{table_name}/"
        write_data(df, delta_processing_store_zone, "append")

    spark.stop()