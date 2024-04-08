## Introduction

This is an example how Keboola users can build on the top of artifacts within the platform, specifically aiming for `dbt` users.

First of all, Keboola documentation and developers docs provide a lot of information regarding [artifacts](https://developers.keboola.com/integrate/artifacts/), including the [tutorial](https://developers.keboola.com/integrate/artifacts/tutorial/) as well. 

*Disclaimer: Code used does not aspire to be 100% pythonic code, nor the best coding possible. I am not a pro :)*

## What are the dbt artifacts?

The platform introduced artifacts at the same time as `dbt` support - to facilitate files produced by frameworks like `dbt`, as it is known those files can be leveraged to produce further insights in the dbt run.   

In a fact, Keboola UI uses them to draw the model timing chart and also hosts the documentation:   
![Keboola Model Timing UI](/Images/Keboola_dbt_image_01.png)

[dbt produces artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts) - files like `manifest.json`, `catalog.json`, `run_results.json`, `sources.json` and other (mostly) JSON files.

Keboola stores them within the *file storage* and tags them, so users can retrieve them programatically and use them to build on a top of them. Try to search in file storage for `tags:"artifact"`
![Zipped dbt artifacts in the storage](/Images/Keboola_dbt_image_02.png)

This means you can retrieve files in *any* component file input mapping. For the sake of this example, lets use a standard `Python transformation` to parse them and materialize them in a relation storage as tables.

## Parsing Artifact files

I have included two code examples:   
1) Parsing zipped artifact archive (test-artifact-parser)   
2) Parsing directly the artifact files (run-artifact-parser)

In a nutshell, the trick is to set up correct file input mapping and then parse files into a table structure.

### Parsing zipped artifact archive
![Zipped dbt artifacts in the storage](/Images/Keboola_dbt_image_03.png)
 - Use file mapping with necessary tags and specify filename as `artifacts.tar.gz` as this is the main dbt artifact. 
 - Use python code provided to materialize results ino tables.
 - Code example parses specifically `run_results.json` file to produce table with all object renders (models, tests, etc.)
  - This is super handy if you want to create an observability over your model built or test warnings and executions.
 ![Test results as a table](/Images/Keboola_dbt_image_04.png)

### Parsing directly the artifact files
 ![Parsing direct artifact files](/Images/Keboola_dbt_image_05.png)
 - Second code example is to showcase both a direct file parsing and also parsing of other types of artifacts
 - Use file mapping with necessary tags to control which artifacts are parsed.
 - Script used produces tables with model timing
  ![Materialized model timing](/Images/Keboola_dbt_image_06.png)
 - Second part of the stript materializes full dbt log, including pre-parsing of the first character of the code sign to determine a stage  
  ![Materialized model timing](/Images/Keboola_dbt_image_07.png)


## Conclusion
Thats all! Check out the scripts in the `/Code` folder. If you can, please share with me what you have build on the top of artifacts!


## Tips
Please note you can also have a single python transformation that has only those tags: `artifact` and `componentId-keboola.dbt-transformation` and parse all artifacts across all dbt configurations.

You can also override the artifact zip behaviour - you can control this in the configuration debug (raw mode):
![Configuration raw mode](/Images/Keboola_dbt_image_10.png)

You can also use [elementary package](https://hub.getdbt.com/elementary-data/elementary/latest/) to parse the artifacts as a part of the run and store them as tables. However, I have noticed the extra time added to the run is much longer than just simply parse the artifact in python within 10-20s.
![Configuration raw mode](/Images/Keboola_dbt_image_08.png)
