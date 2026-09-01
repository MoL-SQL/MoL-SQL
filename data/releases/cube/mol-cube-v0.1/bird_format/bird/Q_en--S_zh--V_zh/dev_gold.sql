SELECT CAST(SUM(IIF(`货币类型` = '欧元', 1, 0)) AS FLOAT) / SUM(IIF(`货币类型` = '捷克克朗', 1, 0)) AS ratio FROM `客户`	debit_card_specializing
SELECT AVG(T2.`消费量`) / 12 FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE SUBSTR(T2.`日期`, 1, 4) = '2013' AND T1.`客户群组` = '中小企业'	debit_card_specializing
SELECT SUM(IIF(T1.`货币类型` = '捷克克朗', T2.`消费量`, 0)) - SUM(IIF(T1.`货币类型` = '欧元', T2.`消费量`, 0)) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE SUBSTR(T2.`日期`, 1, 4) = '2012'	debit_card_specializing
SELECT CAST(SUM(IIF(T1.`客户群组` = '中小企业', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = 'LAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) , CAST(SUM(IIF(T1.`客户群组` = 'LAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = 'KAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) , CAST(SUM(IIF(T1.`客户群组` = 'KAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = '中小企业', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`货币类型` = '捷克克朗' AND T2.`消费量` = ( SELECT MIN(`消费量`) FROM `年月消费` ) AND T2.`日期` BETWEEN 201301 AND 201312	debit_card_specializing
SELECT CAST((SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0))) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)), CAST(SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) , CAST(SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号`	debit_card_specializing
SELECT SUM(IIF(`国家` = 'CZE', 1, 0)) - SUM(IIF(`国家` = 'SVK', 1, 0)) FROM `加油站` WHERE `业务分区` = '折扣型'	debit_card_specializing
SELECT CAST(SUM(IIF(`消费量` > 528.3, 1, 0)) AS FLOAT) * 100 / COUNT(`客户编号`) FROM `年月消费` WHERE `日期` = '201202'	debit_card_specializing
SELECT CAST(SUM(IIF(T2.`货币类型` = '欧元', 1, 0)) AS FLOAT) * 100 / COUNT(T1.`客户编号`) FROM `交易记录` AS T1 INNER JOIN `客户` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`交易日期` = '2012-08-25'	debit_card_specializing
SELECT CAST(SUM(IIF(`国家` = 'SVK' AND `业务分区` = '高端型', 1, 0)) AS FLOAT) * 100 / SUM(IIF(`国家` = 'SVK', 1, 0)) FROM `加油站`	debit_card_specializing
SELECT T2.`金额` FROM `成员` AS T1 INNER JOIN `收入` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`职位` = '副主席'	student_club
SELECT `备注` FROM `收入` WHERE `来源` = '筹款' AND `收款日期` = '2019-09-14'	student_club
SELECT T1.`活动状态` FROM `预算` AS T1 INNER JOIN `支出` AS T2 ON T1.`预算编号` = T2.`关联预算` WHERE T2.`支出描述` = '明信片、海报' AND T2.`支出日期` = '2019-08-20'	student_club
SELECT COUNT(T1.`成员编号`) FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T2.`专业名称` = 'Business' AND T1.`T恤尺码` = '中号'	student_club
SELECT CAST(SUM(CASE WHEN T2.`活动名称` = 'Yearly Kickoff' THEN T1.`金额` ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.`活动名称` = 'October Meeting' THEN T1.`金额` ELSE 0 END) FROM `预算` AS T1 INNER JOIN `活动` AS T2 ON T1.`关联活动` = T2.`活动编号` WHERE T1.`类别` = '宣传推广' AND T2.`类型` = '会议'	student_club
SELECT SUM(`费用`) FROM `支出` WHERE `支出描述` = '披萨'	student_club
SELECT T1.`名`, T1.`姓` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T2.`院系` = '应用科学、技术与教育学院'	student_club
SELECT SUM(`已支出`) FROM `预算` WHERE `类别` = '餐饮'	student_club
SELECT T2.`名`, T2.`姓`, T1.`费用` FROM `支出` AS T1 INNER JOIN `成员` AS T2 ON T1.`关联成员` = T2.`成员编号` WHERE T1.`支出描述` = '矿泉水、蔬菜拼盘、耗材'	student_club
SELECT SUM(CASE WHEN `入院日期` = '+' THEN 1.0 ELSE 0 END) / SUM(CASE WHEN `入院日期` = '-' THEN 1 ELSE 0 END) FROM `患者` WHERE `诊断` = '系统性红斑狼疮'	thrombosis_prediction
SELECT T1.`检验日期`, STRFTIME('%Y', T2.`初诊日期`) - STRFTIME('%Y', T2.`出生日期`),T2.`出生日期` FROM `检验报告` AS T1 INNER JOIN `患者` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`诊断` = '史蒂文斯-约翰逊综合征' AND T2.`出生日期` IS NOT NULL ORDER BY T2.`出生日期` ASC LIMIT 1	thrombosis_prediction
SELECT `抗心磷脂抗体IgA`, `抗心磷脂抗体IgG`, `抗心磷脂抗体IgM` FROM `检查记录` WHERE `编号` IN ( SELECT `编号` FROM `患者` WHERE `诊断` = '系统性红斑狼疮' AND `描述` = '1994-02-19' ) AND `检查日期` = '1993-11-12'	thrombosis_prediction
SELECT COUNT(`编号`) FROM `患者` WHERE `性别` = 'F' AND `诊断` = '抗磷脂综合征'	thrombosis_prediction
SELECT CAST(SUM(CASE WHEN `性别` = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(`编号`) FROM `患者` WHERE `诊断` = '类风湿关节炎' AND STRFTIME('%Y', `出生日期`) = '1980'	thrombosis_prediction
SELECT T1.`编号`, T1.`性别` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`诊断` = '系统性红斑狼疮' AND T2.`血红蛋白` > 10 AND T2.`血红蛋白` < 17 ORDER BY T1.`出生日期` ASC LIMIT 1	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T3.`编号` = T2.`编号` WHERE T2.`免疫球蛋白G` BETWEEN 900 AND 2000 AND T3.`症状` IS NOT NULL	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `检查记录` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`斯密斯抗体` IN ('阴性','0') AND T1.`血栓形成` = 0	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T3.`编号` = T2.`编号` WHERE (T2.`肝肾微粒体抗体` = '阴性' OR T2.`肝肾微粒体抗体` = '0') AND T1.`性别` = 'F' AND T3.`症状` IS NULL	thrombosis_prediction
SELECT CAST(COUNT(CASE WHEN t2.`惯用脚` = '左脚' THEN t1.`编号` ELSE NULL END) AS REAL) * 100 / COUNT(t1.`编号`) percent FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE SUBSTR(t1.`生日`, 1, 4) BETWEEN '1987' AND '1992'	european_football_2
SELECT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`身高` > 180 GROUP BY t1.`编号` ORDER BY CAST(SUM(t2.`头球精度`) AS REAL) / COUNT(t2.`球员FIFA编号`) DESC LIMIT 10	european_football_2
SELECT COUNT(DISTINCT t1.`球员姓名`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE STRFTIME('%Y',t1.`生日`) < '1986' AND t2.`防守积极性` = '高'	european_football_2
SELECT `球员姓名` FROM (SELECT `球员姓名`, `身高`, DENSE_RANK() OVER (ORDER BY `身高` DESC) as rank FROM `球员`) WHERE rank = 1	european_football_2
SELECT DISTINCT t1.`球队简称` FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t2.`创造机会传球等级` = '低风险'	european_football_2
SELECT SUM(CASE WHEN t1.`编号` = 6 THEN t1.`弹跳` ELSE 0 END) - SUM(CASE WHEN t1.`编号` = 23 THEN t1.`弹跳` ELSE 0 END) FROM `球员属性` AS t1	european_football_2
SELECT COUNT(t1.`编号`) FROM `球员属性` AS t1 WHERE t1.`惯用脚` = '左脚' AND t1.`传中` = ( SELECT MAX(`传中`) FROM `球员属性`)	european_football_2
SELECT CAST(COUNT(CASE WHEN t2.`综合评分` > 70  AND t1.`身高` < 180 THEN t1.`编号` ELSE NULL END) AS REAL) * 100 / COUNT(t1.`编号`) percent FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号`	european_football_2
SELECT T1.`名`, T1.`姓` FROM `车手` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T2.`比赛编号` = 872 AND T2.`用时` IS NOT NULL ORDER BY T1.`出生日期` DESC LIMIT 1	formula_1
SELECT STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', `出生日期`), `名` , `姓` FROM `车手` WHERE `国籍` = '日本籍' ORDER BY `出生日期` DESC LIMIT 1	formula_1
SELECT MAX(T1.`积分`) FROM `车队年度积分榜` AS T1 INNER JOIN `车队` AS T2 on T1.`车队编号` = T2.`车队编号` WHERE T2.`国籍` = '英国籍'	formula_1
SELECT COUNT(T1.`比赛编号`) FROM `车队年度积分榜` AS T1 INNER JOIN `车队` AS T2 on T1.`车队编号` = T2.`车队编号` WHERE T1.`积分` = 0 AND T2.`国籍` = '日本籍' GROUP BY T1.`车队编号` HAVING COUNT(`比赛编号`) = 2	formula_1
SELECT CAST(SUM(IIF(T1.`用时` IS NOT NULL, 1, 0)) AS REAL) * 100 / COUNT(T1.`比赛编号`) FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `车手` AS T3 on T1.`车手编号` = T3.`车手编号` WHERE T3.`国籍` = '日本籍' AND T2.`年份` BETWEEN 2007 AND 2009	formula_1
SELECT COUNT(T1.`车手编号`) FROM `车手` AS T1 INNER JOIN `单圈用时` AS T2 on T1.`车手编号` = T2.`车手编号` WHERE T1.`国籍` = '法国籍' AND (CAST(SUBSTR(T2.`用时`, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(T2.`用时`, 4, 2) AS INTEGER) + CAST(SUBSTR(T2.`用时`, 7, 2) AS REAL) / 1000) < 120	formula_1
SELECT T3.`年份`, T3.`名称`, T3.`日期`, T3.`时间` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 on T1.`比赛编号` = T3.`比赛编号` WHERE T1.`车手编号` = ( SELECT `车手编号` FROM `车手` ORDER BY `出生日期` DESC LIMIT 1 ) ORDER BY T3.`日期` ASC LIMIT 1	formula_1
SELECT T2.`名`, T2.`姓` FROM `进站记录` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` WHERE T2.`国籍` = '德国籍' AND STRFTIME('%Y', T2.`出生日期`) BETWEEN '1980' AND '1985' GROUP BY T2.`名`, T2.`姓` ORDER BY AVG(T1.`进站时长`) LIMIT 3	formula_1
SELECT T1.`名`, T1.`姓`, T1.`国籍`, T3.`名称` FROM `车手` AS T1 INNER JOIN `车手年度积分榜` AS T2 on T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 on T2.`比赛编号` = T3.`比赛编号` ORDER BY JULIANDAY(T1.`出生日期`) DESC LIMIT 1	formula_1
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`发色编号` = T3.`编号` WHERE T2.`颜色` = '蓝色' AND T3.`颜色` = '金发色'	superhero
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` INNER JOIN `性别` AS T4 ON T1.`性别编号` = T4.`编号` WHERE T3.`属性名称` = 'Strength' AND T2.`属性值` = 100 AND T4.`性别` = '女性'	superhero
SELECT AVG(T1.`体重（千克）`) FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号` WHERE T2.`性别` = '女性'	superhero
SELECT DISTINCT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T1.`身高（厘米）` BETWEEN 170 AND 190 AND T2.`颜色` = '无颜色'	superhero
SELECT T1.`瞳色编号`, T1.`发色编号`, T1.`肤色编号` FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T2.`编号` = T1.`出版商编号` INNER JOIN `性别` AS T3 ON T3.`编号` = T1.`性别编号` WHERE T2.`出版商名称` = 'Dark Horse Comics' AND T3.`性别` = '女性'	superhero
SELECT T1.`身高（厘米）` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T2.`颜色` = '琥珀色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `阵营` AS T2 ON T1.`阵营编号` = T2.`编号` WHERE T2.`阵营` = '中立'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`发色编号` = T3.`编号` WHERE T2.`颜色` = '蓝色' AND T3.`颜色` = '棕色'	superhero
SELECT CAST(COUNT(CASE WHEN T2.`性别` = '男性' THEN T1.`编号` ELSE NULL END) AS REAL) / COUNT(CASE WHEN T2.`性别` = '女性' THEN T1.`编号` ELSE NULL END) FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号`	superhero
SELECT CAST(SUM(IIF(T2.`年龄` > 65, 1, 0)) AS REAL) * 100 / COUNT(T1.`编号`) FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T1.`评分` > 5	codebase_community
SELECT T1.`收藏数` FROM `帖子` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`帖子编号` WHERE T2.`创建日期` = '2014-04-23 20:29:39.0' AND T2.`用户编号` = 3025	codebase_community
SELECT COUNT(T1.`编号`) FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`显示名称` = 'Tiago Pasqualini'	codebase_community
SELECT T1.`显示名称` FROM `用户` AS T1 INNER JOIN `投票` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T2.`编号` = 6347	codebase_community
SELECT T2.`用户编号` FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T2.`帖子编号` = T3.`编号` WHERE T3.`浏览次数` >= 1000 GROUP BY T2.`用户编号` HAVING COUNT(DISTINCT T2.`帖子历史类型编号`) = 1	codebase_community
SELECT AVG(T1.`赞成票数`), AVG(T1.`年龄`) FROM `用户` AS T1 INNER JOIN ( SELECT `所有者用户编号`, COUNT(*) AS post_count FROM `帖子` GROUP BY `所有者用户编号` HAVING post_count > 10) AS T2 ON T1.`编号` = T2.`所有者用户编号`	codebase_community
SELECT COUNT(T2.`编号`) FROM `帖子` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`帖子编号` GROUP BY T1.`编号` ORDER BY T1.`评分` DESC LIMIT 1	codebase_community
SELECT CAST(SUM(CASE WHEN T2.`评分` > 50 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.`编号`) FROM `用户` T1 INNER JOIN `帖子` T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`声望值` = (SELECT MAX(`声望值`) FROM `用户`)	codebase_community
SELECT id FROM `卡牌` WHERE `边框颜色` = '无边框' AND (`CardKingdom编号` IS NULL OR `CardKingdom编号` IS NULL)	card_games
SELECT DISTINCT T1.id FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T2.`赛制` = '角斗士赛制' AND T2.`状态` = '禁用' AND T1.`稀有度` = '神话'	card_games
SELECT DISTINCT T2.`状态` FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T1.`类别` = 'Artifact' AND T2.`赛制` = '经典赛制' AND T1.`面` IS NULL	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '简体中文' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '法语' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T1.`是否为故事聚焦卡` = 1	card_games
SELECT CAST(SUM(CASE WHEN `是否为无文字卡` = 0 AND  `是否为故事聚焦卡` = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM `卡牌`	card_games
SELECT T2.`语言` FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T1.`代码` = T2.`系列代码` WHERE T1.`区块` = '拉尼卡' AND T1.`基础系列大小` = 180	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '法语' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T1.`力量` IS NULL OR T1.`力量` = '*'	card_games
SELECT COUNT(DISTINCT T1.`编号`) FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`代码` WHERE T1.`区块` = '冰封时代' AND T2.`语言` = '意大利语' AND T2.`翻译` IS NOT NULL	card_games
SELECT CAST(COUNT(DISTINCT CASE WHEN T1.`元素` = '碳' THEN T1.`原子编号` ELSE NULL END) AS REAL) * 100 / COUNT(DISTINCT T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `化学键` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`键类型` = '='	toxicology
SELECT COUNT(DISTINCT CASE WHEN T1.`元素` = '碘' THEN T1.`原子编号` ELSE NULL END) AS iodine_nums , COUNT(DISTINCT CASE WHEN T1.`元素` = '硫' THEN T1.`原子编号` ELSE NULL END) AS sulfur_nums FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` INNER JOIN `化学键` AS T3 ON T2.`化学键编号` = T3.`化学键编号` WHERE T3.`键类型` = '-'	toxicology
SELECT ROUND(CAST(COUNT(CASE WHEN T.`元素` = '氢' THEN T.`原子编号` ELSE NULL END) AS REAL) * 100 / COUNT(T.`原子编号`),4) FROM `原子` AS T WHERE T.`分子编号` = 'TR206'	toxicology
SELECT T2.`化学键编号` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T2.`化学键编号` IN ( SELECT T3.`化学键编号` FROM `连接关系` AS T3 INNER JOIN `原子` AS T4 ON T3.`原子编号` = T4.`原子编号` WHERE T4.`元素` = '磷' ) AND T1.`元素` = '氮'	toxicology
SELECT CAST(COUNT(T2.`化学键编号`) AS REAL) / COUNT(T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T1.`元素` = '碘'	toxicology
SELECT DISTINCT T.`元素` FROM `原子` AS T WHERE T.`元素` NOT IN ( SELECT DISTINCT T1.`元素` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` )	toxicology
SELECT COUNT(T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `化学键` AS T3 ON T2.`分子编号` = T3.`分子编号` WHERE T3.`键类型` = '#' AND T1.`元素` IN ('磷', '溴')	toxicology
SELECT CAST(COUNT( CASE WHEN T1.`元素` = '氯' THEN T1.`元素` ELSE NULL END) AS REAL) * 100 / COUNT(T1.`元素`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`标签` = '+'	toxicology
WITH SubQuery AS (SELECT DISTINCT T1.`原子编号`, T1.`元素`, T1.`分子编号`, T2.`标签` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`分子编号` = 'TR006') SELECT CAST(COUNT(CASE WHEN `元素` = '氢' THEN `原子编号` ELSE NULL END) AS REAL) / (CASE WHEN COUNT(`原子编号`) = 0 THEN NULL ELSE COUNT(`原子编号`) END) AS ratio, `标签` FROM SubQuery GROUP BY `标签`	toxicology
SELECT T2.`CDS编号` FROM `学校` AS T1 INNER JOIN `免费及减价午餐计划` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`K-12年级注册人数` + T2.`5-17岁学生注册人数` > 500	california_schools
SELECT T1.`学校名称`, T2.`街道`, T2.`城市`, T2.`州`, T2.`邮政编码` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'Monterey' AND T1.`5-17岁学生免费餐食人数` > 800 AND T1.`学校类型` = '高中（公立）'	california_schools
SELECT T2.`学校`, T2.`DOC代码` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`资金类型` = '地方资助' AND (T1.`K-12年级注册人数` - T1.`5-17岁学生注册人数`) > (SELECT AVG(T3.`K-12年级注册人数` - T3.`5-17岁学生注册人数`) FROM `免费及减价午餐计划` AS T3 INNER JOIN `学校` AS T4 ON T3.`CDS编号` = T4.`CDS编号` WHERE T4.`资金类型` = '地方资助')	california_schools
SELECT CAST(T1.`K-12年级免费及减价餐食（FRPM）人数` AS REAL) / T1.`K-12年级注册人数` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`SOC代码` = 66 ORDER BY T1.`K-12年级免费及减价餐食（FRPM）人数` DESC LIMIT 5	california_schools
SELECT T2.`学校`, T1.`写作平均分` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`管理员1名` = 'Ricci' AND T2.`管理员1姓` = 'Ulrich'	california_schools
SELECT CAST(SUM(CASE WHEN `DOC代码` = 54 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN `DOC代码` = 52 THEN 1 ELSE 0 END) FROM `学校` WHERE `状态类型` = '已合并' AND `县` = 'Orange'	california_schools
SELECT T2.`学校`, T1.`5-17岁学生免费及减价餐食（FRPM）人数` * 100 / T1.`5-17岁学生注册人数` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'Los Angeles' AND T2.`服务年级范围` = '幼儿园至9年级'	california_schools
SELECT T2.`城市`, COUNT(T2.`CDS编号`) FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`磁石学校（是/否）` = 1 AND T2.`提供年级范围` = '幼儿园至8年级' AND T1.`国家学校午餐计划（NSLP）供餐资格状态` = '多种供应条款类型' GROUP BY T2.`城市`	california_schools
SELECT COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`性别` = 'M' AND T2.A3 = '北波希米亚' AND T2.A11 > 8000	financial
SELECT T1.`账户编号`  FROM `账户` AS T1 INNER JOIN `授权关系` AS T2 ON T1.`账户编号` = T2.`账户编号` INNER JOIN `客户` AS T3 ON T2.`客户编号` = T3.`客户编号` INNER JOIN `行政区` AS T4 on T4.`行政区编号` = T1.`行政区编号` WHERE T2.`客户编号` = ( SELECT `客户编号` FROM `客户` ORDER BY `出生日期` DESC LIMIT 1) GROUP BY T4.A11, T1.`账户编号`	financial
SELECT COUNT(T2.`客户编号`) FROM `行政区` AS T1 INNER JOIN `客户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.`性别` = 'F' AND STRFTIME('%Y', T2.`出生日期`) < '1950' AND T1.A2 = '索科洛夫'	financial
SELECT T1.`账户编号` FROM `交易` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE STRFTIME('%Y', T1.`交易日期`) = '1998' AND T1.`交易操作` = '银行卡取款' AND T1.`交易金额` < (SELECT AVG(`交易金额`) FROM `交易` WHERE STRFTIME('%Y', `交易日期`) = '1998')	financial
SELECT T4.`交易编号` FROM `客户` AS T1 INNER JOIN `授权关系` AS T2 ON T1.`客户编号` = T2.`客户编号` INNER JOIN `账户` AS T3 ON T2.`账户编号` = T3.`账户编号` INNER JOIN `交易` AS T4 ON T3.`账户编号` = T4.`账户编号` WHERE T1.`客户编号` = 3356 AND T4.`交易操作` = '取款'	financial
SELECT CAST(SUM(T1.`性别` = 'M') AS REAL) * 100 / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T3 ON T1.`行政区编号` = T3.`行政区编号` INNER JOIN `账户` AS T2 ON T2.`行政区编号` = T3.`行政区编号` INNER JOIN `授权关系` as T4 on T1.`客户编号` = T4.`客户编号` AND T2.`账户编号` = T4.`账户编号` WHERE T2.`交易频率` = '每周扣款'	financial
SELECT T1.`客户编号`, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T3.`出生日期`) FROM `授权关系` AS T1 INNER JOIN `银行卡` AS T2 ON T2.`授权编号` = T1.`授权编号` INNER JOIN `客户` AS T3 ON T1.`客户编号` = T3.`客户编号` WHERE T2.`授权类型` = '金卡' AND T1.`授权类型` = '所有人'	financial
SELECT T1.`账户编号`, T2.A2, T2.A3 FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`交易频率` = '按交易额扣款' AND STRFTIME('%Y', T1.`开户日期`)= '1993'	financial
SELECT T1.`账户编号`, T1.`交易频率` FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.A3 = '东波希米亚' AND STRFTIME('%Y', T1.`开户日期`) BETWEEN '1995' AND '2000'	financial
