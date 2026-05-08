CREATE CONSTRAINT FOR (a:Airport) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT FOR (air:Airline) REQUIRE air.name IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///airlines_nodes.csv' AS row
MERGE (air:Airline {name: row.name})
SET air.country = row.country;

LOAD CSV WITH HEADERS FROM 'file:///airports_nodes.csv' AS row
MERGE (a:Airport {name: row.name})
SET a.city = row.city,
    a.country = row.country;

LOAD CSV WITH HEADERS FROM 'file:///routes_edges.csv' AS row
MATCH (dep:Airport {name: row.departure_airport})
MATCH (arr:Airport {name: row.arrival_airport})
MERGE (dep)-[r:ROUTE]->(arr)
SET r.airline_names = split(row.airline_names, ';'),
    r.aircraft_types = split(row.aircraft_types, ';');