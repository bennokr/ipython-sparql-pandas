# IPython Sparql Pandas Extension

Jupyter/IPython Extension for Sparql Pandas dataframe queries.

## Install
Via pip:

```bash
pip install ipython-sparql-pandas
```

## Usage

Load the extension:

```
%load_ext ipython_sparql_pandas
```

Query:

```sparql
%%sparql http://dbpedia.org/sparql/ -qs foo
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcb: <http://dbpedia.org/resource/Category:>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?name ?capital ?populationTotal WHERE {
    ?capital dct:subject dcb:Capitals_in_Europe ;
             dbp:populationTotal ?populationTotal ; 
             foaf:name ?name. 
}
ORDER BY DESC(?populationTotal)
LIMIT 5
```

The variable `foo` is now a Pandas dataframe of SPARQL results:

```python
foo.plot.barh('name', 'populationTotal').invert_yaxis()
```

![plot](https://raw.githubusercontent.com/bennokr/ipython_sparql_pandas/main/plot.png)

## Acknowledgements
This package is inspired by [ipython_sparql](https://github.com/baito/ipython_sparql).