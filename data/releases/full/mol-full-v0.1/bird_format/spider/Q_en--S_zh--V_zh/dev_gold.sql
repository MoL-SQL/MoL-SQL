SELECT count(*) FROM `歌手`	concert_singer
SELECT count(*) FROM `歌手`	concert_singer
SELECT `姓名` ,  `国籍` ,  `年龄` FROM `歌手` ORDER BY `年龄` DESC	concert_singer
SELECT `姓名` ,  `国籍` ,  `年龄` FROM `歌手` ORDER BY `年龄` DESC	concert_singer
SELECT avg(`年龄`) ,  min(`年龄`) ,  max(`年龄`) FROM `歌手` WHERE `国籍`  =  'France'	concert_singer
SELECT avg(`年龄`) ,  min(`年龄`) ,  max(`年龄`) FROM `歌手` WHERE `国籍`  =  'France'	concert_singer
SELECT `歌曲名称` ,  `歌曲发行年份` FROM `歌手` ORDER BY `年龄` LIMIT 1	concert_singer
SELECT `歌曲名称` ,  `歌曲发行年份` FROM `歌手` ORDER BY `年龄` LIMIT 1	concert_singer
SELECT DISTINCT `国籍` FROM `歌手` WHERE `年龄`  >  20	concert_singer
SELECT DISTINCT `国籍` FROM `歌手` WHERE `年龄`  >  20	concert_singer
SELECT `国籍` ,  count(*) FROM `歌手` GROUP BY `国籍`	concert_singer
SELECT `国籍` ,  count(*) FROM `歌手` GROUP BY `国籍`	concert_singer
SELECT `歌曲名称` FROM `歌手` WHERE `年龄`  >  (SELECT avg(`年龄`) FROM `歌手`)	concert_singer
SELECT `歌曲名称` FROM `歌手` WHERE `年龄`  >  (SELECT avg(`年龄`) FROM `歌手`)	concert_singer
SELECT `所在地` ,  `名称` FROM `体育场` WHERE `容量` BETWEEN 5000 AND 10000	concert_singer
SELECT `所在地` ,  `名称` FROM `体育场` WHERE `容量` BETWEEN 5000 AND 10000	concert_singer
select max(`容量`), `平均票价` from `体育场`	concert_singer
select avg(`容量`) ,  max(`容量`) from `体育场`	concert_singer
SELECT `名称` ,  `容量` FROM `体育场` ORDER BY `平均票价` DESC LIMIT 1	concert_singer
SELECT `名称` ,  `容量` FROM `体育场` ORDER BY `平均票价` DESC LIMIT 1	concert_singer
SELECT count(*) FROM `演唱会` WHERE `年份`  =  2014 OR `年份`  =  2015	concert_singer
SELECT count(*) FROM `演唱会` WHERE `年份`  =  2014 OR `年份`  =  2015	concert_singer
SELECT T2.`名称` ,  count(*) FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` GROUP BY T1.`体育场编号`	concert_singer
SELECT T2.`名称` ,  count(*) FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` GROUP BY T1.`体育场编号`	concert_singer
SELECT T2.`名称` ,  T2.`容量` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  >=  2014 GROUP BY T2.`体育场编号` ORDER BY count(*) DESC LIMIT 1	concert_singer
select t2.`名称` ,  t2.`容量` from `演唱会` as t1 join `体育场` as t2 on t1.`体育场编号`  =  t2.`体育场编号` where t1.`年份`  >  2013 group by t2.`体育场编号` order by count(*) desc limit 1	concert_singer
SELECT `年份` FROM `演唱会` GROUP BY `年份` ORDER BY count(*) DESC LIMIT 1	concert_singer
SELECT `年份` FROM `演唱会` GROUP BY `年份` ORDER BY count(*) DESC LIMIT 1	concert_singer
SELECT `名称` FROM `体育场` WHERE `体育场编号` NOT IN (SELECT `体育场编号` FROM `演唱会`)	concert_singer
SELECT `名称` FROM `体育场` WHERE `体育场编号` NOT IN (SELECT `体育场编号` FROM `演唱会`)	concert_singer
SELECT `国籍` FROM `歌手` WHERE `年龄`  >  40 INTERSECT SELECT `国籍` FROM `歌手` WHERE `年龄`  <  30	concert_singer
SELECT `名称` FROM `体育场` EXCEPT SELECT T2.`名称` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2014	concert_singer
SELECT `名称` FROM `体育场` EXCEPT SELECT T2.`名称` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2014	concert_singer
SELECT T2.`演唱会名称` ,  T2.`主题` ,  count(*) FROM `歌手参演` AS T1 JOIN `演唱会` AS T2 ON T1.`演唱会编号`  =  T2.`演唱会编号` GROUP BY T2.`演唱会编号`	concert_singer
select t2.`演唱会名称` ,  t2.`主题` ,  count(*) from `歌手参演` as t1 join `演唱会` as t2 on t1.`演唱会编号`  =  t2.`演唱会编号` group by t2.`演唱会编号`	concert_singer
SELECT T2.`姓名` ,  count(*) FROM `歌手参演` AS T1 JOIN `歌手` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T2.`歌手编号`	concert_singer
SELECT T2.`姓名` ,  count(*) FROM `歌手参演` AS T1 JOIN `歌手` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T2.`歌手编号`	concert_singer
SELECT T2.`姓名` FROM `歌手参演` AS T1 JOIN `歌手` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` JOIN `演唱会` AS T3 ON T1.`演唱会编号`  =  T3.`演唱会编号` WHERE T3.`年份`  =  2014	concert_singer
SELECT T2.`姓名` FROM `歌手参演` AS T1 JOIN `歌手` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` JOIN `演唱会` AS T3 ON T1.`演唱会编号`  =  T3.`演唱会编号` WHERE T3.`年份`  =  2014	concert_singer
SELECT `姓名` ,  `国籍` FROM `歌手` WHERE `歌曲名称` LIKE '%Hey%'	concert_singer
SELECT `姓名` ,  `国籍` FROM `歌手` WHERE `歌曲名称` LIKE '%Hey%'	concert_singer
SELECT T2.`名称` ,  T2.`所在地` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2014 INTERSECT SELECT T2.`名称` ,  T2.`所在地` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2015	concert_singer
SELECT T2.`名称` ,  T2.`所在地` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2014 INTERSECT SELECT T2.`名称` ,  T2.`所在地` FROM `演唱会` AS T1 JOIN `体育场` AS T2 ON T1.`体育场编号`  =  T2.`体育场编号` WHERE T1.`年份`  =  2015	concert_singer
select count(*) from `演唱会` where `体育场编号` = (select `体育场编号` from `体育场` order by `容量` desc limit 1)	concert_singer
select count(*) from `演唱会` where `体育场编号` = (select `体育场编号` from `体育场` order by `容量` desc limit 1)	concert_singer
SELECT count(*) FROM `宠物` WHERE `体重`  >  10	pets_1
SELECT count(*) FROM `宠物` WHERE `体重`  >  10	pets_1
SELECT `体重` FROM `宠物` ORDER BY `宠物年龄` LIMIT 1	pets_1
SELECT `体重` FROM `宠物` ORDER BY `宠物年龄` LIMIT 1	pets_1
SELECT max(`体重`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT max(`体重`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT count(*) FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T1.`年龄`  >  20	pets_1
SELECT count(*) FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T1.`年龄`  >  20	pets_1
SELECT count(*) FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T2.`宠物编号`  =  T3.`宠物编号` WHERE T1.`性别`  =  'F' AND T3.`宠物类型`  =  '狗'	pets_1
SELECT count(*) FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T2.`宠物编号`  =  T3.`宠物编号` WHERE T1.`性别`  =  'F' AND T3.`宠物类型`  =  '狗'	pets_1
SELECT count(DISTINCT `宠物类型`) FROM `宠物`	pets_1
SELECT count(DISTINCT `宠物类型`) FROM `宠物`	pets_1
SELECT DISTINCT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫' OR T3.`宠物类型`  =  '狗'	pets_1
SELECT DISTINCT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫' OR T3.`宠物类型`  =  '狗'	pets_1
select t1.`名` from `学生` as t1 join `拥有宠物` as t2 on t1.`学生编号`  =  t2.`学生编号` join `宠物` as t3 on t3.`宠物编号`  =  t2.`宠物编号` where t3.`宠物类型`  =  '猫' intersect select t1.`名` from `学生` as t1 join `拥有宠物` as t2 on t1.`学生编号`  =  t2.`学生编号` join `宠物` as t3 on t3.`宠物编号`  =  t2.`宠物编号` where t3.`宠物类型`  =  '狗'	pets_1
SELECT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫' INTERSECT SELECT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '狗'	pets_1
SELECT `专业` ,  `年龄` FROM `学生` WHERE `学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT `专业` ,  `年龄` FROM `学生` WHERE `学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT `学生编号` FROM `学生` EXCEPT SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫'	pets_1
SELECT `学生编号` FROM `学生` EXCEPT SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫'	pets_1
SELECT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '狗' AND T1.`学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '狗' AND T1.`学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT `宠物类型` ,  `体重` FROM `宠物` ORDER BY `宠物年龄` LIMIT 1	pets_1
SELECT `宠物类型` ,  `体重` FROM `宠物` ORDER BY `宠物年龄` LIMIT 1	pets_1
SELECT `宠物编号` ,  `体重` FROM `宠物` WHERE `宠物年龄`  >  1	pets_1
SELECT `宠物编号` ,  `体重` FROM `宠物` WHERE `宠物年龄`  >  1	pets_1
SELECT avg(`宠物年龄`) ,  max(`宠物年龄`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT avg(`宠物年龄`) ,  max(`宠物年龄`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT avg(`体重`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT avg(`体重`) ,  `宠物类型` FROM `宠物` GROUP BY `宠物类型`	pets_1
SELECT DISTINCT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号`	pets_1
SELECT DISTINCT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号`	pets_1
SELECT T2.`宠物编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T1.`姓`  =  'Smith'	pets_1
SELECT T2.`宠物编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T1.`姓`  =  'Smith'	pets_1
SELECT count(*) ,  T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号`	pets_1
select count(*) ,  t1.`学生编号` from `学生` as t1 join `拥有宠物` as t2 on t1.`学生编号`  =  t2.`学生编号` group by t1.`学生编号`	pets_1
SELECT T1.`名` ,  T1.`性别` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >  1	pets_1
SELECT T1.`名` ,  T1.`性别` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >  1	pets_1
SELECT T1.`姓` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物年龄`  =  3 AND T3.`宠物类型`  =  '猫'	pets_1
SELECT T1.`姓` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物年龄`  =  3 AND T3.`宠物类型`  =  '猫'	pets_1
select avg(`年龄`) from `学生` where `学生编号` not in (select `学生编号` from `拥有宠物`)	pets_1
select avg(`年龄`) from `学生` where `学生编号` not in (select `学生编号` from `拥有宠物`)	pets_1
SELECT count(*) FROM `大洲`;	car_1
SELECT count(*) FROM `大洲`;	car_1
SELECT T1.`大洲编号` ,  T1.`大洲名称` ,  count(*) FROM `大洲` AS T1 JOIN `国家` AS T2 ON T1.`大洲编号`  =  T2.`所属大洲` GROUP BY T1.`大洲编号`;	car_1
SELECT T1.`大洲编号` ,  T1.`大洲名称` ,  count(*) FROM `大洲` AS T1 JOIN `国家` AS T2 ON T1.`大洲编号`  =  T2.`所属大洲` GROUP BY T1.`大洲编号`;	car_1
SELECT count(*) FROM `国家`;	car_1
SELECT count(*) FROM `国家`;	car_1
SELECT T1.`制造商全称` ,  T1.`制造商编号` ,  count(*) FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` GROUP BY T1.`制造商编号`;	car_1
SELECT T1.`制造商全称` ,  T1.`制造商编号` ,  count(*) FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` GROUP BY T1.`制造商编号`;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` ORDER BY T2.`马力` ASC LIMIT 1;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` ORDER BY T2.`马力` ASC LIMIT 1;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`车重（磅）`  <  (SELECT avg(`车重（磅）`) FROM `汽车数据`)	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`车重（磅）`  <  (SELECT avg(`车重（磅）`) FROM `汽车数据`)	car_1
SELECT DISTINCT T1.`制造商简称` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` JOIN `汽车名称` AS T3 ON T2.`车型名称`  =  T3.`车型名称` JOIN `汽车数据` AS T4 ON T3.`品牌编号`  =  T4.`汽车编号` WHERE T4.`生产年份`  =  '1970';	car_1
SELECT DISTINCT T1.`制造商简称` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` JOIN `汽车名称` AS T3 ON T2.`车型名称`  =  T3.`车型名称` JOIN `汽车数据` AS T4 ON T3.`品牌编号`  =  T4.`汽车编号` WHERE T4.`生产年份`  =  '1970';	car_1
SELECT T2.`品牌名称` ,  T1.`生产年份` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T1.`生产年份`  =  (SELECT min(`生产年份`) FROM `汽车数据`);	car_1
SELECT T2.`品牌名称` ,  T1.`生产年份` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T1.`生产年份`  =  (SELECT min(`生产年份`) FROM `汽车数据`);	car_1
SELECT DISTINCT T1.`车型名称` FROM `车型列表` AS T1 JOIN `汽车名称` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车数据` AS T3 ON T2.`品牌编号`  =  T3.`汽车编号` WHERE T3.`生产年份`  >  1980;	car_1
SELECT DISTINCT T1.`车型名称` FROM `车型列表` AS T1 JOIN `汽车名称` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车数据` AS T3 ON T2.`品牌编号`  =  T3.`汽车编号` WHERE T3.`生产年份`  >  1980;	car_1
SELECT T1.`大洲名称` ,  count(*) FROM `大洲` AS T1 JOIN `国家` AS T2 ON T1.`大洲编号`  =  T2.`所属大洲` JOIN `汽车制造商` AS T3 ON T2.`国家编号`  =  T3.`所属国家` GROUP BY T1.`大洲名称`;	car_1
SELECT T1.`大洲名称` ,  count(*) FROM `大洲` AS T1 JOIN `国家` AS T2 ON T1.`大洲编号`  =  T2.`所属大洲` JOIN `汽车制造商` AS T3 ON T2.`国家编号`  =  T3.`所属国家` GROUP BY T1.`大洲名称`;	car_1
SELECT T2.`国家名称` FROM `汽车制造商` AS T1 JOIN `国家` AS T2 ON T1.`所属国家`  =  T2.`国家编号` GROUP BY T1.`所属国家` ORDER BY Count(*) DESC LIMIT 1;	car_1
SELECT T2.`国家名称` FROM `汽车制造商` AS T1 JOIN `国家` AS T2 ON T1.`所属国家`  =  T2.`国家编号` GROUP BY T1.`所属国家` ORDER BY Count(*) DESC LIMIT 1;	car_1
select count(*) ,  t2.`制造商全称` from `车型列表` as t1 join `汽车制造商` as t2 on t1.`制造商简称`  =  t2.`制造商编号` group by t2.`制造商编号`;	car_1
SELECT Count(*) ,  T2.`制造商全称` ,  T2.`制造商编号` FROM `车型列表` AS T1 JOIN `汽车制造商` AS T2 ON T1.`制造商简称`  =  T2.`制造商编号` GROUP BY T2.`制造商编号`;	car_1
SELECT T1.`0–60英里/小时加速时间（秒）` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`品牌名称`  =  'AMC Hornet Sportabout（旅行版）';	car_1
SELECT T1.`0–60英里/小时加速时间（秒）` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`品牌名称`  =  'AMC Hornet Sportabout（旅行版）';	car_1
SELECT count(*) FROM `汽车制造商` AS T1 JOIN `国家` AS T2 ON T1.`所属国家`  =  T2.`国家编号` WHERE T2.`国家名称`  =  'france';	car_1
SELECT count(*) FROM `汽车制造商` AS T1 JOIN `国家` AS T2 ON T1.`所属国家`  =  T2.`国家编号` WHERE T2.`国家名称`  =  'france';	car_1
SELECT count(*) FROM `车型列表` AS T1 JOIN `汽车制造商` AS T2 ON T1.`制造商简称`  =  T2.`制造商编号` JOIN `国家` AS T3 ON T2.`所属国家`  =  T3.`国家编号` WHERE T3.`国家名称`  =  'usa';	car_1
SELECT count(*) FROM `车型列表` AS T1 JOIN `汽车制造商` AS T2 ON T1.`制造商简称`  =  T2.`制造商编号` JOIN `国家` AS T3 ON T2.`所属国家`  =  T3.`国家编号` WHERE T3.`国家名称`  =  'usa';	car_1
SELECT avg(`百公里油耗（英里/加仑）`) FROM `汽车数据` WHERE `气缸数`  =  4;	car_1
SELECT avg(`百公里油耗（英里/加仑）`) FROM `汽车数据` WHERE `气缸数`  =  4;	car_1
select min(`车重（磅）`) from `汽车数据` where `气缸数`  =  8 and `生产年份`  =  1974	car_1
select min(`车重（磅）`) from `汽车数据` where `气缸数`  =  8 and `生产年份`  =  1974	car_1
SELECT `制造商简称` ,  `车型名称` FROM `车型列表`;	car_1
SELECT `制造商简称` ,  `车型名称` FROM `车型列表`;	car_1
SELECT T1.`国家名称` ,  T1.`国家编号` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` GROUP BY T1.`国家编号` HAVING count(*)  >=  1;	car_1
SELECT T1.`国家名称` ,  T1.`国家编号` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` GROUP BY T1.`国家编号` HAVING count(*)  >=  1;	car_1
SELECT count(*) FROM `汽车数据` WHERE `马力`  >  150;	car_1
SELECT count(*) FROM `汽车数据` WHERE `马力`  >  150;	car_1
SELECT avg(`车重（磅）`) ,  `生产年份` FROM `汽车数据` GROUP BY `生产年份`;	car_1
SELECT avg(`车重（磅）`) ,  `生产年份` FROM `汽车数据` GROUP BY `生产年份`;	car_1
SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `大洲` AS T2 ON T1.`所属大洲`  =  T2.`大洲编号` JOIN `汽车制造商` AS T3 ON T1.`国家编号`  =  T3.`所属国家` WHERE T2.`大洲名称`  =  '欧洲' GROUP BY T1.`国家名称` HAVING count(*)  >=  3;	car_1
SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `大洲` AS T2 ON T1.`所属大洲`  =  T2.`大洲编号` JOIN `汽车制造商` AS T3 ON T1.`国家编号`  =  T3.`所属国家` WHERE T2.`大洲名称`  =  '欧洲' GROUP BY T1.`国家名称` HAVING count(*)  >=  3;	car_1
SELECT T2.`马力` ,  T1.`品牌名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`气缸数`  =  3 ORDER BY T2.`马力` DESC LIMIT 1;	car_1
SELECT T2.`马力` ,  T1.`品牌名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`气缸数`  =  3 ORDER BY T2.`马力` DESC LIMIT 1;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` ORDER BY T2.`百公里油耗（英里/加仑）` DESC LIMIT 1;	car_1
select t1.`车型名称` from `汽车名称` as t1 join `汽车数据` as t2 on t1.`品牌编号`  =  t2.`汽车编号` order by t2.`百公里油耗（英里/加仑）` desc limit 1;	car_1
SELECT avg(`马力`) FROM `汽车数据` WHERE `生产年份`  <  1980;	car_1
select avg(`马力`) from `汽车数据` where `生产年份`  <  1980;	car_1
SELECT avg(T2.`排量（升）`) FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T1.`车型名称`  =  '沃尔沃';	car_1
SELECT avg(T2.`排量（升）`) FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T1.`车型名称`  =  '沃尔沃';	car_1
SELECT max(`0–60英里/小时加速时间（秒）`) ,  `气缸数` FROM `汽车数据` GROUP BY `气缸数`;	car_1
SELECT max(`0–60英里/小时加速时间（秒）`) ,  `气缸数` FROM `汽车数据` GROUP BY `气缸数`;	car_1
SELECT `车型名称` FROM `汽车名称` GROUP BY `车型名称` ORDER BY count(*) DESC LIMIT 1;	car_1
SELECT `车型名称` FROM `汽车名称` GROUP BY `车型名称` ORDER BY count(*) DESC LIMIT 1;	car_1
SELECT count(*) FROM `汽车数据` WHERE `气缸数`  >  4;	car_1
SELECT count(*) FROM `汽车数据` WHERE `气缸数`  >  4;	car_1
SELECT count(*) FROM `汽车数据` WHERE `生产年份`  =  1980;	car_1
SELECT count(*) FROM `汽车数据` WHERE `生产年份`  =  1980;	car_1
SELECT count(*) FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` WHERE T1.`制造商全称`  =  'American Motor Company';	car_1
SELECT count(*) FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` WHERE T1.`制造商全称`  =  'American Motor Company';	car_1
SELECT T1.`制造商全称` ,  T1.`制造商编号` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` GROUP BY T1.`制造商编号` HAVING count(*)  >  3;	car_1
SELECT T1.`制造商全称` ,  T1.`制造商编号` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` GROUP BY T1.`制造商编号` HAVING count(*)  >  3;	car_1
SELECT DISTINCT T2.`车型名称` FROM `汽车名称` AS T1 JOIN `车型列表` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车制造商` AS T3 ON T2.`制造商简称`  =  T3.`制造商编号` JOIN `汽车数据` AS T4 ON T1.`品牌编号`  =  T4.`汽车编号` WHERE T3.`制造商全称`  =  'General Motors' OR T4.`车重（磅）`  >  3500;	car_1
SELECT DISTINCT T2.`车型名称` FROM `汽车名称` AS T1 JOIN `车型列表` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车制造商` AS T3 ON T2.`制造商简称`  =  T3.`制造商编号` JOIN `汽车数据` AS T4 ON T1.`品牌编号`  =  T4.`汽车编号` WHERE T3.`制造商全称`  =  'General Motors' OR T4.`车重（磅）`  >  3500;	car_1
select distinct `生产年份` from `汽车数据` where `车重（磅）` between 3000 and 4000;	car_1
select distinct `生产年份` from `汽车数据` where `车重（磅）` between 3000 and 4000;	car_1
SELECT T1.`马力` FROM `汽车数据` AS T1 ORDER BY T1.`0–60英里/小时加速时间（秒）` DESC LIMIT 1;	car_1
SELECT T1.`马力` FROM `汽车数据` AS T1 ORDER BY T1.`0–60英里/小时加速时间（秒）` DESC LIMIT 1;	car_1
SELECT T1.`气缸数` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`车型名称`  =  '沃尔沃' ORDER BY T1.`0–60英里/小时加速时间（秒）` ASC LIMIT 1;	car_1
SELECT T1.`气缸数` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`车型名称`  =  '沃尔沃' ORDER BY T1.`0–60英里/小时加速时间（秒）` ASC LIMIT 1;	car_1
SELECT COUNT(*) FROM `汽车数据` WHERE `0–60英里/小时加速时间（秒）`  >  ( SELECT `0–60英里/小时加速时间（秒）` FROM `汽车数据` ORDER BY `马力` DESC LIMIT 1 );	car_1
SELECT COUNT(*) FROM `汽车数据` WHERE `0–60英里/小时加速时间（秒）`  >  ( SELECT `0–60英里/小时加速时间（秒）` FROM `汽车数据` ORDER BY `马力` DESC LIMIT 1 );	car_1
select count(*) from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` group by t1.`国家编号` having count(*)  >  2	car_1
select count(*) from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` group by t1.`国家编号` having count(*)  >  2	car_1
SELECT COUNT(*) FROM `汽车数据` WHERE `气缸数`  >  6;	car_1
SELECT COUNT(*) FROM `汽车数据` WHERE `气缸数`  >  6;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`气缸数`  =  4 ORDER BY T2.`马力` DESC LIMIT 1;	car_1
SELECT T1.`车型名称` FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T2.`气缸数`  =  4 ORDER BY T2.`马力` DESC LIMIT 1;	car_1
SELECT T2.`品牌编号` ,  T2.`品牌名称` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T1.`马力`  >  (SELECT min(`马力`) FROM `汽车数据`) AND T1.`气缸数`  <=  3;	car_1
select t2.`品牌编号` ,  t2.`品牌名称` from `汽车数据` as t1 join `汽车名称` as t2 on t1.`汽车编号`  =  t2.`品牌编号` where t1.`马力`  >  (select min(`马力`) from `汽车数据`) and t1.`气缸数`  <  4;	car_1
select max(`百公里油耗（英里/加仑）`) from `汽车数据` where `气缸数`  =  8 or `生产年份`  <  1980	car_1
select max(`百公里油耗（英里/加仑）`) from `汽车数据` where `气缸数`  =  8 or `生产年份`  <  1980	car_1
SELECT DISTINCT T1.`车型名称` FROM `车型列表` AS T1 JOIN `汽车名称` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车数据` AS T3 ON T2.`品牌编号`  =  T3.`汽车编号` JOIN `汽车制造商` AS T4 ON T1.`制造商简称`  =  T4.`制造商编号` WHERE T3.`车重（磅）`  <  3500 AND T4.`制造商全称` != 'Ford Motor Company';	car_1
SELECT DISTINCT T1.`车型名称` FROM `车型列表` AS T1 JOIN `汽车名称` AS T2 ON T1.`车型名称`  =  T2.`车型名称` JOIN `汽车数据` AS T3 ON T2.`品牌编号`  =  T3.`汽车编号` JOIN `汽车制造商` AS T4 ON T1.`制造商简称`  =  T4.`制造商编号` WHERE T3.`车重（磅）`  <  3500 AND T4.`制造商全称` != 'Ford Motor Company';	car_1
SELECT `国家名称` FROM `国家` EXCEPT SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家`;	car_1
SELECT `国家名称` FROM `国家` EXCEPT SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家`;	car_1
select t1.`制造商编号` ,  t1.`制造商简称` from `汽车制造商` as t1 join `车型列表` as t2 on t1.`制造商编号`  =  t2.`制造商简称` group by t1.`制造商编号` having count(*)  >=  2 intersect select t1.`制造商编号` ,  t1.`制造商简称` from `汽车制造商` as t1 join `车型列表` as t2 on t1.`制造商编号`  =  t2.`制造商简称` join `汽车名称` as t3 on t2.`车型名称`  =  t3.`车型名称` group by t1.`制造商编号` having count(*)  >  3;	car_1
SELECT T1.`制造商编号` ,  T1.`制造商简称` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` GROUP BY T1.`制造商编号` HAVING count(*)  >=  2 INTERSECT SELECT T1.`制造商编号` ,  T1.`制造商简称` FROM `汽车制造商` AS T1 JOIN `车型列表` AS T2 ON T1.`制造商编号`  =  T2.`制造商简称` JOIN `汽车名称` AS T3 ON T2.`车型名称`  =  T3.`车型名称` GROUP BY T1.`制造商编号` HAVING count(*)  >  3;	car_1
SELECT T1.`国家编号` ,  T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` GROUP BY T1.`国家编号` HAVING count(*)  >  3 UNION SELECT T1.`国家编号` ,  T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` JOIN `车型列表` AS T3 ON T2.`制造商编号`  =  T3.`制造商简称` WHERE T3.`车型名称`  =  '菲亚特';	car_1
select t1.`国家编号` ,  t1.`国家名称` from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` group by t1.`国家编号` having count(*)  >  3 union select t1.`国家编号` ,  t1.`国家名称` from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` join `车型列表` as t3 on t2.`制造商编号`  =  t3.`制造商简称` where t3.`车型名称`  =  '菲亚特';	car_1
SELECT `所属国家` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `所属国家` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `缩写` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `缩写` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `航空公司名称` ,  `缩写` FROM `航空公司` WHERE `所属国家`  =  "USA"	flight_2
SELECT `航空公司名称` ,  `缩写` FROM `航空公司` WHERE `所属国家`  =  "USA"	flight_2
SELECT `机场代码` ,  `机场名称` FROM `机场` WHERE `所在城市`  =  "Anthony"	flight_2
SELECT `机场代码` ,  `机场名称` FROM `机场` WHERE `所在城市`  =  "Anthony"	flight_2
SELECT count(*) FROM `航空公司`	flight_2
SELECT count(*) FROM `航空公司`	flight_2
SELECT count(*) FROM `机场`	flight_2
SELECT count(*) FROM `机场`	flight_2
SELECT count(*) FROM `航班`	flight_2
SELECT count(*) FROM `航班`	flight_2
SELECT `航空公司名称` FROM `航空公司` WHERE `缩写`  =  "UAL（联合航空控股公司）"	flight_2
SELECT `航空公司名称` FROM `航空公司` WHERE `缩写`  =  "UAL（联合航空控股公司）"	flight_2
SELECT count(*) FROM `航空公司` WHERE `所属国家`  =  "USA"	flight_2
SELECT count(*) FROM `航空公司` WHERE `所属国家`  =  "USA"	flight_2
SELECT `所在城市` ,  `所属国家` FROM `机场` WHERE `机场名称`  =  "Alton"	flight_2
SELECT `所在城市` ,  `所属国家` FROM `机场` WHERE `机场名称`  =  "Alton"	flight_2
SELECT `机场名称` FROM `机场` WHERE `机场代码`  =  "AKO"	flight_2
SELECT `机场名称` FROM `机场` WHERE `机场代码`  =  "AKO"	flight_2
SELECT `机场名称` FROM `机场` WHERE `所在城市` = "Aberdeen"	flight_2
SELECT `机场名称` FROM `机场` WHERE `所在城市` = "Aberdeen"	flight_2
SELECT count(*) FROM `航班` WHERE `出发机场`  =  "APG"	flight_2
SELECT count(*) FROM `航班` WHERE `出发机场`  =  "APG"	flight_2
SELECT count(*) FROM `航班` WHERE `到达机场`  =  "ATO"	flight_2
SELECT count(*) FROM `航班` WHERE `到达机场`  =  "ATO"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`出发机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`出发机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` JOIN `机场` AS T3 ON T1.`出发机场`  =  T3.`机场代码` WHERE T2.`所在城市`  =  "Ashley" AND T3.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` JOIN `机场` AS T3 ON T1.`出发机场`  =  T3.`机场代码` WHERE T2.`所在城市`  =  "Ashley" AND T3.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T1.`航空公司名称`  =  T2.`唯一标识符` WHERE T2.`航空公司名称` = "捷蓝航空"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T1.`航空公司名称`  =  T2.`唯一标识符` WHERE T2.`航空公司名称` = "捷蓝航空"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`到达机场`  =  "ASY"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`到达机场`  =  "ASY"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`出发机场`  =  "AHD"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`出发机场`  =  "AHD"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` JOIN `航空公司` AS T3 ON T3.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`所在城市`  =  "Aberdeen" AND T3.`航空公司名称`  =  "联合航空"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` JOIN `航空公司` AS T3 ON T3.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`所在城市`  =  "Aberdeen" AND T3.`航空公司名称`  =  "联合航空"	flight_2
SELECT T1.`所在城市` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` GROUP BY T1.`所在城市` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`所在城市` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` GROUP BY T1.`所在城市` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`所在城市` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`所在城市` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`所在城市` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`所在城市` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`机场代码` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` OR T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`机场代码` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`机场代码` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` OR T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`机场代码` ORDER BY count(*) DESC LIMIT 1	flight_2
SELECT T1.`机场代码` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` OR T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`机场代码` ORDER BY count(*) LIMIT 1	flight_2
SELECT T1.`机场代码` FROM `机场` AS T1 JOIN `航班` AS T2 ON T1.`机场代码`  =  T2.`到达机场` OR T1.`机场代码`  =  T2.`出发机场` GROUP BY T1.`机场代码` ORDER BY count(*) LIMIT 1	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` ORDER BY count(*) DESC, MIN(T1.`唯一标识符`) ASC LIMIT 1	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` ORDER BY count(*) DESC, MIN(T1.`唯一标识符`) ASC LIMIT 1	flight_2
SELECT T1.`缩写` ,  T1.`所属国家` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` ORDER BY count(*) ASC, MIN(T1.`唯一标识符`) ASC LIMIT 1	flight_2
SELECT T1.`缩写` ,  T1.`所属国家` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` ORDER BY count(*) ASC, MIN(T1.`唯一标识符`) ASC LIMIT 1	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "AHD"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "AHD"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`到达机场`  =  "AHD"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`到达机场`  =  "AHD"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "APG" INTERSECT SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "CVO"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "APG" INTERSECT SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "CVO"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "CVO" EXCEPT SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "APG"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "CVO" EXCEPT SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` WHERE T2.`出发机场`  =  "APG"	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` HAVING count(*)  >  10	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` HAVING count(*)  >  10	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` HAVING count(*)  <  200	flight_2
SELECT T1.`航空公司名称` FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T1.`唯一标识符`  =  T2.`航空公司名称` GROUP BY T1.`航空公司名称` HAVING count(*)  <  200	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T2.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`航空公司名称`  =  "联合航空"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T2.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`航空公司名称`  =  "联合航空"	flight_2
SELECT `航班号` FROM `航班` WHERE `出发机场`  =  "APG"	flight_2
SELECT `航班号` FROM `航班` WHERE `出发机场`  =  "APG"	flight_2
SELECT `航班号` FROM `航班` WHERE `到达机场`  =  "APG"	flight_2
SELECT `航班号` FROM `航班` WHERE `到达机场`  =  "APG"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`出发机场`   =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`出发机场`   =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`   =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`   =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen" OR T2.`所在城市`  =  "Abilene"	flight_2
SELECT count(*) FROM `航班` AS T1 JOIN `机场` AS T2 ON T1.`到达机场`  =  T2.`机场代码` WHERE T2.`所在城市`  =  "Aberdeen" OR T2.`所在城市`  =  "Abilene"	flight_2
SELECT `机场名称` FROM `机场` WHERE `机场代码` NOT IN (SELECT `出发机场` FROM `航班` UNION SELECT `到达机场` FROM `航班`)	flight_2
SELECT `机场名称` FROM `机场` WHERE `机场代码` NOT IN (SELECT `出发机场` FROM `航班` UNION SELECT `到达机场` FROM `航班`)	flight_2
SELECT count(*) FROM `员工`	employee_hire_evaluation
SELECT count(*) FROM `员工`	employee_hire_evaluation
SELECT `姓名` FROM `员工` ORDER BY `年龄`	employee_hire_evaluation
SELECT `姓名` FROM `员工` ORDER BY `年龄`	employee_hire_evaluation
SELECT count(*) ,  `所在城市` FROM `员工` GROUP BY `所在城市`	employee_hire_evaluation
SELECT count(*) ,  `所在城市` FROM `员工` GROUP BY `所在城市`	employee_hire_evaluation
SELECT `所在城市` FROM `员工` WHERE `年龄`  <  30 GROUP BY `所在城市` HAVING count(*)  >  1	employee_hire_evaluation
SELECT `所在城市` FROM `员工` WHERE `年龄`  <  30 GROUP BY `所在城市` HAVING count(*)  >  1	employee_hire_evaluation
SELECT count(*) ,  `地址` FROM `门店` GROUP BY `地址`	employee_hire_evaluation
SELECT count(*) ,  `地址` FROM `门店` GROUP BY `地址`	employee_hire_evaluation
SELECT `经理姓名` ,  `行政区` FROM `门店` ORDER BY `商品数量` DESC LIMIT 1	employee_hire_evaluation
SELECT `经理姓名` ,  `行政区` FROM `门店` ORDER BY `商品数量` DESC LIMIT 1	employee_hire_evaluation
SELECT min(`商品数量`) ,  max(`商品数量`) FROM `门店`	employee_hire_evaluation
SELECT min(`商品数量`) ,  max(`商品数量`) FROM `门店`	employee_hire_evaluation
SELECT `门店名称` ,  `地址` ,  `行政区` FROM `门店` ORDER BY `商品数量` DESC	employee_hire_evaluation
SELECT `门店名称` ,  `地址` ,  `行政区` FROM `门店` ORDER BY `商品数量` DESC	employee_hire_evaluation
SELECT `门店名称` FROM `门店` WHERE `商品数量`  >  (SELECT avg(`商品数量`) FROM `门店`)	employee_hire_evaluation
SELECT `门店名称` FROM `门店` WHERE `商品数量`  >  (SELECT avg(`商品数量`) FROM `门店`)	employee_hire_evaluation
SELECT t1.`姓名` FROM `员工` AS t1 JOIN `绩效评估` AS t2 ON t1.`员工编号`  =  t2.`员工编号` GROUP BY t2.`员工编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t1.`姓名` FROM `员工` AS t1 JOIN `绩效评估` AS t2 ON t1.`员工编号`  =  t2.`员工编号` GROUP BY t2.`员工编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t1.`姓名` FROM `员工` AS t1 JOIN `绩效评估` AS t2 ON t1.`员工编号`  =  t2.`员工编号` ORDER BY t2.`奖金` DESC LIMIT 1	employee_hire_evaluation
SELECT t1.`姓名` FROM `员工` AS t1 JOIN `绩效评估` AS t2 ON t1.`员工编号`  =  t2.`员工编号` ORDER BY t2.`奖金` DESC LIMIT 1	employee_hire_evaluation
SELECT `姓名` FROM `员工` WHERE `员工编号` NOT IN (SELECT `员工编号` FROM `绩效评估`)	employee_hire_evaluation
SELECT `姓名` FROM `员工` WHERE `员工编号` NOT IN (SELECT `员工编号` FROM `绩效评估`)	employee_hire_evaluation
SELECT t2.`门店名称` FROM `聘用记录` AS t1 JOIN `门店` AS t2 ON t1.`门店编号`  =  t2.`门店编号` GROUP BY t1.`门店编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t2.`门店名称` FROM `聘用记录` AS t1 JOIN `门店` AS t2 ON t1.`门店编号`  =  t2.`门店编号` GROUP BY t1.`门店编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT `门店名称` FROM `门店` WHERE `门店编号` NOT IN (SELECT `门店编号` FROM `聘用记录`)	employee_hire_evaluation
SELECT `门店名称` FROM `门店` WHERE `门店编号` NOT IN (SELECT `门店编号` FROM `聘用记录`)	employee_hire_evaluation
SELECT count(*) ,  t2.`门店名称` FROM `聘用记录` AS t1 JOIN `门店` AS t2 ON t1.`门店编号`  =  t2.`门店编号` GROUP BY t2.`门店名称`	employee_hire_evaluation
SELECT count(*) ,  t2.`门店名称` FROM `聘用记录` AS t1 JOIN `门店` AS t2 ON t1.`门店编号`  =  t2.`门店编号` GROUP BY t2.`门店名称`	employee_hire_evaluation
SELECT sum(`奖金`) FROM `绩效评估`	employee_hire_evaluation
SELECT sum(`奖金`) FROM `绩效评估`	employee_hire_evaluation
SELECT * FROM `聘用记录`	employee_hire_evaluation
SELECT * FROM `聘用记录`	employee_hire_evaluation
SELECT `行政区` FROM `门店` WHERE `商品数量`  <  3000 INTERSECT SELECT `行政区` FROM `门店` WHERE `商品数量`  >  10000	employee_hire_evaluation
SELECT `行政区` FROM `门店` WHERE `商品数量`  <  3000 INTERSECT SELECT `行政区` FROM `门店` WHERE `商品数量`  >  10000	employee_hire_evaluation
SELECT count(DISTINCT `地址`) FROM `门店`	employee_hire_evaluation
SELECT count(DISTINCT `地址`) FROM `门店`	employee_hire_evaluation
SELECT count(*) FROM `文档`	cre_Doc_Template_Mgt
SELECT count(*) FROM `文档`	cre_Doc_Template_Mgt
SELECT `文档编号` ,  `文档名称` ,  `文档描述` FROM `文档`	cre_Doc_Template_Mgt
SELECT `文档编号` ,  `文档名称` ,  `文档描述` FROM `文档`	cre_Doc_Template_Mgt
SELECT `文档名称` ,  `模板编号` FROM `文档` WHERE `文档描述` LIKE "%w%"	cre_Doc_Template_Mgt
SELECT `文档名称` ,  `模板编号` FROM `文档` WHERE `文档描述` LIKE "%w%"	cre_Doc_Template_Mgt
SELECT `文档编号` ,  `模板编号` ,  `文档描述` FROM `文档` WHERE `文档名称`  =  "Robbin CV"	cre_Doc_Template_Mgt
SELECT `文档编号` ,  `模板编号` ,  `文档描述` FROM `文档` WHERE `文档名称`  =  "Robbin CV"	cre_Doc_Template_Mgt
SELECT count(DISTINCT `模板编号`) FROM `文档`	cre_Doc_Template_Mgt
SELECT count(DISTINCT `模板编号`) FROM `文档`	cre_Doc_Template_Mgt
SELECT count(*) FROM `文档` AS T1 JOIN `模板` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T2.`模板类型编码`  =  'PPT'	cre_Doc_Template_Mgt
SELECT count(*) FROM `文档` AS T1 JOIN `模板` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T2.`模板类型编码`  =  'PPT'	cre_Doc_Template_Mgt
SELECT `模板编号` ,  count(*) FROM `文档` GROUP BY `模板编号`	cre_Doc_Template_Mgt
SELECT `模板编号` ,  count(*) FROM `文档` GROUP BY `模板编号`	cre_Doc_Template_Mgt
SELECT T1.`模板编号` ,  T2.`模板类型编码` FROM `文档` AS T1 JOIN `模板` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板编号` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT T1.`模板编号` ,  T2.`模板类型编码` FROM `文档` AS T1 JOIN `模板` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板编号` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `文档` GROUP BY `模板编号` HAVING count(*)  >  1	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `文档` GROUP BY `模板编号` HAVING count(*)  >  1	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `模板` EXCEPT SELECT `模板编号` FROM `文档`	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `模板` EXCEPT SELECT `模板编号` FROM `文档`	cre_Doc_Template_Mgt
SELECT count(*) FROM `模板`	cre_Doc_Template_Mgt
SELECT count(*) FROM `模板`	cre_Doc_Template_Mgt
SELECT `模板编号` ,  `版本号` ,  `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT `模板编号` ,  `版本号` ,  `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT DISTINCT `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT DISTINCT `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `模板` WHERE `模板类型编码`  =  "PP" OR `模板类型编码`  =  "PPT"	cre_Doc_Template_Mgt
SELECT `模板编号` FROM `模板` WHERE `模板类型编码`  =  "PP" OR `模板类型编码`  =  "PPT"	cre_Doc_Template_Mgt
SELECT count(*) FROM `模板` WHERE `模板类型编码`  =  "CV"	cre_Doc_Template_Mgt
SELECT count(*) FROM `模板` WHERE `模板类型编码`  =  "CV"	cre_Doc_Template_Mgt
SELECT `版本号` ,  `模板类型编码` FROM `模板` WHERE `版本号`  >  5	cre_Doc_Template_Mgt
SELECT `版本号` ,  `模板类型编码` FROM `模板` WHERE `版本号`  >  5	cre_Doc_Template_Mgt
SELECT `模板类型编码` ,  count(*) FROM `模板` GROUP BY `模板类型编码`	cre_Doc_Template_Mgt
SELECT `模板类型编码` ,  count(*) FROM `模板` GROUP BY `模板类型编码`	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` GROUP BY `模板类型编码` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` GROUP BY `模板类型编码` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` GROUP BY `模板类型编码` HAVING count(*)  <  3	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` GROUP BY `模板类型编码` HAVING count(*)  <  3	cre_Doc_Template_Mgt
SELECT min(`版本号`) ,  `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT min(`版本号`) ,  `模板类型编码` FROM `模板`	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T2.`文档名称`  =  "Data base"	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T2.`文档名称`  =  "Data base"	cre_Doc_Template_Mgt
SELECT T2.`文档名称` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T1.`模板类型编码`  =  "BK"	cre_Doc_Template_Mgt
SELECT T2.`文档名称` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` WHERE T1.`模板类型编码`  =  "BK"	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` ,  count(*) FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板类型编码`	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` ,  count(*) FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板类型编码`	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板类型编码` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT T1.`模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号` GROUP BY T1.`模板类型编码` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` EXCEPT SELECT `模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号`	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板` EXCEPT SELECT `模板类型编码` FROM `模板` AS T1 JOIN `文档` AS T2 ON T1.`模板编号`  =  T2.`模板编号`	cre_Doc_Template_Mgt
SELECT `模板类型编码` ,  `模板类型描述` FROM `模板类型参考表`	cre_Doc_Template_Mgt
SELECT `模板类型编码` ,  `模板类型描述` FROM `模板类型参考表`	cre_Doc_Template_Mgt
SELECT `模板类型描述` FROM `模板类型参考表` WHERE `模板类型编码`  =  "AD"	cre_Doc_Template_Mgt
SELECT `模板类型描述` FROM `模板类型参考表` WHERE `模板类型编码`  =  "AD"	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板类型参考表` WHERE `模板类型描述`  =  "图书"	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板类型参考表` WHERE `模板类型描述`  =  "图书"	cre_Doc_Template_Mgt
SELECT DISTINCT T1.`模板类型描述` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` JOIN `文档` AS T3 ON T2.`模板编号`  =  T3.`模板编号`	cre_Doc_Template_Mgt
SELECT DISTINCT T1.`模板类型描述` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` JOIN `文档` AS T3 ON T2.`模板编号`  =  T3.`模板编号`	cre_Doc_Template_Mgt
SELECT T2.`模板编号` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` WHERE T1.`模板类型描述`  =  "演示文稿"	cre_Doc_Template_Mgt
SELECT T2.`模板编号` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` WHERE T1.`模板类型描述`  =  "演示文稿"	cre_Doc_Template_Mgt
SELECT count(*) FROM `段落`	cre_Doc_Template_Mgt
SELECT count(*) FROM `段落`	cre_Doc_Template_Mgt
SELECT count(*) FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  'Summer Show'	cre_Doc_Template_Mgt
SELECT count(*) FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  'Summer Show'	cre_Doc_Template_Mgt
select `其他详情` from `段落` where `段落文本` like '韩国'	cre_Doc_Template_Mgt
select `其他详情` from `段落` where `段落文本` like '韩国'	cre_Doc_Template_Mgt
SELECT T1.`段落编号` ,   T1.`段落文本` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  'Welcome to NY'	cre_Doc_Template_Mgt
SELECT T1.`段落编号` ,   T1.`段落文本` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  'Welcome to NY'	cre_Doc_Template_Mgt
SELECT T1.`段落文本` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  "Customer reviews"	cre_Doc_Template_Mgt
SELECT T1.`段落文本` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` WHERE T2.`文档名称`  =  "Customer reviews"	cre_Doc_Template_Mgt
SELECT `文档编号` ,  count(*) FROM `段落` GROUP BY `文档编号` ORDER BY `文档编号`	cre_Doc_Template_Mgt
SELECT `文档编号` ,  count(*) FROM `段落` GROUP BY `文档编号` ORDER BY `文档编号`	cre_Doc_Template_Mgt
SELECT T1.`文档编号` ,  T2.`文档名称` ,  count(*) FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` GROUP BY T1.`文档编号`	cre_Doc_Template_Mgt
SELECT T1.`文档编号` ,  T2.`文档名称` ,  count(*) FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` GROUP BY T1.`文档编号`	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` HAVING count(*)  >=  2	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` HAVING count(*)  >=  2	cre_Doc_Template_Mgt
SELECT T1.`文档编号` ,  T2.`文档名称` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` GROUP BY T1.`文档编号` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT T1.`文档编号` ,  T2.`文档名称` FROM `段落` AS T1 JOIN `文档` AS T2 ON T1.`文档编号`  =  T2.`文档编号` GROUP BY T1.`文档编号` ORDER BY count(*) DESC LIMIT 1	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` ORDER BY count(*) ASC LIMIT 1	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` ORDER BY count(*) ASC LIMIT 1	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` HAVING count(*) BETWEEN 1 AND 2	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` GROUP BY `文档编号` HAVING count(*) BETWEEN 1 AND 2	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '巴西' INTERSECT SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '爱尔兰'	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '巴西' INTERSECT SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '爱尔兰'	cre_Doc_Template_Mgt
SELECT count(*) FROM `教师`	course_teach
SELECT count(*) FROM `教师`	course_teach
SELECT `姓名` FROM `教师` ORDER BY `年龄` ASC	course_teach
SELECT `姓名` FROM `教师` ORDER BY `年龄` ASC	course_teach
SELECT `年龄` ,  `籍贯` FROM `教师`	course_teach
SELECT `年龄` ,  `籍贯` FROM `教师`	course_teach
select `姓名` from `教师` where `籍贯` != "little lever urban district"	course_teach
select `姓名` from `教师` where `籍贯` != "little lever urban district"	course_teach
SELECT `姓名` FROM `教师` WHERE `年龄`  =  32 OR `年龄`  =  33	course_teach
SELECT `姓名` FROM `教师` WHERE `年龄`  =  32 OR `年龄`  =  33	course_teach
SELECT `籍贯` FROM `教师` ORDER BY `年龄` ASC LIMIT 1	course_teach
SELECT `籍贯` FROM `教师` ORDER BY `年龄` ASC LIMIT 1	course_teach
SELECT `籍贯` ,  COUNT(*) FROM `教师` GROUP BY `籍贯`	course_teach
SELECT `籍贯` ,  COUNT(*) FROM `教师` GROUP BY `籍贯`	course_teach
SELECT `籍贯` FROM `教师` GROUP BY `籍贯` ORDER BY COUNT(*) DESC, MIN(`教师编号`) ASC LIMIT 1	course_teach
SELECT `籍贯` FROM `教师` GROUP BY `籍贯` ORDER BY COUNT(*) DESC, MIN(`教师编号`) ASC LIMIT 1	course_teach
SELECT `籍贯` FROM `教师` GROUP BY `籍贯` HAVING COUNT(*)  >=  2	course_teach
SELECT `籍贯` FROM `教师` GROUP BY `籍贯` HAVING COUNT(*)  >=  2	course_teach
SELECT T3.`姓名` ,  T2.`课程名称` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号`	course_teach
SELECT T3.`姓名` ,  T2.`课程名称` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号`	course_teach
SELECT T3.`姓名` ,  T2.`课程名称` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` ORDER BY T3.`姓名`	course_teach
SELECT T3.`姓名` ,  T2.`课程名称` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` ORDER BY T3.`姓名`	course_teach
SELECT T3.`姓名` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` WHERE T2.`课程名称`  =  "数学"	course_teach
SELECT T3.`姓名` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` WHERE T2.`课程名称`  =  "数学"	course_teach
SELECT T2.`姓名` ,  COUNT(*) FROM `课程安排` AS T1 JOIN `教师` AS T2 ON T1.`教师编号`  =  T2.`教师编号` GROUP BY T2.`姓名`	course_teach
SELECT T2.`姓名` ,  COUNT(*) FROM `课程安排` AS T1 JOIN `教师` AS T2 ON T1.`教师编号`  =  T2.`教师编号` GROUP BY T2.`姓名`	course_teach
SELECT T2.`姓名` FROM `课程安排` AS T1 JOIN `教师` AS T2 ON T1.`教师编号`  =  T2.`教师编号` GROUP BY T2.`姓名` HAVING COUNT(*)  >=  2	course_teach
SELECT T2.`姓名` FROM `课程安排` AS T1 JOIN `教师` AS T2 ON T1.`教师编号`  =  T2.`教师编号` GROUP BY T2.`姓名` HAVING COUNT(*)  >=  2	course_teach
SELECT `姓名` FROM `教师` WHERE `教师编号` NOT IN (SELECT `教师编号` FROM `课程安排`)	course_teach
SELECT `姓名` FROM `教师` WHERE `教师编号` NOT IN (SELECT `教师编号` FROM `课程安排`)	course_teach
SELECT count(*) FROM `访客` WHERE `年龄`  <  30	museum_visit
SELECT `姓名` FROM `访客` WHERE `会员等级`  >  4 ORDER BY `会员等级` DESC	museum_visit
SELECT avg(`年龄`) FROM `访客` WHERE `会员等级`  <=  4	museum_visit
SELECT `姓名` ,  `会员等级` FROM `访客` WHERE `会员等级`  >  4 ORDER BY `年龄` DESC	museum_visit
SELECT `博物馆编号` ,  `名称` FROM `博物馆` ORDER BY `员工人数` DESC LIMIT 1	museum_visit
SELECT avg(`员工人数`) FROM `博物馆` WHERE `开馆年份`  <  2009	museum_visit
SELECT `员工人数` ,  `开馆年份` FROM `博物馆` WHERE `名称`  =  'Plaza Museum'	museum_visit
SELECT `名称` FROM `博物馆` WHERE `员工人数`  >  (SELECT min(`员工人数`) FROM `博物馆` WHERE `开馆年份`  >  2010)	museum_visit
SELECT t1.`访客编号` ,  t1.`姓名` ,  t1.`年龄` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` GROUP BY t1.`访客编号` HAVING count(*)  >  1	museum_visit
SELECT t2.`访客编号` ,  t1.`姓名` ,  t1.`会员等级` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` GROUP BY t2.`访客编号` ORDER BY sum(t2.`总消费金额`) DESC LIMIT 1	museum_visit
SELECT t2.`博物馆编号` ,  t1.`名称` FROM `博物馆` AS t1 JOIN `参观记录` AS t2 ON t1.`博物馆编号`  =  t2.`博物馆编号` GROUP BY t2.`博物馆编号` ORDER BY count(*) DESC LIMIT 1	museum_visit
SELECT `名称` FROM `博物馆` WHERE `博物馆编号` NOT IN (SELECT `博物馆编号` FROM `参观记录`)	museum_visit
SELECT t1.`姓名` ,  t1.`年龄` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` ORDER BY t2.`购票数量` DESC LIMIT 1	museum_visit
SELECT avg(`购票数量`) ,  max(`购票数量`) FROM `参观记录`	museum_visit
SELECT sum(t2.`总消费金额`) FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` WHERE t1.`会员等级`  =  1	museum_visit
SELECT t1.`姓名` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` JOIN `博物馆` AS t3 ON t3.`博物馆编号`  =  t2.`博物馆编号` WHERE t3.`开馆年份`  <  2009 INTERSECT SELECT t1.`姓名` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` JOIN `博物馆` AS t3 ON t3.`博物馆编号`  =  t2.`博物馆编号` WHERE t3.`开馆年份`  >  2011	museum_visit
SELECT count(*) FROM `访客` WHERE `访客编号` NOT IN (SELECT t2.`访客编号` FROM `博物馆` AS t1 JOIN `参观记录` AS t2 ON t1.`博物馆编号`  =  t2.`博物馆编号` WHERE t1.`开馆年份`  >  2010)	museum_visit
SELECT count(*) FROM `博物馆` WHERE `开馆年份`  >  2013 OR `开馆年份`  <  2008	museum_visit
SELECT count(*) FROM `球员`	wta_1
SELECT count(*) FROM `球员`	wta_1
SELECT count(*) FROM `比赛`	wta_1
SELECT count(*) FROM `比赛`	wta_1
SELECT `名` ,  `出生日期` FROM `球员` WHERE `国家代码`  =  'USA'	wta_1
SELECT `名` ,  `出生日期` FROM `球员` WHERE `国家代码`  =  'USA'	wta_1
SELECT avg(`负方年龄`) ,  avg(`胜方年龄`) FROM `比赛`	wta_1
SELECT avg(`负方年龄`) ,  avg(`胜方年龄`) FROM `比赛`	wta_1
SELECT avg(`胜方排名`) FROM `比赛`	wta_1
SELECT avg(`胜方排名`) FROM `比赛`	wta_1
SELECT min(`负方排名`) FROM `比赛`	wta_1
SELECT min(`负方排名`) FROM `比赛`	wta_1
SELECT count(DISTINCT `国家代码`) FROM `球员`	wta_1
SELECT count(DISTINCT `国家代码`) FROM `球员`	wta_1
SELECT count(DISTINCT `负方姓名`) FROM `比赛`	wta_1
SELECT count(DISTINCT `负方姓名`) FROM `比赛`	wta_1
SELECT `赛事名称` FROM `比赛` GROUP BY `赛事名称` HAVING count(*)  >  10	wta_1
SELECT `赛事名称` FROM `比赛` GROUP BY `赛事名称` HAVING count(*)  >  10	wta_1
SELECT `胜方姓名` FROM `比赛` WHERE `年份`  =  2013 INTERSECT SELECT `胜方姓名` FROM `比赛` WHERE `年份`  =  2016	wta_1
SELECT `胜方姓名` FROM `比赛` WHERE `年份`  =  2013 INTERSECT SELECT `胜方姓名` FROM `比赛` WHERE `年份`  =  2016	wta_1
SELECT count(*) FROM `比赛` WHERE `年份`  =  2013 OR `年份`  =  2016	wta_1
SELECT count(*) FROM `比赛` WHERE `年份`  =  2013 OR `年份`  =  2016	wta_1
SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` WHERE T2.`赛事名称`  =  'WTA Championships' INTERSECT SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` WHERE T2.`赛事名称`  =  'Australian Open'	wta_1
SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` WHERE T2.`赛事名称`  =  'WTA Championships' INTERSECT SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` WHERE T2.`赛事名称`  =  'Australian Open'	wta_1
SELECT `名` ,  `国家代码` FROM `球员` ORDER BY `出生日期` LIMIT 1	wta_1
SELECT `名` ,  `国家代码` FROM `球员` ORDER BY `出生日期` LIMIT 1	wta_1
SELECT `名` ,  `姓` FROM `球员` ORDER BY `出生日期`	wta_1
SELECT `名` ,  `姓` FROM `球员` ORDER BY `出生日期`	wta_1
SELECT `名` ,  `姓` FROM `球员` WHERE `持拍手`  =  'L' ORDER BY `出生日期`	wta_1
SELECT `名` ,  `姓` FROM `球员` WHERE `持拍手`  =  'L' ORDER BY `出生日期`	wta_1
SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` ORDER BY T2.`巡回赛次数` DESC LIMIT 1	wta_1
SELECT T1.`国家代码` ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` ORDER BY T2.`巡回赛次数` DESC LIMIT 1	wta_1
SELECT `年份` FROM `比赛` GROUP BY `年份` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `年份` FROM `比赛` GROUP BY `年份` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `胜方姓名` ,  `胜方排名积分` FROM `比赛` GROUP BY `胜方姓名` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `胜方姓名` ,  `胜方排名积分` FROM `比赛` GROUP BY `胜方姓名` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `胜方姓名` FROM `比赛` WHERE `赛事名称`  =  'Australian Open' ORDER BY `胜方排名积分` DESC LIMIT 1	wta_1
SELECT `胜方姓名` FROM `比赛` WHERE `赛事名称`  =  'Australian Open' ORDER BY `胜方排名积分` DESC LIMIT 1	wta_1
SELECT `胜方姓名` ,  `负方姓名` FROM `比赛` ORDER BY `比赛时长（分钟）` DESC LIMIT 1	wta_1
SELECT `胜方姓名` ,  `负方姓名` FROM `比赛` ORDER BY `比赛时长（分钟）` DESC LIMIT 1	wta_1
SELECT avg(`排名`) ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` GROUP BY T1.`名`	wta_1
SELECT avg(`排名`) ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` GROUP BY T1.`名`	wta_1
SELECT sum(`排名积分`) ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` GROUP BY T1.`名`	wta_1
SELECT sum(`排名积分`) ,  T1.`名` FROM `球员` AS T1 JOIN `排名` AS T2 ON T1.`球员编号`  =  T2.`球员编号` GROUP BY T1.`名`	wta_1
SELECT count(*) ,  `国家代码` FROM `球员` GROUP BY `国家代码`	wta_1
SELECT count(*) ,  `国家代码` FROM `球员` GROUP BY `国家代码`	wta_1
SELECT `国家代码` FROM `球员` GROUP BY `国家代码` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `国家代码` FROM `球员` GROUP BY `国家代码` ORDER BY count(*) DESC LIMIT 1	wta_1
SELECT `国家代码` FROM `球员` GROUP BY `国家代码` HAVING count(*)  >  50	wta_1
SELECT `国家代码` FROM `球员` GROUP BY `国家代码` HAVING count(*)  >  50	wta_1
SELECT sum(`巡回赛次数`) ,  `排名日期` FROM `排名` GROUP BY `排名日期`	wta_1
SELECT sum(`巡回赛次数`) ,  `排名日期` FROM `排名` GROUP BY `排名日期`	wta_1
SELECT count(*) ,  `年份` FROM `比赛` GROUP BY `年份`	wta_1
SELECT count(*) ,  `年份` FROM `比赛` GROUP BY `年份`	wta_1
SELECT DISTINCT `胜方姓名` ,  `胜方排名` FROM `比赛` ORDER BY `胜方年龄` LIMIT 3	wta_1
SELECT DISTINCT `胜方姓名` ,  `胜方排名` FROM `比赛` ORDER BY `胜方年龄` LIMIT 3	wta_1
SELECT count(DISTINCT `胜方姓名`) FROM `比赛` WHERE `赛事名称`  =  'WTA Championships' AND `胜方持拍手`  =  'L'	wta_1
SELECT count(DISTINCT `胜方姓名`) FROM `比赛` WHERE `赛事名称`  =  'WTA Championships' AND `胜方持拍手`  =  'L'	wta_1
SELECT T1.`名` ,  T1.`国家代码` ,  T1.`出生日期` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` ORDER BY T2.`胜方排名积分` DESC LIMIT 1	wta_1
SELECT T1.`名` ,  T1.`国家代码` ,  T1.`出生日期` FROM `球员` AS T1 JOIN `比赛` AS T2 ON T1.`球员编号`  =  T2.`胜方编号` ORDER BY T2.`胜方排名积分` DESC LIMIT 1	wta_1
SELECT count(*) ,  `持拍手` FROM `球员` GROUP BY `持拍手`	wta_1
SELECT count(*) ,  `持拍手` FROM `球员` GROUP BY `持拍手`	wta_1
SELECT count(*) FROM `舰船` WHERE `舰船处置方式`  =  '被俘获'	battle_death
SELECT `名称` ,  `吨位` FROM `舰船` ORDER BY `名称` DESC	battle_death
SELECT `名称` ,  `日期` FROM `战役`	battle_death
SELECT max(`死亡人数`) ,  min(`死亡人数`) FROM `伤亡`	battle_death
SELECT avg(`受伤人数`) FROM `伤亡`	battle_death
SELECT T1.`死亡人数` ,  T1.`受伤人数` FROM `伤亡` AS T1 JOIN `舰船` AS t2 ON T1.`致损舰船编号`  =  T2.`编号` WHERE T2.`吨位`  =  't'	battle_death
SELECT `名称` ,  `结果` FROM `战役` WHERE `保加利亚指挥官` != '博里尔'	battle_death
SELECT DISTINCT T1.`编号` ,  T1.`名称` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`舰船类型`  =  '双桅横帆船'	battle_death
SELECT T1.`编号` ,  T1.`名称` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` JOIN `伤亡` AS T3 ON T2.`编号`  =  T3.`致损舰船编号` GROUP BY T1.`编号` HAVING sum(T3.`死亡人数`)  >  10	battle_death
SELECT T2.`编号` ,  T2.`名称` FROM `伤亡` AS T1 JOIN `舰船` AS t2 ON T1.`致损舰船编号`  =  T2.`编号` GROUP BY T2.`编号` ORDER BY count(*) DESC LIMIT 1	battle_death
SELECT `名称` FROM `战役` WHERE `保加利亚指挥官`  =  '卡洛扬' AND `拉丁指挥官`  =  '鲍德温一世'	battle_death
SELECT count(DISTINCT `结果`) FROM `战役`	battle_death
SELECT count(*) FROM `战役` WHERE `编号` NOT IN ( SELECT `战损状态` FROM `舰船` WHERE `吨位`  =  '225' );	battle_death
SELECT T1.`名称` ,  T1.`日期` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`名称`  =  'Lettice' INTERSECT SELECT T1.`名称` ,  T1.`日期` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`名称`  =  'HMS Atalanta'	battle_death
SELECT `名称` ,  `结果` ,  `保加利亚指挥官` FROM `战役` EXCEPT SELECT T1.`名称` ,  T1.`结果` ,  T1.`保加利亚指挥官` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`位置`  =  '英吉利海峡'	battle_death
SELECT `备注` FROM `伤亡` WHERE `备注` LIKE '%东%'	battle_death
SELECT `地址行1` ,  `地址行2` FROM `地址`	student_transcripts_tracking
SELECT `地址行1` ,  `地址行2` FROM `地址`	student_transcripts_tracking
SELECT count(*) FROM `课程`	student_transcripts_tracking
SELECT count(*) FROM `课程`	student_transcripts_tracking
SELECT `课程描述` FROM `课程` WHERE `课程名称`  =  'math'	student_transcripts_tracking
SELECT `课程描述` FROM `课程` WHERE `课程名称`  =  'math'	student_transcripts_tracking
SELECT `邮政编码` FROM `地址` WHERE `城市`  =  'Port Chelsea'	student_transcripts_tracking
SELECT `邮政编码` FROM `地址` WHERE `城市`  =  'Port Chelsea'	student_transcripts_tracking
SELECT T2.`学院名称` ,  T1.`学院编号` FROM `学位项目` AS T1 JOIN `学院` AS T2 ON T1.`学院编号`  =  T2.`学院编号` GROUP BY T1.`学院编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
select t2.`学院名称` ,  t1.`学院编号` from `学位项目` as t1 join `学院` as t2 on t1.`学院编号`  =  t2.`学院编号` group by t1.`学院编号` order by count(*) desc limit 1	student_transcripts_tracking
SELECT count(DISTINCT `学院编号`) FROM `学位项目`	student_transcripts_tracking
SELECT count(DISTINCT `学院编号`) FROM `学位项目`	student_transcripts_tracking
SELECT count(DISTINCT `学位简称`) FROM `学位项目`	student_transcripts_tracking
SELECT count(DISTINCT `学位简称`) FROM `学位项目`	student_transcripts_tracking
SELECT count(*) FROM `学院` AS T1 JOIN `学位项目` AS T2 ON T1.`学院编号`  =  T2.`学院编号` WHERE T1.`学院名称`  =  'engineer'	student_transcripts_tracking
SELECT count(*) FROM `学院` AS T1 JOIN `学位项目` AS T2 ON T1.`学院编号`  =  T2.`学院编号` WHERE T1.`学院名称`  =  'engineer'	student_transcripts_tracking
SELECT `教学班名称` ,  `教学班描述` FROM `教学班`	student_transcripts_tracking
SELECT `教学班名称` ,  `教学班描述` FROM `教学班`	student_transcripts_tracking
SELECT T1.`课程名称` ,  T1.`课程编号` FROM `课程` AS T1 JOIN `教学班` AS T2 ON T1.`课程编号`  =  T2.`课程编号` GROUP BY T1.`课程编号` HAVING count(*)  <=  2	student_transcripts_tracking
SELECT T1.`课程名称` ,  T1.`课程编号` FROM `课程` AS T1 JOIN `教学班` AS T2 ON T1.`课程编号`  =  T2.`课程编号` GROUP BY T1.`课程编号` HAVING count(*)  <=  2	student_transcripts_tracking
SELECT `教学班名称` FROM `教学班` ORDER BY `教学班名称` DESC	student_transcripts_tracking
SELECT `教学班名称` FROM `教学班` ORDER BY `教学班名称` DESC	student_transcripts_tracking
SELECT T1.`学期名称` ,  T1.`学期编号` FROM `学期` AS T1 JOIN `学生注册` AS T2 ON T1.`学期编号`  =  T2.`学期编号` GROUP BY T1.`学期编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学期名称` ,  T1.`学期编号` FROM `学期` AS T1 JOIN `学生注册` AS T2 ON T1.`学期编号`  =  T2.`学期编号` GROUP BY T1.`学期编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT `学院描述` FROM `学院` WHERE `学院名称` LIKE '%computer%'	student_transcripts_tracking
SELECT `学院描述` FROM `学院` WHERE `学院名称` LIKE '%computer%'	student_transcripts_tracking
SELECT T1.`名` ,  T1.`中间名` ,  T1.`姓` ,  T1.`学生编号` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  =  2	student_transcripts_tracking
SELECT T1.`名` ,  T1.`中间名` ,  T1.`姓` ,  T1.`学生编号` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  =  2	student_transcripts_tracking
SELECT DISTINCT T1.`名` ,  T1.`中间名` ,  T1.`姓` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `学位项目` AS T3 ON T2.`学位项目编号`  =  T3.`学位项目编号` WHERE T3.`学位简称`  =  'Bachelor'	student_transcripts_tracking
SELECT DISTINCT T1.`名` ,  T1.`中间名` ,  T1.`姓` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `学位项目` AS T3 ON T2.`学位项目编号`  =  T3.`学位项目编号` WHERE T3.`学位简称`  =  'Bachelor'	student_transcripts_tracking
SELECT T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位简称` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位简称` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学位项目编号` ,  T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位项目编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学位项目编号` ,  T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位项目编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学生编号` ,  T1.`名` ,  T1.`中间名` ,  T1.`姓` ,  count(*) ,  T1.`学生编号` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学生编号` ,  T1.`名` ,  T1.`中间名` ,  T1.`姓` ,  count(*) ,  T1.`学生编号` FROM `学生` AS T1 JOIN `学生注册` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT `学期名称` FROM `学期` WHERE `学期编号` NOT IN( SELECT `学期编号` FROM `学生注册` )	student_transcripts_tracking
SELECT `学期名称` FROM `学期` WHERE `学期编号` NOT IN( SELECT `学期编号` FROM `学生注册` )	student_transcripts_tracking
SELECT DISTINCT T1.`课程名称` FROM `课程` AS T1 JOIN `学生选课` AS T2 ON T1.`课程编号`  =  T2.`课程编号`	student_transcripts_tracking
SELECT DISTINCT T1.`课程名称` FROM `课程` AS T1 JOIN `学生选课` AS T2 ON T1.`课程编号`  =  T2.`课程编号`	student_transcripts_tracking
SELECT  T1.`课程名称` FROM `课程` AS T1 JOIN `学生选课` AS T2 ON T1.`课程编号`  =  T2.`课程编号` GROUP BY T1.`课程名称` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT  T1.`课程名称` FROM `课程` AS T1 JOIN `学生选课` AS T2 ON T1.`课程编号`  =  T2.`课程编号` GROUP BY T1.`课程名称` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`姓` FROM `学生` AS T1 JOIN `地址` AS T2 ON T1.`当前地址编号`  =  T2.`地址编号` WHERE T2.`州省县`  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.`姓` FROM `学生` AS T3 JOIN `学生注册` AS T4 ON T3.`学生编号`  =  T4.`学生编号`	student_transcripts_tracking
SELECT T1.`姓` FROM `学生` AS T1 JOIN `地址` AS T2 ON T1.`当前地址编号`  =  T2.`地址编号` WHERE T2.`州省县`  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.`姓` FROM `学生` AS T3 JOIN `学生注册` AS T4 ON T3.`学生编号`  =  T4.`学生编号`	student_transcripts_tracking
SELECT T2.`成绩单日期` ,  T1.`成绩单编号` FROM `成绩单明细` AS T1 JOIN `成绩单` AS T2 ON T1.`成绩单编号`  =  T2.`成绩单编号` GROUP BY T1.`成绩单编号` HAVING count(*)  >=  2	student_transcripts_tracking
SELECT T2.`成绩单日期` ,  T1.`成绩单编号` FROM `成绩单明细` AS T1 JOIN `成绩单` AS T2 ON T1.`成绩单编号`  =  T2.`成绩单编号` GROUP BY T1.`成绩单编号` HAVING count(*)  >=  2	student_transcripts_tracking
SELECT `手机号码` FROM `学生` WHERE `名`  =  'Timmothy' AND `姓`  =  'Ward'	student_transcripts_tracking
select `手机号码` from `学生` where `名`  =  'timmothy' and `姓`  =  'ward'	student_transcripts_tracking
SELECT `名` ,  `中间名` ,  `姓` FROM `学生` ORDER BY `首次注册日期` ASC LIMIT 1	student_transcripts_tracking
SELECT `名` ,  `中间名` ,  `姓` FROM `学生` ORDER BY `首次注册日期` ASC LIMIT 1	student_transcripts_tracking
SELECT `名` ,  `中间名` ,  `姓` FROM `学生` ORDER BY `离校日期` ASC LIMIT 1	student_transcripts_tracking
SELECT `名` ,  `中间名` ,  `姓` FROM `学生` ORDER BY `离校日期` ASC LIMIT 1	student_transcripts_tracking
SELECT `名` FROM `学生` WHERE `当前地址编号` != `永久地址编号`	student_transcripts_tracking
SELECT `名` FROM `学生` WHERE `当前地址编号` != `永久地址编号`	student_transcripts_tracking
SELECT T1.`地址编号` ,  T1.`地址行1` ,  T1.`地址行2` FROM `地址` AS T1 JOIN `学生` AS T2 ON T1.`地址编号`  =  T2.`当前地址编号` GROUP BY T1.`地址编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`地址编号` ,  T1.`地址行1` ,  T1.`地址行2` FROM `地址` AS T1 JOIN `学生` AS T2 ON T1.`地址编号`  =  T2.`当前地址编号` GROUP BY T1.`地址编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT avg(`成绩单日期`) FROM `成绩单`	student_transcripts_tracking
SELECT avg(`成绩单日期`) FROM `成绩单`	student_transcripts_tracking
SELECT `成绩单日期` ,  `其他成绩单信息` FROM `成绩单` ORDER BY `成绩单日期` ASC LIMIT 1	student_transcripts_tracking
SELECT `成绩单日期` ,  `其他成绩单信息` FROM `成绩单` ORDER BY `成绩单日期` ASC LIMIT 1	student_transcripts_tracking
SELECT count(*) FROM `成绩单`	student_transcripts_tracking
SELECT count(*) FROM `成绩单`	student_transcripts_tracking
SELECT `成绩单日期` FROM `成绩单` ORDER BY `成绩单日期` DESC LIMIT 1	student_transcripts_tracking
SELECT `成绩单日期` FROM `成绩单` ORDER BY `成绩单日期` DESC LIMIT 1	student_transcripts_tracking
SELECT count(*) ,  `学生选课编号` FROM `成绩单明细` GROUP BY `学生选课编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT count(*) ,  `学生选课编号` FROM `成绩单明细` GROUP BY `学生选课编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T2.`成绩单日期` ,  T1.`成绩单编号` FROM `成绩单明细` AS T1 JOIN `成绩单` AS T2 ON T1.`成绩单编号`  =  T2.`成绩单编号` GROUP BY T1.`成绩单编号` ORDER BY count(*) ASC LIMIT 1	student_transcripts_tracking
SELECT T2.`成绩单日期` ,  T1.`成绩单编号` FROM `成绩单明细` AS T1 JOIN `成绩单` AS T2 ON T1.`成绩单编号`  =  T2.`成绩单编号` GROUP BY T1.`成绩单编号` ORDER BY count(*) ASC LIMIT 1	student_transcripts_tracking
SELECT DISTINCT T2.`学期编号` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` WHERE `学位简称`  =  'Master' INTERSECT SELECT DISTINCT T2.`学期编号` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` WHERE `学位简称`  =  'Bachelor'	student_transcripts_tracking
SELECT DISTINCT T2.`学期编号` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` WHERE `学位简称`  =  'Master' INTERSECT SELECT DISTINCT T2.`学期编号` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` WHERE `学位简称`  =  'Bachelor'	student_transcripts_tracking
SELECT count(DISTINCT `当前地址编号`) FROM `学生`	student_transcripts_tracking
SELECT count(DISTINCT `当前地址编号`) FROM `学生`	student_transcripts_tracking
SELECT `教学班描述` FROM `教学班` WHERE `教学班名称`  =  'h'	student_transcripts_tracking
SELECT `教学班描述` FROM `教学班` WHERE `教学班名称`  =  'h'	student_transcripts_tracking
select t1.`名` from `学生` as t1 join `地址` as t2 on t1.`永久地址编号`  =  t2.`地址编号` where t2.`国家`  =  'haiti' or t1.`手机号码`  =  '09700166582'	student_transcripts_tracking
select t1.`名` from `学生` as t1 join `地址` as t2 on t1.`永久地址编号`  =  t2.`地址编号` where t2.`国家`  =  'haiti' or t1.`手机号码`  =  '09700166582'	student_transcripts_tracking
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯";	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯";	tvshow
SELECT count(*) FROM `动画片` WHERE `编剧` = "约瑟夫·库尔";	tvshow
SELECT count(*) FROM `动画片` WHERE `编剧` = "约瑟夫·库尔";	tvshow
SELECT `标题` ,  `导演` FROM `动画片` ORDER BY `首播日期`	tvshow
SELECT `标题` ,  `导演` FROM `动画片` ORDER BY `首播日期`	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯" OR `导演` = "布兰登·维蒂";	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯" OR `导演` = "布兰登·维蒂";	tvshow
SELECT `国家` ,  count(*) FROM `电视频道` GROUP BY `国家` ORDER BY count(*) DESC LIMIT 1;	tvshow
SELECT `国家` ,  count(*) FROM `电视频道` GROUP BY `国家` ORDER BY count(*) DESC LIMIT 1;	tvshow
SELECT count(DISTINCT `节目名称`) ,  count(DISTINCT `内容类型`) FROM `电视频道`;	tvshow
SELECT count(DISTINCT `节目名称`) ,  count(DISTINCT `内容类型`) FROM `电视频道`;	tvshow
SELECT `内容类型` FROM `电视频道` WHERE `节目名称` = "Sky Radio";	tvshow
SELECT `内容类型` FROM `电视频道` WHERE `节目名称` = "Sky Radio";	tvshow
SELECT `套餐选项` FROM `电视频道` WHERE `节目名称` = "Sky Radio";	tvshow
SELECT `套餐选项` FROM `电视频道` WHERE `节目名称` = "Sky Radio";	tvshow
SELECT count(*) FROM `电视频道` WHERE `语言` = "英语";	tvshow
SELECT count(*) FROM `电视频道` WHERE `语言` = "英语";	tvshow
SELECT `语言` ,  count(*) FROM `电视频道` GROUP BY `语言` ORDER BY count(*) ASC LIMIT 1;	tvshow
SELECT `语言` ,  count(*) FROM `电视频道` GROUP BY `语言` ORDER BY count(*) ASC LIMIT 1;	tvshow
SELECT `语言` ,  count(*) FROM `电视频道` GROUP BY `语言`	tvshow
SELECT `语言` ,  count(*) FROM `电视频道` GROUP BY `语言`	tvshow
SELECT T1.`节目名称` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`标题` = "蓝甲虫的崛起！";	tvshow
SELECT T1.`节目名称` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`标题` = "蓝甲虫的崛起！";	tvshow
SELECT T2.`标题` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T1.`节目名称` = "Sky Radio";	tvshow
SELECT T2.`标题` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T1.`节目名称` = "Sky Radio";	tvshow
SELECT `集数` FROM `电视剧` ORDER BY `收视率`	tvshow
SELECT `集数` FROM `电视剧` ORDER BY `收视率`	tvshow
SELECT `集数` ,  `收视率` FROM `电视剧` ORDER BY `收视率` DESC LIMIT 3;	tvshow
SELECT `集数` ,  `收视率` FROM `电视剧` ORDER BY `收视率` DESC LIMIT 3;	tvshow
SELECT max(`收视份额`) , min(`收视份额`) FROM `电视剧`;	tvshow
SELECT max(`收视份额`) , min(`收视份额`) FROM `电视剧`;	tvshow
SELECT `播出日期` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `播出日期` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `周排名` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `周排名` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT T1.`节目名称` FROM `电视频道` AS T1 JOIN `电视剧` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`集数` = "一生之爱";	tvshow
SELECT T1.`节目名称` FROM `电视频道` AS T1 JOIN `电视剧` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`集数` = "一生之爱";	tvshow
SELECT T2.`集数` FROM `电视频道` AS T1 JOIN `电视剧` AS T2 ON T1.`编号` = T2.`频道` WHERE T1.`节目名称` = "Sky Radio";	tvshow
SELECT T2.`集数` FROM `电视频道` AS T1 JOIN `电视剧` AS T2 ON T1.`编号` = T2.`频道` WHERE T1.`节目名称` = "Sky Radio";	tvshow
SELECT count(*) ,  `导演` FROM `动画片` GROUP BY `导演`	tvshow
SELECT count(*) ,  `导演` FROM `动画片` GROUP BY `导演`	tvshow
select `制作编号` ,  `频道` from `动画片` order by `首播日期` desc limit 1	tvshow
select `制作编号` ,  `频道` from `动画片` order by `首播日期` desc limit 1	tvshow
SELECT `套餐选项` ,  `节目名称` FROM `电视频道` WHERE `高清电视`  =  "是"	tvshow
SELECT `套餐选项` ,  `节目名称` FROM `电视频道` WHERE `高清电视`  =  "是"	tvshow
SELECT T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`编剧`  =  '托德·凯西'	tvshow
SELECT T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`编剧`  =  '托德·凯西'	tvshow
SELECT `国家` FROM `电视频道` EXCEPT SELECT T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`编剧`  =  '托德·凯西'	tvshow
SELECT `国家` FROM `电视频道` EXCEPT SELECT T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`编剧`  =  '托德·凯西'	tvshow
SELECT T1.`节目名称` ,  T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`导演`  =  '迈克尔·张' INTERSECT SELECT T1.`节目名称` ,  T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`导演`  =  '本·琼斯'	tvshow
SELECT T1.`节目名称` ,  T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`导演`  =  '迈克尔·张' INTERSECT SELECT T1.`节目名称` ,  T1.`国家` FROM `电视频道` AS T1 JOIN `动画片` AS T2 ON T1.`编号` = T2.`频道` WHERE T2.`导演`  =  '本·琼斯'	tvshow
SELECT `像素宽高比_PAR` ,  `国家` FROM `电视频道` WHERE `语言` != '英语'	tvshow
SELECT `像素宽高比_PAR` ,  `国家` FROM `电视频道` WHERE `语言` != '英语'	tvshow
SELECT `编号` FROM `电视频道` GROUP BY `国家` HAVING count(*)  >  2	tvshow
SELECT `编号` FROM `电视频道` GROUP BY `国家` HAVING count(*)  >  2	tvshow
SELECT `编号` FROM `电视频道` EXCEPT SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯'	tvshow
SELECT `编号` FROM `电视频道` EXCEPT SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯'	tvshow
SELECT `套餐选项` FROM `电视频道` WHERE `编号` NOT IN (SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯')	tvshow
SELECT `套餐选项` FROM `电视频道` WHERE `编号` NOT IN (SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯')	tvshow
SELECT count(*) FROM `扑克选手`	poker_player
SELECT count(*) FROM `扑克选手`	poker_player
SELECT `累计奖金` FROM `扑克选手` ORDER BY `累计奖金` DESC	poker_player
SELECT `累计奖金` FROM `扑克选手` ORDER BY `累计奖金` DESC	poker_player
SELECT `进入决赛桌次数` ,  `最佳名次` FROM `扑克选手`	poker_player
SELECT `进入决赛桌次数` ,  `最佳名次` FROM `扑克选手`	poker_player
SELECT avg(`累计奖金`) FROM `扑克选手`	poker_player
SELECT avg(`累计奖金`) FROM `扑克选手`	poker_player
SELECT `奖金排名` FROM `扑克选手` ORDER BY `累计奖金` DESC LIMIT 1	poker_player
SELECT `奖金排名` FROM `扑克选手` ORDER BY `累计奖金` DESC LIMIT 1	poker_player
SELECT max(`进入决赛桌次数`) FROM `扑克选手` WHERE `累计奖金`  <  200000	poker_player
SELECT max(`进入决赛桌次数`) FROM `扑克选手` WHERE `累计奖金`  <  200000	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号`	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号`	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` WHERE T2.`累计奖金`  >  300000	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` WHERE T2.`累计奖金`  >  300000	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`进入决赛桌次数`	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`进入决赛桌次数`	poker_player
SELECT T1.`出生日期` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`累计奖金` ASC LIMIT 1	poker_player
SELECT T1.`出生日期` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`累计奖金` ASC LIMIT 1	poker_player
SELECT T2.`奖金排名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T1.`身高` DESC LIMIT 1	poker_player
SELECT T2.`奖金排名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T1.`身高` DESC LIMIT 1	poker_player
SELECT avg(T2.`累计奖金`) FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` WHERE T1.`身高`  >  200	poker_player
SELECT avg(T2.`累计奖金`) FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` WHERE T1.`身高`  >  200	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`累计奖金` DESC	poker_player
SELECT T1.`姓名` FROM `人员` AS T1 JOIN `扑克选手` AS T2 ON T1.`人员编号`  =  T2.`人员编号` ORDER BY T2.`累计奖金` DESC	poker_player
SELECT `国籍` ,  COUNT(*) FROM `人员` GROUP BY `国籍`	poker_player
SELECT `国籍` ,  COUNT(*) FROM `人员` GROUP BY `国籍`	poker_player
SELECT `国籍` FROM `人员` GROUP BY `国籍` ORDER BY COUNT(*) DESC LIMIT 1	poker_player
SELECT `国籍` FROM `人员` GROUP BY `国籍` ORDER BY COUNT(*) DESC LIMIT 1	poker_player
SELECT `国籍` FROM `人员` GROUP BY `国籍` HAVING COUNT(*)  >=  2	poker_player
SELECT `国籍` FROM `人员` GROUP BY `国籍` HAVING COUNT(*)  >=  2	poker_player
SELECT `姓名` ,  `出生日期` FROM `人员` ORDER BY `姓名` ASC	poker_player
SELECT `姓名` ,  `出生日期` FROM `人员` ORDER BY `姓名` ASC	poker_player
SELECT `姓名` FROM `人员` WHERE `国籍` != "俄罗斯"	poker_player
SELECT `姓名` FROM `人员` WHERE `国籍` != "俄罗斯"	poker_player
SELECT `姓名` FROM `人员` WHERE `人员编号` NOT IN (SELECT `人员编号` FROM `扑克选手`)	poker_player
SELECT `姓名` FROM `人员` WHERE `人员编号` NOT IN (SELECT `人员编号` FROM `扑克选手`)	poker_player
SELECT count(DISTINCT `国籍`) FROM `人员`	poker_player
SELECT count(DISTINCT `国籍`) FROM `人员`	poker_player
SELECT count(*) FROM `区号州信息`	voter_1
SELECT `参赛者编号` ,  `参赛者姓名` FROM `参赛者` ORDER BY `参赛者姓名` DESC	voter_1
SELECT `投票编号` ,  `电话号码` ,  `州` FROM `投票记录`	voter_1
SELECT max(`区号`) ,  min(`区号`) FROM `区号州信息`	voter_1
SELECT max(`创建时间`) FROM `投票记录` WHERE `州`  =  'CA'	voter_1
SELECT `参赛者姓名` FROM `参赛者` WHERE `参赛者姓名` != 'Jessie Alloway'	voter_1
SELECT DISTINCT `州` ,  `创建时间` FROM `投票记录`	voter_1
SELECT T1.`参赛者编号` , T1.`参赛者姓名` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` GROUP BY T1.`参赛者编号` HAVING count(*)  >=  2	voter_1
SELECT T1.`参赛者编号` , T1.`参赛者姓名` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` GROUP BY T1.`参赛者编号` ORDER BY count(*) ASC LIMIT 1	voter_1
SELECT count(*) FROM `投票记录` WHERE `州`  =  'NY' OR `州`  =  'CA'	voter_1
SELECT count(*) FROM `参赛者` WHERE `参赛者编号` NOT IN ( SELECT `参赛者编号` FROM `投票记录` )	voter_1
SELECT T1.`区号` FROM `区号州信息` AS T1 JOIN `投票记录` AS T2 ON T1.`州`  =  T2.`州` GROUP BY T1.`区号` ORDER BY count(*) DESC LIMIT 1	voter_1
SELECT T2.`创建时间` ,  T2.`州` ,  T2.`电话号码` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` WHERE T1.`参赛者姓名`  =  'Tabatha Gehling'	voter_1
SELECT T3.`区号` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` JOIN `区号州信息` AS T3 ON T2.`州`  =  T3.`州` WHERE T1.`参赛者姓名`  =  'Tabatha Gehling' INTERSECT SELECT T3.`区号` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` JOIN `区号州信息` AS T3 ON T2.`州`  =  T3.`州` WHERE T1.`参赛者姓名`  =  'Kelly Clauss'	voter_1
select `参赛者姓名` from `参赛者` where `参赛者姓名` like "%al%"	voter_1
SELECT `名称` FROM `国家` WHERE `独立年份`  >  1950	world_1
SELECT `名称` FROM `国家` WHERE `独立年份`  >  1950	world_1
SELECT count(*) FROM `国家` WHERE `政体`  =  "共和国"	world_1
SELECT count(*) FROM `国家` WHERE `政体`  =  "共和国"	world_1
SELECT sum(`国土面积`) FROM `国家` WHERE `区域`  =  "加勒比地区"	world_1
SELECT sum(`国土面积`) FROM `国家` WHERE `区域`  =  "加勒比地区"	world_1
SELECT `洲` FROM `国家` WHERE `名称`  =  "Anguilla"	world_1
SELECT `洲` FROM `国家` WHERE `名称`  =  "Anguilla"	world_1
SELECT `区域` FROM `国家` AS T1 JOIN `城市` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`名称`  =  "Kabul"	world_1
SELECT `区域` FROM `国家` AS T1 JOIN `城市` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`名称`  =  "Kabul"	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Aruba" ORDER BY `使用百分比` DESC LIMIT 1	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Aruba" ORDER BY `使用百分比` DESC LIMIT 1	world_1
SELECT `人口` ,  `预期寿命` FROM `国家` WHERE `名称`  =  "Brazil"	world_1
SELECT `人口` ,  `预期寿命` FROM `国家` WHERE `名称`  =  "Brazil"	world_1
SELECT `人口` ,  `区域` FROM `国家` WHERE `名称`  =  "Angola"	world_1
SELECT `人口` ,  `区域` FROM `国家` WHERE `名称`  =  "Angola"	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `区域`  =  "中非"	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `区域`  =  "中非"	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲" ORDER BY `预期寿命` LIMIT 1	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲" ORDER BY `预期寿命` LIMIT 1	world_1
SELECT sum(`人口`) ,  max(`国民生产总值`) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT sum(`人口`) ,  max(`国民生产总值`) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `洲`  =  "非洲" AND `政体`  =  "共和国"	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `洲`  =  "非洲" AND `政体`  =  "共和国"	world_1
SELECT sum(`国土面积`) FROM `国家` WHERE `洲`  =  "亚洲" OR `洲`  =  "欧洲"	world_1
SELECT sum(`国土面积`) FROM `国家` WHERE `洲`  =  "亚洲" OR `洲`  =  "欧洲"	world_1
SELECT sum(`人口`) FROM `城市` WHERE `行政区`  =  "Gelderland"	world_1
SELECT sum(`人口`) FROM `城市` WHERE `行政区`  =  "Gelderland"	world_1
SELECT avg(`国民生产总值`) ,  sum(`人口`) FROM `国家` WHERE `政体`  =  "美国领土"	world_1
SELECT avg(`国民生产总值`) ,  sum(`人口`) FROM `国家` WHERE `政体`  =  "美国领土"	world_1
SELECT count(DISTINCT `语言`) FROM `国家语言`	world_1
SELECT count(DISTINCT `语言`) FROM `国家语言`	world_1
SELECT count(DISTINCT `政体`) FROM `国家` WHERE `洲`  =  "非洲"	world_1
SELECT count(DISTINCT `政体`) FROM `国家` WHERE `洲`  =  "非洲"	world_1
SELECT COUNT(T2.`语言`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Aruba"	world_1
SELECT COUNT(T2.`语言`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Aruba"	world_1
SELECT COUNT(*) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Afghanistan" AND `是否官方语言`  =  "T"	world_1
SELECT COUNT(*) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`名称`  =  "Afghanistan" AND `是否官方语言`  =  "T"	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`名称` ORDER BY COUNT(*) DESC LIMIT 1	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`名称` ORDER BY COUNT(*) DESC LIMIT 1	world_1
SELECT T1.`洲` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`洲` ORDER BY COUNT(*) DESC LIMIT 1	world_1
SELECT T1.`洲` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`洲` ORDER BY COUNT(*) DESC LIMIT 1	world_1
SELECT COUNT(*) FROM (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "Dutch")	world_1
SELECT COUNT(*) FROM (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "Dutch")	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "French"	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "French"	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" AND T2.`是否官方语言`  =  "T" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "French" AND T2.`是否官方语言`  =  "T"	world_1
SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" AND T2.`是否官方语言`  =  "T" INTERSECT SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "French" AND T2.`是否官方语言`  =  "T"	world_1
SELECT COUNT( DISTINCT `洲`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "Chinese"	world_1
SELECT COUNT( DISTINCT `洲`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "Chinese"	world_1
SELECT DISTINCT T1.`区域` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" OR T2.`语言`  =  "Dutch"	world_1
SELECT DISTINCT T1.`区域` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" OR T2.`语言`  =  "Dutch"	world_1
select t1.`名称` from `国家` as t1 join `国家语言` as t2 on t1.`代码`  =  t2.`国家代码` where t2.`语言`  =  "english" and `是否官方语言`  =  "t" union select t1.`名称` from `国家` as t1 join `国家语言` as t2 on t1.`代码`  =  t2.`国家代码` where t2.`语言`  =  "dutch" and `是否官方语言`  =  "t"	world_1
SELECT * FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" AND `是否官方语言`  =  "T" UNION SELECT * FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "Dutch" AND `是否官方语言`  =  "T"	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`洲`  =  "亚洲" GROUP BY T2.`语言` ORDER BY COUNT (*) DESC LIMIT 1	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`洲`  =  "亚洲" GROUP BY T2.`语言` ORDER BY COUNT (*) DESC LIMIT 1	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`政体`  =  "共和国" GROUP BY T2.`语言` HAVING COUNT(*)  =  1	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`政体`  =  "共和国" GROUP BY T2.`语言` HAVING COUNT(*)  =  1	world_1
SELECT T1.`名称` ,  T1.`人口` FROM `城市` AS T1 JOIN `国家语言` AS T2 ON T1.`国家代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" ORDER BY T1.`人口` DESC LIMIT 1	world_1
SELECT T1.`名称` ,  T1.`人口` FROM `城市` AS T1 JOIN `国家语言` AS T2 ON T1.`国家代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" ORDER BY T1.`人口` DESC LIMIT 1	world_1
SELECT `名称` ,  `人口` ,  `预期寿命` FROM `国家` WHERE `洲`  =  "亚洲" ORDER BY `国土面积` DESC LIMIT 1	world_1
SELECT `名称` ,  `人口` ,  `预期寿命` FROM `国家` WHERE `洲`  =  "亚洲" ORDER BY `国土面积` DESC LIMIT 1	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `名称` NOT IN (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" AND T2.`是否官方语言`  =  "T")	world_1
SELECT avg(`预期寿命`) FROM `国家` WHERE `名称` NOT IN (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English" AND T2.`是否官方语言`  =  "T")	world_1
SELECT sum(`人口`) FROM `国家` WHERE `名称` NOT IN (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English")	world_1
SELECT sum(`人口`) FROM `国家` WHERE `名称` NOT IN (SELECT T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T2.`语言`  =  "English")	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`国家元首`  =  "Beatrix" AND T2.`是否官方语言`  =  "T"	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`国家元首`  =  "Beatrix" AND T2.`是否官方语言`  =  "T"	world_1
SELECT count(DISTINCT T2.`语言`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE  `独立年份`  <  1930 AND T2.`是否官方语言`  =  "T"	world_1
SELECT count(DISTINCT T2.`语言`) FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE  `独立年份`  <  1930 AND T2.`是否官方语言`  =  "T"	world_1
SELECT `名称` FROM `国家` WHERE `国土面积`  >  (SELECT min(`国土面积`) FROM `国家` WHERE `洲`  =  "欧洲")	world_1
SELECT `名称` FROM `国家` WHERE `国土面积`  >  (SELECT min(`国土面积`) FROM `国家` WHERE `洲`  =  "欧洲")	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "非洲"  AND `人口`  <  (SELECT max(`人口`) FROM `国家` WHERE `洲`  =  "亚洲")	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "非洲"  AND `人口`  <  (SELECT min(`人口`) FROM `国家` WHERE `洲`  =  "亚洲")	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲"  AND `人口`  >  (SELECT max(`人口`) FROM `国家` WHERE `洲`  =  "非洲")	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲"  AND `人口`  >  (SELECT min(`人口`) FROM `国家` WHERE `洲`  =  "非洲")	world_1
SELECT `国家代码` FROM `国家语言` EXCEPT SELECT `国家代码` FROM `国家语言` WHERE `语言`  =  "English"	world_1
SELECT `国家代码` FROM `国家语言` EXCEPT SELECT `国家代码` FROM `国家语言` WHERE `语言`  =  "English"	world_1
SELECT DISTINCT `国家代码` FROM `国家语言` WHERE `语言` != "English"	world_1
SELECT DISTINCT `国家代码` FROM `国家语言` WHERE `语言` != "English"	world_1
SELECT `代码` FROM `国家` WHERE `政体` != "共和国" EXCEPT SELECT `国家代码` FROM `国家语言` WHERE `语言`  =  "English"	world_1
SELECT `代码` FROM `国家` WHERE `政体` != "共和国" EXCEPT SELECT `国家代码` FROM `国家语言` WHERE `语言`  =  "English"	world_1
SELECT DISTINCT T2.`名称` FROM `国家` AS T1 JOIN `城市` AS T2 ON T2.`国家代码`  =  T1.`代码` WHERE T1.`洲`  =  '欧洲' AND T1.`名称` NOT IN (SELECT T3.`名称` FROM `国家` AS T3 JOIN `国家语言` AS T4 ON T3.`代码`  =  T4.`国家代码` WHERE T4.`是否官方语言`  =  'T' AND T4.`语言`  =  'English')	world_1
SELECT DISTINCT T2.`名称` FROM `国家` AS T1 JOIN `城市` AS T2 ON T2.`国家代码`  =  T1.`代码` WHERE T1.`洲`  =  '欧洲' AND T1.`名称` NOT IN (SELECT T3.`名称` FROM `国家` AS T3 JOIN `国家语言` AS T4 ON T3.`代码`  =  T4.`国家代码` WHERE T4.`是否官方语言`  =  'T' AND T4.`语言`  =  'English')	world_1
select distinct t3.`名称` from `国家` as t1 join `国家语言` as t2 on t1.`代码`  =  t2.`国家代码` join `城市` as t3 on t1.`代码`  =  t3.`国家代码` where t2.`是否官方语言`  =  't' and t2.`语言`  =  'chinese' and t1.`洲`  =  "asia"	world_1
SELECT DISTINCT T3.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` JOIN `城市` AS T3 ON T1.`代码`  =  T3.`国家代码` WHERE T2.`是否官方语言`  =  'T' AND T2.`语言`  =  'Chinese' AND T1.`洲`  =  "亚洲"	world_1
SELECT `名称` ,  `国土面积` ,  `独立年份` FROM `国家` ORDER BY `人口` LIMIT 1	world_1
SELECT `名称` ,  `国土面积` ,  `独立年份` FROM `国家` ORDER BY `人口` LIMIT 1	world_1
SELECT `名称` ,  `人口` ,  `国家元首` FROM `国家` ORDER BY `国土面积` DESC LIMIT 1	world_1
SELECT `名称` ,  `人口` ,  `国家元首` FROM `国家` ORDER BY `国土面积` DESC LIMIT 1	world_1
SELECT COUNT(T2.`语言`) ,  T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`名称` HAVING COUNT(*)  >  2	world_1
SELECT COUNT(T2.`语言`) ,  T1.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` GROUP BY T1.`名称` HAVING COUNT(*)  >  2	world_1
SELECT count(*) ,  `行政区` FROM `城市` WHERE `人口`  >  (SELECT avg(`人口`) FROM `城市`) GROUP BY `行政区`	world_1
SELECT count(*) ,  `行政区` FROM `城市` WHERE `人口`  >  (SELECT avg(`人口`) FROM `城市`) GROUP BY `行政区`	world_1
SELECT sum(`人口`) ,  `政体` FROM `国家` GROUP BY `政体` HAVING avg(`预期寿命`)  >  72	world_1
SELECT sum(`人口`) ,  `政体` FROM `国家` GROUP BY `政体` HAVING avg(`预期寿命`)  >  72	world_1
SELECT sum(`人口`) ,  avg(`预期寿命`) ,  `洲` FROM `国家` GROUP BY `洲` HAVING avg(`预期寿命`)  <  72	world_1
SELECT sum(`人口`) ,  avg(`预期寿命`) ,  `洲` FROM `国家` GROUP BY `洲` HAVING avg(`预期寿命`)  <  72	world_1
SELECT `名称` ,  `国土面积` FROM `国家` ORDER BY `国土面积` DESC LIMIT 5	world_1
SELECT `名称` ,  `国土面积` FROM `国家` ORDER BY `国土面积` DESC LIMIT 5	world_1
SELECT `名称` FROM `国家` ORDER BY `人口` DESC LIMIT 3	world_1
SELECT `名称` FROM `国家` ORDER BY `人口` DESC LIMIT 3	world_1
SELECT `名称` FROM `国家` ORDER BY `人口` ASC LIMIT 3	world_1
SELECT `名称` FROM `国家` ORDER BY `人口` ASC LIMIT 3	world_1
SELECT count(*) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT count(*) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "欧洲" AND `人口`  =  "80000"	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "欧洲" AND `人口`  =  "80000"	world_1
select sum(`人口`) ,  avg(`国土面积`) from `国家` where `洲`  =  "north america" and `国土面积`  >  3000	world_1
select sum(`人口`) ,  avg(`国土面积`) from `国家` where `洲`  =  "north america" and `国土面积`  >  3000	world_1
SELECT `名称` FROM `城市` WHERE `人口` BETWEEN 160000 AND 900000	world_1
select `名称` from `城市` where `人口` between 160000 and 900000	world_1
SELECT `语言` FROM `国家语言` GROUP BY `语言` ORDER BY count(*) DESC LIMIT 1	world_1
SELECT `语言` FROM `国家语言` GROUP BY `语言` ORDER BY count(*) DESC LIMIT 1	world_1
SELECT `语言` ,  `国家代码` ,  max(`使用百分比`) FROM `国家语言` GROUP BY `国家代码`	world_1
SELECT `语言` ,  `国家代码` ,  max(`使用百分比`) FROM `国家语言` GROUP BY `国家代码`	world_1
SELECT count(*) ,   max(`使用百分比`) FROM `国家语言` WHERE `语言`  =  "Spanish" GROUP BY `国家代码`	world_1
SELECT count(*) ,   max(`使用百分比`) FROM `国家语言` WHERE `语言`  =  "Spanish" GROUP BY `国家代码`	world_1
SELECT `国家代码` ,  max(`使用百分比`) FROM `国家语言` WHERE `语言`  =  "Spanish" GROUP BY `国家代码`	world_1
SELECT `国家代码` ,  max(`使用百分比`) FROM `国家语言` WHERE `语言`  =  "Spanish" GROUP BY `国家代码`	world_1
SELECT count(*) FROM `指挥家`	orchestra
SELECT count(*) FROM `指挥家`	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `年龄` ASC	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `年龄` ASC	orchestra
SELECT `姓名` FROM `指挥家` WHERE `国籍` != '美国'	orchestra
SELECT `姓名` FROM `指挥家` WHERE `国籍` != '美国'	orchestra
SELECT `唱片公司` FROM `乐团` ORDER BY `成立年份` DESC	orchestra
SELECT `唱片公司` FROM `乐团` ORDER BY `成立年份` DESC	orchestra
SELECT avg(`出席人数`) FROM `节目`	orchestra
SELECT avg(`出席人数`) FROM `节目`	orchestra
SELECT max(`收视份额`) ,  min(`收视份额`) FROM `演出` WHERE `类型` != "直播总决赛"	orchestra
SELECT max(`收视份额`) ,  min(`收视份额`) FROM `演出` WHERE `类型` != "直播总决赛"	orchestra
SELECT count(DISTINCT `国籍`) FROM `指挥家`	orchestra
SELECT count(DISTINCT `国籍`) FROM `指挥家`	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `从业年份` DESC	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `从业年份` DESC	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `从业年份` DESC LIMIT 1	orchestra
SELECT `姓名` FROM `指挥家` ORDER BY `从业年份` DESC LIMIT 1	orchestra
SELECT T1.`姓名` ,  T2.`乐团名称` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号`	orchestra
SELECT T1.`姓名` ,  T2.`乐团名称` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号`	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` GROUP BY T2.`指挥家编号` HAVING COUNT(*)  >  1	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` GROUP BY T2.`指挥家编号` HAVING COUNT(*)  >  1	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` GROUP BY T2.`指挥家编号` ORDER BY COUNT(*) DESC LIMIT 1	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` GROUP BY T2.`指挥家编号` ORDER BY COUNT(*) DESC LIMIT 1	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` WHERE `成立年份`  >  2008	orchestra
SELECT T1.`姓名` FROM `指挥家` AS T1 JOIN `乐团` AS T2 ON T1.`指挥家编号`  =  T2.`指挥家编号` WHERE `成立年份`  >  2008	orchestra
SELECT `唱片公司` ,  COUNT(*) FROM `乐团` GROUP BY `唱片公司`	orchestra
SELECT `唱片公司` ,  COUNT(*) FROM `乐团` GROUP BY `唱片公司`	orchestra
SELECT `主要录音格式` FROM `乐团` GROUP BY `主要录音格式` ORDER BY COUNT(*) ASC	orchestra
SELECT `主要录音格式` FROM `乐团` GROUP BY `主要录音格式` ORDER BY COUNT(*) ASC	orchestra
SELECT `唱片公司` FROM `乐团` GROUP BY `唱片公司` ORDER BY COUNT(*) DESC LIMIT 1	orchestra
SELECT `唱片公司` FROM `乐团` GROUP BY `唱片公司` ORDER BY COUNT(*) DESC LIMIT 1	orchestra
SELECT `乐团名称` FROM `乐团` WHERE `乐团编号` NOT IN (SELECT `乐团编号` FROM `演出`)	orchestra
SELECT `乐团名称` FROM `乐团` WHERE `乐团编号` NOT IN (SELECT `乐团编号` FROM `演出`)	orchestra
SELECT `唱片公司` FROM `乐团` WHERE `成立年份`  <  2003 INTERSECT SELECT `唱片公司` FROM `乐团` WHERE `成立年份`  >  2003	orchestra
SELECT `唱片公司` FROM `乐团` WHERE `成立年份`  <  2003 INTERSECT SELECT `唱片公司` FROM `乐团` WHERE `成立年份`  >  2003	orchestra
SELECT COUNT(*) FROM `乐团` WHERE `主要录音格式`  =  "CD" OR `主要录音格式`  =  "DVD"	orchestra
SELECT COUNT(*) FROM `乐团` WHERE `主要录音格式`  =  "CD" OR `主要录音格式`  =  "DVD"	orchestra
SELECT `成立年份` FROM `乐团` AS T1 JOIN `演出` AS T2 ON T1.`乐团编号`  =  T2.`乐团编号` GROUP BY T2.`乐团编号` HAVING COUNT(*)  >  1	orchestra
SELECT `成立年份` FROM `乐团` AS T1 JOIN `演出` AS T2 ON T1.`乐团编号`  =  T2.`乐团编号` GROUP BY T2.`乐团编号` HAVING COUNT(*)  >  1	orchestra
SELECT count(*) FROM `高中生`	network_1
SELECT count(*) FROM `高中生`	network_1
SELECT `姓名` ,  `年级` FROM `高中生`	network_1
SELECT `姓名` ,  `年级` FROM `高中生`	network_1
SELECT `年级` FROM `高中生`	network_1
SELECT `年级` FROM `高中生`	network_1
SELECT `年级` FROM `高中生` WHERE `姓名`  =  "Kyle"	network_1
SELECT `年级` FROM `高中生` WHERE `姓名`  =  "Kyle"	network_1
SELECT `姓名` FROM `高中生` WHERE `年级`  =  10	network_1
SELECT `姓名` FROM `高中生` WHERE `年级`  =  10	network_1
SELECT `学生编号` FROM `高中生` WHERE `姓名`  =  "Kyle"	network_1
SELECT `学生编号` FROM `高中生` WHERE `姓名`  =  "Kyle"	network_1
SELECT count(*) FROM `高中生` WHERE `年级`  =  9 OR `年级`  =  10	network_1
SELECT count(*) FROM `高中生` WHERE `年级`  =  9 OR `年级`  =  10	network_1
SELECT `年级` ,  count(*) FROM `高中生` GROUP BY `年级`	network_1
SELECT `年级` ,  count(*) FROM `高中生` GROUP BY `年级`	network_1
SELECT `年级` FROM `高中生` GROUP BY `年级` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT `年级` FROM `高中生` GROUP BY `年级` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT `年级` FROM `高中生` GROUP BY `年级` HAVING count(*)  >=  4	network_1
SELECT `年级` FROM `高中生` GROUP BY `年级` HAVING count(*)  >=  4	network_1
SELECT `学生编号` ,  count(*) FROM `好友关系` GROUP BY `学生编号`	network_1
SELECT `学生编号` ,  count(*) FROM `好友关系` GROUP BY `学生编号`	network_1
SELECT T2.`姓名` ,  count(*) FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号`	network_1
SELECT T2.`姓名` ,  count(*) FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号`	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >=  3	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >=  3	network_1
SELECT T3.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `高中生` AS T3 ON T1.`好友编号`  =  T3.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT T3.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `高中生` AS T3 ON T1.`好友编号`  =  T3.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT count(*) FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT count(*) FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT `学生编号` FROM `高中生` EXCEPT SELECT `学生编号` FROM `好友关系`	network_1
SELECT `学生编号` FROM `高中生` EXCEPT SELECT `学生编号` FROM `好友关系`	network_1
SELECT `姓名` FROM `高中生` EXCEPT SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`	network_1
SELECT `姓名` FROM `高中生` EXCEPT SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`	network_1
SELECT `学生编号` FROM `好友关系` INTERSECT SELECT `被点赞者编号` FROM `点赞记录`	network_1
SELECT `学生编号` FROM `好友关系` INTERSECT SELECT `被点赞者编号` FROM `点赞记录`	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` INTERSECT SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`被点赞者编号`  =  T2.`学生编号`	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` INTERSECT SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`被点赞者编号`  =  T2.`学生编号`	network_1
SELECT `学生编号` ,  count(*) FROM `点赞记录` GROUP BY `学生编号`	network_1
SELECT `学生编号` ,  count(*) FROM `点赞记录` GROUP BY `学生编号`	network_1
SELECT T2.`姓名` ,  count(*) FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号`	network_1
SELECT T2.`姓名` ,  count(*) FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号`	network_1
SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >=  2	network_1
SELECT T2.`姓名` FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` HAVING count(*)  >=  2	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`年级`  >  5 GROUP BY T1.`学生编号` HAVING count(*)  >=  2	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`年级`  >  5 GROUP BY T1.`学生编号` HAVING count(*)  >=  2	network_1
SELECT count(*) FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT count(*) FROM `点赞记录` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` WHERE T2.`姓名`  =  "Kyle"	network_1
SELECT avg(`年级`) FROM `高中生` WHERE `学生编号` IN (SELECT T1.`学生编号` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`)	network_1
SELECT avg(`年级`) FROM `高中生` WHERE `学生编号` IN (SELECT T1.`学生编号` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`)	network_1
SELECT min(`年级`) FROM `高中生` WHERE `学生编号` NOT IN (SELECT T1.`学生编号` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`)	network_1
SELECT min(`年级`) FROM `高中生` WHERE `学生编号` NOT IN (SELECT T1.`学生编号` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号`)	network_1
SELECT `州` FROM `主人` INTERSECT SELECT `州` FROM `专业人员`	dog_kennels
SELECT `州` FROM `主人` INTERSECT SELECT `州` FROM `专业人员`	dog_kennels
SELECT avg(`年龄`) FROM `犬只` WHERE `犬只编号` IN ( SELECT `犬只编号` FROM `治疗记录` )	dog_kennels
SELECT avg(`年龄`) FROM `犬只` WHERE `犬只编号` IN ( SELECT `犬只编号` FROM `治疗记录` )	dog_kennels
SELECT `专业人员编号` ,  `姓` ,  `手机号码` FROM `专业人员` WHERE `州`  =  'Indiana' UNION SELECT T1.`专业人员编号` ,  T1.`姓` ,  T1.`手机号码` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >  2	dog_kennels
SELECT `专业人员编号` ,  `姓` ,  `手机号码` FROM `专业人员` WHERE `州`  =  'Indiana' UNION SELECT T1.`专业人员编号` ,  T1.`姓` ,  T1.`手机号码` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >  2	dog_kennels
select `犬只名称` from `犬只` where `犬只编号` not in ( select `犬只编号` from `治疗记录` group by `犬只编号` having sum(`治疗费用`)  >  1000 )	dog_kennels
select `犬只名称` from `犬只` where `犬只编号` not in ( select `犬只编号` from `治疗记录` group by `犬只编号` having sum(`治疗费用`)  >  1000 )	dog_kennels
SELECT `名` FROM `专业人员` UNION SELECT `名` FROM `主人` EXCEPT SELECT `犬只名称` FROM `犬只`	dog_kennels
SELECT `名` FROM `专业人员` UNION SELECT `名` FROM `主人` EXCEPT SELECT `犬只名称` FROM `犬只`	dog_kennels
SELECT `专业人员编号` ,  `角色编码` ,  `电子邮箱` FROM `专业人员` EXCEPT SELECT T1.`专业人员编号` ,  T1.`角色编码` ,  T1.`电子邮箱` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号`	dog_kennels
SELECT `专业人员编号` ,  `角色编码` ,  `电子邮箱` FROM `专业人员` EXCEPT SELECT T1.`专业人员编号` ,  T1.`角色编码` ,  T1.`电子邮箱` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号`	dog_kennels
SELECT T1.`主人编号` ,  T2.`名` ,  T2.`姓` FROM `犬只` AS T1 JOIN `主人` AS T2 ON T1.`主人编号`  =  T2.`主人编号` GROUP BY T1.`主人编号` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`主人编号` ,  T2.`名` ,  T2.`姓` FROM `犬只` AS T1 JOIN `主人` AS T2 ON T1.`主人编号`  =  T2.`主人编号` GROUP BY T1.`主人编号` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`专业人员编号` ,  T1.`角色编码` ,  T1.`名` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >=  2	dog_kennels
SELECT T1.`专业人员编号` ,  T1.`角色编码` ,  T1.`名` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >=  2	dog_kennels
SELECT T1.`犬种名称` FROM `犬种` AS T1 JOIN `犬只` AS T2 ON T1.`犬种编码`  =  T2.`犬种编码` GROUP BY T1.`犬种名称` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`犬种名称` FROM `犬种` AS T1 JOIN `犬只` AS T2 ON T1.`犬种编码`  =  T2.`犬种编码` GROUP BY T1.`犬种名称` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`主人编号` ,  T1.`姓` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` JOIN `治疗记录` AS T3 ON T2.`犬只编号`  =  T3.`犬只编号` GROUP BY T1.`主人编号` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`主人编号` ,  T1.`姓` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` JOIN `治疗记录` AS T3 ON T2.`犬只编号`  =  T3.`犬只编号` GROUP BY T1.`主人编号` ORDER BY count(*) DESC LIMIT 1	dog_kennels
SELECT T1.`治疗类型描述` FROM `治疗类型` AS T1 JOIN `治疗记录` AS T2 ON T1.`治疗类型编码`  =  T2.`治疗类型编码` GROUP BY T1.`治疗类型编码` ORDER BY sum(`治疗费用`) ASC LIMIT 1	dog_kennels
SELECT T1.`治疗类型描述` FROM `治疗类型` AS T1 JOIN `治疗记录` AS T2 ON T1.`治疗类型编码`  =  T2.`治疗类型编码` GROUP BY T1.`治疗类型编码` ORDER BY sum(`治疗费用`) ASC LIMIT 1	dog_kennels
SELECT T1.`主人编号` ,  T1.`邮政编码` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` JOIN `治疗记录` AS T3 ON T2.`犬只编号`  =  T3.`犬只编号` GROUP BY T1.`主人编号` ORDER BY sum(T3.`治疗费用`) DESC LIMIT 1	dog_kennels
SELECT T1.`主人编号` ,  T1.`邮政编码` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` JOIN `治疗记录` AS T3 ON T2.`犬只编号`  =  T3.`犬只编号` GROUP BY T1.`主人编号` ORDER BY sum(T3.`治疗费用`) DESC LIMIT 1	dog_kennels
SELECT T1.`专业人员编号` ,  T1.`手机号码` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >=  2	dog_kennels
SELECT T1.`专业人员编号` ,  T1.`手机号码` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >=  2	dog_kennels
SELECT DISTINCT T1.`名` ,  T1.`姓` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 WHERE `治疗费用`  <  ( SELECT avg(`治疗费用`) FROM `治疗记录` )	dog_kennels
SELECT DISTINCT T1.`名` ,  T1.`姓` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 WHERE `治疗费用`  <  ( SELECT avg(`治疗费用`) FROM `治疗记录` )	dog_kennels
SELECT T1.`治疗日期` ,  T2.`名` FROM `治疗记录` AS T1 JOIN `专业人员` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号`	dog_kennels
SELECT T1.`治疗日期` ,  T2.`名` FROM `治疗记录` AS T1 JOIN `专业人员` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号`	dog_kennels
SELECT T1.`治疗费用` ,  T2.`治疗类型描述` FROM `治疗记录` AS T1 JOIN `治疗类型` AS T2 ON T1.`治疗类型编码`  =  T2.`治疗类型编码`	dog_kennels
SELECT T1.`治疗费用` ,  T2.`治疗类型描述` FROM `治疗记录` AS T1 JOIN `治疗类型` AS T2 ON T1.`治疗类型编码`  =  T2.`治疗类型编码`	dog_kennels
SELECT T1.`名` ,  T1.`姓` ,  T2.`体型编码` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号`	dog_kennels
SELECT T1.`名` ,  T1.`姓` ,  T2.`体型编码` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号`	dog_kennels
SELECT T1.`名` ,  T2.`犬只名称` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号`	dog_kennels
SELECT T1.`名` ,  T2.`犬只名称` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号`	dog_kennels
SELECT T1.`犬只名称` ,  T2.`治疗日期` FROM `犬只` AS T1 JOIN `治疗记录` AS T2 ON T1.`犬只编号`  =  T2.`犬只编号` WHERE T1.`犬种编码`  =  ( SELECT `犬种编码` FROM `犬只` GROUP BY `犬种编码` ORDER BY count(*) ASC LIMIT 1 )	dog_kennels
SELECT T1.`犬只名称` ,  T2.`治疗日期` FROM `犬只` AS T1 JOIN `治疗记录` AS T2 ON T1.`犬只编号`  =  T2.`犬只编号` WHERE T1.`犬种编码`  =  ( SELECT `犬种编码` FROM `犬只` GROUP BY `犬种编码` ORDER BY count(*) ASC LIMIT 1 )	dog_kennels
SELECT T1.`名` ,  T2.`犬只名称` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` WHERE T1.`州`  =  'Virginia'	dog_kennels
SELECT T1.`名` ,  T2.`犬只名称` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` WHERE T1.`州`  =  'Virginia'	dog_kennels
SELECT DISTINCT T1.`入所日期` ,  T1.`离所日期` FROM `犬只` AS T1 JOIN `治疗记录` AS T2 ON T1.`犬只编号`  =  T2.`犬只编号`	dog_kennels
SELECT DISTINCT T1.`入所日期` ,  T1.`离所日期` FROM `犬只` AS T1 JOIN `治疗记录` AS T2 ON T1.`犬只编号`  =  T2.`犬只编号`	dog_kennels
SELECT T1.`姓` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` WHERE T2.`年龄`  =  ( SELECT max(`年龄`) FROM `犬只` )	dog_kennels
SELECT T1.`姓` FROM `主人` AS T1 JOIN `犬只` AS T2 ON T1.`主人编号`  =  T2.`主人编号` WHERE T2.`年龄`  =  ( SELECT max(`年龄`) FROM `犬只` )	dog_kennels
SELECT `电子邮箱` FROM `专业人员` WHERE `州`  =  'Hawaii' OR `州`  =  'Wisconsin'	dog_kennels
SELECT `电子邮箱` FROM `专业人员` WHERE `州`  =  'Hawaii' OR `州`  =  'Wisconsin'	dog_kennels
SELECT `入所日期` ,  `离所日期` FROM `犬只`	dog_kennels
SELECT `入所日期` ,  `离所日期` FROM `犬只`	dog_kennels
SELECT count(DISTINCT `犬只编号`) FROM `治疗记录`	dog_kennels
SELECT count(DISTINCT `犬只编号`) FROM `治疗记录`	dog_kennels
SELECT count(DISTINCT `专业人员编号`) FROM `治疗记录`	dog_kennels
SELECT count(DISTINCT `专业人员编号`) FROM `治疗记录`	dog_kennels
SELECT `角色编码` ,  `街道地址` ,  `城市` ,  `州` FROM `专业人员` WHERE `城市` LIKE '%West%'	dog_kennels
SELECT `角色编码` ,  `街道地址` ,  `城市` ,  `州` FROM `专业人员` WHERE `城市` LIKE '%West%'	dog_kennels
SELECT `名` ,  `姓` ,  `电子邮箱` FROM `主人` WHERE `州` LIKE '%North%'	dog_kennels
SELECT `名` ,  `姓` ,  `电子邮箱` FROM `主人` WHERE `州` LIKE '%North%'	dog_kennels
SELECT count(*) FROM `犬只` WHERE `年龄`  <  ( SELECT avg(`年龄`) FROM `犬只` )	dog_kennels
SELECT count(*) FROM `犬只` WHERE `年龄`  <  ( SELECT avg(`年龄`) FROM `犬只` )	dog_kennels
SELECT `治疗费用` FROM `治疗记录` ORDER BY `治疗日期` DESC LIMIT 1	dog_kennels
SELECT `治疗费用` FROM `治疗记录` ORDER BY `治疗日期` DESC LIMIT 1	dog_kennels
SELECT count(*) FROM `犬只` WHERE `犬只编号` NOT IN ( SELECT `犬只编号` FROM `治疗记录` )	dog_kennels
select count(*) from `犬只` where `犬只编号` not in ( select `犬只编号` from `治疗记录` )	dog_kennels
SELECT count(*) FROM `主人` WHERE `主人编号` NOT IN ( SELECT `主人编号` FROM `犬只` )	dog_kennels
SELECT count(*) FROM `主人` WHERE `主人编号` NOT IN ( SELECT `主人编号` FROM `犬只` )	dog_kennels
SELECT count(*) FROM `专业人员` WHERE `专业人员编号` NOT IN ( SELECT `专业人员编号` FROM `治疗记录` )	dog_kennels
SELECT count(*) FROM `专业人员` WHERE `专业人员编号` NOT IN ( SELECT `专业人员编号` FROM `治疗记录` )	dog_kennels
SELECT `犬只名称` ,  `年龄` ,  `体重` FROM `犬只` WHERE `是否弃养`  =  1	dog_kennels
SELECT `犬只名称` ,  `年龄` ,  `体重` FROM `犬只` WHERE `是否弃养`  =  1	dog_kennels
SELECT avg(`年龄`) FROM `犬只`	dog_kennels
SELECT avg(`年龄`) FROM `犬只`	dog_kennels
SELECT max(`年龄`) FROM `犬只`	dog_kennels
SELECT max(`年龄`) FROM `犬只`	dog_kennels
SELECT `收费类型` ,  `收费标准` FROM `收费项目`	dog_kennels
SELECT `收费类型` ,  `收费标准` FROM `收费项目`	dog_kennels
SELECT max(`收费标准`) FROM `收费项目`	dog_kennels
SELECT max(`收费标准`) FROM `收费项目`	dog_kennels
SELECT `电子邮箱` ,  `手机号码` ,  `家庭电话` FROM `专业人员`	dog_kennels
SELECT `电子邮箱` ,  `手机号码` ,  `家庭电话` FROM `专业人员`	dog_kennels
SELECT DISTINCT `犬种编码` ,  `体型编码` FROM `犬只`	dog_kennels
SELECT DISTINCT `犬种编码` ,  `体型编码` FROM `犬只`	dog_kennels
SELECT DISTINCT T1.`名` ,  T3.`治疗类型描述` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` JOIN `治疗类型` AS T3 ON T2.`治疗类型编码`  =  T3.`治疗类型编码`	dog_kennels
SELECT DISTINCT T1.`名` ,  T3.`治疗类型描述` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` JOIN `治疗类型` AS T3 ON T2.`治疗类型编码`  =  T3.`治疗类型编码`	dog_kennels
SELECT count(*) FROM `歌手`	singer
SELECT count(*) FROM `歌手`	singer
SELECT `姓名` FROM `歌手` ORDER BY `净资产（百万美元）` ASC	singer
SELECT `姓名` FROM `歌手` ORDER BY `净资产（百万美元）` ASC	singer
SELECT `出生年份` ,  `国籍` FROM `歌手`	singer
SELECT `出生年份` ,  `国籍` FROM `歌手`	singer
SELECT `姓名` FROM `歌手` WHERE `国籍` != "法国"	singer
SELECT `姓名` FROM `歌手` WHERE `国籍` != "法国"	singer
SELECT `姓名` FROM `歌手` WHERE `出生年份`  =  1948 OR `出生年份`  =  1949	singer
SELECT `姓名` FROM `歌手` WHERE `出生年份`  =  1948 OR `出生年份`  =  1949	singer
SELECT `姓名` FROM `歌手` ORDER BY `净资产（百万美元）` DESC LIMIT 1	singer
SELECT `姓名` FROM `歌手` ORDER BY `净资产（百万美元）` DESC LIMIT 1	singer
SELECT `国籍` ,  COUNT(*) FROM `歌手` GROUP BY `国籍`	singer
SELECT `国籍` ,  COUNT(*) FROM `歌手` GROUP BY `国籍`	singer
SELECT `国籍` FROM `歌手` GROUP BY `国籍` ORDER BY COUNT(*) DESC LIMIT 1	singer
select `国籍` from `歌手` group by `国籍` order by count(*) desc limit 1	singer
SELECT `国籍` ,  max(`净资产（百万美元）`) FROM `歌手` GROUP BY `国籍`	singer
SELECT `国籍` ,  max(`净资产（百万美元）`) FROM `歌手` GROUP BY `国籍`	singer
SELECT T2.`标题` ,  T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号`	singer
SELECT T2.`标题` ,  T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号`	singer
SELECT DISTINCT T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` WHERE T2.`销量`  >  300000	singer
SELECT DISTINCT T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` WHERE T2.`销量`  >  300000	singer
SELECT T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T1.`姓名` HAVING COUNT(*)  >  1	singer
SELECT T1.`姓名` FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T1.`姓名` HAVING COUNT(*)  >  1	singer
SELECT T1.`姓名` ,  sum(T2.`销量`) FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T1.`姓名`	singer
SELECT T1.`姓名` ,  sum(T2.`销量`) FROM `歌手` AS T1 JOIN `歌曲` AS T2 ON T1.`歌手编号`  =  T2.`歌手编号` GROUP BY T1.`姓名`	singer
SELECT `姓名` FROM `歌手` WHERE `歌手编号` NOT IN (SELECT `歌手编号` FROM `歌曲`)	singer
SELECT `姓名` FROM `歌手` WHERE `歌手编号` NOT IN (SELECT `歌手编号` FROM `歌曲`)	singer
SELECT `国籍` FROM `歌手` WHERE `出生年份`  <  1945 INTERSECT SELECT `国籍` FROM `歌手` WHERE `出生年份`  >  1955	singer
SELECT `国籍` FROM `歌手` WHERE `出生年份`  <  1945 INTERSECT SELECT `国籍` FROM `歌手` WHERE `出生年份`  >  1955	singer
SELECT count(*) FROM `其他可用设施`	real_estate_properties
SELECT T2.`设施类型名称` FROM `其他可用设施` AS T1 JOIN `设施类型参考表` AS T2 ON T1.`设施类型编码`  =  T2.`设施类型编码` WHERE T1.`设施名称`  =  "AirCon"	real_estate_properties
SELECT T2.`房产类型描述` FROM `房产` AS T1 JOIN `房产类型参考表` AS T2 ON T1.`房产类型编码`  =  T2.`房产类型编码` GROUP BY T1.`房产类型编码`	real_estate_properties
SELECT `房产名称` FROM `房产` WHERE `房产类型编码`  =  "House" UNION SELECT `房产名称` FROM `房产` WHERE `房产类型编码`  =  "Apartment" AND `房间数量`  >  1	real_estate_properties
