SELECT CAST(SUM(IIF(`货币类型` = '欧元', 1, 0)) AS FLOAT) / SUM(IIF(`货币类型` = '捷克克朗', 1, 0)) AS ratio FROM `客户`	debit_card_specializing
SELECT T1.`客户编号` FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`客户群组` = 'LAM' AND SUBSTR(T2.`日期`, 1, 4) = '2012' GROUP BY T1.`客户编号` ORDER BY SUM(T2.`消费量`) ASC LIMIT 1	debit_card_specializing
SELECT AVG(T2.`消费量`) / 12 FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE SUBSTR(T2.`日期`, 1, 4) = '2013' AND T1.`客户群组` = '中小企业'	debit_card_specializing
SELECT SUM(IIF(T1.`货币类型` = '捷克克朗', T2.`消费量`, 0)) - SUM(IIF(T1.`货币类型` = '欧元', T2.`消费量`, 0)) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE SUBSTR(T2.`日期`, 1, 4) = '2012'	debit_card_specializing
SELECT SUBSTR(T2.`日期`, 1, 4) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`货币类型` = '捷克克朗' GROUP BY SUBSTR(T2.`日期`, 1, 4) ORDER BY SUM(T2.`消费量`) DESC LIMIT 1	debit_card_specializing
SELECT SUBSTR(T2.`日期`, 5, 2) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE SUBSTR(T2.`日期`, 1, 4) = '2013' AND T1.`客户群组` = '中小企业' GROUP BY SUBSTR(T2.`日期`, 5, 2) ORDER BY SUM(T2.`消费量`) DESC LIMIT 1	debit_card_specializing
SELECT CAST(SUM(IIF(T1.`客户群组` = '中小企业', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = 'LAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) , CAST(SUM(IIF(T1.`客户群组` = 'LAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = 'KAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) , CAST(SUM(IIF(T1.`客户群组` = 'KAM', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) - CAST(SUM(IIF(T1.`客户群组` = '中小企业', T2.`消费量`, 0)) AS REAL) / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`货币类型` = '捷克克朗' AND T2.`消费量` = ( SELECT MIN(`消费量`) FROM `年月消费` ) AND T2.`日期` BETWEEN 201301 AND 201312	debit_card_specializing
SELECT CAST((SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0))) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = '中小企业' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)), CAST(SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = 'LAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) , CAST(SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2013%', T2.`消费量`, 0)) - SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) AS FLOAT) * 100 / SUM(IIF(T1.`客户群组` = 'KAM' AND T2.`日期` LIKE '2012%', T2.`消费量`, 0)) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号`	debit_card_specializing
SELECT SUM(`消费量`) FROM `年月消费` WHERE `客户编号` = 6 AND `日期` BETWEEN '201308' AND '201311'	debit_card_specializing
SELECT SUM(IIF(`国家` = 'CZE', 1, 0)) - SUM(IIF(`国家` = 'SVK', 1, 0)) FROM `加油站` WHERE `业务分区` = '折扣型'	debit_card_specializing
SELECT SUM(`货币类型` = '捷克克朗') - SUM(`货币类型` = '欧元') FROM `客户` WHERE `客户群组` = '中小企业'	debit_card_specializing
SELECT CAST(SUM(IIF(T2.`消费量` > 46.73, 1, 0)) AS FLOAT) * 100 / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`客户群组` = 'LAM'	debit_card_specializing
SELECT CAST(SUM(IIF(`消费量` > 528.3, 1, 0)) AS FLOAT) * 100 / COUNT(`客户编号`) FROM `年月消费` WHERE `日期` = '201202'	debit_card_specializing
SELECT SUM(`消费量`) FROM `年月消费` WHERE SUBSTR(`日期`, 1, 4) = '2012' GROUP BY SUBSTR(`日期`, 5, 2) ORDER BY SUM(`消费量`) DESC LIMIT 1	debit_card_specializing
SELECT T3.`商品描述` FROM `交易记录` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` INNER JOIN `商品` AS T3 ON T1.`商品编号` = T3.`商品编号` WHERE T2.`日期` = '201309'	debit_card_specializing
SELECT DISTINCT T2.`国家` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` INNER JOIN `年月消费` AS T3 ON T1.`客户编号` = T3.`客户编号` WHERE T3.`日期` = '201306'	debit_card_specializing
SELECT COUNT(*) FROM `年月消费` AS T1 INNER JOIN `客户` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T2.`货币类型` = '欧元' AND T1.`消费量` > 1000.00	debit_card_specializing
SELECT DISTINCT T3.`商品描述` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` INNER JOIN `商品` AS T3 ON T1.`商品编号` = T3.`商品编号` WHERE T2.`国家` = 'CZE'	debit_card_specializing
SELECT DISTINCT T1.`交易时间` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` WHERE T2.`连锁集团编号` = 11	debit_card_specializing
SELECT COUNT(T1.`交易编号`) FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` WHERE T2.`国家` = 'CZE' AND STRFTIME('%Y', T1.`交易日期`) >= '2012'	debit_card_specializing
SELECT DISTINCT T3.`货币类型` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` INNER JOIN `客户` AS T3 ON T1.`客户编号` = T3.`客户编号` WHERE T1.`交易日期` = '2012-08-24' AND T1.`交易时间` = '16:25:00'	debit_card_specializing
SELECT T2.`客户群组` FROM `交易记录` AS T1 INNER JOIN `客户` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`交易日期` = '2012-08-23' AND T1.`交易时间` = '21:20:00'	debit_card_specializing
SELECT COUNT(T1.`交易编号`) FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` WHERE T1.`交易日期` = '2012-08-26' AND T1.`交易时间` BETWEEN '08:00:00' AND '09:00:00' AND T2.`国家` = 'CZE'	debit_card_specializing
SELECT T2.`国家` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` WHERE T1.`交易日期` = '2012-08-24' AND T1.`单价`  = 548.4	debit_card_specializing
SELECT CAST(SUM(IIF(T2.`货币类型` = '欧元', 1, 0)) AS FLOAT) * 100 / COUNT(T1.`客户编号`) FROM `交易记录` AS T1 INNER JOIN `客户` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`交易日期` = '2012-08-25'	debit_card_specializing
SELECT CAST(SUM(IIF(SUBSTRING(`日期`, 1, 4) = '2012', `消费量`, 0)) - SUM(IIF(SUBSTRING(`日期`, 1, 4) = '2013', `消费量`, 0)) AS FLOAT) / SUM(IIF(SUBSTRING(`日期`, 1, 4) = '2012', `消费量`, 0)) FROM `年月消费` WHERE `客户编号` = ( SELECT T1.`客户编号` FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` WHERE T1.`交易日期` = '2012-08-25' AND T1.`单价`  = 1513.12 )	debit_card_specializing
SELECT CAST(SUM(IIF(`国家` = 'SVK' AND `业务分区` = '高端型', 1, 0)) AS FLOAT) * 100 / SUM(IIF(`国家` = 'SVK', 1, 0)) FROM `加油站`	debit_card_specializing
SELECT SUM(T1.`单价` ) , SUM(IIF(T3.`日期` = '201201', T1.`单价`, 0)) FROM `交易记录` AS T1 INNER JOIN `加油站` AS T2 ON T1.`加油站编号` = T2.`加油站编号` INNER JOIN `年月消费` AS T3 ON T1.`客户编号` = T3.`客户编号` WHERE T1.`客户编号` = '38508'	debit_card_specializing
SELECT T2.`客户编号`, SUM(T2.`单价` / T2.`交易金额`), T1.`货币类型` FROM `客户` AS T1 INNER JOIN `交易记录` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T2.`客户编号` = ( SELECT `客户编号` FROM `年月消费` ORDER BY `消费量` DESC LIMIT 1 ) GROUP BY T2.`客户编号`, T1.`货币类型`	debit_card_specializing
SELECT T2.`消费量` FROM `交易记录` AS T1 INNER JOIN `年月消费` AS T2 ON T1.`客户编号` = T2.`客户编号` WHERE T1.`单价` / T1.`交易金额` > 29.00 AND T1.`商品编号` = 5 AND T2.`日期` = '201208'	debit_card_specializing
SELECT T2.`专业名称` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T1.`名` = 'Angela' AND T1.`姓` = 'Sanders'	student_club
SELECT COUNT(T1.`活动编号`) FROM `活动` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `成员` AS T3 ON T2.`关联成员` = T3.`成员编号` WHERE T1.`活动名称` = 'Women''s Soccer' AND T3.`T恤尺码` = '中号'	student_club
SELECT COUNT(DISTINCT T1.`活动编号`) FROM `活动` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`活动编号` = T2.`关联活动` WHERE T1.`类型` = '会议' GROUP BY T1.`活动编号` HAVING COUNT(T2.`关联活动`) > 10	student_club
SELECT T1.`活动名称` FROM `活动` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`活动编号` = T2.`关联活动` GROUP BY T1.`活动编号` HAVING COUNT(T2.`关联活动`) > 20 EXCEPT SELECT T1.`活动名称` FROM `活动` AS T1  WHERE T1.`类型` = 'Fundraiser'	student_club
SELECT T2.`金额` FROM `成员` AS T1 INNER JOIN `收入` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`职位` = '副主席'	student_club
SELECT T1.`名`, T1.`姓` FROM `成员` AS T1 INNER JOIN `邮政编码` AS T2 ON T1.`邮政编码` = T2.`邮政编码` WHERE T2.`州` = 'Illinois'	student_club
SELECT T3.`是否批准` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算` WHERE T1.`活动名称` = 'October Meeting' AND T1.`活动日期` LIKE '2019-10-08%'	student_club
SELECT AVG(T2.`费用`) FROM `成员` AS T1 INNER JOIN `支出` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`姓` = 'Allen' AND T1.`名` = 'Elijah' AND (SUBSTR(T2.`支出日期`, 6, 2) = '09' OR SUBSTR(T2.`支出日期`, 6, 2) = '10')	student_club
SELECT SUM(CASE WHEN SUBSTR(T1.`活动日期`, 1, 4) = '2019' THEN T2.`已支出` ELSE 0 END) - SUM(CASE WHEN SUBSTR(T1.`活动日期`, 1, 4) = '2020' THEN T2.`已支出` ELSE 0 END) AS num FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动`	student_club
SELECT `备注` FROM `收入` WHERE `来源` = '筹款' AND `收款日期` = '2019-09-14'	student_club
SELECT `电话` FROM `成员` WHERE `名` = 'Carlo' AND `姓` = 'Jacobs'	student_club
SELECT T1.`活动状态` FROM `预算` AS T1 INNER JOIN `支出` AS T2 ON T1.`预算编号` = T2.`关联预算` WHERE T2.`支出描述` = '明信片、海报' AND T2.`支出日期` = '2019-08-20'	student_club
SELECT T2.`专业名称` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T1.`名` = 'Brent' AND T1.`姓` = 'Thomason'	student_club
SELECT COUNT(T1.`成员编号`) FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T2.`专业名称` = 'Business' AND T1.`T恤尺码` = '中号'	student_club
SELECT T2.`院系` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T1.`职位` = '主席'	student_club
SELECT T2.`收款日期` FROM `成员` AS T1 INNER JOIN `收入` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`名` = 'Connor' AND T1.`姓` = 'Hilton' AND T2.`来源` = '会费'	student_club
SELECT CAST(SUM(CASE WHEN T2.`活动名称` = 'Yearly Kickoff' THEN T1.`金额` ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.`活动名称` = 'October Meeting' THEN T1.`金额` ELSE 0 END) FROM `预算` AS T1 INNER JOIN `活动` AS T2 ON T1.`关联活动` = T2.`活动编号` WHERE T1.`类别` = '宣传推广' AND T2.`类型` = '会议'	student_club
SELECT SUM(`费用`) FROM `支出` WHERE `支出描述` = '披萨'	student_club
SELECT COUNT(`城市`) FROM `邮政编码` WHERE `县` = 'Orange County' AND `州` = 'Virginia'	student_club
SELECT T2.`专业名称` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T1.`电话` = '809-555-3360'	student_club
SELECT COUNT(T2.`关联成员`) FROM `活动` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`活动编号` = T2.`关联活动` WHERE T1.`活动名称` = 'Women''s Soccer'	student_club
SELECT T1.`名`, T1.`姓` FROM `成员` AS T1 INNER JOIN `专业` AS T2 ON T1.`关联专业` = T2.`专业编号` WHERE T2.`院系` = '应用科学、技术与教育学院'	student_club
SELECT T2.`活动名称` FROM `预算` AS T1 INNER JOIN `活动` AS T2 ON T1.`关联活动` = T2.`活动编号` WHERE T2.`状态` = '已关闭' ORDER BY T1.`已支出` / T1.`金额` DESC LIMIT 1	student_club
SELECT MAX(`已支出`) FROM `预算`	student_club
SELECT SUM(`已支出`) FROM `预算` WHERE `类别` = '餐饮'	student_club
SELECT T1.`名`, T1.`姓` FROM `成员` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`成员编号` = T2.`关联成员` GROUP BY T2.`关联成员` HAVING COUNT(T2.`关联活动`) > 7	student_club
SELECT T4.`名`, T4.`姓` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算` INNER JOIN `成员` AS T4 ON T3.`关联成员` = T4.`成员编号` WHERE T1.`活动名称` = 'Yearly Kickoff'	student_club
SELECT T1.`活动名称` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算` ORDER BY T3.`费用` LIMIT 1	student_club
SELECT CAST(SUM(CASE WHEN T1.`活动名称` = 'Yearly Kickoff' THEN T3.`费用` ELSE 0 END) AS REAL) * 100 / SUM(T3.`费用`) FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算`	student_club
SELECT `来源` FROM `收入` WHERE `收款日期` BETWEEN '2019-09-01' and '2019-09-30' ORDER BY `金额` DESC, `收入编号` ASC LIMIT 1	student_club
SELECT COUNT(T2.`成员编号`) FROM `专业` AS T1 INNER JOIN `成员` AS T2 ON T1.`专业编号` = T2.`关联专业` WHERE T1.`专业名称` = 'Physics Teaching'	student_club
SELECT T2.`活动名称` FROM `预算` AS T1 INNER JOIN `活动` AS T2 ON T1.`关联活动` = T2.`活动编号` WHERE T1.`类别` = '宣传推广' ORDER BY T1.`已支出` DESC LIMIT 1	student_club
SELECT CASE WHEN T3.`活动名称` = 'Women''s Soccer' THEN 'YES' END AS result FROM `成员` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`成员编号` = T2.`关联成员` INNER JOIN `活动` AS T3 ON T2.`关联活动` = T3.`活动编号` WHERE T1.`名` = 'Maya' AND T1.`姓` = 'Mclean'	student_club
SELECT T3.`费用` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算` WHERE T1.`活动名称` = 'September Speaker' AND T3.`支出描述` = '海报'	student_club
SELECT T2.`活动名称` FROM `预算` AS T1 INNER JOIN `活动` AS T2 ON T2.`活动编号` = T1.`关联活动` WHERE T1.`活动状态` = '已关闭' AND T1.`剩余金额` < 0 ORDER BY T1.`剩余金额` LIMIT 1	student_club
SELECT T1.`类型`, SUM(T3.`费用`) FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `支出` AS T3 ON T2.`预算编号` = T3.`关联预算` WHERE T1.`活动名称` = 'October Meeting'	student_club
SELECT T2.`类别`, SUM(T2.`金额`) FROM `活动` AS T1 JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` WHERE T1.`活动名称` = 'April Speaker' GROUP BY T2.`类别` ORDER BY SUM(T2.`金额`) ASC	student_club
SELECT SUM(`费用`) FROM `支出` WHERE `支出日期` = '2019-08-20'	student_club
SELECT T1.`名`, T1.`姓`, SUM(T2.`费用`) FROM `成员` AS T1 INNER JOIN `支出` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`成员编号` = 'rec4BLdZHS2Blfp4v'	student_club
SELECT T2.`支出描述` FROM `成员` AS T1 INNER JOIN `支出` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`名` = 'Sacha' AND T1.`姓` = 'Harrison'	student_club
SELECT DISTINCT T2.`类别` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` WHERE T1.`地点` = 'MU 215'	student_club
SELECT T2.`姓`, T1.`院系`, T1.`学院` FROM `专业` AS T1 INNER JOIN `成员` AS T2 ON T1.`专业编号` = T2.`关联专业` WHERE T2.`职位` = '会员' AND T1.`专业名称` = 'Environmental Engineering'	student_club
SELECT DISTINCT T2.`类别`, T1.`类型` FROM `活动` AS T1 INNER JOIN `预算` AS T2 ON T1.`活动编号` = T2.`关联活动` WHERE T1.`地点` = 'MU 215' AND T2.`已支出` = 0 AND T1.`类型` = '特邀嘉宾讲座'	student_club
SELECT CAST(SUM(CASE WHEN T2.`金额` = 50 THEN 1.0 ELSE 0 END) AS REAL) * 100 / COUNT(T2.`收入编号`) FROM `成员` AS T1 INNER JOIN `收入` AS T2 ON T1.`成员编号` = T2.`关联成员` WHERE T1.`职位` = '会员' AND T1.`T恤尺码` = '中号'	student_club
SELECT DISTINCT `活动名称` FROM `活动` WHERE `类型` = '游戏活动' AND date(SUBSTR(`活动日期`, 1, 10)) BETWEEN '2019-03-15' AND '2020-03-20' AND `状态` = '已关闭'	student_club
SELECT DISTINCT T3.`名`, T3.`姓`, T3.`电话` FROM `支出` AS T1 INNER JOIN `预算` AS T2 ON T1.`关联预算` = T2.`预算编号` INNER JOIN `成员` AS T3 ON T3.`成员编号` = T1.`关联成员` WHERE T1.`费用` > ( SELECT AVG(T1.`费用`) FROM `支出` AS T1 INNER JOIN `预算` AS T2 ON T1.`关联预算` = T2.`预算编号` INNER JOIN `成员` AS T3 ON T3.`成员编号` = T1.`关联成员` )	student_club
SELECT T2.`名`, T2.`姓`, T1.`费用` FROM `支出` AS T1 INNER JOIN `成员` AS T2 ON T1.`关联成员` = T2.`成员编号` WHERE T1.`支出描述` = '矿泉水、蔬菜拼盘、耗材'	student_club
SELECT DISTINCT T3.`名`, T3.`姓`, T4.`金额` FROM `活动` AS T1 INNER JOIN `出席记录` AS T2 ON T1.`活动编号` = T2.`关联活动` INNER JOIN `成员` AS T3 ON T3.`成员编号` = T2.`关联成员` INNER JOIN `收入` AS T4 ON T4.`关联成员` = T3.`成员编号` WHERE T4.`收款日期` = '2019-09-09'	student_club
SELECT CAST(SUM(CASE WHEN `入院日期` = '+' THEN 1 ELSE 0 END) AS REAL) * 100 / SUM(CASE WHEN `入院日期` = '-' THEN 1 ELSE 0 END) FROM `患者` WHERE `性别` = 'M'	thrombosis_prediction
SELECT CAST(SUM(CASE WHEN STRFTIME('%Y', `出生日期`) > '1930' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM `患者` WHERE `性别` = 'F'	thrombosis_prediction
SELECT SUM(CASE WHEN `入院日期` = '+' THEN 1.0 ELSE 0 END) / SUM(CASE WHEN `入院日期` = '-' THEN 1 ELSE 0 END) FROM `患者` WHERE `诊断` = '系统性红斑狼疮'	thrombosis_prediction
SELECT T1.`诊断`, T2.`检验日期` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`编号` = 30609	thrombosis_prediction
SELECT DISTINCT T1.`编号`, T1.`性别`, T1.`出生日期` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`乳酸脱氢酶` > 500	thrombosis_prediction
SELECT DISTINCT T1.`编号`, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.`出生日期`) FROM `患者` AS T1 INNER JOIN `检查记录` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`稀释蝰蛇毒时间` = '+'	thrombosis_prediction
SELECT DISTINCT T1.`编号`, T1.`性别`, T1.`诊断` FROM `患者` AS T1 INNER JOIN `检查记录` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`血栓形成` = 2	thrombosis_prediction
SELECT COUNT(*) FROM `患者` WHERE STRFTIME('%Y', `描述`) = '1997' AND `性别` = 'F' AND `入院日期` = '-'	thrombosis_prediction
SELECT  COUNT(*) FROM `患者` AS T1 INNER JOIN `检查记录` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`性别` = 'F' AND STRFTIME('%Y', T2.`检查日期`) = '1997' AND T2.`血栓形成` = 1	thrombosis_prediction
SELECT T2.`症状`, T1.`诊断` FROM `患者` AS T1 INNER JOIN `检查记录` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`症状` IS NOT NULL ORDER BY T1.`出生日期` DESC LIMIT 1	thrombosis_prediction
SELECT T1.`检验日期`, STRFTIME('%Y', T2.`初诊日期`) - STRFTIME('%Y', T2.`出生日期`),T2.`出生日期` FROM `检验报告` AS T1 INNER JOIN `患者` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`诊断` = '史蒂文斯-约翰逊综合征' AND T2.`出生日期` IS NOT NULL ORDER BY T2.`出生日期` ASC LIMIT 1	thrombosis_prediction
SELECT CAST(SUM(CASE WHEN T2.`尿酸` <= 8.0 AND T1.`性别` = 'M' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN T2.`尿酸` <= 6.5 AND T1.`性别` = 'F' THEN 1 ELSE 0 END) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号`	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检查记录` AS T2 ON T1.`编号` = T2.`编号` WHERE STRFTIME('%Y', T2.`检查日期`) BETWEEN '1990' AND '1993' AND STRFTIME('%Y', T2.`检查日期`) - STRFTIME('%Y', T1.`出生日期`) < 18	thrombosis_prediction
SELECT STRFTIME('%Y', T2.`检验日期`) - STRFTIME('%Y', T1.`出生日期`), T1.`诊断` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` ORDER BY T2.`血红蛋白` DESC LIMIT 1	thrombosis_prediction
SELECT `抗心磷脂抗体IgA`, `抗心磷脂抗体IgG`, `抗心磷脂抗体IgM` FROM `检查记录` WHERE `编号` IN ( SELECT `编号` FROM `患者` WHERE `诊断` = '系统性红斑狼疮' AND `描述` = '1994-02-19' ) AND `检查日期` = '1993-11-12'	thrombosis_prediction
SELECT CAST((SUM(CASE WHEN T2.`检验日期` LIKE '1981-11-%' THEN T2.`总胆固醇` ELSE 0 END) - SUM(CASE WHEN T2.`检验日期` LIKE '1981-12-%' THEN T2.`总胆固醇` ELSE 0 END)) AS REAL) / SUM(CASE WHEN T2.`检验日期` LIKE '1981-12-%' THEN T2.`总胆固醇` ELSE 0 END) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`出生日期` = '1959-02-18'	thrombosis_prediction
SELECT DISTINCT `编号` FROM `检验报告` WHERE `检验日期` BETWEEN '1987-07-06' AND '1996-01-31' AND `谷丙转氨酶` > 30 AND `白蛋白` < 4	thrombosis_prediction
SELECT COUNT(*) FROM `检查记录` WHERE `血栓形成` = 2 AND `抗核抗体荧光模式` = '斑点型' AND `抗心磷脂抗体IgM` > (SELECT AVG(`抗心磷脂抗体IgM`) * 1.2 FROM `检查记录` WHERE `血栓形成` = 2 AND `抗核抗体荧光模式` = '斑点型')	thrombosis_prediction
SELECT DISTINCT T1.`编号` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`入院日期` = '-' AND T2.`总胆红素` < 2.0 AND T2.`检验日期` LIKE '1991-10-%'	thrombosis_prediction
SELECT AVG(T2.`白蛋白`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`血小板计数` > 400 AND T1.`诊断` = '系统性红斑狼疮' AND T1.`性别` = 'F'	thrombosis_prediction
SELECT COUNT(`编号`) FROM `患者` WHERE `性别` = 'F' AND `诊断` = '抗磷脂综合征'	thrombosis_prediction
SELECT CAST(SUM(CASE WHEN `性别` = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(`编号`) FROM `患者` WHERE `诊断` = '类风湿关节炎' AND STRFTIME('%Y', `出生日期`) = '1980'	thrombosis_prediction
SELECT CASE WHEN (T1.`性别` = 'F' AND T2.`尿酸` > 6.5) OR (T1.`性别` = 'M' AND T2.`尿酸` > 8.0) THEN true ELSE false END FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`编号` = 57266	thrombosis_prediction
SELECT DISTINCT T1.`编号` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`性别` = 'M' AND T2.`谷丙转氨酶` >= 60	thrombosis_prediction
SELECT DISTINCT T1.`诊断` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`谷丙转氨酶` > 60 ORDER BY T1.`出生日期` ASC	thrombosis_prediction
SELECT DISTINCT T1.`编号`, T1.`性别`, T1.`出生日期` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`尿素氮` = 29	thrombosis_prediction
SELECT T1.`编号`,T1.`性别` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`总胆红素` >= 2.0 GROUP BY T1.`性别`,T1.`编号`	thrombosis_prediction
SELECT AVG(STRFTIME('%Y', date('NOW')) - STRFTIME('%Y', T1.`出生日期`)) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`总胆固醇` >= 250 AND T1.`性别` = 'M'	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`甘油三酯` >= 200 AND STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.`出生日期`) > 50	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE STRFTIME('%Y', T1.`出生日期`) BETWEEN '1936' AND '1956' AND T1.`性别` = 'M' AND T2.`肌酸激酶` >= 250	thrombosis_prediction
SELECT DISTINCT T1.`编号`, T1.`性别` , STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.`出生日期`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`血糖` >= 180 AND T2.`总胆固醇` < 250	thrombosis_prediction
SELECT DISTINCT T1.`诊断`, T1.`编号` , STRFTIME('%Y', CURRENT_TIMESTAMP) -STRFTIME('%Y', T1.`出生日期`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`红细胞计数` < 3.5	thrombosis_prediction
SELECT T1.`编号`, T1.`性别` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`诊断` = '系统性红斑狼疮' AND T2.`血红蛋白` > 10 AND T2.`血红蛋白` < 17 ORDER BY T1.`出生日期` ASC LIMIT 1	thrombosis_prediction
SELECT DISTINCT T1.`编号`, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.`出生日期`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T1.`编号` IN ( SELECT `编号` FROM `检验报告` WHERE `红细胞压积` >= 52 GROUP BY `编号` HAVING COUNT(`编号`) >= 2 )	thrombosis_prediction
SELECT SUM(CASE WHEN T2.`血小板计数` <= 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.`血小板计数` >= 400 THEN 1 ELSE 0 END) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号`	thrombosis_prediction
SELECT DISTINCT T1.`编号` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`血小板计数` BETWEEN 100 AND 400 AND STRFTIME('%Y', T2.`检验日期`) - STRFTIME('%Y', T1.`出生日期`) < 50 AND STRFTIME('%Y', T2.`检验日期`) = '1984'	thrombosis_prediction
SELECT CAST(SUM(CASE WHEN T2.`凝血酶原时间` >= 14 AND T1.`性别` = 'F' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(CASE WHEN T2.`凝血酶原时间` >= 14 THEN 1 ELSE 0 END) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T1.`出生日期`) > 55	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`纤维蛋白原` <= 150 OR T2.`纤维蛋白原` >= 450 AND T2.`白细胞计数` > 3.5 AND T2.`白细胞计数` < 9.0 AND T1.`性别` = 'M'	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T3.`编号` = T2.`编号` WHERE T2.`免疫球蛋白G` >= 2000	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T3.`编号` = T2.`编号` WHERE T2.`免疫球蛋白G` BETWEEN 900 AND 2000 AND T3.`症状` IS NOT NULL	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`免疫球蛋白A` BETWEEN 80 AND 500 AND  strftime('%Y',  T1.`初诊日期`) > '1990'	thrombosis_prediction
SELECT T1.`诊断` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`免疫球蛋白M` NOT BETWEEN 40 AND 400 GROUP BY T1.`诊断` ORDER BY COUNT(T1.`诊断`) DESC LIMIT 1	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE (T2.`C反应蛋白` = '+' ) AND T1.`描述` IS NULL	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`肌酐` >= 1.5 AND STRFTIME('%Y', Date('now')) - STRFTIME('%Y', T1.`出生日期`) < 70	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`核糖核蛋白` = '阴性' OR T2.`核糖核蛋白` = '0' AND T1.`入院日期` = '+'	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `检查记录` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`斯密斯抗体` IN ('阴性','0') AND T1.`血栓形成` = 0	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T3.`编号` = T2.`编号` WHERE (T2.`肝肾微粒体抗体` = '阴性' OR T2.`肝肾微粒体抗体` = '0') AND T1.`性别` = 'F' AND T3.`症状` IS NULL	thrombosis_prediction
SELECT COUNT(DISTINCT T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`着丝点抗体` IN ('阴性', '0') AND T2.`干燥综合征B抗体` IN ('阴性', '0') AND T1.`性别` = 'M'	thrombosis_prediction
SELECT T1.`出生日期` FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` WHERE T2.`谷草转氨酶` >= 60 ORDER BY T1.`出生日期` DESC LIMIT 1	thrombosis_prediction
SELECT COUNT(T1.`编号`) FROM `患者` AS T1 INNER JOIN `检验报告` AS T2 ON T1.`编号` = T2.`编号` INNER JOIN `检查记录` AS T3 ON T1.`编号` = T3.`编号` WHERE T2.`肌酸激酶` < 250 AND (T3.`凝血酶时间` = '+' OR T3.`稀释蝰蛇毒时间` = '+' OR T3.`狼疮抗凝物` = '+')	thrombosis_prediction
SELECT t2.`联赛名称` FROM `比赛` AS t1 INNER JOIN `联赛` AS t2 ON t1.`联赛编号` = t2.`编号` WHERE t1.`赛季` = '2015/2016' GROUP BY t2.`联赛名称` ORDER BY SUM(t1.`主队进球数` + t1.`客队进球数`) DESC LIMIT 1	european_football_2
SELECT teamInfo.`球队全称` FROM `联赛` AS leagueData INNER JOIN `比赛` AS matchData ON leagueData.`编号` = matchData.`联赛编号` INNER JOIN `球队` AS teamInfo ON matchData.`客队API编号` = teamInfo.`球队API编号` WHERE leagueData.`联赛名称` = 'Scotland Premier League' AND matchData.`赛季` = '2009/2010' AND matchData.`客队进球数` - matchData.`主队进球数` > 0 GROUP BY matchData.`客队API编号` ORDER BY COUNT(*) DESC LIMIT 1	european_football_2
SELECT t1.`进攻推进速度` FROM `球队属性` AS t1 INNER JOIN `球队` AS t2 ON t1.`球队API编号` = t2.`球队API编号` ORDER BY t1.`进攻推进速度` ASC LIMIT 4	european_football_2
SELECT t2.`联赛名称` FROM `比赛` AS t1 INNER JOIN `联赛` AS t2 ON t1.`联赛编号` = t2.`编号` WHERE t1.`赛季` = '2015/2016' AND t1.`主队进球数` = t1.`客队进球数` GROUP BY t2.`联赛名称` ORDER BY COUNT(t1.`编号`) DESC LIMIT 1	european_football_2
SELECT DISTINCT DATETIME() - T2.`生日` age FROM `球员属性` AS t1 INNER JOIN `球员` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE STRFTIME('%Y',t1.`日期`) >= '2013' AND STRFTIME('%Y',t1.`日期`) <= '2015' AND t1.`冲刺速度` >= 97	european_football_2
SELECT t2.`联赛名称`, t1.max_count FROM `联赛` AS t2 JOIN (SELECT `联赛编号`, MAX(cnt) AS max_count FROM (SELECT `联赛编号`, COUNT(`编号`) AS cnt FROM `比赛` GROUP BY `联赛编号`) AS subquery) AS t1 ON t1.`联赛编号` = t2.`编号`	european_football_2
SELECT DISTINCT `球队FIFA编号` FROM `球队属性` WHERE `进攻推进速度` > 50 AND `进攻推进速度` < 60	european_football_2
SELECT DISTINCT t4.`球队全称` FROM `球队属性` AS t3 INNER JOIN `球队` AS t4 ON t3.`球队API编号` = t4.`球队API编号` WHERE SUBSTR(t3.`日期`, 1, 4) = '2012' AND t3.`进攻推进传球` > ( SELECT CAST(SUM(t2.`进攻推进传球`) AS REAL) / COUNT(t1.`编号`) FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE STRFTIME('%Y',t2.`日期`) = '2012')	european_football_2
SELECT CAST(COUNT(CASE WHEN t2.`惯用脚` = '左脚' THEN t1.`编号` ELSE NULL END) AS REAL) * 100 / COUNT(t1.`编号`) percent FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE SUBSTR(t1.`生日`, 1, 4) BETWEEN '1987' AND '1992'	european_football_2
SELECT CAST(SUM(t2.`远射`) AS REAL) / COUNT(t2.`日期`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`球员姓名` = 'Ahmed Samir Farag'	european_football_2
SELECT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`身高` > 180 GROUP BY t1.`编号` ORDER BY CAST(SUM(t2.`头球精度`) AS REAL) / COUNT(t2.`球员FIFA编号`) DESC LIMIT 10	european_football_2
SELECT t1.`联赛名称` FROM `联赛` AS t1 INNER JOIN `比赛` AS t2 ON t1.`编号` = t2.`联赛编号` WHERE t2.`赛季` = '2009/2010' GROUP BY t1.`联赛名称` HAVING (CAST(SUM(t2.`主队进球数`) AS REAL) / COUNT(DISTINCT t2.`编号`)) - (CAST(SUM(t2.`客队进球数`) AS REAL) / COUNT(DISTINCT t2.`编号`)) > 0	european_football_2
SELECT `球员姓名` FROM `球员` WHERE SUBSTR(`生日`, 1, 7) = '1970-10'	european_football_2
SELECT t2.`综合评分` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`球员姓名` = 'Gabriel Tamas' AND strftime('%Y', t2.`日期`) = '2011'	european_football_2
SELECT CAST(SUM(t2.`主队进球数`) AS REAL) / COUNT(t2.`编号`) FROM `国家` AS t1 INNER JOIN `比赛` AS t2 ON t1.`编号` = t2.`国家编号` WHERE t1.`国家名称` = 'Poland' AND t2.`赛季` = '2010/2011'	european_football_2
SELECT A FROM ( SELECT AVG(`射门`) result, 'Max' A FROM `球员` AS T1 INNER JOIN `球员属性` AS T2 ON T1.`球员API编号` = T2.`球员API编号` WHERE T1.`身高` = ( SELECT MAX(`身高`) FROM `球员` ) UNION SELECT AVG(`射门`) result, 'Min' A FROM `球员` AS T1 INNER JOIN `球员属性` AS T2 ON T1.`球员API编号` = T2.`球员API编号` WHERE T1.`身高` = ( SELECT MIN(`身高`) FROM `球员` ) ) ORDER BY result DESC LIMIT 1	european_football_2
SELECT CAST(SUM(t2.`综合评分`) AS REAL) / COUNT(t2.`编号`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`身高` > 170 AND STRFTIME('%Y',t2.`日期`) >= '2010' AND STRFTIME('%Y',t2.`日期`) <= '2015'	european_football_2
SELECT CAST(SUM(CASE WHEN t1.`球员姓名` = 'Abdou Diallo' THEN t2.`控球` ELSE 0 END) AS REAL) / COUNT(CASE WHEN t1.`球员姓名` = 'Abdou Diallo' THEN t2.`编号` ELSE NULL END) - CAST(SUM(CASE WHEN t1.`球员姓名` = 'Aaron Appindangoye' THEN t2.`控球` ELSE 0 END) AS REAL) / COUNT(CASE WHEN t1.`球员姓名` = 'Aaron Appindangoye' THEN t2.`编号` ELSE NULL END) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号`	european_football_2
SELECT `球员姓名` FROM `球员` WHERE `球员姓名` IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY `生日` ASC LIMIT 1	european_football_2
SELECT `球员姓名` FROM `球员` ORDER BY `身高` DESC LIMIT 1	european_football_2
SELECT COUNT(`球员API编号`) FROM `球员属性` WHERE `惯用脚` = '左脚' AND `进攻积极性` = '低'	european_football_2
SELECT COUNT(DISTINCT t1.`球员姓名`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE STRFTIME('%Y',t1.`生日`) < '1986' AND t2.`防守积极性` = '高'	european_football_2
SELECT DISTINCT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t2.`凌空抽射` > 70 AND t2.`盘带` > 70	european_football_2
SELECT COUNT(t2.`编号`) FROM `联赛` AS t1 INNER JOIN `比赛` AS t2 ON t1.`编号` = t2.`联赛编号` WHERE t1.`联赛名称` = 'Belgium Jupiler League' AND SUBSTR(t2.`日期`, 1, 7) = '2009-04'	european_football_2
SELECT t1.`联赛名称` FROM `联赛` AS t1 JOIN `比赛` AS t2 ON t1.`编号` = t2.`联赛编号` WHERE t2.`赛季` = '2008/2009' GROUP BY t1.`联赛名称` HAVING COUNT(t2.`编号`) = (SELECT MAX(match_count) FROM (SELECT COUNT(t2.`编号`) AS match_count FROM `比赛` AS t2 WHERE t2.`赛季` = '2008/2009' GROUP BY t2.`联赛编号`))	european_football_2
SELECT (SUM(CASE WHEN t1.`球员姓名` = 'Ariel Borysiuk' THEN t2.`综合评分` ELSE 0 END) * 1.0 - SUM(CASE WHEN t1.`球员姓名` = 'Paulin Puel' THEN t2.`综合评分` ELSE 0 END)) * 100 / SUM(CASE WHEN t1.`球员姓名` = 'Paulin Puel' THEN t2.`综合评分` ELSE 0 END) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号`	european_football_2
SELECT CAST(SUM(t2.`综合评分`) AS REAL) / COUNT(t2.`编号`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t1.`球员姓名` = 'Pietro Marino'	european_football_2
SELECT t2.`创造机会传球`, t2.`创造机会传球等级` FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t1.`球队全称` = 'Ajax' ORDER BY t2.`创造机会传球` DESC LIMIT 1	european_football_2
SELECT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE SUBSTR(t2.`日期`, 1, 10) = '2016-06-23' AND t2.`综合评分` = 77 ORDER BY t1.`生日` ASC LIMIT 1	european_football_2
SELECT t2.`综合评分` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE SUBSTR(t2.`日期`, 1, 10) = '2016-02-04' AND t1.`球员姓名` = 'Aaron Mooy'	european_football_2
SELECT t2.`进攻积极性` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t2.`日期` LIKE '2015-05-01%' AND t1.`球员姓名` = 'Francesco Migliore'	european_football_2
SELECT `日期` FROM ( SELECT t2.`传中`, t2.`日期` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员FIFA编号` = t2.`球员FIFA编号` WHERE t1.`球员姓名` = 'Kevin Constant' ORDER BY t2.`传中` DESC) ORDER BY `日期` DESC LIMIT 1	european_football_2
SELECT t2.`进攻推进传球等级` FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t1.`球队全称` = 'FC Lorient' AND t2.`日期` LIKE '2010-02-22%'	european_football_2
SELECT t2.`防守侵略性等级` FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t1.`球队全称` = 'Hannover 96' AND t2.`日期` LIKE '2015-09-10%'	european_football_2
SELECT CAST(SUM(t2.`综合评分`) AS REAL) / COUNT(t2.`编号`) FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员FIFA编号` = t2.`球员FIFA编号` WHERE t1.`球员姓名` = 'Marko Arnautovic' AND SUBSTR(t2.`日期`, 1, 10) BETWEEN '2007-02-22' AND '2016-04-21'	european_football_2
SELECT (SUM(CASE WHEN t1.`球员姓名` = 'Landon Donovan' THEN t2.`综合评分` ELSE 0 END) * 1.0 - SUM(CASE WHEN t1.`球员姓名` = 'Jordan Bowery' THEN t2.`综合评分` ELSE 0 END)) * 100 / SUM(CASE WHEN t1.`球员姓名` = 'Landon Donovan' THEN t2.`综合评分` ELSE 0 END) LvsJ_percent FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员FIFA编号` = t2.`球员FIFA编号` WHERE SUBSTR(t2.`日期`, 1, 10) = '2013-07-12'	european_football_2
SELECT `球员姓名` FROM (SELECT `球员姓名`, `身高`, DENSE_RANK() OVER (ORDER BY `身高` DESC) as rank FROM `球员`) WHERE rank = 1	european_football_2
SELECT DISTINCT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t2.`综合评分` = (SELECT MAX(`综合评分`) FROM `球员属性`)	european_football_2
SELECT DISTINCT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t2.`进攻积极性` = '高'	european_football_2
SELECT DISTINCT t1.`球队简称` FROM `球队` AS t1 INNER JOIN `球队属性` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t2.`创造机会传球等级` = '低风险'	european_football_2
SELECT COUNT(`编号`) FROM `球员` WHERE `生日` > '1990' AND `球员姓名` LIKE 'Aaron%'	european_football_2
SELECT SUM(CASE WHEN t1.`编号` = 6 THEN t1.`弹跳` ELSE 0 END) - SUM(CASE WHEN t1.`编号` = 23 THEN t1.`弹跳` ELSE 0 END) FROM `球员属性` AS t1	european_football_2
SELECT `编号` FROM `球员属性` WHERE `惯用脚` = '右脚' ORDER BY `潜力值` ASC LIMIT 4	european_football_2
SELECT COUNT(t1.`编号`) FROM `球员属性` AS t1 WHERE t1.`惯用脚` = '左脚' AND t1.`传中` = ( SELECT MAX(`传中`) FROM `球员属性`)	european_football_2
SELECT t2.`主队进球数`, t2.`客队进球数` FROM `联赛` AS t1 INNER JOIN `比赛` AS t2 ON t1.`编号` = t2.`联赛编号` WHERE t1.`联赛名称` = 'Belgium Jupiler League' AND t2.`日期` LIKE '2008-09-24%'	european_football_2
SELECT DISTINCT t1.`进攻推进速度等级` FROM `球队属性` AS t1 INNER JOIN `球队` AS t2 ON t1.`球队API编号` = t2.`球队API编号` WHERE t2.`球队全称` = 'KSV Cercle Brugge'	european_football_2
SELECT `编号`, `射门`, `弧线球` FROM `球员属性` WHERE `球员API编号` = ( SELECT `球员API编号` FROM `球员` ORDER BY `体重` DESC LIMIT 1 ) LIMIT 1	european_football_2
SELECT t1.`联赛名称` FROM `联赛` AS t1 INNER JOIN `比赛` AS t2 ON t1.`编号` = t2.`联赛编号` WHERE t2.`赛季` = '2015/2016' GROUP BY t1.`联赛名称` ORDER BY COUNT(t2.`编号`) DESC LIMIT 4	european_football_2
SELECT t2.`球队全称` FROM `比赛` AS t1 INNER JOIN `球队` AS t2 ON t1.`客队API编号` = t2.`球队API编号` ORDER BY t1.`客队进球数` DESC LIMIT 1	european_football_2
SELECT DISTINCT t1.`球员姓名` FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号` WHERE t2.`综合评分` = ( SELECT MAX(`综合评分`) FROM `球员属性`)	european_football_2
SELECT CAST(COUNT(CASE WHEN t2.`综合评分` > 70  AND t1.`身高` < 180 THEN t1.`编号` ELSE NULL END) AS REAL) * 100 / COUNT(t1.`编号`) percent FROM `球员` AS t1 INNER JOIN `球员属性` AS t2 ON t1.`球员API编号` = t2.`球员API编号`	european_football_2
SELECT T2.`车手代码` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 20 ORDER BY T1.`Q1成绩` DESC LIMIT 5	formula_1
SELECT T2.`姓` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 19 ORDER BY T1.`Q2成绩` ASC LIMIT 1	formula_1
SELECT DISTINCT T2.`名称` FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T1.`国家` = 'Germany'	formula_1
SELECT DISTINCT T1.`纬度`, T1.`经度` FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T2.`名称` = 'Australian Grand Prix'	formula_1
SELECT DISTINCT T1.`纬度`, T1.`经度` FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T2.`名称` = 'Abu Dhabi Grand Prix'	formula_1
SELECT T1.`Q1成绩` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 354 AND T2.`名` = 'Bruno' AND T2.`姓` = 'Senna'	formula_1
SELECT T2.`车号` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 903 AND T1.`Q3成绩` LIKE '1:54%'	formula_1
SELECT COUNT(T3.`车手编号`) FROM `比赛` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T1.`年份` = 2007 AND T1.`名称` = 'Bahrain Grand Prix' AND T2.`用时` IS NULL	formula_1
SELECT T1.`名`, T1.`姓` FROM `车手` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T2.`比赛编号` = 592 AND T2.`用时` IS NOT NULL AND T1.`出生日期` IS NOT NULL ORDER BY T1.`出生日期` ASC LIMIT 1	formula_1
SELECT DISTINCT T2.`名`, T2.`姓`, T2.`网址` FROM `单圈用时` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 161 AND T1.`用时` LIKE '1:27%'	formula_1
SELECT DISTINCT T1.`纬度`, T1.`经度` FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T2.`名称` = 'Malaysian Grand Prix'	formula_1
SELECT T2.`网址` FROM `车队比赛成绩` AS T1 INNER JOIN `车队` AS T2 ON T2.`车队编号` = T1.`车队编号` WHERE T1.`比赛编号` = 9 ORDER BY T1.`积分` DESC LIMIT 1	formula_1
SELECT T2.`车手代号` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`比赛编号` = 45 AND T1.`Q3成绩` LIKE '1:33%'	formula_1
SELECT T2.`网址` FROM `比赛` AS T1 INNER JOIN `赛季` AS T2 ON T2.`年份` = T1.`年份` WHERE T1.`比赛编号` = 901	formula_1
SELECT T1.`名`, T1.`姓` FROM `车手` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T2.`比赛编号` = 872 AND T2.`用时` IS NOT NULL ORDER BY T1.`出生日期` DESC LIMIT 1	formula_1
SELECT T1.`国籍` FROM `车手` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`车手编号` = T1.`车手编号` ORDER BY T2.`最快单圈平均速度` DESC LIMIT 1	formula_1
SELECT (SUM(IIF(T2.`比赛编号` = 853, T2.`最快单圈平均速度`, 0)) - SUM(IIF(T2.`比赛编号` = 854, T2.`最快单圈平均速度`, 0))) * 100 / SUM(IIF(T2.`比赛编号` = 853, T2.`最快单圈平均速度`, 0)) FROM `车手` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T1.`名` = 'Paul' AND T1.`姓` = 'di Resta'	formula_1
SELECT CAST(COUNT(CASE WHEN T2.`用时` IS NOT NULL THEN T2.`车手编号` END) AS REAL) * 100 / COUNT(T2.`车手编号`) FROM `比赛` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`比赛编号` = T1.`比赛编号` WHERE T1.`日期` = '1983-07-16'	formula_1
SELECT `名称` FROM `比赛` WHERE STRFTIME('%Y', `日期`) = ( SELECT STRFTIME('%Y', `日期`) FROM `比赛` ORDER BY `日期` ASC LIMIT 1 ) AND STRFTIME('%m', `日期`) = ( SELECT STRFTIME('%m', `日期`) FROM `比赛` ORDER BY `日期` ASC LIMIT 1 )	formula_1
SELECT T3.`名`, T3.`姓`, T2.`积分` FROM `比赛` AS T1 INNER JOIN `车手年度积分榜` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` ORDER BY T2.`积分` DESC LIMIT 1	formula_1
SELECT T2.`毫秒数`, T1.`名`, T1.`姓`, T3.`名称` FROM `车手` AS T1 INNER JOIN `单圈用时` AS T2 ON T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 ON T2.`比赛编号` = T3.`比赛编号` ORDER BY T2.`毫秒数` ASC LIMIT 1	formula_1
SELECT AVG(T2.`毫秒数`) FROM `比赛` AS T1 INNER JOIN `单圈用时` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`名` = 'Lewis' AND T3.`姓` = 'Hamilton' AND T1.`年份` = 2009 AND T1.`名称` = 'Malaysian Grand Prix'	formula_1
SELECT CAST(COUNT(CASE WHEN T2.`排名` <> 1 THEN T2.`排名` END) AS REAL) * 100 / COUNT(T2.`车手年度积分榜编号`) FROM `比赛` AS T1 INNER JOIN `车手年度积分榜` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`姓` = 'Hamilton' AND T1.`年份` >= 2010	formula_1
SELECT T1.`名`, T1.`姓`, T1.`国籍`, MAX(T2.`积分`) FROM `车手` AS T1 INNER JOIN `车手年度积分榜` AS T2 ON T2.`车手编号` = T1.`车手编号` WHERE T2.`胜场数` >= 1 GROUP BY T1.`名`, T1.`姓`, T1.`国籍` ORDER BY COUNT(T2.`胜场数`) DESC LIMIT 1	formula_1
SELECT STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', `出生日期`), `名` , `姓` FROM `车手` WHERE `国籍` = '日本籍' ORDER BY `出生日期` DESC LIMIT 1	formula_1
SELECT DISTINCT T2.`名称`, T1.`名称`, T1.`所在地` FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T2.`年份` = 2005 AND STRFTIME('%m', T2.`日期`) = '09'	formula_1
SELECT T1.`名称` FROM `比赛` AS T1 INNER JOIN `车手年度积分榜` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`名` = 'Alex' AND T3.`姓` = 'Yoong' AND T2.`排名` < 20	formula_1
SELECT T1.`名称`, T1.`年份` FROM `比赛` AS T1 INNER JOIN `单圈用时` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`名` = 'Michael' AND T3.`姓` = 'Schumacher' ORDER BY T2.`毫秒数` ASC LIMIT 1	formula_1
SELECT T1.`名称`, T2.`积分` FROM `比赛` AS T1 INNER JOIN `车手年度积分榜` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`名` = 'Lewis' AND T3.`姓` = 'Hamilton' ORDER BY T1.`年份` ASC LIMIT 1	formula_1
SELECT CAST(COUNT(CASE WHEN T1.`国家` = 'Germany' THEN T2.`赛道编号` END) AS REAL) * 100 / COUNT(T2.`赛道编号`) FROM `赛道` AS T1 INNER JOIN `比赛` AS T2 ON T2.`赛道编号` = T1.`赛道编号` WHERE T2.`名称` = 'European Grand Prix'	formula_1
SELECT `纬度`, `经度` FROM `赛道` WHERE `名称` = 'Silverstone Circuit'	formula_1
SELECT `赛道代码` FROM `赛道` WHERE `名称` = 'Marina Bay Street Circuit'	formula_1
SELECT `国籍` FROM `车手` WHERE `出生日期` IS NOT NULL ORDER BY `出生日期` ASC LIMIT 1	formula_1
SELECT T3.`名`, T3.`姓`, T3.`车手代码` FROM `比赛` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T1.`名称` = 'Canadian Grand Prix' AND T2.`最快单圈排名` = 1 AND T1.`年份` = 2007	formula_1
SELECT `名称` FROM `比赛` WHERE `比赛编号` IN ( SELECT `比赛编号` FROM `正赛成绩` WHERE `最快单圈排名` = 1 AND `车手编号` = ( SELECT `车手编号` FROM `车手` WHERE `名` = 'Lewis' AND `姓` = 'Hamilton' ) )	formula_1
SELECT T2.`最快单圈平均速度` FROM `比赛` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`比赛编号` = T1.`比赛编号` WHERE T1.`名称` = 'Spanish Grand Prix' AND T1.`年份` = 2009 AND T2.`最快单圈平均速度` IS NOT NULL ORDER BY T2.`最快单圈平均速度` DESC LIMIT 1	formula_1
SELECT T2.`完赛名次序号` FROM `比赛` AS T1 INNER JOIN `正赛成绩` AS T2 ON T2.`比赛编号` = T1.`比赛编号` INNER JOIN `车手` AS T3 ON T3.`车手编号` = T2.`车手编号` WHERE T3.`名` = 'Lewis' AND T3.`姓` = 'Hamilton' AND T1.`名称` = 'Chinese Grand Prix' AND T1.`年份` = 2008	formula_1
SELECT T1.`用时` FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` WHERE T1.`最快单圈排名` = 2 AND T2.`名称` = 'Chinese Grand Prix' AND T2.`年份` = 2008	formula_1
SELECT COUNT(*) FROM ( SELECT T1.`车手编号` FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` WHERE T2.`名称` = 'Chinese Grand Prix' AND T2.`年份` = 2008 AND T1.`用时` IS NOT NULL GROUP BY T1.`车手编号` HAVING COUNT(T2.`比赛编号`) > 0 )	formula_1
WITH time_in_seconds AS ( SELECT T1.`完赛名次序号`, CASE WHEN T1.`完赛名次序号` = 1 THEN (CAST(SUBSTR(T1.`用时`, 1, 1) AS REAL) * 3600) + (CAST(SUBSTR(T1.`用时`, 3, 2) AS REAL) * 60) + CAST(SUBSTR(T1.`用时`, 6) AS REAL) ELSE CAST(SUBSTR(T1.`用时`, 2) AS REAL) END AS time_seconds FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 ON T1.`比赛编号` = T2.`比赛编号` WHERE T2.`名称` = 'Australian Grand Prix' AND T1.`用时` IS NOT NULL AND T2.`年份` = 2008 ), champion_time AS ( SELECT time_seconds FROM time_in_seconds WHERE `完赛名次序号` = 1), last_driver_incremental AS ( SELECT time_seconds FROM time_in_seconds WHERE `完赛名次序号` = (SELECT MAX(`完赛名次序号`) FROM time_in_seconds) ) SELECT (CAST((SELECT time_seconds FROM last_driver_incremental) AS REAL) * 100) / (SELECT time_seconds + (SELECT time_seconds FROM last_driver_incremental) FROM champion_time)	formula_1
SELECT COUNT(`赛道编号`) FROM `赛道` WHERE `所在地` = 'Adelaide' AND `国家` = 'Australia'	formula_1
SELECT MAX(T1.`积分`) FROM `车队年度积分榜` AS T1 INNER JOIN `车队` AS T2 on T1.`车队编号` = T2.`车队编号` WHERE T2.`国籍` = '英国籍'	formula_1
SELECT T2.`名称` FROM `车队年度积分榜` AS T1 INNER JOIN `车队` AS T2 on T1.`车队编号` = T2.`车队编号` WHERE T1.`积分` = 0 AND T1.`比赛编号` = 291	formula_1
SELECT COUNT(T1.`比赛编号`) FROM `车队年度积分榜` AS T1 INNER JOIN `车队` AS T2 on T1.`车队编号` = T2.`车队编号` WHERE T1.`积分` = 0 AND T2.`国籍` = '日本籍' GROUP BY T1.`车队编号` HAVING COUNT(`比赛编号`) = 2	formula_1
SELECT CAST(SUM(IIF(T1.`用时` IS NOT NULL, 1, 0)) AS REAL) * 100 / COUNT(T1.`比赛编号`) FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `车手` AS T3 on T1.`车手编号` = T3.`车手编号` WHERE T3.`国籍` = '日本籍' AND T2.`年份` BETWEEN 2007 AND 2009	formula_1
WITH time_in_seconds AS ( SELECT T2.`年份`, T2.`比赛编号`, T1.`完赛名次序号`, CASE WHEN T1.`完赛名次序号` = 1 THEN (CAST(SUBSTR(T1.`用时`, 1, 1) AS REAL) * 3600) + (CAST(SUBSTR(T1.`用时`, 3, 2) AS REAL) * 60) + CAST(SUBSTR(T1.`用时`, 6,2) AS REAL )   + CAST(SUBSTR(T1.`用时`, 9) AS REAL)/1000 ELSE 0 END AS time_seconds FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 ON T1.`比赛编号` = T2.`比赛编号` WHERE T1.`用时` IS NOT NULL ), champion_time AS ( SELECT `年份`, `比赛编号`, time_seconds FROM time_in_seconds WHERE `完赛名次序号` = 1 ) SELECT `年份`, AVG(time_seconds) FROM champion_time WHERE `年份` < 1975 GROUP BY `年份` HAVING AVG(time_seconds) IS NOT NULL	formula_1
SELECT T1.`最快单圈` FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` WHERE T2.`年份` = 2009 AND T1.`用时` LIKE '_:%:__.___'	formula_1
SELECT AVG(T1.`最快单圈平均速度`) FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` WHERE T2.`年份` = 2009 AND T2.`名称` = 'Spanish Grand Prix'	formula_1
SELECT CAST(SUM(IIF(STRFTIME('%Y', T3.`出生日期`) < '1985' AND T1.`完成圈数` > 50, 1, 0)) AS REAL) * 100 / COUNT(*) FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `车手` AS T3 on T1.`车手编号` = T3.`车手编号` WHERE T2.`年份` BETWEEN 2000 AND 2005	formula_1
SELECT COUNT(T1.`车手编号`) FROM `车手` AS T1 INNER JOIN `单圈用时` AS T2 on T1.`车手编号` = T2.`车手编号` WHERE T1.`国籍` = '法国籍' AND (CAST(SUBSTR(T2.`用时`, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(T2.`用时`, 4, 2) AS INTEGER) + CAST(SUBSTR(T2.`用时`, 7, 2) AS REAL) / 1000) < 120	formula_1
SELECT `车手代号` FROM `车手` WHERE `国籍` = '美国籍'	formula_1
SELECT COUNT(*) FROM ( SELECT T1.`国籍` FROM `车手` AS T1 ORDER BY JULIANDAY(T1.`出生日期`) DESC LIMIT 3) AS T3 WHERE T3.`国籍` = '荷兰籍'	formula_1
SELECT `车手代码` FROM `车手` WHERE `国籍` = '德国籍' ORDER BY JULIANDAY(`出生日期`) ASC LIMIT 1	formula_1
SELECT T2.`车手编号`, T2.`车手代号` FROM `正赛成绩` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` WHERE STRFTIME('%Y', T2.`出生日期`) = '1971' AND T1.`最快单圈用时` IS NOT NULL	formula_1
SELECT SUM(IIF(`用时` IS NOT NULL, 1, 0)) FROM `正赛成绩` WHERE `状态编号` = 2 AND `比赛编号` < 100 AND `比赛编号` > 50	formula_1
SELECT DISTINCT `所在地`, `纬度`, `经度` FROM `赛道` WHERE `国家` = 'Austria'	formula_1
SELECT T3.`年份`, T3.`名称`, T3.`日期`, T3.`时间` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 on T1.`比赛编号` = T3.`比赛编号` WHERE T1.`车手编号` = ( SELECT `车手编号` FROM `车手` ORDER BY `出生日期` DESC LIMIT 1 ) ORDER BY T3.`日期` ASC LIMIT 1	formula_1
SELECT T2.`名`, T2.`姓` FROM `进站记录` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` WHERE T2.`国籍` = '德国籍' AND STRFTIME('%Y', T2.`出生日期`) BETWEEN '1980' AND '1985' GROUP BY T2.`名`, T2.`姓` ORDER BY AVG(T1.`进站时长`) LIMIT 3	formula_1
SELECT T1.`用时` FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 ON T1.`比赛编号` = T2.`比赛编号` WHERE T2.`名称` = 'Canadian Grand Prix' AND T2.`年份` = 2008 AND T1.`用时` LIKE '_:%:__.___'	formula_1
SELECT T3.`车队代码`, T3.`网址` FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `车队` AS T3 on T1.`车队编号` = T3.`车队编号` WHERE T2.`名称` = 'Singapore Grand Prix' AND T2.`年份` = 2009 AND T1.`用时` LIKE '_:%:__.___'	formula_1
SELECT T3.`能力名称` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T1.`超级英雄名称` = '3-D Man'	superhero
SELECT SUM(T1.`积分`), T2.`名称`, T2.`国籍` FROM `车队比赛成绩` AS T1 INNER JOIN `车队` AS T2 ON T1.`车队编号` = T2.`车队编号` INNER JOIN `比赛` AS T3 ON T3.`比赛编号` = T1.`比赛编号` WHERE T3.`名称` = 'Monaco Grand Prix' AND T3.`年份` BETWEEN 1980 AND 2010 GROUP BY T2.`名称` ORDER BY SUM(T1.`积分`) DESC LIMIT 1	formula_1
SELECT T2.`名`, T2.`姓` FROM `排位赛成绩` AS T1 INNER JOIN `车手` AS T2 on T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 ON T1.`比赛编号` = T3.`比赛编号` WHERE `Q3成绩` IS NOT NULL AND T3.`年份` = 2008 AND T3.`赛道编号` IN ( SELECT `赛道编号` FROM `赛道` WHERE `名称` = 'Marina Bay Street Circuit' ) ORDER BY CAST(SUBSTR(`Q3成绩`, 1, INSTR(`Q3成绩`, ':') - 1) AS INTEGER) * 60 + CAST(SUBSTR(`Q3成绩`, INSTR(`Q3成绩`, ':') + 1, INSTR(`Q3成绩`, '.') - INSTR(`Q3成绩`, ':') - 1) AS REAL) + CAST(SUBSTR(`Q3成绩`, INSTR(`Q3成绩`, '.') + 1) AS REAL) / 1000 ASC LIMIT 1	formula_1
SELECT T1.`名`, T1.`姓`, T1.`国籍`, T3.`名称` FROM `车手` AS T1 INNER JOIN `车手年度积分榜` AS T2 on T1.`车手编号` = T2.`车手编号` INNER JOIN `比赛` AS T3 on T2.`比赛编号` = T3.`比赛编号` ORDER BY JULIANDAY(T1.`出生日期`) DESC LIMIT 1	formula_1
SELECT COUNT(T1.`车手编号`) FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `状态` AS T3 on T1.`状态编号` = T3.`状态编号` WHERE T3.`状态编号` = 3 AND T2.`名称` = 'Canadian Grand Prix' GROUP BY T1.`车手编号` ORDER BY COUNT(T1.`车手编号`) DESC LIMIT 1	formula_1
WITH lap_times_in_seconds AS (SELECT `车手编号`, (CASE WHEN SUBSTR(`用时`, 1, INSTR(`用时`, ':') - 1) <> '' THEN CAST(SUBSTR(`用时`, 1, INSTR(`用时`, ':') - 1) AS REAL) * 60 ELSE 0 END + CASE WHEN SUBSTR(`用时`, INSTR(`用时`, ':') + 1, INSTR(`用时`, '.') - INSTR(`用时`, ':') - 1) <> '' THEN CAST(SUBSTR(`用时`, INSTR(`用时`, ':') + 1, INSTR(`用时`, '.') - INSTR(`用时`, ':') - 1) AS REAL) ELSE 0 END + CASE WHEN SUBSTR(`用时`, INSTR(`用时`, '.') + 1) <> '' THEN CAST(SUBSTR(`用时`, INSTR(`用时`, '.') + 1) AS REAL) / 1000 ELSE 0 END) AS time_in_seconds FROM `单圈用时`) SELECT T2.`名`, T2.`姓`, T1.`车手编号` FROM (SELECT `车手编号`, MIN(time_in_seconds) AS min_time_in_seconds FROM lap_times_in_seconds GROUP BY `车手编号`) AS T1 INNER JOIN `车手` AS T2 ON T1.`车手编号` = T2.`车手编号` ORDER BY T1.min_time_in_seconds ASC LIMIT 20	formula_1
WITH fastest_lap_times AS (SELECT T1.`比赛编号`, T1.`最快单圈用时`, (CAST(SUBSTR(T1.`最快单圈用时`, 1, INSTR(T1.`最快单圈用时`, ':') - 1) AS REAL) * 60) + (CAST(SUBSTR(T1.`最快单圈用时`, INSTR(T1.`最快单圈用时`, ':') + 1, INSTR(T1.`最快单圈用时`, '.') - INSTR(T1.`最快单圈用时`, ':') - 1) AS REAL)) + (CAST(SUBSTR(T1.`最快单圈用时`, INSTR(T1.`最快单圈用时`, '.') + 1) AS REAL) / 1000) as time_in_seconds FROM `正赛成绩` AS T1 WHERE T1.`最快单圈用时` IS NOT NULL ) SELECT T1.`最快单圈用时` as lap_record FROM `正赛成绩` AS T1 INNER JOIN `比赛` AS T2 on T1.`比赛编号` = T2.`比赛编号` INNER JOIN `赛道` AS T3 on T2.`赛道编号` = T3.`赛道编号` INNER JOIN (SELECT MIN(fastest_lap_times.time_in_seconds) as min_time_in_seconds FROM fastest_lap_times INNER JOIN `比赛` AS T2 on fastest_lap_times.`比赛编号` = T2.`比赛编号` INNER JOIN `赛道` AS T3 on T2.`赛道编号` = T3.`赛道编号` WHERE T3.`国家` = 'Italy' ) AS T4 ON (CAST(SUBSTR(T1.`最快单圈用时`, 1, INSTR(T1.`最快单圈用时`, ':') - 1) AS REAL) * 60) + (CAST(SUBSTR(T1.`最快单圈用时`, INSTR(T1.`最快单圈用时`, ':') + 1, INSTR(T1.`最快单圈用时`, '.') - INSTR(T1.`最快单圈用时`, ':') - 1) AS REAL)) + (CAST(SUBSTR(T1.`最快单圈用时`, INSTR(T1.`最快单圈用时`, '.') + 1) AS REAL) / 1000) = T4.min_time_in_seconds LIMIT 1	formula_1
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T3.`能力名称` = 'Super Strength' AND T1.`身高（厘米）` > 200	superhero
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` INNER JOIN `颜色` AS T4 ON T1.`瞳色编号` = T4.`编号` WHERE T3.`能力名称` = 'Agility' AND T4.`颜色` = '蓝色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`发色编号` = T3.`编号` WHERE T2.`颜色` = '蓝色' AND T3.`颜色` = '金发色'	superhero
SELECT `超级英雄名称`, `身高（厘米）`, RANK() OVER (ORDER BY `身高（厘米）` DESC) AS HeightRank FROM `超级英雄` INNER JOIN `出版商` ON `超级英雄`.`出版商编号` = `出版商`.`编号` WHERE `出版商`.`出版商名称` = 'Marvel Comics'	superhero
SELECT `颜色`.`颜色` AS EyeColor, COUNT(`超级英雄`.`编号`) AS Count, RANK() OVER (ORDER BY COUNT(`超级英雄`.`编号`) DESC) AS PopularityRank FROM `超级英雄` INNER JOIN `颜色` ON `超级英雄`.`瞳色编号` = `颜色`.`编号` INNER JOIN `出版商` ON `超级英雄`.`出版商编号` = `出版商`.`编号` WHERE `出版商`.`出版商名称` = 'Marvel Comics' GROUP BY `颜色`.`颜色`	superhero
SELECT `超级英雄名称` FROM `超级英雄` AS T1 WHERE EXISTS (SELECT 1 FROM `英雄能力` AS T2 INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T3.`能力名称` = 'Super Strength' AND T1.`编号` = T2.`英雄编号`)AND EXISTS (SELECT 1 FROM `出版商` AS T4 WHERE T4.`出版商名称` = 'Marvel Comics' AND T1.`出版商编号` = T4.`编号`)	superhero
SELECT T2.`出版商名称` FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` INNER JOIN `英雄属性` AS T3 ON T1.`编号` = T3.`英雄编号` INNER JOIN `属性` AS T4 ON T3.`属性编号` = T4.`编号` WHERE T4.`属性名称` = 'Speed' ORDER BY T3.`属性值` LIMIT 1	superhero
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`瞳色编号` = T3.`编号` WHERE T2.`出版商名称` = 'Marvel Comics' AND T3.`颜色` = '金色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` WHERE T3.`属性名称` = 'Intelligence' ORDER BY T2.`属性值` LIMIT 1	superhero
SELECT T2.`种族` FROM `超级英雄` AS T1 INNER JOIN `种族` AS T2 ON T1.`种族编号` = T2.`编号` WHERE T1.`超级英雄名称` = 'Copycat'	superhero
SELECT `超级英雄名称` FROM `超级英雄` AS T1 WHERE EXISTS (SELECT 1 FROM `英雄属性` AS T2 INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` WHERE T3.`属性名称` = 'Durability' AND T2.`属性值` < 50 AND T1.`编号` = T2.`英雄编号`)	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T3.`能力名称` = 'Death Touch'	superhero
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` INNER JOIN `性别` AS T4 ON T1.`性别编号` = T4.`编号` WHERE T3.`属性名称` = 'Strength' AND T2.`属性值` = 100 AND T4.`性别` = '女性'	superhero
SELECT (CAST(COUNT(*) AS REAL) * 100 / (SELECT COUNT(*) FROM `超级英雄`)), CAST(SUM(CASE WHEN T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE 0 END) AS REAL) FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` INNER JOIN `阵营` AS T3 ON T3.`编号` = T1.`阵营编号` WHERE T3.`阵营` = '邪恶'	superhero
SELECT SUM(CASE WHEN T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.`出版商名称` = 'DC Comics' THEN 1 ELSE 0 END) FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号`	superhero
SELECT `编号` FROM `出版商` WHERE `出版商名称` = 'Star Trek'	superhero
SELECT COUNT(`编号`) FROM `超级英雄` WHERE `全名` IS NULL	superhero
SELECT AVG(T1.`体重（千克）`) FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号` WHERE T2.`性别` = '女性'	superhero
SELECT T3.`能力名称` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T3.`编号` = T2.`能力编号` INNER JOIN `性别` AS T4 ON T4.`编号` = T1.`性别编号` WHERE T4.`性别` = '男性' LIMIT 5	superhero
SELECT DISTINCT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T1.`身高（厘米）` BETWEEN 170 AND 190 AND T2.`颜色` = '无颜色'	superhero
SELECT DISTINCT T3.`颜色` FROM `超级英雄` AS T1 INNER JOIN `种族` AS T2 ON T1.`种族编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`发色编号` = T3.`编号` WHERE T1.`身高（厘米）` = 185 AND T2.`种族` = '人类'	superhero
SELECT CAST(COUNT(CASE WHEN T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` WHERE T1.`身高（厘米）` BETWEEN 150 AND 180	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号` WHERE T2.`性别` = '男性' AND T1.`体重（千克）` * 100 > ( SELECT AVG(`体重（千克）`) FROM `超级英雄` ) * 79	superhero
SELECT DISTINCT T2.`能力名称` FROM `英雄能力` AS T1 INNER JOIN `超能力` AS T2 ON T1.`能力编号` = T2.`编号` WHERE T1.`英雄编号` = 1	superhero
SELECT COUNT(T1.`英雄编号`) FROM `英雄能力` AS T1 INNER JOIN `超能力` AS T2 ON T1.`能力编号` = T2.`编号` WHERE T2.`能力名称` = 'Stealth'	superhero
SELECT T1.`全名` FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` WHERE T3.`属性名称` = 'Strength' ORDER BY T2.`属性值` DESC LIMIT 1	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T3.`编号` = T2.`属性编号` INNER JOIN `出版商` AS T4 ON T4.`编号` = T1.`出版商编号` WHERE T4.`出版商名称` = 'Dark Horse Comics' AND T3.`属性名称` = 'Durability' ORDER BY T2.`属性值` DESC LIMIT 1	superhero
SELECT T1.`瞳色编号`, T1.`发色编号`, T1.`肤色编号` FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T2.`编号` = T1.`出版商编号` INNER JOIN `性别` AS T3 ON T3.`编号` = T1.`性别编号` WHERE T2.`出版商名称` = 'Dark Horse Comics' AND T3.`性别` = '女性'	superhero
SELECT T1.`超级英雄名称`, T2.`出版商名称` FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` WHERE T1.`瞳色编号` = T1.`发色编号` AND T1.`瞳色编号` = T1.`肤色编号`	superhero
SELECT CAST(COUNT(CASE WHEN T3.`颜色` = '蓝色' THEN T1.`编号` ELSE NULL END) AS REAL) * 100 / COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`肤色编号` = T3.`编号` WHERE T2.`性别` = '女性'	superhero
SELECT COUNT(T1.`能力编号`) FROM `英雄能力` AS T1 INNER JOIN `超级英雄` AS T2 ON T1.`英雄编号` = T2.`编号` WHERE T2.`超级英雄名称` = 'Amazo'	superhero
SELECT T1.`身高（厘米）` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T2.`颜色` = '琥珀色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` AND T1.`发色编号` = T2.`编号` WHERE T2.`颜色` = '黑色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `阵营` AS T2 ON T1.`阵营编号` = T2.`编号` WHERE T2.`阵营` = '中立'	superhero
SELECT COUNT(T1.`英雄编号`) FROM `英雄属性` AS T1 INNER JOIN `属性` AS T2 ON T1.`属性编号` = T2.`编号` WHERE T2.`属性名称` = 'Strength' AND T1.`属性值` = ( SELECT MAX(`属性值`) FROM `英雄属性` )	superhero
SELECT CAST(COUNT(CASE WHEN T3.`性别` = '女性' AND T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE NULL END) AS REAL) / COUNT(CASE WHEN T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE NULL END) * 100 FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` INNER JOIN `性别` AS T3 ON T1.`性别编号` = T3.`编号`	superhero
SELECT ( SELECT `体重（千克）` FROM `超级英雄` WHERE `全名` LIKE 'Emil Blonsky' ) - ( SELECT `体重（千克）` FROM `超级英雄` WHERE `全名` LIKE 'Charles Chandler' ) AS CALCULATE	superhero
SELECT CAST(SUM(`身高（厘米）`) AS REAL) / COUNT(`编号`) FROM `超级英雄`	superhero
SELECT T3.`能力名称` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T1.`超级英雄名称` = 'Abomination'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` WHERE T3.`属性名称` = 'Speed' ORDER BY T2.`属性值` DESC LIMIT 1	superhero
SELECT T3.`属性名称`, T2.`属性值` FROM `超级英雄` AS T1 INNER JOIN `英雄属性` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `属性` AS T3 ON T2.`属性编号` = T3.`编号` WHERE T1.`超级英雄名称` = '3-D Man'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`发色编号` = T3.`编号` WHERE T2.`颜色` = '蓝色' AND T3.`颜色` = '棕色'	superhero
SELECT T2.`出版商名称` FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号` WHERE T1.`超级英雄名称` IN ('Hawkman', 'Karate Kid', 'Speedy')	superhero
SELECT CAST(COUNT(CASE WHEN T2.`颜色` = '蓝色' THEN 1 ELSE NULL END) AS REAL) * 100 / COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号`	superhero
SELECT CAST(COUNT(CASE WHEN T2.`性别` = '男性' THEN T1.`编号` ELSE NULL END) AS REAL) / COUNT(CASE WHEN T2.`性别` = '女性' THEN T1.`编号` ELSE NULL END) FROM `超级英雄` AS T1 INNER JOIN `性别` AS T2 ON T1.`性别编号` = T2.`编号`	superhero
SELECT T2.`颜色` FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T1.`全名` = 'Karen Beecher-Duncan'	superhero
SELECT SUM(CASE WHEN T2.`编号` = 7 THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.`编号` = 1 THEN 1 ELSE 0 END) FROM `超级英雄` AS T1 INNER JOIN `颜色` AS T2 ON T1.`瞳色编号` = T2.`编号` WHERE T1.`体重（千克）` = 0 OR T1.`体重（千克）` is NULL	superhero
SELECT COUNT(T1.`编号`) FROM `超级英雄` AS T1 INNER JOIN `阵营` AS T2 ON T1.`阵营编号` = T2.`编号` INNER JOIN `颜色` AS T3 ON T1.`肤色编号` = T3.`编号` WHERE T2.`阵营` = '邪恶' AND T3.`颜色` = '绿色'	superhero
SELECT T1.`超级英雄名称` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` WHERE T3.`能力名称` = 'Wind Control' ORDER BY T1.`超级英雄名称`	superhero
SELECT T4.`性别` FROM `超级英雄` AS T1 INNER JOIN `英雄能力` AS T2 ON T1.`编号` = T2.`英雄编号` INNER JOIN `超能力` AS T3 ON T2.`能力编号` = T3.`编号` INNER JOIN `性别` AS T4 ON T1.`性别编号` = T4.`编号` WHERE T3.`能力名称` = 'Phoenix Force'	superhero
SELECT SUM(CASE WHEN T2.`出版商名称` = 'DC Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.`出版商名称` = 'Marvel Comics' THEN 1 ELSE 0 END) FROM `超级英雄` AS T1 INNER JOIN `出版商` AS T2 ON T1.`出版商编号` = T2.`编号`	superhero
SELECT `显示名称` FROM `用户` WHERE `显示名称` IN ('Harlan', 'Jarrod Dixon') AND `声望值` = ( SELECT MAX(`声望值`) FROM `用户` WHERE `显示名称` IN ('Harlan', 'Jarrod Dixon') )	codebase_community
SELECT `显示名称` FROM `用户` WHERE STRFTIME('%Y', `创建日期`) = '2011'	codebase_community
SELECT COUNT(`编号`) FROM `用户` WHERE date(`最后访问日期`) > '2014-09-01'	codebase_community
SELECT T2.`显示名称` FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T1.`标题` = 'Eliciting priors from experts'	codebase_community
SELECT COUNT(T1.`编号`) FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T2.`显示名称` = 'csgillespie'	codebase_community
SELECT T2.`显示名称` FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`最后编辑者用户编号` = T2.`编号` WHERE T1.`标题` = 'Examples for teaching: Correlation does not mean causation'	codebase_community
SELECT COUNT(T1.`编号`) FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T1.`评分` >= 20 AND T2.`年龄` > 65	codebase_community
SELECT T2.`正文` FROM `标签` AS T1 INNER JOIN `帖子` AS T2 ON T2.`编号` = T1.`摘要帖子编号` WHERE T1.`标签名称` = 'bayesian'	codebase_community
SELECT AVG(T1.`评分`) FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T2.`显示名称` = 'csgillespie'	codebase_community
SELECT CAST(SUM(IIF(T2.`年龄` > 65, 1, 0)) AS REAL) * 100 / COUNT(T1.`编号`) FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T1.`评分` > 5	codebase_community
SELECT T1.`收藏数` FROM `帖子` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`帖子编号` WHERE T2.`创建日期` = '2014-04-23 20:29:39.0' AND T2.`用户编号` = 3025	codebase_community
SELECT IIF(T2.`关闭日期` IS NULL, 'NOT well-finished', 'well-finished') AS resylt FROM `评论` AS T1 INNER JOIN `帖子` AS T2 ON T1.`帖子编号` = T2.`编号` WHERE T1.`用户编号` = 23853 AND T1.`创建日期` = '2013-07-12 09:08:18.0'	codebase_community
SELECT COUNT(T1.`编号`) FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`显示名称` = 'Tiago Pasqualini'	codebase_community
SELECT T1.`显示名称` FROM `用户` AS T1 INNER JOIN `投票` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T2.`编号` = 6347	codebase_community
SELECT CAST(COUNT(DISTINCT T2.`编号`) AS REAL) / COUNT(DISTINCT T1.`编号`) FROM `投票` AS T1 INNER JOIN `帖子` AS T2 ON T1.`用户编号` = T2.`所有者用户编号` WHERE T1.`用户编号` = 24	codebase_community
SELECT `浏览次数` FROM `帖子` WHERE `标题` = 'Integration of Weka and/or RapidMiner into Informatica PowerCenter/Developer'	codebase_community
SELECT `内容` FROM `评论` WHERE `评分` = 17	codebase_community
SELECT T1.`显示名称` FROM `用户` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T2.`内容` = 'thank you user93!'	codebase_community
SELECT T1.`显示名称`, T1.`声望值` FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T2.`标题` = 'Understanding what Dassault iSight is doing?'	codebase_community
SELECT T2.`显示名称` FROM `帖子` AS T1 INNER JOIN `用户` AS T2 ON T1.`所有者用户编号` = T2.`编号` WHERE T1.`标题` = 'Open source tools for visualizing multi-dimensional data?'	codebase_community
SELECT T2.`评论` FROM `帖子` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`帖子编号` WHERE T1.`标题` = 'Why square the difference instead of taking the absolute value in standard deviation?'	codebase_community
SELECT T3.`显示名称`, T1.`标题` FROM `帖子` AS T1 INNER JOIN `投票` AS T2 ON T1.`编号` = T2.`帖子编号` INNER JOIN `用户` AS T3 ON T3.`编号` = T2.`用户编号` WHERE T2.`赏金金额` = 50 AND T1.`标题` LIKE '%variance%'	codebase_community
SELECT AVG(T2.`浏览次数`), T2.`标题`, T1.`内容` FROM `评论` AS T1 INNER JOIN `帖子` AS T2 ON T2.`编号` = T1.`帖子编号`  WHERE T2.`标签` = '<humor>' GROUP BY T2.`标题`, T1.`内容`	codebase_community
SELECT COUNT(`用户编号`) FROM ( SELECT `用户编号`, COUNT(`徽章名称`) AS num FROM `徽章` GROUP BY `用户编号` ) T WHERE T.num > 5	codebase_community
SELECT T2.`用户编号` FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T2.`帖子编号` = T3.`编号` WHERE T3.`浏览次数` >= 1000 GROUP BY T2.`用户编号` HAVING COUNT(DISTINCT T2.`帖子历史类型编号`) = 1	codebase_community
SELECT CAST(SUM(IIF(STRFTIME('%Y', `授予日期`) = '2010', 1, 0)) AS REAL) * 100 / COUNT(`编号`) - CAST(SUM(IIF(STRFTIME('%Y', `授予日期`) = '2011', 1, 0)) AS REAL) * 100 / COUNT(`编号`) FROM `徽章` WHERE `徽章名称` = 'Student'	codebase_community
SELECT AVG(T1.`赞成票数`), AVG(T1.`年龄`) FROM `用户` AS T1 INNER JOIN ( SELECT `所有者用户编号`, COUNT(*) AS post_count FROM `帖子` GROUP BY `所有者用户编号` HAVING post_count > 10) AS T2 ON T1.`编号` = T2.`所有者用户编号`	codebase_community
SELECT CAST(SUM(IIF(STRFTIME('%Y', `创建日期`) = '2010', 1, 0)) AS REAL) / SUM(IIF(STRFTIME('%Y', `创建日期`) = '2011', 1, 0)) FROM `投票`	codebase_community
SELECT T2.`帖子编号` FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T2.`帖子编号` = T3.`编号` WHERE T1.`显示名称` = 'slashnick' ORDER BY T3.`回答数` DESC LIMIT 1	codebase_community
SELECT T1.`显示名称` FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T2.`帖子编号` = T3.`编号` WHERE T1.`显示名称` = 'Harvey Motulsky' OR T1.`显示名称` = 'Noah Snyder' GROUP BY T1.`显示名称` ORDER BY SUM(T3.`浏览次数`) DESC LIMIT 1	codebase_community
SELECT T3.`标签` FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T3.`编号` = T2.`帖子编号` WHERE T1.`显示名称` = 'Mark Meckes' AND T3.`评论数` = 0	codebase_community
SELECT CAST(SUM(IIF(T3.`标签名称` = 'r', 1, 0)) AS REAL) * 100 / COUNT(T1.`编号`) FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `标签` AS T3 ON T3.`摘要帖子编号` = T2.`帖子编号` WHERE T1.`显示名称` = 'Community'	codebase_community
SELECT SUM(IIF(T1.`显示名称` = 'Mornington', T3.`浏览次数`, 0)) - SUM(IIF(T1.`显示名称` = 'Amos', T3.`浏览次数`, 0)) AS diff FROM `用户` AS T1 INNER JOIN `帖子历史` AS T2 ON T1.`编号` = T2.`用户编号` INNER JOIN `帖子` AS T3 ON T3.`编号` = T2.`帖子编号`	codebase_community
SELECT CAST(COUNT(T1.`编号`) AS REAL) / 12 FROM `帖子链接` AS T1 INNER JOIN `帖子` AS T2 ON T1.`帖子编号` = T2.`编号` WHERE T2.`回答数` <= 2 AND STRFTIME('%Y', T1.`创建日期`) = '2010'	codebase_community
SELECT T2.`创建日期` FROM `用户` AS T1 INNER JOIN `投票` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T1.`显示名称` = 'chl' ORDER BY T2.`创建日期` LIMIT 1	codebase_community
SELECT T1.`显示名称` FROM `用户` AS T1 INNER JOIN `徽章` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T2.`徽章名称` = 'Autobiographer' ORDER BY T2.`授予日期` LIMIT 1	codebase_community
SELECT COUNT(T1.`编号`) FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`所在地` = 'United Kingdom' AND T2.`收藏数` >= 4	codebase_community
SELECT T2.`编号`, T2.`标题` FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`显示名称` = 'Harvey Motulsky' ORDER BY T2.`浏览次数` DESC LIMIT 1	codebase_community
SELECT T2.`所有者用户编号`, T1.`显示名称` FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` WHERE STRFTIME('%Y', T1.`创建日期`) = '2010' ORDER BY T2.`收藏数` DESC LIMIT 1	codebase_community
SELECT CAST(SUM(IIF(STRFTIME('%Y', T2.`创建日期`) = '2011' AND T1.`声望值` > 1000, 1, 0)) AS REAL) * 100 / COUNT(T1.`编号`) FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号`	codebase_community
SELECT T2.`浏览次数`, T3.`显示名称` FROM `帖子历史` AS T1 INNER JOIN `帖子` AS T2 ON T1.`帖子编号` = T2.`编号` INNER JOIN `用户` AS T3 ON T2.`最后编辑者用户编号` = T3.`编号` WHERE T1.`内容` = 'Computer Game Datasets'	codebase_community
SELECT COUNT(T2.`编号`) FROM `帖子` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`帖子编号` GROUP BY T1.`编号` ORDER BY T1.`评分` DESC LIMIT 1	codebase_community
SELECT T3.`内容`, T1.`显示名称` FROM `用户` AS T1 INNER JOIN `帖子` AS T2 ON T1.`编号` = T2.`所有者用户编号` INNER JOIN `评论` AS T3 ON T2.`编号` = T3.`帖子编号` WHERE T2.`标题` = 'Analysing wind data with R' ORDER BY T1.`创建日期` DESC LIMIT 10	codebase_community
SELECT CAST(SUM(CASE WHEN T2.`评分` > 50 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.`编号`) FROM `用户` T1 INNER JOIN `帖子` T2 ON T1.`编号` = T2.`所有者用户编号` WHERE T1.`声望值` = (SELECT MAX(`声望值`) FROM `用户`)	codebase_community
SELECT `摘要帖子编号`, `维基帖子编号` FROM `标签` WHERE `标签名称` = 'sample'	codebase_community
SELECT T2.`声望值`, T2.`赞成票数` FROM `评论` AS T1 INNER JOIN `用户` AS T2 ON T1.`用户编号` = T2.`编号` WHERE T1.`内容` = 'fine, you win :)'	codebase_community
SELECT `内容` FROM `评论` WHERE `帖子编号` IN ( SELECT `编号` FROM `帖子` WHERE `浏览次数` BETWEEN 100 AND 150 ) ORDER BY `评分` DESC LIMIT 1	codebase_community
SELECT COUNT(T1.`编号`) FROM `评论` AS T1 INNER JOIN `帖子` AS T2 ON T1.`帖子编号` = T2.`编号` WHERE T2.`评论数` = 1 AND T2.`评分` = 0	codebase_community
SELECT CAST(SUM(IIF(T1.`赞成票数` = 0, 1, 0)) AS REAL) * 100/ COUNT(T1.`编号`) AS per FROM `用户` AS T1 INNER JOIN `评论` AS T2 ON T1.`编号` = T2.`用户编号` WHERE T2.`评分` BETWEEN 5 AND 10	codebase_community
SELECT id FROM `卡牌` WHERE `CardKingdom闪卡编号` IS NOT NULL AND `CardKingdom编号` IS NOT NULL	card_games
SELECT id FROM `卡牌` WHERE `边框颜色` = '无边框' AND (`CardKingdom编号` IS NULL OR `CardKingdom编号` IS NULL)	card_games
SELECT DISTINCT T1.id FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T2.`赛制` = '角斗士赛制' AND T2.`状态` = '禁用' AND T1.`稀有度` = '神话'	card_games
SELECT DISTINCT T2.`状态` FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T1.`类别` = 'Artifact' AND T2.`赛制` = '经典赛制' AND T1.`面` IS NULL	card_games
SELECT T1.id, T1.`画师` FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T2.`状态` = '合法' AND T2.`赛制` = '指挥官赛制' AND (T1.`力量` IS NULL OR T1.`力量` = '*')	card_games
SELECT T1.id, T2.`描述`, T1.`是否含内容警告` FROM `卡牌` AS T1 INNER JOIN `规则说明` AS T2 ON T1.UUID = T2.UUID WHERE T1.`画师` = 'Stephen Daniele'	card_games
SELECT T1.`名称`, T1.`画师`, T1.`是否为促销卡` FROM `卡牌` AS T1 INNER JOIN `规则说明` AS T2 ON T1.UUID = T2.UUID WHERE T1.`是否为促销卡` = 1 AND T1.`画师` = (SELECT `画师` FROM `卡牌` WHERE `是否为促销卡` = 1 GROUP BY `画师` HAVING COUNT(DISTINCT UUID) = (SELECT MAX(count_uuid) FROM ( SELECT COUNT(DISTINCT UUID) AS count_uuid FROM `卡牌` WHERE `是否为促销卡` = 1 GROUP BY `画师` ))) LIMIT 1	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '简体中文' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID	card_games
SELECT COUNT(*) FROM `卡牌` WHERE `力量` = '*'	card_games
SELECT DISTINCT `边框颜色` FROM `卡牌` WHERE `名称` = 'Ancestor''s Chosen'	card_games
SELECT T2.`赛制` FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T1.`名称` = 'Benalish Knight'	card_games
SELECT CAST(SUM(CASE WHEN `边框颜色` = '无边框' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM `卡牌`	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '法语' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T1.`是否为故事聚焦卡` = 1	card_games
SELECT COUNT(id) FROM `卡牌` WHERE `原始类别` = 'Summon - Angel' AND `子类型` != 'Angel'	card_games
SELECT id FROM `卡牌` WHERE `对决套牌` = 'a'	card_games
SELECT COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T2.`状态` = '禁用' AND T1.`边框颜色` = '白色'	card_games
SELECT DISTINCT T1.`名称` FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T1.`原始类别` = 'Artifact' AND T1.`颜色` = '黑'	card_games
SELECT `法术力费用` FROM `卡牌` WHERE `可获取性` = 'MTGO与实体卡牌' AND `边框颜色` = '黑色' AND `边框版本` = 2003 AND `布局` = '普通'	card_games
SELECT CAST(SUM(CASE WHEN `是否为无文字卡` = 0 AND  `是否为故事聚焦卡` = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM `卡牌`	card_games
SELECT COUNT(T1.`编号`) FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T1.`代码` = T2.`系列代码` WHERE T2.`语言` = '葡萄牙语（巴西）' AND T1.`区块` = '指挥官'	card_games
SELECT T1.`子类型`, T1.`超类型` FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T2.`语言` = '德语' AND T1.`子类型` IS NOT NULL AND T1.`超类型` IS NOT NULL	card_games
SELECT Count(DISTINCT T1.id) FROM `卡牌` AS T1 INNER JOIN `规则说明` AS T2 ON T1.UUID = T2.UUID WHERE (T1.`力量` IS NULL OR T1.`力量` = '*') AND T2.`描述` LIKE '%triggered ability%'	card_games
SELECT COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID INNER JOIN `规则说明` AS T3 ON T1.UUID = T3.UUID WHERE T2.`赛制` = '前现代赛制' AND T3.`描述` = 'This is a triggered mana ability.' AND T1.`面` IS NULL	card_games
SELECT `名称` FROM `外文数据` WHERE UUID IN ( SELECT UUID FROM `卡牌` WHERE `类型` = 'Creature' AND `布局` = '普通' AND `边框颜色` = '黑色' AND `画师` = 'Matthew D. Wilson' ) AND `语言` = '法语'	card_games
SELECT T2.`语言` FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T1.`代码` = T2.`系列代码` WHERE T1.`区块` = '拉尼卡' AND T1.`基础系列大小` = 180	card_games
SELECT CAST(SUM(CASE WHEN T1.`是否含内容警告` = 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T2.`赛制` = '指挥官赛制' AND T2.`状态` = '合法'	card_games
SELECT CAST(SUM(CASE WHEN T2.`语言` = '法语' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T1.UUID = T2.UUID WHERE T1.`力量` IS NULL OR T1.`力量` = '*'	card_games
SELECT `语言` FROM `外文数据` WHERE `万智牌宇宙编号` = 149934	card_games
SELECT CAST(SUM(CASE WHEN `是否为无文字卡` = 1 AND `布局` = '普通' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM `卡牌`	card_games
SELECT T2.`语言` FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T1.`代码` = T2.`系列代码` WHERE T1.`MCM名称` = 'Archenemy' AND T2.`系列代码` = 'ARC'	card_games
SELECT DISTINCT `语言` FROM `外文数据` WHERE `名称` = 'A Pedra Fellwar'	card_games
SELECT `名称` FROM `卡牌` WHERE `名称` IN ('Serra Angel', 'Shrine Keeper') ORDER BY `法术力费用总值` DESC LIMIT 1	card_games
SELECT `翻译` FROM `系列翻译` WHERE `系列代码` IN ( SELECT `系列代码` FROM `卡牌` WHERE `名称` = 'Ancestor''s Chosen' ) AND `语言` = '意大利语'	card_games
SELECT IIF(SUM(CASE WHEN T2.`语言` = '韩语' AND T2.`翻译` IS NOT NULL THEN 1 ELSE 0 END) > 0, 'YES', 'NO') FROM `卡牌` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`系列代码` WHERE T1.`名称` = 'Ancestor''s Chosen'	card_games
SELECT COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`系列代码` WHERE T2.`翻译` = 'Hauptset Zehnte Edition' AND T1.`画师` = 'Adam Rex'	card_games
SELECT T2.`翻译` FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`代码` WHERE T1.`名称` = 'Eighth Edition' AND T2.`语言` = '简体中文'	card_games
SELECT IIF(T2.`MTGO代码` IS NOT NULL, 'YES', 'NO') FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE T1.`名称` = 'Angel of Mercy'	card_games
SELECT COUNT(DISTINCT T1.`编号`) FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`代码` WHERE T1.`区块` = '冰封时代' AND T2.`语言` = '意大利语' AND T2.`翻译` IS NOT NULL	card_games
SELECT IIF(`是否仅含外文版` = 1, 'YES', 'NO') FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE T1.`名称` = 'Adarkar Valkyrie'	card_games
SELECT COUNT(T1.`编号`) FROM `系列` AS T1 INNER JOIN `系列翻译` AS T2 ON T2.`系列代码` = T1.`代码` WHERE T2.`翻译` IS NOT NULL AND T1.`基础系列大小` < 100 AND T2.`语言` = '意大利语'	card_games
SELECT T1.`画师` FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE (T2.`名称` = 'Coldsnap' AND T1.`画师` = 'Chippy') OR (T2.`名称` = 'Coldsnap' AND T1.`画师` = 'Aaron Miller') OR (T2.`名称` = 'Coldsnap' AND T1.`画师` = 'Jeremy Jarvis') GROUP BY T1.`画师`	card_games
SELECT SUM(CASE WHEN T1.`力量` = '*' OR T1.`力量` IS NULL THEN 1 ELSE 0 END) FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE T2.`名称` = 'Coldsnap' AND T1.`法术力费用总值` > 5	card_games
SELECT T2.`风味描述` FROM `卡牌` AS T1 INNER JOIN `外文数据` AS T2 ON T2.UUID = T1.UUID WHERE T1.`名称` = 'Ancestor''s Chosen' AND T2.`语言` = '意大利语'	card_games
SELECT DISTINCT T1.`描述` FROM `外文数据` AS T1 INNER JOIN `卡牌` AS T2 ON T2.UUID = T1.UUID INNER JOIN `系列` AS T3 ON T3.`代码` = T2.`系列代码` WHERE T3.`名称` = 'Coldsnap' AND T1.`语言` = '意大利语'	card_games
SELECT T2.`名称` FROM `外文数据` AS T1 INNER JOIN `卡牌` AS T2 ON T2.UUID = T1.UUID INNER JOIN `系列` AS T3 ON T3.`代码` = T2.`系列代码` WHERE T3.`名称` = 'Coldsnap' AND T1.`语言` = '意大利语' ORDER BY T2.`法术力费用总值` DESC	card_games
SELECT CAST(SUM(CASE WHEN T1.`法术力费用总值` = 7 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE T2.`名称` = 'Coldsnap'	card_games
SELECT CAST(SUM(CASE WHEN T1.`CardKingdom闪卡编号` IS NOT NULL AND T1.`CardKingdom编号` IS NOT NULL THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.id) FROM `卡牌` AS T1 INNER JOIN `系列` AS T2 ON T2.`代码` = T1.`系列代码` WHERE T2.`名称` = 'Coldsnap'	card_games
SELECT T2.`赛制`, T1.`名称` FROM `合法性` AS T2 INNER JOIN `卡牌` AS T1 ON T2.UUID = T1.UUID WHERE T2.`状态` = '禁用' AND T2.`赛制` = (SELECT `赛制` FROM `合法性` WHERE `状态` = '禁用' GROUP BY `赛制` ORDER BY COUNT(*) DESC, MIN(UUID) ASC LIMIT 1)	card_games
SELECT T1.`名称`, T2.`赛制` FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T2.UUID = T1.UUID WHERE T1.`EDHREC排名` = 1 AND T2.`状态` = '禁用' GROUP BY T1.`名称`, T2.`赛制`	card_games
SELECT DISTINCT T2.`名称` , CASE WHEN T1.`状态` = '合法' THEN T1.`赛制` ELSE NULL END FROM `合法性` AS T1 INNER JOIN `卡牌` AS T2 ON T2.UUID = T1.UUID WHERE T2.`系列代码` IN ( SELECT `代码` FROM `系列` WHERE `名称` = 'Hour of Devastation' )	card_games
SELECT `名称` FROM `系列` WHERE `代码` IN ( SELECT `系列代码` FROM `系列翻译` WHERE `语言` = '韩语' AND `语言` NOT LIKE '%Japanese%' )	card_games
SELECT DISTINCT T1.`边框版本`, T1.`名称` , IIF(T2.`状态` = '禁用', T1.`名称`, 'NO') FROM `卡牌` AS T1 INNER JOIN `合法性` AS T2 ON T1.UUID = T2.UUID WHERE T1.`画师` = 'Allen Williams'	card_games
SELECT T.`键类型` FROM ( SELECT `键类型`, COUNT(`化学键编号`) FROM `化学键` GROUP BY `键类型` ORDER BY COUNT(`化学键编号`) DESC LIMIT 1 ) AS T	toxicology
SELECT AVG(oxygen_count) FROM (SELECT T1.`分子编号`, COUNT(T1.`元素`) AS oxygen_count FROM `原子` AS T1 INNER JOIN `化学键` AS T2 ON T1.`分子编号` = T2.`分子编号`  WHERE T2.`键类型` = '-' AND T1.`元素` = '氧'  GROUP BY T1.`分子编号`) AS oxygen_counts	toxicology
SELECT AVG(single_bond_count) FROM (SELECT T3.`分子编号`, COUNT(T1.`键类型`) AS single_bond_count FROM `化学键` AS T1  INNER JOIN `原子` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `分子` AS T3 ON T3.`分子编号` = T2.`分子编号` WHERE T1.`键类型` = '-' AND T3.`标签` = '+' GROUP BY T3.`分子编号`) AS subquery	toxicology
SELECT DISTINCT T2.`分子编号` FROM `化学键` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T1.`键类型` = '#' AND T2.`标签` = '+'	toxicology
SELECT CAST(COUNT(DISTINCT CASE WHEN T1.`元素` = '碳' THEN T1.`原子编号` ELSE NULL END) AS REAL) * 100 / COUNT(DISTINCT T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `化学键` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`键类型` = '='	toxicology
SELECT DISTINCT T1.`元素` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T2.`化学键编号` = 'TR004_8_9'	toxicology
SELECT DISTINCT T1.`元素` FROM `原子` AS T1 INNER JOIN `化学键` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `连接关系` AS T3 ON T1.`原子编号` = T3.`原子编号` WHERE T2.`键类型` = '='	toxicology
SELECT T.`标签` FROM ( SELECT T2.`标签`, COUNT(T2.`分子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T1.`元素` = '氢' GROUP BY T2.`标签` ORDER BY COUNT(T2.`分子编号`) DESC LIMIT 1 ) t	toxicology
SELECT T.`元素` FROM (SELECT T1.`元素`, COUNT(DISTINCT T1.`分子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`标签` = '-' GROUP BY T1.`元素` ORDER BY COUNT(DISTINCT T1.`分子编号`) ASC, MIN(T1.`原子编号`) ASC LIMIT 1) t	toxicology
SELECT T1.`键类型` FROM `化学键` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`化学键编号` = T2.`化学键编号` WHERE T2.`原子编号` = 'TR004_8' AND T2.`另一原子编号` = 'TR004_20' OR T2.`另一原子编号` = 'TR004_8' AND T2.`原子编号` = 'TR004_20'	toxicology
SELECT COUNT(DISTINCT CASE WHEN T1.`元素` = '碘' THEN T1.`原子编号` ELSE NULL END) AS iodine_nums , COUNT(DISTINCT CASE WHEN T1.`元素` = '硫' THEN T1.`原子编号` ELSE NULL END) AS sulfur_nums FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` INNER JOIN `化学键` AS T3 ON T2.`化学键编号` = T3.`化学键编号` WHERE T3.`键类型` = '-'	toxicology
SELECT CAST(COUNT(DISTINCT CASE WHEN T1.`元素` <> '氟' THEN T2.`分子编号` ELSE NULL END) AS REAL) * 100 / COUNT(DISTINCT T2.`分子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`标签` = '+'	toxicology
SELECT CAST(COUNT(DISTINCT CASE WHEN T2.`标签` = '+' THEN T2.`分子编号` ELSE NULL END) AS REAL) * 100 / COUNT(DISTINCT T2.`分子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `化学键` AS T3 ON T2.`分子编号` = T3.`分子编号` WHERE T3.`键类型` = '#'	toxicology
SELECT ROUND(CAST(COUNT(CASE WHEN T.`键类型` = '=' THEN T.`化学键编号` ELSE NULL END) AS REAL) * 100 / COUNT(T.`化学键编号`),5) FROM `化学键` AS T WHERE T.`分子编号` = 'TR008'	toxicology
SELECT ROUND(CAST(COUNT(CASE WHEN T.`标签` = '+' THEN T.`分子编号` ELSE NULL END) AS REAL) * 100 / COUNT(T.`分子编号`),3) FROM `分子` t	toxicology
SELECT ROUND(CAST(COUNT(CASE WHEN T.`元素` = '氢' THEN T.`原子编号` ELSE NULL END) AS REAL) * 100 / COUNT(T.`原子编号`),4) FROM `原子` AS T WHERE T.`分子编号` = 'TR206'	toxicology
SELECT DISTINCT T1.`元素`, T2.`标签` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`分子编号` = 'TR060'	toxicology
SELECT T.`键类型` FROM ( SELECT T1.`键类型`, COUNT(T1.`分子编号`) FROM `化学键` AS T1  WHERE T1.`分子编号` = 'TR010' GROUP BY T1.`键类型` ORDER BY COUNT(T1.`分子编号`) DESC LIMIT 1 ) AS T	toxicology
SELECT DISTINCT T2.`分子编号` FROM `化学键` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T1.`键类型` = '-' AND T2.`标签` = '-' ORDER BY T2.`分子编号` LIMIT 3	toxicology
SELECT COUNT(T2.`化学键编号`) FROM `化学键` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`化学键编号` = T2.`化学键编号` WHERE T1.`分子编号` = 'TR009' AND T2.`原子编号` = T1.`分子编号` || '_1' OR T2.`另一原子编号` = T1.`分子编号` || '_2'	toxicology
SELECT T1.`键类型`, T2.`原子编号`, T2.`另一原子编号` FROM `化学键` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`化学键编号` = T2.`化学键编号` WHERE T2.`化学键编号` = 'TR001_6_9'	toxicology
SELECT COUNT(T.`化学键编号`) FROM `连接关系` AS T WHERE SUBSTR(T.`原子编号`, -2) = '19'	toxicology
SELECT DISTINCT T.`元素` FROM `原子` AS T WHERE T.`分子编号` = 'TR004'	toxicology
SELECT DISTINCT T2.`分子编号` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE SUBSTR(T1.`原子编号`, -2) BETWEEN '21' AND '25' AND T2.`标签` = '+'	toxicology
SELECT T2.`化学键编号` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T2.`化学键编号` IN ( SELECT T3.`化学键编号` FROM `连接关系` AS T3 INNER JOIN `原子` AS T4 ON T3.`原子编号` = T4.`原子编号` WHERE T4.`元素` = '磷' ) AND T1.`元素` = '氮'	toxicology
SELECT T1.`标签` FROM `分子` AS T1 INNER JOIN ( SELECT T.`分子编号`, COUNT(T.`键类型`) FROM `化学键` AS T WHERE T.`键类型` = '=' GROUP BY T.`分子编号` ORDER BY COUNT(T.`键类型`) DESC LIMIT 1 ) AS T2 ON T1.`分子编号` = T2.`分子编号`	toxicology
SELECT CAST(COUNT(T2.`化学键编号`) AS REAL) / COUNT(T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T1.`元素` = '碘'	toxicology
SELECT DISTINCT T.`元素` FROM `原子` AS T WHERE T.`元素` NOT IN ( SELECT DISTINCT T1.`元素` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` )	toxicology
SELECT T2.`原子编号`, T2.`另一原子编号` FROM `原子` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`原子编号` = T2.`原子编号` INNER JOIN `化学键` AS T3 ON T2.`化学键编号` = T3.`化学键编号` WHERE T3.`键类型` = '#' AND T3.`分子编号` = 'TR041'	toxicology
SELECT T2.`元素` FROM `连接关系` AS T1 INNER JOIN `原子` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T1.`化学键编号` = 'TR144_8_19'	toxicology
SELECT DISTINCT T3.`元素` FROM `化学键` AS T1 INNER JOIN `连接关系` AS T2 ON T1.`化学键编号` = T2.`化学键编号` INNER JOIN `原子` AS T3 ON T2.`原子编号` = T3.`原子编号` WHERE T1.`键类型` = '#'	toxicology
SELECT ROUND(CAST(COUNT(CASE WHEN T2.`标签` = '+' THEN T1.`化学键编号` ELSE NULL END) AS REAL) * 100 / COUNT(T1.`化学键编号`),5) FROM `化学键` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T1.`键类型` = '-'	toxicology
SELECT COUNT(T1.`原子编号`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `化学键` AS T3 ON T2.`分子编号` = T3.`分子编号` WHERE T3.`键类型` = '#' AND T1.`元素` IN ('磷', '溴')	toxicology
SELECT CAST(COUNT(CASE WHEN T.`元素` = '氯' THEN T.`原子编号` ELSE NULL END) AS REAL) * 100 / COUNT(T.`原子编号`) FROM ( SELECT T1.`原子编号`, T1.`元素` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` INNER JOIN `化学键` AS T3 ON T2.`分子编号` = T3.`分子编号` WHERE T3.`键类型` = '-' ) AS T	toxicology
SELECT T2.`元素` FROM `连接关系` AS T1 INNER JOIN `原子` AS T2 ON T1.`原子编号` = T2.`原子编号` WHERE T1.`化学键编号` = 'TR001_10_11'	toxicology
SELECT CAST(COUNT( CASE WHEN T1.`元素` = '氯' THEN T1.`元素` ELSE NULL END) AS REAL) * 100 / COUNT(T1.`元素`) FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`标签` = '+'	toxicology
SELECT DISTINCT T1.`元素` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`标签` = '+' AND SUBSTR(T1.`原子编号`, -1) = '4' AND LENGTH(T1.`原子编号`) = 7	toxicology
WITH SubQuery AS (SELECT DISTINCT T1.`原子编号`, T1.`元素`, T1.`分子编号`, T2.`标签` FROM `原子` AS T1 INNER JOIN `分子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T2.`分子编号` = 'TR006') SELECT CAST(COUNT(CASE WHEN `元素` = '氢' THEN `原子编号` ELSE NULL END) AS REAL) / (CASE WHEN COUNT(`原子编号`) = 0 THEN NULL ELSE COUNT(`原子编号`) END) AS ratio, `标签` FROM SubQuery GROUP BY `标签`	toxicology
SELECT T.`分子编号` FROM ( SELECT T1.`分子编号`, COUNT(T2.`原子编号`) FROM `分子` AS T1 INNER JOIN `原子` AS T2 ON T1.`分子编号` = T2.`分子编号` WHERE T1.`标签` = '-' GROUP BY T1.`分子编号` HAVING COUNT(T2.`原子编号`) > 5 ) t	toxicology
SELECT COUNT(DISTINCT T2.`学校`) FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`虚拟学校（是/否）` = 'F' AND T1.`数学平均分` > 400	california_schools
SELECT T2.`CDS编号` FROM `学校` AS T1 INNER JOIN `免费及减价午餐计划` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`K-12年级注册人数` + T2.`5-17岁学生注册人数` > 500	california_schools
SELECT MAX(CAST(T1.`5-17岁学生免费餐食人数` AS REAL) / T1.`5-17岁学生注册人数`) FROM `免费及减价午餐计划` AS T1 INNER JOIN `SAT成绩` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE CAST(T2.`总分≥1500人数` AS REAL) / T2.`参考试人数` > 0.3	california_schools
SELECT `特许学校编号`, `写作平均分`, RANK() OVER (ORDER BY `写作平均分` DESC) AS WritingScoreRank FROM `学校` AS T1  INNER JOIN `SAT成绩` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`写作平均分` > 499 AND `特许学校编号` is not null	california_schools
SELECT T1.`学校`, T1.`街道` FROM `学校` AS T1 INNER JOIN `免费及减价午餐计划` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`K-12年级注册人数` - T2.`5-17岁学生注册人数` > 30	california_schools
SELECT T2.`学校名称` FROM `SAT成绩` AS T1 INNER JOIN `免费及减价午餐计划` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE CAST(T2.`K-12年级免费餐食人数` AS REAL) / T2.`K-12年级注册人数` > 0.1 AND T1.`总分≥1500人数` > 0	california_schools
SELECT T1.`学校名称`, T2.`特许资金类型` FROM `SAT成绩` AS T1 INNER JOIN `免费及减价午餐计划` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`学区名称` LIKE 'Riverside%' GROUP BY T1.`学校名称`, T2.`特许资金类型` HAVING CAST(SUM(T1.`数学平均分`) AS REAL) / COUNT(T1.`CDS编号`) > 400	california_schools
SELECT T1.`学校名称`, T2.`街道`, T2.`城市`, T2.`州`, T2.`邮政编码` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'Monterey' AND T1.`5-17岁学生免费餐食人数` > 800 AND T1.`学校类型` = '高中（公立）'	california_schools
SELECT T2.`学校`, T1.`写作平均分`, T2.`电话` FROM `学校` AS T2 LEFT JOIN `SAT成绩` AS T1 ON T2.`CDS编号` = T1.`CDS编号` WHERE strftime('%Y', T2.`开办日期`) > '1991' OR strftime('%Y', T2.`关闭日期`) < '2000'	california_schools
SELECT T2.`学校`, T2.`DOC代码` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`资金类型` = '地方资助' AND (T1.`K-12年级注册人数` - T1.`5-17岁学生注册人数`) > (SELECT AVG(T3.`K-12年级注册人数` - T3.`5-17岁学生注册人数`) FROM `免费及减价午餐计划` AS T3 INNER JOIN `学校` AS T4 ON T3.`CDS编号` = T4.`CDS编号` WHERE T4.`资金类型` = '地方资助')	california_schools
SELECT CAST(`K-12年级免费餐食人数` AS REAL) / `K-12年级注册人数` FROM `免费及减价午餐计划` ORDER BY `K-12年级注册人数` DESC LIMIT 9, 2	california_schools
SELECT CAST(T1.`K-12年级免费及减价餐食（FRPM）人数` AS REAL) / T1.`K-12年级注册人数` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`SOC代码` = 66 ORDER BY T1.`K-12年级免费及减价餐食（FRPM）人数` DESC LIMIT 5	california_schools
SELECT T2.`街道`, T2.`城市`, T2.`州`, T2.`邮政编码` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` ORDER BY CAST(T1.`总分≥1500人数` AS REAL) / T1.`参考试人数` ASC LIMIT 1	california_schools
SELECT T2.`管理员1名`, T2.`管理员1姓`, T2.`管理员2名`, T2.`管理员2姓`, T2.`管理员3名`, T2.`管理员3姓` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` ORDER BY T1.`总分≥1500人数` DESC LIMIT 1	california_schools
SELECT AVG(T1.`参考试人数`) FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE strftime('%Y', T2.`开办日期`) = '1980' AND T2.`县` = 'Fresno'	california_schools
SELECT T2.`电话` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`学区` = 'Fresno Unified' AND T1.`阅读平均分` IS NOT NULL ORDER BY T1.`阅读平均分` ASC LIMIT 1	california_schools
SELECT `学校` FROM (SELECT T2.`学校`,T1.`阅读平均分`, RANK() OVER (PARTITION BY T2.`县` ORDER BY T1.`阅读平均分` DESC) AS rnk FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`虚拟学校（是/否）` = 'F' ) ranked_schools WHERE rnk <= 5	california_schools
SELECT T2.`学校`, T1.`写作平均分` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`管理员1名` = 'Ricci' AND T2.`管理员1姓` = 'Ulrich'	california_schools
SELECT T2.`学校` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`DOC代码` = 31 ORDER BY T1.`K-12年级注册人数` DESC LIMIT 1	california_schools
SELECT CAST(COUNT(`学校`) AS REAL) / 12 FROM `学校` WHERE `DOC代码` = 52 AND `县` = 'Alameda' AND strftime('%Y', `开办日期`) = '1980'	california_schools
SELECT CAST(SUM(CASE WHEN `DOC代码` = 54 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN `DOC代码` = 52 THEN 1 ELSE 0 END) FROM `学校` WHERE `状态类型` = '已合并' AND `县` = 'Orange'	california_schools
SELECT T2.`通信地址街道`, T2.`学校` FROM `SAT成绩` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` ORDER BY T1.`数学平均分` DESC LIMIT 6, 1	california_schools
SELECT COUNT(T2.`学校`) FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'Los Angeles' AND T2.`特许学校（是/否）` = 0 AND CAST(T1.`K-12年级免费餐食人数` AS REAL) * 100 / T1.`K-12年级注册人数` < 0.18	california_schools
SELECT T1.`5-17岁学生注册人数` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`教育运营代码` = 'SSS' AND T2.`城市` = 'Fremont' AND T1.`学年` BETWEEN 2014 AND 2015	california_schools
SELECT T2.`学校`, T1.`5-17岁学生免费及减价餐食（FRPM）人数` * 100 / T1.`5-17岁学生注册人数` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'Los Angeles' AND T2.`服务年级范围` = '幼儿园至9年级'	california_schools
SELECT `县`, COUNT(`虚拟学校（是/否）`) FROM `学校` WHERE (`县` = 'San Diego' OR `县` = 'Santa Barbara') AND `虚拟学校（是/否）` = 'F' GROUP BY `县` ORDER BY COUNT(`虚拟学校（是/否）`) DESC LIMIT 1	california_schools
SELECT `提供年级范围` FROM `学校` ORDER BY ABS(`经度`) DESC LIMIT 1	california_schools
SELECT T2.`城市`, COUNT(T2.`CDS编号`) FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`磁石学校（是/否）` = 1 AND T2.`提供年级范围` = '幼儿园至8年级' AND T1.`国家学校午餐计划（NSLP）供餐资格状态` = '多种供应条款类型' GROUP BY T2.`城市`	california_schools
SELECT T1.`K-12年级免费餐食人数` * 100 / T1.`K-12年级注册人数`, T1.`学区编号` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`管理员1名` = 'Alusine'	california_schools
SELECT T2.`管理员1邮箱`, T2.`管理员2邮箱` FROM `免费及减价午餐计划` AS T1 INNER JOIN `学校` AS T2 ON T1.`CDS编号` = T2.`CDS编号` WHERE T2.`县` = 'San Bernardino' AND T2.`城市` = 'San Bernardino' AND T2.`DOC代码` = 54 AND strftime('%Y', T2.`开办日期`) BETWEEN '2009' AND '2010' AND T2.`SOC代码` = 62	california_schools
SELECT COUNT(T2.`账户编号`) FROM `行政区` AS T1 INNER JOIN `账户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.A3 = '东波希米亚' AND T2.`交易频率` = '按交易额扣款'	financial
SELECT COUNT(DISTINCT T2.`行政区编号`)  FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`性别` = 'F' AND T2.A11 BETWEEN 6000 AND 10000	financial
SELECT COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`性别` = 'M' AND T2.A3 = '北波希米亚' AND T2.A11 > 8000	financial
SELECT T1.`账户编号` , ( SELECT MAX(A11) - MIN(A11) FROM `行政区` ) FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` INNER JOIN `授权关系` AS T3 ON T1.`账户编号` = T3.`账户编号` INNER JOIN `客户` AS T4 ON T3.`客户编号` = T4.`客户编号` WHERE T2.`行政区编号` = ( SELECT `行政区编号` FROM `客户` WHERE `性别` = 'F' ORDER BY `出生日期` ASC LIMIT 1 ) ORDER BY T2.A11 DESC LIMIT 1	financial
SELECT T1.`账户编号`  FROM `账户` AS T1 INNER JOIN `授权关系` AS T2 ON T1.`账户编号` = T2.`账户编号` INNER JOIN `客户` AS T3 ON T2.`客户编号` = T3.`客户编号` INNER JOIN `行政区` AS T4 on T4.`行政区编号` = T1.`行政区编号` WHERE T2.`客户编号` = ( SELECT `客户编号` FROM `客户` ORDER BY `出生日期` DESC LIMIT 1) GROUP BY T4.A11, T1.`账户编号`	financial
SELECT T2.`账户编号` FROM `贷款` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE STRFTIME('%Y', T1.`申请日期`) = '1997' AND T2.`交易频率` = '每周扣款' ORDER BY T1.`贷款金额` LIMIT 1	financial
SELECT T1.`账户编号` FROM `贷款` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE STRFTIME('%Y', T2.`开户日期`) = '1993' AND T1.`贷款期限（月）` > 12 ORDER BY T1.`贷款金额` DESC LIMIT 1	financial
SELECT COUNT(T2.`客户编号`) FROM `行政区` AS T1 INNER JOIN `客户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.`性别` = 'F' AND STRFTIME('%Y', T2.`出生日期`) < '1950' AND T1.A2 = '索科洛夫'	financial
SELECT T1.A2 FROM `行政区` AS T1 INNER JOIN `客户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.`出生日期` = '1976-01-29' AND T2.`性别` = 'F'	financial
SELECT CAST(SUM(T1.`性别` = 'M') AS REAL) * 100 / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.A3 = '南波希米亚' GROUP BY T2.A4 ORDER BY T2.A4 DESC LIMIT 1	financial
SELECT CAST((SUM(IIF(T3.`交易日期` = '1998-12-27', T3.`交易后余额`, 0)) - SUM(IIF(T3.`交易日期` = '1993-03-22', T3.`交易后余额`, 0))) AS REAL) * 100 / SUM(IIF(T3.`交易日期` = '1993-03-22', T3.`交易后余额`, 0)) FROM `贷款` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` INNER JOIN `交易` AS T3 ON T3.`账户编号` = T2.`账户编号` WHERE T1.`申请日期` = '1993-07-05'	financial
SELECT (CAST(SUM(CASE WHEN `贷款状态` = 'A' THEN `贷款金额` ELSE 0 END) AS REAL) * 100) / SUM(`贷款金额`) FROM `贷款`	financial
SELECT CAST(SUM(`贷款状态` = 'C') AS REAL) * 100 / COUNT(`账户编号`) FROM `贷款` WHERE `贷款金额` < 100000	financial
SELECT CAST((T3.A13 - T3.A12) AS REAL) * 100 / T3.A12 FROM `贷款` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` INNER JOIN `行政区` AS T3 ON T2.`行政区编号` = T3.`行政区编号` WHERE T1.`贷款状态` = 'D'	financial
SELECT T2.A2, COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`性别` = 'F' GROUP BY T2.`行政区编号`, T2.A2 ORDER BY COUNT(T1.`客户编号`) DESC LIMIT 9	financial
SELECT COUNT(T1.`账户编号`) FROM `账户` AS T1 INNER JOIN `贷款` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE T2.`申请日期` BETWEEN '1995-01-01' AND '1997-12-31' AND T1.`交易频率` = '每月扣款' AND T2.`贷款金额` >= 250000	financial
SELECT COUNT(T1.`账户编号`) FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` INNER JOIN `贷款` AS T3 ON T1.`账户编号` = T3.`账户编号` WHERE T1.`行政区编号` = 1 AND (T3.`贷款状态` = 'C' OR T3.`贷款状态` = 'D')	financial
SELECT COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`性别` = 'M' AND T2.A15 = (SELECT T3.A15 FROM `行政区` AS T3 ORDER BY T3.A15 DESC LIMIT 1, 1)	financial
SELECT T1.`账户编号` FROM `交易` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE STRFTIME('%Y', T1.`交易日期`) = '1998' AND T1.`交易操作` = '银行卡取款' AND T1.`交易金额` < (SELECT AVG(`交易金额`) FROM `交易` WHERE STRFTIME('%Y', `交易日期`) = '1998')	financial
SELECT T3.`授权类型` FROM `行政区` AS T1 INNER JOIN `账户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` INNER JOIN `授权关系` AS T3 ON T2.`账户编号` = T3.`账户编号` WHERE T3.`授权类型` != '所有人' AND T1.A11 BETWEEN 8000 AND 9000	financial
SELECT AVG(T1.A15) FROM `行政区` AS T1 INNER JOIN `账户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE STRFTIME('%Y', T2.`开户日期`) >= '1997' AND T1.A15 > 4000	financial
SELECT T4.`交易编号` FROM `客户` AS T1 INNER JOIN `授权关系` AS T2 ON T1.`客户编号` = T2.`客户编号` INNER JOIN `账户` AS T3 ON T2.`账户编号` = T3.`账户编号` INNER JOIN `交易` AS T4 ON T3.`账户编号` = T4.`账户编号` WHERE T1.`客户编号` = 3356 AND T4.`交易操作` = '取款'	financial
SELECT CAST(SUM(T2.`性别` = 'F') AS REAL) * 100 / COUNT(T2.`客户编号`) FROM `行政区` AS T1 INNER JOIN `客户` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.A11 > 10000	financial
SELECT CAST((SUM(CASE WHEN STRFTIME('%Y', T1.`申请日期`) = '1997' THEN T1.`贷款金额` ELSE 0 END) - SUM(CASE WHEN STRFTIME('%Y', T1.`申请日期`) = '1996' THEN T1.`贷款金额` ELSE 0 END)) AS REAL) * 100 / SUM(CASE WHEN STRFTIME('%Y', T1.`申请日期`) = '1996' THEN T1.`贷款金额` ELSE 0 END) FROM `贷款` AS T1 INNER JOIN `账户` AS T2 ON T1.`账户编号` = T2.`账户编号` INNER JOIN `授权关系` AS T3 ON T3.`账户编号` = T2.`账户编号` INNER JOIN `客户` AS T4 ON T4.`客户编号` = T3.`客户编号` WHERE T4.`性别` = 'M' AND T3.`授权类型` = '所有人'	financial
SELECT T1.`交易频率`, T2.`交易备注` FROM `账户` AS T1 INNER JOIN (SELECT `账户编号`, `交易备注`, SUM(`转账金额`) AS total_amount FROM `转账指令` GROUP BY `账户编号`, `交易备注`) AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE T1.`账户编号` = 3 AND T2.total_amount = 3539	financial
SELECT CAST(SUM(T1.`性别` = 'M') AS REAL) * 100 / COUNT(T1.`客户编号`) FROM `客户` AS T1 INNER JOIN `行政区` AS T3 ON T1.`行政区编号` = T3.`行政区编号` INNER JOIN `账户` AS T2 ON T2.`行政区编号` = T3.`行政区编号` INNER JOIN `授权关系` as T4 on T1.`客户编号` = T4.`客户编号` AND T2.`账户编号` = T4.`账户编号` WHERE T2.`交易频率` = '每周扣款'	financial
SELECT T3.`账户编号` FROM `客户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` INNER JOIN `账户` AS T3 ON T2.`行政区编号` = T3.`行政区编号` INNER JOIN `授权关系` AS T4 ON T1.`客户编号` = T4.`客户编号` AND T4.`账户编号` = T3.`账户编号`  WHERE T1.`性别` = 'F' ORDER BY T1.`出生日期` ASC, T2.A11 ASC LIMIT 1	financial
SELECT AVG(T2.`贷款金额`) FROM `账户` AS T1 INNER JOIN `贷款` AS T2 ON T1.`账户编号` = T2.`账户编号` WHERE T2.`贷款状态` IN ('C', 'D') AND T1.`交易频率` = '按交易额扣款'	financial
SELECT T1.`客户编号`, STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', T3.`出生日期`) FROM `授权关系` AS T1 INNER JOIN `银行卡` AS T2 ON T2.`授权编号` = T1.`授权编号` INNER JOIN `客户` AS T3 ON T1.`客户编号` = T3.`客户编号` WHERE T2.`授权类型` = '金卡' AND T1.`授权类型` = '所有人'	financial
SELECT T1.`账户编号`, T2.A2, T2.A3 FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T1.`交易频率` = '按交易额扣款' AND STRFTIME('%Y', T1.`开户日期`)= '1993'	financial
SELECT T1.`账户编号`, T1.`交易频率` FROM `账户` AS T1 INNER JOIN `行政区` AS T2 ON T1.`行政区编号` = T2.`行政区编号` WHERE T2.A3 = '东波希米亚' AND STRFTIME('%Y', T1.`开户日期`) BETWEEN '1995' AND '2000'	financial
