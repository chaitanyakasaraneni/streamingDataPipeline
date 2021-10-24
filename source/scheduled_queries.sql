/*Country Counts: Query that counts the number of IP addresses based on country */
WITH source_of_ip_addresses AS (
  SELECT remote_addr ip, COUNT(*) c
  FROM egen-training-kck.training_capstone.userLogs
  WHERE remote_addr IS NOT null  
  GROUP BY 1
)

SELECT country_name, SUM(c) c
FROM (
  SELECT ip, country_name, c
  FROM (
    SELECT *, NET.SAFE_IP_FROM_STRING(ip) & NET.IP_NET_MASK(4, mask) network_bin
    FROM source_of_ip_addresses, UNNEST(GENERATE_ARRAY(9,32)) mask
    WHERE BYTE_LENGTH(NET.SAFE_IP_FROM_STRING(ip)) = 4
  )
  JOIN `fh-bigquery.geocode.201806_geolite2_city_ipv4_locs`  
  USING (network_bin, mask)
)
GROUP BY 1
ORDER BY 2 DESC;

/* City Counts: Query that counts the number of IP addresses based on city */
WITH source_of_ip_addresses AS (
  SELECT remote_addr  ip, COUNT(*) c
  FROM egen-training-kck.training_capstone.userLogs
  WHERE remote_addr IS NOT null  
  GROUP BY 1
)

SELECT city_name, SUM(c) c, ST_GeogPoint(AVG(longitude), AVG(latitude)) point
FROM (
  SELECT ip, city_name, c, latitude, longitude, geoname_id
  FROM (
    SELECT *, NET.SAFE_IP_FROM_STRING(ip) & NET.IP_NET_MASK(4, mask) network_bin
    FROM source_of_ip_addresses, UNNEST(GENERATE_ARRAY(9,32)) mask
    WHERE BYTE_LENGTH(NET.SAFE_IP_FROM_STRING(ip)) = 4
  )
  JOIN `fh-bigquery.geocode.201806_geolite2_city_ipv4_locs`  
  USING (network_bin, mask)
)
WHERE city_name  IS NOT null
GROUP BY city_name, geoname_id
ORDER BY c DESC;

