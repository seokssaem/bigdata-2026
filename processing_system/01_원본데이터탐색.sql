-- 1. subway_raw의 컬럼명과 데이터 형식
SELECT * FROM subway_raw;

-- 2. 전체 행 수
SELECT COUNT(*) FROM subway_raw;

-- 3. 지하철역 개수
SELECT COUNT(DISTINCT 역명) FROM subway_raw;

-- 4. 승하차 구분에 저장된 값의 종류
SELECT DISTINCT 승하차 FROM subway_raw;

-- 5. 승하차 구분별 행 수
SELECT 승하차, COUNT(*) FROM subway_raw
GROUP BY 승하차;

-- 6. 인원 값이 가장 큰 데이터 10건
SELECT * FROM subway_raw
ORDER BY 인원수 DESC
LIMIT 10;

-- 7. 날짜의 최솟값과 최댓값
SELECT MIN(날짜), MAX(날짜)
FROM subway_raw;

-- 8. 인원 값이 NULL인 행의 수
SELECT COUNT(*) FROM subway_raw
WHERE 인원수 IS NULL;