select `基金经理` , `基金名称` from `公募基金获奖情况` where `评奖单位` = '证券时报';	ccks_fund
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '成立以来' and a.`同类基金收益率均值(%)` > 0 group by b.`基金运作方式`	ccks_fund
select a.`所属基金/股票简称` , b.`董事会秘书` , b.`董秘电话` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='3D玻璃' ;	ccks_stock
select a.`姓名` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中低' group by a.`姓名` having count(a.`证券简称`) > 5	ccks_fund
select count(*) from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`总规模(亿元)` > 100 and b.`最高学历` = '本科'	ccks_fund
select a.`所属基金/股票简称` , b.`董事会秘书` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='大飞机' ;	ccks_stock
select a.`基金经理姓名`, b.`最高学历` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`时间区间` = '今年以来' order by a.`平均规模(亿元)` desc limit 3	ccks_fund
select count(*) from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中' and b.`基金投资类型`= '综合型'	ccks_fund
select b.`证券简称`,b.`基金经理`,b.`风险收益特征` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`本周以来基金基准增长率(%)` desc limit 10;	ccks_fund
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '六个月' and a.`同类基金收益率均值(%)` < 0 group by b.`基金运作方式`	ccks_fund
select `基金简称` from `公募基金最新收益率排名` where `指标周期` = '六个月' order by `基金收益率(%)` desc limit 1	ccks_fund
select a.`基金经理姓名`, b.`最高学历`, b.`证券从业经历(年)` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`月平均收益率(%)` > 0	ccks_fund
select `证券简称`,`基金经理` from `公募基金概况` where `基金管理人`='合煦智远基金管理有限公司' and `基金类别`='债券型';	ccks_fund
select a.`总管理规模同类均值(亿元)` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select `证券简称` from `公募基金概况` where `基金类别`='其他型' and `基金投资风格`='配置型';	ccks_fund
select a.`中文名称缩写`, a.`总经理`, a.`法人代表` from `公司概况` as a join `公司实际控制人` as b on a.`公司代码` = b.`公司代码` where b.`国籍描述` = '美国';	ccks_stock
select `股东名称`,`实配股数(股)` from `配股大股东认配状况` where `所属基金/股票代码`='600110';	ccks_stock
select `指数` from `工业品出厂价格指数`  where `指数名称` ='金属制品业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `最高比率(%)` from `税率表` where `税率类别` ='农村信用社' and `税率项目` ='超额存款准备金率';	ccks_macro
select b.`中文名称缩写`, a.`一级行业名称` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`总股本(股)` > 10000000000	ccks_stock
select `国内生产总值(百万元)`, `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select a.`中文名称缩写` , b.`省份`, b.`所属城市` from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`行业名称` ='资本市场服务';	ccks_stock
select a.`中文名称缩写` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '广东省' and b.`一级行业名称` = '房地产业'	ccks_stock
select `领导姓名`, `中文名称缩写` from `公司报告期管理层持股` where `职位描述` like '%董事长%' or `职位描述` like '%副董事长%'	ccks_stock
select a.`姓名`, b.`最高学历` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`时间区间` = '近1年' order by a.`同类经理收益率均值(%)` desc limit 5	ccks_fund
select `国有单位`, `集体单位`, `合营单位` from `社会消费品零售总额` ;	ccks_macro
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款` where `统计区间` ='期末累计' ;	ccks_macro
select count(*)  from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='互联网金融' and b.`所属城市` ='杭州市';	ccks_stock
select `指数` from `工业品出厂价格指数` where `数据统计期间` ='上年同期' and `指数类别` ='工业结构分类指数' and `指数名称` ='生产资料-加工';	ccks_macro
select `指数` from `工业品出厂价格指数`  where `指数名称` ='医药制造业' and `数据统计期间` ='上年同月' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1 ;	ccks_macro
select b.`基金经理姓名` from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` group by b.`基金经理姓名` order by count(*) desc limit 1	ccks_fund
select `证券简称`,`基金经理` from `公募基金概况` where `基金投资风格`='大盘价值股票';	ccks_fund
select `中文名称缩写` from `公司行业划分表` where `一级行业名称` = '建筑业'	ccks_stock
select `证券简称` from `公募基金风险等级表` where `风险等级` = '中高'	ccks_fund
select `中文名称缩写`,avg(`实配股数(股)`) from `配股大股东认配状况` group by `中文名称缩写`;	ccks_stock
select `基金管理人` from `公募基金概况` group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select `股东名称`,`应配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='天山股份';	ccks_stock
select `集体单位`, `个体单位` from `社会消费品零售总额`  where `统计区域类别` ='省市' and `数据统计期间` ='期末累计' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='北京';	ccks_macro
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='北京' and `数据统计期间` ='期末累计';	ccks_macro
select a.`中文名称缩写`, a.`股权被冻结质押股东名称` from `股东股权冻结和质押统计` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '建筑业' order by a.`累计占总股本比例` desc	ccks_stock
select `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select `计费基准` , `最低比率(%)`, `最高比率(%)` from `税率表` where `税率类别` ='企债质押式回购' and `税率项目` = '经手费' ;	ccks_macro
select max(`指数`) from `工业品出厂价格指数`  where `指数名称` ='纺织业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_macro
select b.`证券简称`, a.`一年回报率(%)`, a.`二年回报率(%)` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where b.`基金类别` = '债券型';	ccks_fund
select `截止日期`, `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='上海' and `数据统计期间` ='年度' and strftime('%Y', `截止日期`)<'2010';	ccks_macro
select `截止日期`, `工业增加值(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select `最高比率(%)` from `税率表` where `税率类别` ='A股' and `税率项目` = '证券交易印花税' and `证券市场` ='深圳证券交易所' ;	ccks_macro
select max(`指数`), min(`指数`) from `工业品出厂价格指数`  where `指数名称` ='食品制造业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`)='2008' ;	ccks_macro
select `二级行业名称` from `公司行业划分表` where `一级行业名称` = '信息传输、软件和信息技术服务业' group by `二级行业名称` order by count(*) desc limit 2	ccks_stock
select `截止日期`, `省市`, `工业增加值(百万元)` from `工业生产` where `统计区域类别` = '省市' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='年度' ;	ccks_macro
select `证券简称`,`风险收益特征` from `公募基金概况` where `基金投资风格`='行业股票-医药';	ccks_fund
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款`  where `统计区间` ='期末累计' and `金额(亿元)` > 150000 and strftime('%Y', `截止日期`)>='2000';	ccks_macro
select  `最高比率(%)` from `税率表` where `税率类别` ='中资大型银行' and `税率项目` = '超额存款准备金率'  ;	ccks_macro
select `国内信贷`, `外币存款` from `中国货币与银行概览` where strftime('%Y', `截止日期`)>='2005';	ccks_macro
select a.`平均管理规模同类排名` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select a.`中文名称缩写`, b.`领导姓名`, b.`职位描述` from `股东股权变动` as a join `公司报告期管理层持股` as b on a.`公司代码` = b.`公司代码` order by a.`出让前持股比例` desc limit 5	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '六个月' and a.`同类基金收益率均值(%)` < 0 group by b.`基金运作方式`	ccks_fund
select b.`基金经理姓名`,b.`出生日期` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` order by a.`债券型管理规模(亿元)` desc limit 10;	ccks_fund
select `其他国外资产(百万元)`, `其他负债(百万元)` from `货币当局资产负债表` ;	ccks_macro
select a.`同类经理收益率排名` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`证券从业经历(年)` > 10	ccks_fund
select `截止日期`, `国外净资产` from `中国货币与银行概览` where `国外净资产` > 1000000;	ccks_macro
select `截止日期`,  `金额(亿元)`, `同比增减(%)` from `金融机构新增贷款`  where `统计区间` ='月份' and `金额(亿元)` > 100000 and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select `中文名称缩写` from `限售股票解禁时间表` where `本次新增可售A股(万股)` <= 1000	ccks_stock
select count(*) from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '江苏省' and a.`行业名称` ='农副食品加工业';	ccks_stock
select `工业增加值(百万元)` from `工业生产`  where `省市` ='上海' and `统计口径` ='全部工业企业' and `数据统计区间` ='年度' and strftime('%Y', `截止日期`)='2000';	ccks_macro
select a.`中文名称缩写` from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '制造业' order by a.`本次新增可售A股占上期末已流通A股比例(%)` desc limit 1	ccks_stock
select `基金名称` from `公募基金获奖情况` where `奖项名称` = '中国股票型对冲基金奖提名' and `评奖单位` ='晨星资讯';	ccks_fund
select `截止日期`, `社会消费品零售总额(百万元)` from `社会消费品零售总额`  where `统计区域类别` ='全国' and `数据统计期间` ='年度' and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select count(*) from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`总规模(亿元)` > 100 and b.`最高学历` = '本科'	ccks_fund
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '一个月' and a.`基金收益率(%)` > 0 group by b.`基金运作方式`	ccks_fund
select b.`最高学历`, count(*) from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` where a.`基金管理人名称` like '富国基金%' and a.`是否在任` = '是'  group by b.`最高学历`	ccks_fund
select a.`省份` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='大飞机' group by a.`省份` ;	ccks_stock
select b.`基金经理姓名`, b.`总管理规模(亿元)`, b.`股票型管理规模(亿元)`, b.`混合型管理规模(亿元)` from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`国籍` != '中国';	ccks_fund
select `基金经理` , `奖项名称` from `公募基金获奖情况` where `评奖单位` = '证券时报';	ccks_fund
select `人均国内生产总值(元/人)` from `国内生产总值` ;	ccks_macro
select `截止日期`,  `准备金存款` , `库存现金` from `其他存款性公司资产负债表`  where strftime('%Y', `截止日期`)>='2008';	ccks_macro
select a.`中文名称缩写` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省' and b.`一级行业名称` = '科学研究和技术服务业'	ccks_stock
select `所属基金/股票代码`, `中文名称缩写` from `概念所属公司表` where `概念名称` like '%新能源%';	ccks_stock
select a.`所属基金/股票代码` , b.`公司办公地址` from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`行业名称` ='零售业';	ccks_stock
select `中文名称缩写` from `限售股票解禁时间表` order by `A股总数(万股)` desc limit 10	ccks_stock
select a.`所属基金/股票代码`, a.`中文名称缩写` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` ='安徽省' and a.`概念名称` ='无人驾驶';	ccks_stock
select  `最高比率(%)` from `税率表` where `税率类别` ='中资大型银行' and `税率项目` = '超额存款准备金率'  ;	ccks_macro
select a.`所属基金/股票代码` , b.`省份`  from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='元宇宙' ;	ccks_stock
select `数据统计期间`, `指数类别`, `指数` from `工业品出厂价格指数` where  `指数名称` ='冶金工业';	ccks_macro
select `截止日期`, `工业总产值(现价)(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='全部工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select `领导姓名`, `期末持股数(股)` from `公司报告期管理层持股` where `职位描述` like '%副总裁%'	ccks_stock
select b.`证券简称`,b.`基金投资范围` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`本月以来基金基准增长率(%)`<0;	ccks_fund
select count(*) from `A股发行申报企业信息` where `所属行业/领域`='银行业';	ccks_stock
select a.`一级行业名称` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`未流通A股(股)` > 200000000 group by a.`一级行业名称` having count(*) > 50	ccks_stock
select a.`省份` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='石墨烯' group by a.`省份` having count(*)>1;	ccks_stock
select b.`中文名称缩写` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where a.`一级行业名称` = '建筑业' and b.`总股本(股)` > 10000000000	ccks_stock
select `指数` from `工业品出厂价格指数`  where `指数名称` ='饮料制造业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `二级行业名称` from `公司行业划分表` where `一级行业名称` = '制造业' group by `二级行业名称` order by count(*) desc limit 1	ccks_stock
select b.`二级行业名称`, count(*) from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`已流通A股(万股)` > 5000 group by b.`二级行业名称`	ccks_stock
select `基金经理姓名` from `公募基金经理基本资料` where `国籍` != '中国';	ccks_fund
