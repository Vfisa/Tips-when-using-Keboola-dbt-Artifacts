## What is this?

Those are two configurations in Keboola you can use as an example for Artifacts parsing. Notice we have limit 1 to just use the last one, though the code can parse and backfill multiple if needed. Please note the file input mapping filters you need to adjust to your dbt config ID:
```
{
          "limit": 1,
          "source": {
            "tags": [
              {
                "name": "artifact"
              },
              {
                "name": "branchId-15940"
              },
              {
                "name": "componentId-keboola.dbt-transformation"
              },
              {
                "name": "configId-65241962"
              }
            ]
          },
          "query": "run_results.json"
        }
```

## How to use this?

 *Note: If you are new to Keboola CLI - please check [Keboola CLI tutorial](https://developers.keboola.com/cli/getting-started/)*

Simply paste configs in the respecttive folders, persist the code `kbc local persist`, potentially check the diff with `kbc diff` and push `kbc sync push`.

