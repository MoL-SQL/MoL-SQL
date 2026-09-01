SELECT COUNT(*) AS _col_0 FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.country = 'Japan' AND nuclear_power_plants.status = '建设中'	GeoNuclearData
SELECT COUNT(nuclear_power_plants.name) AS _col_0 FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.status = '建设中'	GeoNuclearData
SELECT COUNT(*) AS _col_0 FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.country = 'France' AND nuclear_power_plants.status = '运行中'	GeoNuclearData
SELECT nuclear_power_plants.name AS name FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.status = '运行中' AND nuclear_power_plants.country = 'Japan'	GeoNuclearData
SELECT MAX(nuclear_power_plants.capacity) AS _col_0 FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.reactortype = '压水堆' AND nuclear_power_plants.status = '运行中'	GeoNuclearData
SELECT nuclear_power_plants.name AS name FROM nuclear_power_plants AS nuclear_power_plants ORDER BY nuclear_power_plants.capacity DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.longitude AS longitude, nuclear_power_plants.latitude AS latitude FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.reactortype = '沸水堆' ORDER BY nuclear_power_plants.constructionstartat LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.country AS country FROM nuclear_power_plants AS nuclear_power_plants GROUP BY nuclear_power_plants.country ORDER BY SUM(nuclear_power_plants.capacity) DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.country AS country FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.status = '建设中' GROUP BY nuclear_power_plants.country ORDER BY COUNT(*) DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.country AS country FROM nuclear_power_plants AS nuclear_power_plants GROUP BY nuclear_power_plants.country ORDER BY SUM(nuclear_power_plants.capacity) DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.country AS country FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.status = '已停运' GROUP BY nuclear_power_plants.country ORDER BY COUNT(nuclear_power_plants.name) DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants.country AS country FROM nuclear_power_plants AS nuclear_power_plants WHERE nuclear_power_plants.status = '建设中' GROUP BY nuclear_power_plants.country ORDER BY COUNT(*) DESC LIMIT 1	GeoNuclearData
SELECT COUNT(*) AS _col_0 FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.outcome LIKE '%正在调查中%'	GreaterManchesterCrime
SELECT COUNT(*) AS _col_0 FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.outcome = '正在调查中'	GreaterManchesterCrime
SELECT COUNT(*) AS _col_0 FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.type LIKE '%毒品%'	GreaterManchesterCrime
SELECT greatermanchestercrime.outcome AS outcome FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.crimeid = '6B:E2:54:C6:58:D2'	GreaterManchesterCrime
SELECT greatermanchestercrime.type AS type FROM greatermanchestercrime AS greatermanchestercrime GROUP BY greatermanchestercrime.type ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.location AS location FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.type = '暴力及性犯罪' GROUP BY greatermanchestercrime.location ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.location AS location FROM greatermanchestercrime AS greatermanchestercrime GROUP BY greatermanchestercrime.location ORDER BY COUNT(*) LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.location AS location FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.type LIKE '%毒品%' GROUP BY greatermanchestercrime.location ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.type AS type FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.lsoa LIKE '%Salford%' GROUP BY greatermanchestercrime.type ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.type AS type FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.outcome LIKE '%调查已完成%' GROUP BY greatermanchestercrime.type ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.type AS type FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.outcome = '调查已完成；未确认嫌疑人' GROUP BY greatermanchestercrime.type ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime.type AS type FROM greatermanchestercrime AS greatermanchestercrime WHERE greatermanchestercrime.outcome = '等待法院判决结果' GROUP BY greatermanchestercrime.type ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT sampledata15.country AS country FROM sampledata15 AS sampledata15 WHERE sampledata15.sample_pk = 6480 AND sampledata15.origin = 2	Pesticide
SELECT sampledata15.commod AS commod FROM sampledata15 AS sampledata15 WHERE sampledata15.origin = 2 AND NOT sampledata15.commod IN (SELECT sampledata15.commod AS commod FROM sampledata15 AS sampledata15 WHERE sampledata15.origin = 1)	Pesticide
SELECT resultsdata15.testclass AS testclass FROM resultsdata15 AS resultsdata15 WHERE resultsdata15.sample_pk = 7498	Pesticide
SELECT resultsdata15.mean AS mean FROM resultsdata15 AS resultsdata15 WHERE resultsdata15.commod = '苹果'	Pesticide
SELECT resultsdata15.conunit AS conunit FROM resultsdata15 AS resultsdata15 WHERE resultsdata15.commod = '桃'	Pesticide
SELECT resultsdata15.lab AS lab FROM resultsdata15 AS resultsdata15 GROUP BY resultsdata15.lab ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT resultsdata15.lab AS lab FROM resultsdata15 AS resultsdata15 WHERE resultsdata15.commod = '苹果'	Pesticide
SELECT sampledata15.growst AS growst FROM sampledata15 AS sampledata15 WHERE sampledata15.commod = '苹果' GROUP BY sampledata15.growst ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT sampledata15.distst AS distst FROM sampledata15 AS sampledata15 WHERE sampledata15.commod = '苹果' GROUP BY sampledata15.distst ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT sampledata15.state AS state FROM sampledata15 AS sampledata15 WHERE sampledata15.claim = '采购订单' GROUP BY sampledata15.state ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT t1.variety AS variety FROM resultsdata15 AS t2 JOIN sampledata15 AS t1 ON t1.sample_pk = t2.sample_pk WHERE t2.commod = '苹果' GROUP BY t1.variety ORDER BY SUM(t2.concen) DESC LIMIT 1	Pesticide
SELECT DISTINCT sampledata15.commod AS commod FROM sampledata15 AS sampledata15	Pesticide
SELECT COUNT(DISTINCT t1.school_district) AS _col_0 FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code WHERE t2.state = 'Indiana'	StudentMathScore
SELECT SUM(t1.c14) AS _col_0, SUM(t1.c25) AS _col_1 FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code WHERE t2.state = 'Colorado'	StudentMathScore
SELECT t1.school_district AS school_district, MAX(t1.t_fed_rev / t3.average_scale_score) AS _col_1 FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state	StudentMathScore
SELECT t1.school_district AS school_district, MIN(t1.t_fed_rev / t3.average_scale_score) AS _col_1 FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state	StudentMathScore
SELECT ndecoreexcel_math_grade8.average_scale_score AS average_scale_score FROM ndecoreexcel_math_grade8 AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8.state = 'North Carolina' UNION SELECT ndecoreexcel_math_grade8.average_scale_score AS average_scale_score FROM ndecoreexcel_math_grade8 AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8.state = 'New York'	StudentMathScore
SELECT t1.school_district AS school_district, MAX(t1.c14) AS _col_1, t3.average_scale_score AS average_scale_score FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state UNION SELECT t1.school_district AS school_district, MAX(t1.c25) AS _col_1, t3.average_scale_score AS average_scale_score FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state	StudentMathScore
SELECT ndecoreexcel_math_grade8.average_scale_score AS average_scale_score FROM ndecoreexcel_math_grade8 AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8.state = 'North Carolina' UNION SELECT ndecoreexcel_math_grade8.average_scale_score AS average_scale_score FROM ndecoreexcel_math_grade8 AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8.state = 'South Carolina'	StudentMathScore
SELECT t2.state AS state, SUM(t1.c14) AS _col_1, SUM(t1.c25) AS _col_2 FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state GROUP BY t2.state ORDER BY t3.average_scale_score DESC LIMIT 10	StudentMathScore
SELECT t1.school_district AS school_district FROM finrev_fed_17 AS t1 JOIN finrev_fed_key_17 AS t2 ON t1.state_code = t2.state_code WHERE t2.state = 'Wisconsin' ORDER BY t1.t_fed_rev DESC LIMIT 1	StudentMathScore
SELECT t2.state AS state FROM finrev_fed_key_17 AS t2 JOIN finrev_fed_17 AS t1 ON t1.state_code = t2.state_code GROUP BY t2.state ORDER BY SUM(t1.t_fed_rev) DESC LIMIT 1	StudentMathScore
SELECT t2.state AS state, t3.average_scale_score AS average_scale_score FROM finrev_fed_key_17 AS t2 JOIN finrev_fed_17 AS t1 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state GROUP BY t2.state ORDER BY SUM(t1.t_fed_rev) LIMIT 1	StudentMathScore
SELECT t2.state AS state, t3.average_scale_score AS average_scale_score FROM finrev_fed_key_17 AS t2 JOIN finrev_fed_17 AS t1 ON t1.state_code = t2.state_code JOIN ndecoreexcel_math_grade8 AS t3 ON t2.state = t3.state GROUP BY t2.state ORDER BY SUM(t1.t_fed_rev) DESC LIMIT 1	StudentMathScore
SELECT AVG(t1.weight) AS _col_0 FROM player AS t1 JOIN player_award AS t2 ON t1.player_id = t2.player_id GROUP BY t2.notes	TheHistoryofBaseball
SELECT COUNT(*) AS _col_0 FROM (SELECT player_award.player_id AS player_id FROM player_award AS player_award GROUP BY player_award.player_id HAVING COUNT(*) > 10) AS _0	TheHistoryofBaseball
SELECT t1.birth_country AS birth_country FROM player AS t1 JOIN hall_of_fame AS t2 ON t1.player_id = t2.player_id WHERE t2.inducted = 'Y' GROUP BY t1.birth_country ORDER BY COUNT(*) DESC, MIN(t1.player_id) ASC LIMIT 10	TheHistoryofBaseball
SELECT t2.team_id AS team_id FROM hall_of_fame AS t1 JOIN salary AS t2 ON t1.player_id = t2.player_id AND t1.yearid = t2.year WHERE t1.inducted = 'Y' GROUP BY t2.team_id ORDER BY COUNT(*) DESC LIMIT 10	TheHistoryofBaseball
SELECT t1.birth_country AS birth_country FROM hall_of_fame AS t2 JOIN player AS t1 ON t1.player_id = t2.player_id WHERE t2.inducted = 'Y' AND t2.yearid >= 1871	TheHistoryofBaseball
SELECT salary.salary AS salary FROM salary AS salary WHERE salary.league_id = '美国联盟'	TheHistoryofBaseball
SELECT salary.salary AS salary FROM salary AS salary WHERE salary.league_id = '国家联盟'	TheHistoryofBaseball
SELECT AVG(t1.weight) AS _col_0 FROM player AS t1 JOIN player_award AS t2 ON t1.player_id = t2.player_id WHERE t2.award_id = '《The Sporting News》全明星' AND t2.notes = '三垒手'	TheHistoryofBaseball
SELECT t1.birth_country AS birth_country FROM player AS t1 JOIN player_award AS t2 ON t1.player_id = t2.player_id GROUP BY t1.birth_country ORDER BY COUNT(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT player_award.league_id AS league_id FROM player_award AS player_award WHERE player_award.year = '2006' GROUP BY player_award.league_id ORDER BY COUNT(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT salary.player_id AS player_id FROM salary AS salary WHERE salary.year >= 2010 ORDER BY salary.salary DESC LIMIT 1	TheHistoryofBaseball
SELECT player_award.player_id AS player_id FROM player_award AS player_award WHERE player_award.year = 2010 AND player_award.award_id = '年度最佳新秀'	TheHistoryofBaseball
SELECT COUNT(*) AS _col_0 FROM fires AS fires WHERE fires.fire_year = 2010 AND fires.stat_cause_descr LIKE '%纵火%'	USWildFires
SELECT COUNT(*) AS _col_0 FROM fires AS fires WHERE fires.owner_descr = '缺失/未指定'	USWildFires
SELECT COUNT(*) AS _col_0 FROM fires AS fires WHERE fires.owner_descr = '缺失/未指定'	USWildFires
SELECT COUNT(*) AS _col_0 FROM fires AS fires WHERE fires.county = 'Gloucester' AND fires.fire_size > 10	USWildFires
SELECT COUNT(*) AS _col_0 FROM fires AS fires WHERE fires.stat_cause_descr LIKE '%营火%' AND fires.fire_year = 2014	USWildFires
SELECT fires.owner_descr AS owner_descr FROM fires AS fires GROUP BY fires.owner_descr ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT fires.fire_year AS fire_year, fires.discovery_date AS discovery_date, fires.discovery_doy AS discovery_doy, fires.discovery_time AS discovery_time, fires.stat_cause_code AS stat_cause_code, fires.stat_cause_descr AS stat_cause_descr, fires.cont_date AS cont_date, fires.cont_doy AS cont_doy, fires.cont_time AS cont_time, fires.fire_size AS fire_size, fires.fire_size_class AS fire_size_class, fires.latitude AS latitude, fires.longitude AS longitude, fires.owner_code AS owner_code, fires.owner_descr AS owner_descr, fires.state AS state, fires.county AS county, fires.fips_code AS fips_code, fires.fips_name AS fips_name FROM fires AS fires WHERE fires.state = 'TX' AND fires.stat_cause_descr LIKE '营火'	USWildFires
SELECT fires.stat_cause_descr AS stat_cause_descr FROM fires AS fires GROUP BY fires.stat_cause_descr ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT fires.stat_cause_descr AS stat_cause_descr FROM fires AS fires GROUP BY fires.stat_cause_descr ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT SUM(fires.fire_size) AS _col_0 FROM fires AS fires	USWildFires
SELECT fires.county AS county FROM fires AS fires WHERE fires.state = 'WA' AND fires.fire_year = 2012	USWildFires
SELECT fires.state AS state FROM fires AS fires GROUP BY fires.state ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT COUNT(*) AS _col_0 FROM (SELECT torrents.groupname AS groupname FROM torrents AS torrents GROUP BY torrents.groupname HAVING COUNT(*) > 1) AS _0	WhatCDHipHop
SELECT torrents.groupname AS groupname FROM torrents AS torrents WHERE torrents.artist = 'lasean camry' AND torrents.totalsnatched = (SELECT MAX(torrents.totalsnatched) AS _col_0 FROM torrents AS torrents WHERE torrents.artist = 'lasean camry') UNION SELECT torrents.groupname AS groupname FROM torrents AS torrents WHERE torrents.artist = 'lasean camry' AND torrents.totalsnatched = (SELECT MIN(torrents.totalsnatched) AS _col_0 FROM torrents AS torrents WHERE torrents.artist = 'lasean camry')	WhatCDHipHop
SELECT t2.groupname AS groupname FROM torrents AS t2 JOIN tags AS t1 ON t1.id = t2.id WHERE t1.tag = 'houston' ORDER BY t2.totalsnatched DESC LIMIT 1	WhatCDHipHop
SELECT torrents.artist AS artist FROM torrents AS torrents WHERE torrents.groupyear > 2010 GROUP BY torrents.artist	WhatCDHipHop
SELECT SUM(torrents.totalsnatched) AS _col_0, torrents.releasetype AS releasetype FROM torrents AS torrents GROUP BY torrents.releasetype	WhatCDHipHop
SELECT SUM(torrents.totalsnatched) AS _col_0 FROM torrents AS torrents WHERE torrents.groupyear BETWEEN 2000 AND 2010 UNION SELECT SUM(torrents.totalsnatched) AS _col_0 FROM torrents AS torrents WHERE torrents.groupyear < 2000	WhatCDHipHop
SELECT DISTINCT torrents.groupname AS groupname FROM torrents AS torrents WHERE torrents.totalsnatched > 100 AND torrents.releasetype = 'album'	WhatCDHipHop
SELECT torrents.artist AS artist FROM torrents AS torrents GROUP BY torrents.artist ORDER BY COUNT(torrents.groupname) DESC LIMIT 1	WhatCDHipHop
SELECT torrents.releasetype AS releasetype FROM torrents AS torrents GROUP BY torrents.releasetype ORDER BY SUM(torrents.totalsnatched) DESC LIMIT 1	WhatCDHipHop
SELECT torrents.groupyear AS groupyear FROM torrents AS torrents GROUP BY torrents.groupyear ORDER BY COUNT(torrents.groupname) LIMIT 1	WhatCDHipHop
SELECT torrents.groupyear AS groupyear FROM torrents AS torrents GROUP BY torrents.groupyear ORDER BY COUNT(torrents.groupname) DESC LIMIT 1	WhatCDHipHop
SELECT torrents.artist AS artist FROM torrents AS torrents WHERE torrents.groupyear = 2015 GROUP BY torrents.artist ORDER BY torrents.totalsnatched DESC LIMIT 1	WhatCDHipHop
SELECT COUNT(football_data.league) AS _col_0 FROM football_data AS football_data WHERE football_data.country <> 'Scotland' AND football_data.country <> 'England' AND football_data.referee <> ''	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM football_data AS football_data WHERE football_data.fthg + football_data.ftag > 5	WorldSoccerDataBase
SELECT COUNT(football_data.div) AS _col_0 FROM football_data AS football_data	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM football_data AS football_data WHERE football_data.b365h > football_data.psh	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM football_data AS football_data WHERE football_data.psh <> '' AND football_data.psd <> '' AND football_data.psa <> ''	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM football_data AS football_data WHERE football_data.season LIKE '%2010%' AND football_data.country = 'Spain'	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM football_data AS football_data WHERE football_data.fthg = 0 AND football_data.ftag = 0	WorldSoccerDataBase
SELECT football_data.awayteam AS awayteam FROM football_data AS football_data WHERE football_data.hometeam = 'Omiya Ardija' AND football_data.season LIKE '%2018%'	WorldSoccerDataBase
SELECT MAX(football_data.b365a) AS _col_0 FROM football_data AS football_data	WorldSoccerDataBase
SELECT football_data.b365d AS b365d FROM football_data AS football_data WHERE football_data.hometeam = 'Swindon' AND football_data.awayteam = 'Millwall' AND football_data.season = '2016/2017'	WorldSoccerDataBase
SELECT betfront.match AS match FROM betfront AS betfront ORDER BY betfront.draw_opening DESC LIMIT 1	WorldSoccerDataBase
SELECT betfront.year AS year FROM betfront AS betfront GROUP BY betfront.year ORDER BY COUNT(*) DESC LIMIT 1	WorldSoccerDataBase
