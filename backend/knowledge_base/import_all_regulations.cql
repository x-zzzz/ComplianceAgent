// law1_个人信息保护法.csv
LOAD CSV WITH HEADERS FROM 'file:///law1_个人信息保护法.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law2_GDPR.csv
LOAD CSV WITH HEADERS FROM 'file:///law2_GDPR.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law3_香港个人资料私隐条例.csv
LOAD CSV WITH HEADERS FROM 'file:///law3_香港个人资料私隐条例.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law4_澳门个人资料保护法.csv
LOAD CSV WITH HEADERS FROM 'file:///law4_澳门个人资料保护法.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law5_网络安全标准实践指南-敏感个人信息指南.csv
LOAD CSV WITH HEADERS FROM 'file:///law5_网络安全标准实践指南-敏感个人信息指南.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law6_人类遗传资源管理条例实施细则.csv
LOAD CSV WITH HEADERS FROM 'file:///law6_人类遗传资源管理条例实施细则.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law7_广东省健康医疗数据安全分类分级管理技术规范.csv
LOAD CSV WITH HEADERS FROM 'file:///law7_广东省健康医疗数据安全分类分级管理技术规范.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law8_数据出境安全评估办法.csv
LOAD CSV WITH HEADERS FROM 'file:///law8_数据出境安全评估办法.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);

// law9_中华人民共和国疫苗管理法.csv
LOAD CSV WITH HEADERS FROM 'file:///law9_中华人民共和国疫苗管理法.csv' AS row
WITH TRIM(REPLACE(REPLACE(row.law_name,'《',''),'》','')) AS cleanLaw,
     TRIM(REPLACE(REPLACE(row.clause,'《',''),'》','')) AS cleanClause,
     TRIM(coalesce(row.content,'')) AS content
WHERE cleanLaw <> '' AND cleanClause <> ''
MERGE (r:Regulation {name: cleanLaw})
MERGE (c:Clause {id: cleanLaw + '_' + cleanClause})
SET c.name = cleanClause, c.text = content
MERGE (r)-[:HAS_CLAUSE]->(c);


