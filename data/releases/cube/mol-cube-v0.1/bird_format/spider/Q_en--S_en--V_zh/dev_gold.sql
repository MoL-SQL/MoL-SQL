SELECT COUNT(*) AS _col_0 FROM concert AS concert WHERE concert.year = 2014 OR concert.year = 2015	concert_singer
SELECT t2.name AS name, t2.capacity AS capacity FROM concert AS t1 JOIN stadium AS t2 ON t1.stadium_id = t2.stadium_id WHERE t1.year > 2013 GROUP BY t2.stadium_id ORDER BY COUNT(*) DESC LIMIT 1	concert_singer
SELECT COUNT(*) AS _col_0 FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t2.petid = t3.petid WHERE t1.sex = 'F' AND t3.pettype = '狗'	pets_1
SELECT DISTINCT t1.fname AS fname FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫' OR t3.pettype = '狗'	pets_1
SELECT t1.fname AS fname FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫' INTERSECT SELECT t1.fname AS fname FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '狗'	pets_1
SELECT student.major AS major, student.age AS age FROM student AS student WHERE NOT student.stuid IN (SELECT t1.stuid AS stuid FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫')	pets_1
SELECT student.stuid AS stuid FROM student AS student EXCEPT SELECT t1.stuid AS stuid FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫'	pets_1
SELECT t1.fname AS fname, t1.age AS age FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '狗' AND NOT t1.stuid IN (SELECT t1.stuid AS stuid FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫')	pets_1
SELECT t1.fname AS fname, t1.age AS age FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '狗' AND NOT t1.stuid IN (SELECT t1.stuid AS stuid FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pettype = '猫')	pets_1
SELECT t1.lname AS lname FROM student AS t1 JOIN has_pet AS t2 ON t1.stuid = t2.stuid JOIN pets AS t3 ON t3.petid = t2.petid WHERE t3.pet_age = 3 AND t3.pettype = '猫'	pets_1
SELECT t1.accelerate AS accelerate FROM cars_data AS t1 JOIN car_names AS t2 ON t1.id = t2.makeid WHERE t2.make = 'AMC Hornet Sportabout（旅行版）'	car_1
SELECT t1.countryname AS countryname FROM countries AS t1 JOIN continents AS t2 ON t1.continent = t2.contid JOIN car_makers AS t3 ON t1.countryid = t3.country WHERE t2.continent = '欧洲' GROUP BY t1.countryname HAVING COUNT(*) >= 3	car_1
SELECT t1.countryname AS countryname FROM countries AS t1 JOIN continents AS t2 ON t1.continent = t2.contid JOIN car_makers AS t3 ON t1.countryid = t3.country WHERE t2.continent = '欧洲' GROUP BY t1.countryname HAVING COUNT(*) >= 3	car_1
SELECT AVG(t2.edispl) AS _col_0 FROM car_names AS t1 JOIN cars_data AS t2 ON t1.makeid = t2.id WHERE t1.model = '沃尔沃'	car_1
SELECT AVG(t2.edispl) AS _col_0 FROM car_names AS t1 JOIN cars_data AS t2 ON t1.makeid = t2.id WHERE t1.model = '沃尔沃'	car_1
SELECT t1.cylinders AS cylinders FROM cars_data AS t1 JOIN car_names AS t2 ON t1.id = t2.makeid WHERE t2.model = '沃尔沃' ORDER BY t1.accelerate ASC LIMIT 1	car_1
SELECT t1.countryid AS countryid, t1.countryname AS countryname FROM countries AS t1 JOIN car_makers AS t2 ON t1.countryid = t2.country GROUP BY t1.countryid HAVING COUNT(*) > 3 UNION SELECT t1.countryid AS countryid, t1.countryname AS countryname FROM countries AS t1 JOIN car_makers AS t2 ON t1.countryid = t2.country JOIN model_list AS t3 ON t2.id = t3.maker WHERE t3.model = '菲亚特'	car_1
SELECT t1.countryid AS countryid, t1.countryname AS countryname FROM countries AS t1 JOIN car_makers AS t2 ON t1.countryid = t2.country GROUP BY t1.countryid HAVING COUNT(*) > 3 UNION SELECT t1.countryid AS countryid, t1.countryname AS countryname FROM countries AS t1 JOIN car_makers AS t2 ON t1.countryid = t2.country JOIN model_list AS t3 ON t2.id = t3.maker WHERE t3.model = '菲亚特'	car_1
SELECT airlines.country AS country FROM airlines AS airlines WHERE airlines.airline = '捷蓝航空'	flight_2
SELECT airlines.country AS country FROM airlines AS airlines WHERE airlines.airline = '捷蓝航空'	flight_2
SELECT airlines.abbreviation AS abbreviation FROM airlines AS airlines WHERE airlines.airline = '捷蓝航空'	flight_2
SELECT airlines.abbreviation AS abbreviation FROM airlines AS airlines WHERE airlines.airline = '捷蓝航空'	flight_2
SELECT airlines.airline AS airline FROM airlines AS airlines WHERE airlines.abbreviation = 'UAL（联合航空控股公司）'	flight_2
SELECT airlines.airline AS airline FROM airlines AS airlines WHERE airlines.abbreviation = 'UAL（联合航空控股公司）'	flight_2
SELECT COUNT(*) AS _col_0 FROM airlines AS t1 JOIN flights AS t2 ON t2.airline = t1.uid WHERE t1.airline = '联合航空' AND t2.destairport = 'ASY'	flight_2
SELECT COUNT(*) AS _col_0 FROM airlines AS t1 JOIN flights AS t2 ON t2.airline = t1.uid WHERE t1.airline = '联合航空' AND t2.sourceairport = 'AHD'	flight_2
SELECT t1.flightno AS flightno FROM flights AS t1 JOIN airlines AS t2 ON t2.uid = t1.airline WHERE t2.airline = '联合航空'	flight_2
SELECT t1.flightno AS flightno FROM flights AS t1 JOIN airlines AS t2 ON t2.uid = t1.airline WHERE t2.airline = '联合航空'	flight_2
SELECT t1.name AS name FROM employee AS t1 JOIN evaluation AS t2 ON t1.employee_id = t2.employee_id GROUP BY t2.employee_id ORDER BY COUNT(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t2.name AS name FROM hiring AS t1 JOIN shop AS t2 ON t1.shop_id = t2.shop_id GROUP BY t1.shop_id ORDER BY COUNT(*) DESC LIMIT 1	employee_hire_evaluation
SELECT ref_template_types.template_type_code AS template_type_code FROM ref_template_types AS ref_template_types WHERE ref_template_types.template_type_description = '图书'	cre_Doc_Template_Mgt
SELECT ref_template_types.template_type_code AS template_type_code FROM ref_template_types AS ref_template_types WHERE ref_template_types.template_type_description = '图书'	cre_Doc_Template_Mgt
SELECT t2.template_id AS template_id FROM ref_template_types AS t1 JOIN templates AS t2 ON t1.template_type_code = t2.template_type_code WHERE t1.template_type_description = '演示文稿'	cre_Doc_Template_Mgt
SELECT t2.template_id AS template_id FROM ref_template_types AS t1 JOIN templates AS t2 ON t1.template_type_code = t2.template_type_code WHERE t1.template_type_description = '演示文稿'	cre_Doc_Template_Mgt
SELECT paragraphs.other_details AS other_details FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text LIKE '韩国'	cre_Doc_Template_Mgt
SELECT paragraphs.other_details AS other_details FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text LIKE '韩国'	cre_Doc_Template_Mgt
SELECT paragraphs.document_id AS document_id FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text = '巴西' INTERSECT SELECT paragraphs.document_id AS document_id FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text = '爱尔兰'	cre_Doc_Template_Mgt
SELECT paragraphs.document_id AS document_id FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text = '巴西' INTERSECT SELECT paragraphs.document_id AS document_id FROM paragraphs AS paragraphs WHERE paragraphs.paragraph_text = '爱尔兰'	cre_Doc_Template_Mgt
SELECT COUNT(*) AS _col_0 FROM teacher AS teacher	course_teach
SELECT t3.name AS name FROM course_arrange AS t1 JOIN course AS t2 ON t1.course_id = t2.course_id JOIN teacher AS t3 ON t1.teacher_id = t3.teacher_id WHERE t2.course = '数学'	course_teach
SELECT t3.name AS name FROM course_arrange AS t1 JOIN course AS t2 ON t1.course_id = t2.course_id JOIN teacher AS t3 ON t1.teacher_id = t3.teacher_id WHERE t2.course = '数学'	course_teach
SELECT AVG(visitor.age) AS _col_0 FROM visitor AS visitor WHERE visitor.level_of_membership <= 4	museum_visit
SELECT t1.id AS id, t1.name AS name, t1.age AS age FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id GROUP BY t1.id HAVING COUNT(*) > 1	museum_visit
SELECT players.first_name AS first_name, players.last_name AS last_name FROM players AS players ORDER BY players.birth_date	wta_1
SELECT COUNT(*) AS _col_0, players.country_code AS country_code FROM players AS players GROUP BY players.country_code	wta_1
SELECT COUNT(*) AS _col_0 FROM ship AS ship WHERE ship.disposition_of_ship = '被俘获'	battle_death
SELECT battle.name AS name, battle.result AS result FROM battle AS battle WHERE battle.bulgarian_commander <> '博里尔'	battle_death
SELECT DISTINCT t1.id AS id, t1.name AS name FROM battle AS t1 JOIN ship AS t2 ON t1.id = t2.lost_in_battle WHERE t2.ship_type = '双桅横帆船'	battle_death
SELECT battle.name AS name FROM battle AS battle WHERE battle.bulgarian_commander = '卡洛扬' AND battle.latin_commander = '鲍德温一世'	battle_death
SELECT battle.name AS name, battle.result AS result, battle.bulgarian_commander AS bulgarian_commander FROM battle AS battle EXCEPT SELECT t1.name AS name, t1.result AS result, t1.bulgarian_commander AS bulgarian_commander FROM battle AS t1 JOIN ship AS t2 ON t1.id = t2.lost_in_battle WHERE t2.location = '英吉利海峡'	battle_death
SELECT death.note AS note FROM death AS death WHERE death.note LIKE '%东%'	battle_death
SELECT t1.degree_program_id AS degree_program_id, t1.degree_summary_name AS degree_summary_name FROM degree_programs AS t1 JOIN student_enrolment AS t2 ON t1.degree_program_id = t2.degree_program_id GROUP BY t1.degree_program_id ORDER BY COUNT(*) DESC LIMIT 1	student_transcripts_tracking
SELECT t1.degree_program_id AS degree_program_id, t1.degree_summary_name AS degree_summary_name FROM degree_programs AS t1 JOIN student_enrolment AS t2 ON t1.degree_program_id = t2.degree_program_id GROUP BY t1.degree_program_id ORDER BY COUNT(*) DESC LIMIT 1	student_transcripts_tracking
SELECT cartoon.title AS title FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯'	tvshow
SELECT cartoon.title AS title FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯'	tvshow
SELECT COUNT(*) AS _col_0 FROM cartoon AS cartoon WHERE cartoon.written_by = '约瑟夫·库尔'	tvshow
SELECT COUNT(*) AS _col_0 FROM cartoon AS cartoon WHERE cartoon.written_by = '约瑟夫·库尔'	tvshow
SELECT cartoon.title AS title FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯' OR cartoon.directed_by = '布兰登·维蒂'	tvshow
SELECT cartoon.title AS title FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯' OR cartoon.directed_by = '布兰登·维蒂'	tvshow
SELECT COUNT(*) AS _col_0 FROM tv_channel AS tv_channel WHERE tv_channel.language = '英语'	tvshow
SELECT COUNT(*) AS _col_0 FROM tv_channel AS tv_channel WHERE tv_channel.language = '英语'	tvshow
SELECT tv_series.air_date AS air_date FROM tv_series AS tv_series WHERE tv_series.episode = '一生之爱'	tvshow
SELECT tv_series.air_date AS air_date FROM tv_series AS tv_series WHERE tv_series.episode = '一生之爱'	tvshow
SELECT tv_series.weekly_rank AS weekly_rank FROM tv_series AS tv_series WHERE tv_series.episode = '一生之爱'	tvshow
SELECT tv_series.weekly_rank AS weekly_rank FROM tv_series AS tv_series WHERE tv_series.episode = '一生之爱'	tvshow
SELECT tv_channel.package_option AS package_option, tv_channel.series_name AS series_name FROM tv_channel AS tv_channel WHERE tv_channel.hight_definition_tv = '是'	tvshow
SELECT tv_channel.package_option AS package_option, tv_channel.series_name AS series_name FROM tv_channel AS tv_channel WHERE tv_channel.hight_definition_tv = '是'	tvshow
SELECT tv_channel.pixel_aspect_ratio_par AS pixel_aspect_ratio_par, tv_channel.country AS country FROM tv_channel AS tv_channel WHERE tv_channel.language <> '英语'	tvshow
SELECT tv_channel.id AS id FROM tv_channel AS tv_channel EXCEPT SELECT cartoon.channel AS channel FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯'	tvshow
SELECT tv_channel.package_option AS package_option FROM tv_channel AS tv_channel WHERE NOT tv_channel.id IN (SELECT cartoon.channel AS channel FROM cartoon AS cartoon WHERE cartoon.directed_by = '本·琼斯')	tvshow
SELECT people.name AS name FROM people AS people WHERE people.nationality <> '俄罗斯'	poker_player
SELECT people.name AS name FROM people AS people WHERE people.nationality <> '俄罗斯'	poker_player
SELECT people.name AS name FROM people AS people WHERE NOT people.people_id IN (SELECT poker_player.people_id AS people_id FROM poker_player AS poker_player)	poker_player
SELECT COUNT(*) AS _col_0 FROM area_code_state AS area_code_state	voter_1
SELECT t1.contestant_number AS contestant_number, t1.contestant_name AS contestant_name FROM contestants AS t1 JOIN votes AS t2 ON t1.contestant_number = t2.contestant_number GROUP BY t1.contestant_number ORDER BY COUNT(*) ASC LIMIT 1	voter_1
SELECT COUNT(*) AS _col_0 FROM country AS country WHERE country.governmentform = '共和国'	world_1
SELECT country.name AS name FROM country AS country WHERE country.continent = '亚洲' ORDER BY country.lifeexpectancy LIMIT 1	world_1
SELECT AVG(country.gnp) AS _col_0, SUM(country.population) AS _col_1 FROM country AS country WHERE country.governmentform = '美国领土'	world_1
SELECT t2.language AS language FROM country AS t1 JOIN countrylanguage AS t2 ON t1.code = t2.countrycode WHERE t1.governmentform = '共和国' GROUP BY t2.language HAVING COUNT(*) = 1	world_1
SELECT country.name AS name FROM country AS country WHERE country.continent = '亚洲' AND country.population > (SELECT MIN(country.population) AS _col_0 FROM country AS country WHERE country.continent = '非洲')	world_1
SELECT DISTINCT t2.name AS name FROM country AS t1 JOIN city AS t2 ON t2.countrycode = t1.code WHERE t1.continent = '欧洲' AND NOT t1.name IN (SELECT t3.name AS name FROM country AS t3 JOIN countrylanguage AS t4 ON t3.code = t4.countrycode WHERE t4.isofficial = 'T' AND t4.language = 'English')	world_1
SELECT DISTINCT t3.name AS name FROM country AS t1 JOIN countrylanguage AS t2 ON t1.code = t2.countrycode JOIN city AS t3 ON t1.code = t3.countrycode WHERE t2.isofficial = 'T' AND t2.language = 'Chinese' AND t1.continent = '亚洲'	world_1
SELECT COUNT(*) AS _col_0 FROM country AS country WHERE country.continent = '亚洲'	world_1
SELECT COUNT(*) AS _col_0 FROM country AS country WHERE country.continent = '亚洲'	world_1
SELECT conductor.name AS name FROM conductor AS conductor WHERE conductor.nationality <> '美国'	orchestra
SELECT conductor.name AS name FROM conductor AS conductor WHERE conductor.nationality <> '美国'	orchestra
SELECT MAX(performance.share) AS _col_0, MIN(performance.share) AS _col_1 FROM performance AS performance WHERE performance.type <> '直播总决赛'	orchestra
SELECT MAX(performance.share) AS _col_0, MIN(performance.share) AS _col_1 FROM performance AS performance WHERE performance.type <> '直播总决赛'	orchestra
SELECT highschooler.grade AS grade FROM highschooler AS highschooler GROUP BY highschooler.grade HAVING COUNT(*) >= 4	network_1
SELECT t2.name AS name FROM friend AS t1 JOIN highschooler AS t2 ON t1.student_id = t2.id GROUP BY t1.student_id ORDER BY COUNT(*) DESC LIMIT 1	network_1
SELECT t1.professional_id AS professional_id, t1.cell_number AS cell_number FROM professionals AS t1 JOIN treatments AS t2 ON t1.professional_id = t2.professional_id GROUP BY t1.professional_id HAVING COUNT(*) >= 2	dog_kennels
SELECT t1.name AS name, t2.date_of_treatment AS date_of_treatment FROM dogs AS t1 JOIN treatments AS t2 ON t1.dog_id = t2.dog_id WHERE t1.breed_code = (SELECT dogs.breed_code AS breed_code FROM dogs AS dogs GROUP BY dogs.breed_code ORDER BY COUNT(*) ASC LIMIT 1)	dog_kennels
SELECT COUNT(*) AS _col_0 FROM singer AS singer	singer
SELECT singer.name AS name FROM singer AS singer WHERE singer.citizenship <> '法国'	singer
SELECT singer.name AS name FROM singer AS singer WHERE singer.citizenship <> '法国'	singer
SELECT COUNT(*) AS _col_0 FROM other_available_features AS other_available_features	real_estate_properties
