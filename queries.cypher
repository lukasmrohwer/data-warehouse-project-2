MATCH (air:Airline {country: 'Australia'})
RETURN DISTINCT air.name AS AirlineName;



MATCH (dep:Airport)-[r:ROUTE]->(arr:Airport)
RETURN 
    SUM(CASE WHEN dep.country = arr.country THEN 1 ELSE 0 END) AS DomesticRecords,
    SUM(CASE WHEN dep.country <> arr.country THEN 1 ELSE 0 END) AS InternationalRecords;



MATCH (dep:Airport)-[r:ROUTE]->(arr:Airport)
WITH 
    CASE WHEN dep.name < arr.name THEN dep.name ELSE arr.name END AS Airport1,
    CASE WHEN dep.name < arr.name THEN arr.name ELSE dep.name END AS Airport2,
    r.airline_names as airline_names
UNWIND airline_names AS airline
RETURN Airport1, Airport2, count(DISTINCT airline) AS RecordCount
ORDER BY RecordCount DESC
LIMIT 1



MATCH (dep:Airport)-[r:ROUTE]->(arr:Airport)
WITH 
    CASE WHEN dep.name < arr.name THEN dep.name ELSE arr.name END AS Airport1,
    CASE WHEN dep.name < arr.name THEN arr.name ELSE dep.name END AS Airport2,
    r.aircraft_types AS planes
UNWIND planes AS plane
RETURN Airport1, Airport2, count(DISTINCT plane) AS DistinctAircraftCount
ORDER BY DistinctAircraftCount DESC
LIMIT 5;



MATCH path = (start:Airport {name: 'Beijing Capital International Airport'})-[:ROUTE*1..3]->(end:Airport {name: 'Perth International Airport'})
WITH [a IN nodes(path) | a.name] AS airportSequence
RETURN count(DISTINCT airportSequence) AS NumberOfDistinctRoutes;



MATCH (dep:Airport)-[:ROUTE]->(arr:Airport)
WHERE dep.country <> arr.country
RETURN 
    dep.name AS HubAirport, 
    dep.country AS HubCountry, 
    count(DISTINCT arr.country) AS DistinctForeignCountriesReached
ORDER BY DistinctForeignCountriesReached DESC
LIMIT 5;



MATCH ()-[r:ROUTE]->()
WITH collect(r.aircraft_types) AS nested_planes
WITH apoc.coll.flatten(nested_planes) AS all_planes
UNWIND apoc.coll.frequencies(all_planes) AS plane_data
RETURN 
    plane_data.item AS AircraftType, 
    plane_data.count AS TotalRouteAppearances
ORDER BY TotalRouteAppearances DESC
LIMIT 5;