select FundManager , Fund from mf_awards where AppraisalOrg = 'Securities Times';	ccks_fund
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = 'since inception' and a.FundReturnMean > 0 group by b.Type	ccks_fund
select a.SecuAbbr , b.SecretaryBD , b.SecretaryBDTel from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='3D Glass' ;	ccks_stock
select a.Name from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium-Low' group by a.Name having count(a.SecuAbbr) > 5	ccks_fund
select count(*) from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TotalAUM > 100 and b.Education = 'Bachelor''s degree'	ccks_fund
select a.SecuAbbr , b.SecretaryBD from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Large Aircraft' ;	ccks_stock
select a.ChineseName, b.Education from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TimeInterval = 'Year to Date' order by a.AvgAUM desc limit 3	ccks_fund
select count(*) from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium' and b.InvestmentType= 'Comprehensive'	ccks_fund
select b.SecuAbbr,b.Manager,b.RiskReturncharacter from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.BenchGRForThisWeek desc limit 10;	ccks_fund
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '6 months' and a.FundReturnMean < 0 group by b.Type	ccks_fund
select SecuAbbr from mf_fundreturnrank where IndexCycle = '6 months' order by FundReturn desc limit 1	ccks_fund
select a.ChineseName, b.Education, b.ExperienceTime from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.WeightedAvgMonReturn > 0	ccks_fund
select SecuAbbr,Manager from mf_fundarchives where InvestAdvisorName='合煦智远基金管理有限公司' and FundType='Bond Fund';	ccks_fund
select a.TotalAUMTypeAvg from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select SecuAbbr from mf_fundarchives where FundType='Other Type' and InvestStyle='配置型';	ccks_fund
select a.ChiNameAbbr, a.GeneralManager, a.LegalRepr from lc_stockarchives as a join lc_actualcontroller as b on a.CompanyCode = b.CompanyCode where b.NationalityDesc = 'United States';	ccks_stock
select SHName,ActualShares from lc_largeshsubscription where SecuCode='600110';	ccks_stock
select IndexValue from ed_producerpiformp  where IndexName ='Metal Products' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select RatioCeiling from ed_taxrate where TypeName ='Rural Credit Cooperatives' and ItemName ='Excess Reserve Requirement Ratio';	ccks_macro
select b.ChiNameAbbr, a.FirstIndustryName from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.TotalShares > 10000000000	ccks_stock
select GDP, PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select a.ChiNameAbbr , b.State, b.City from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.IndustryName ='Capital Market Services';	ccks_stock
select a.ChiNameAbbr from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.State = '广东省' and b.FirstIndustryName = 'Real Estate'	ccks_stock
select LeaderName, ChiNameAbbr from lc_executivesholdings where PositionDescription like '%Chairman of the Board%' or PositionDescription like '%Vice Chairman of the Board%'	ccks_stock
select a.ChineseName, b.Education from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TimeInterval = 'Past 1 Year' order by a.ReturnTypeAvg desc limit 5	ccks_fund
select StateOwnedUnits, CollectiveUnits, JointVentures from ed_retailvalueofscgoods ;	ccks_macro
select EndDate,  SubjectSum from ed_newincreasingloan where ReportPeriod ='End-of-period cumulative' ;	ccks_macro
select count(*)  from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Internet Finance' and b.City ='杭州市';	ccks_stock
select IndexValue from ed_producerpiformp where ReportPeriod ='Same period last year' and IndexType ='Industrial Structure Classification Index' and IndexName ='Production Materials – Processing';	ccks_macro
select IndexValue from ed_producerpiformp  where IndexName ='Pharmaceutical Manufacturing' and ReportPeriod ='Same month last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 1 ;	ccks_macro
select b.ChineseName from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode group by b.ChineseName order by count(*) desc limit 1	ccks_fund
select SecuAbbr,Manager from mf_fundarchives where InvestStyle='Large-Cap Value Equity';	ccks_fund
select ChiNameAbbr from lc_exgindustry where FirstIndustryName = 'Construction'	ccks_stock
select SecuAbbr from mf_fundrisklevel where RiskLevel = 'Medium-High'	ccks_fund
select ChiNameAbbr,avg(ActualShares) from lc_largeshsubscription group by ChiNameAbbr;	ccks_stock
select InvestAdvisorName from mf_fundarchives group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select SHName,OughtShares from lc_largeshsubscription where ChiNameAbbr='天山股份';	ccks_stock
select CollectiveUnits, SelfEmployed from ed_retailvalueofscgoods  where ReportArea ='Provincial and Municipal' and ReportPeriod ='End-of-period cumulative' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='北京';	ccks_macro
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='北京' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select a.ChiNameAbbr, a.FPSHName from lc_sharefpsta as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Construction' order by a.AccuProportion desc	ccks_stock
select PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select BasisCode , RatioFloor, RatioCeiling from ed_taxrate where TypeName ='Pledged Repurchase of Corporate Bonds' and ItemName = 'Handling Fee' ;	ccks_macro
select max(IndexValue) from ed_producerpiformp  where IndexName ='Textile' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_macro
select b.SecuAbbr, a.RRInSingleYear, a.RRInTwoYear from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Bond Fund';	ccks_fund
select EndDate, RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='上海' and ReportPeriod ='Year' and strftime('%Y', EndDate)<'2010';	ccks_macro
select EndDate, IndustrialValueAdded from ed_industryproduction where ReportArea ='National' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select RatioCeiling from ed_taxrate where TypeName ='A Share' and ItemName = 'Securities Transaction Stamp Tax' and SecuMarket ='Shenzhen Stock Exchange' ;	ccks_macro
select max(IndexValue), min(IndexValue) from ed_producerpiformp  where IndexName ='Food Manufacturing' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate)='2008' ;	ccks_macro
select SecondIndustryName from lc_exgindustry where FirstIndustryName = 'Information Transmission, Software, and Information Technology Services' group by SecondIndustryName order by count(*) desc limit 2	ccks_stock
select EndDate, Province, IndustrialValueAdded from ed_industryproduction where ReportArea = 'Provincial and Municipal' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='Year' ;	ccks_macro
select SecuAbbr,RiskReturncharacter from mf_fundarchives where InvestStyle='Sector Equity – Pharmaceuticals';	ccks_fund
select EndDate,  SubjectSum from ed_newincreasingloan  where ReportPeriod ='End-of-period cumulative' and SubjectSum > 150000 and strftime('%Y', EndDate)>='2000';	ccks_macro
select  RatioCeiling from ed_taxrate where TypeName ='Chinese Large-Sized Banks' and ItemName = 'Excess Reserve Requirement Ratio'  ;	ccks_macro
select DomesticLoans, FCDeposits from ed_chinamoneyandbanking where strftime('%Y', EndDate)>='2005';	ccks_macro
select a.AvgAUMTypeRank from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select a.ChiNameAbbr, b.LeaderName, b.PositionDescription from lc_sharetransfer as a join lc_executivesholdings as b on a.CompanyCode = b.CompanyCode order by a.PCTBeforeTran desc limit 5	ccks_stock
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '6 months' and a.FundReturnMean < 0 group by b.Type	ccks_fund
select b.ChineseName,b.BirthDate from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode order by a.BondFundNV desc limit 10;	ccks_fund
select OtherForeignAssets, OtherLiability from ed_moneyauthoritybs ;	ccks_macro
select a.ReturnTypeRank from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.ExperienceTime > 10	ccks_fund
select EndDate, NetAbroadAssets from ed_chinamoneyandbanking where NetAbroadAssets > 1000000;	ccks_macro
select EndDate,  SubjectSum, YOY from ed_newincreasingloan  where ReportPeriod ='Month' and SubjectSum > 100000 and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select ChiNameAbbr from lc_sharesfloatingschedule where NewMarketableAShares <= 1000	ccks_stock
select count(*) from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '江苏省' and a.IndustryName ='Agricultural and By-Product Processing';	ccks_stock
select IndustrialValueAdded from ed_industryproduction  where Province ='上海' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='Year' and strftime('%Y', EndDate)='2000';	ccks_macro
select a.ChiNameAbbr from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Manufacturing' order by a.Proportion1 desc limit 1	ccks_stock
select Fund from mf_awards where AwardName = 'China Equity Hedge Fund Award Nomination' and AppraisalOrg ='Morningstar Information';	ccks_fund
select EndDate, RetailValueOfSCGoods from ed_retailvalueofscgoods  where ReportArea ='National' and ReportPeriod ='Year' and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select count(*) from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TotalAUM > 100 and b.Education = 'Bachelor''s degree'	ccks_fund
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '1 month' and a.FundReturn > 0 group by b.Type	ccks_fund
select b.Education, count(*) from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode where a.InvestAdvisorName like '富国基金%' and a.Incumbent = 'Yes'  group by b.Education	ccks_fund
select a.State , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Large Aircraft' group by a.State ;	ccks_stock
select b.ChineseName, b.TotalFundNV, b.EquityFundNV, b.HybridFundNV from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.Nationality != 'China';	ccks_fund
select FundManager , AwardName from mf_awards where AppraisalOrg = 'Securities Times';	ccks_fund
select GDPPerCapita from ed_grossdomesticproduct ;	ccks_macro
select EndDate,  DepositsWithCentralBank , CashInVault from ed_otherdepositorycorpbs  where strftime('%Y', EndDate)>='2008';	ccks_macro
select a.ChiNameAbbr from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省' and b.FirstIndustryName = 'Scientific Research and Technology Services'	ccks_stock
select SecuCode, ChiNameAbbr from lc_coconcept where ConceptName like '%New Energy%';	ccks_stock
select a.SecuCode , b.OfficeAddr from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.IndustryName ='Retail Trade';	ccks_stock
select ChiNameAbbr from lc_sharesfloatingschedule order by TotalAShares desc limit 10	ccks_stock
select a.SecuCode, a.ChiNameAbbr from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State ='安徽省' and a.ConceptName ='Autonomous Driving';	ccks_stock
select  RatioCeiling from ed_taxrate where TypeName ='Chinese Large-Sized Banks' and ItemName = 'Excess Reserve Requirement Ratio'  ;	ccks_macro
select a.SecuCode , b.State  from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Metaverse' ;	ccks_stock
select ReportPeriod, IndexType, IndexValue from ed_producerpiformp where  IndexName ='Metallurgical';	ccks_macro
select EndDate, IndustrialOutputValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select LeaderName, ShareAmount from lc_executivesholdings where PositionDescription like '%Vice President%'	ccks_stock
select b.SecuAbbr,b.InvestField from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.BenchGRForThisMonth<0;	ccks_fund
select count(*) from lc_ipodeclaration where CSRCIndustryName='Banking';	ccks_stock
select a.FirstIndustryName from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonListedShares > 200000000 group by a.FirstIndustryName having count(*) > 50	ccks_stock
select a.State , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Graphene' group by a.State having count(*)>1;	ccks_stock
select b.ChiNameAbbr from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where a.FirstIndustryName = 'Construction' and b.TotalShares > 10000000000	ccks_stock
select IndexValue from ed_producerpiformp  where IndexName ='Beverage Manufacturing' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select SecondIndustryName from lc_exgindustry where FirstIndustryName = 'Manufacturing' group by SecondIndustryName order by count(*) desc limit 1	ccks_stock
select b.SecondIndustryName, count(*) from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.AccuMarketableAShares > 5000 group by b.SecondIndustryName	ccks_stock
select ChineseName from mf_personalinfo where Nationality != 'China';	ccks_fund
