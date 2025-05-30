#### ✅ ERD 자동 생성 (Reverse Engineer)

#### 1. 상단 메뉴에서 Database → Reverse Engineer 클릭

#### 2. Reverse Engineer Database Wizard 창이 뜨면, 아래 순서대로 진행합니다:

```less
Step 1: Stored Connection

연결할 DB를 선택하고 Next

로그인 정보 입력 후 Next
```
```less
Step 2: Retrieve Schema Information

가져올 스키마(데이터베이스)를 선택하고 Next
```
```less
Step 3: Select Objects to Reverse Engineer

테이블 등을 선택 (기본값으로 전체 선택됨) 후 Execute
```
```less
➤ Step 4: 작업 완료 후
Close 클릭

.mwb 파일 생성됨
```

✅ 전체 스키마 쿼리문 한번에 추출 (Export SQL)
```less
1. .mwb 파일 열기

2. 메뉴에서 File → Export → Forward Engineer SQL CREATE Script 클릭

3. Forward Engineering Wizard가 열림

4. 옵션 선택

5. Next → Output 위치 설정 → Finish

🎉 이 방법으로 전체 스키마의 SQL 생성 쿼리를 .sql 파일로 저장하거나 복사할 수 있습니다.
```

✅ 추천 조합 (일반적인 테이블/쿼리 추출용)
```less
Generate DROP Statements Before Each CREATE Statement

Generate Separate CREATE INDEX Statements
```
```less
Generate INSERT Statements for Tables ← 필요 시만

Disable FK checks for inserts ← insert 순서 문제 시
```
이렇게 설정하면, 테이블 구조만 깔끔하게 포함된 SQL 파일을 얻을 수 있습니다.

✅ 기본적으로 체크하면 좋은 옵션

| 옵션 이름                                                        | 설명                            | 추천 여부          |
| ------------------------------------------------------------ | ----------------------------- | -------------- |
| ✅ **Generate DROP Statements Before Each CREATE Statement**  | 기존 테이블이 있을 경우 삭제 후 생성         | 개발 및 배포 시 유용   |
| ✅ **Generate CREATE INDEX Statements** *(실제로는 아래 옵션 이름과 같음)* | 인덱스를 별도로 생성할지 여부              | 데이터 정합성을 위해 유용 |
| ✅ **Generate INSERT Statements for Tables**                  | 초기 데이터도 함께 SQL로 내보냄 (필요한 경우만) | ⚠️ 필요 시에만 체크   |
| ✅ **Create triggers after inserts**                          | 트리거가 있는 경우 포함                 | 트리거가 있다면 꼭 체크  |

⚠️ 상황에 따라 선택

| 옵션 이름                                     | 설명                                       | 언제 체크?                |
| ----------------------------------------- | ---------------------------------------- | --------------------- |
| **Generate DROP SCHEMA**                  | 기존 스키마(데이터베이스) 삭제                        | 새 DB 전체를 배포할 때        |
| **Omit Schema Qualifier in Object Names** | `db_name.table_name` 대신 `table_name`만 사용 | 특정 DB가 아닌 다른 곳에도 적용 시 |
| **Disable FK checks for inserts**         | 외래 키 무시하고 데이터 삽입 허용                      | 순서 때문에 insert가 안 될 때  |

❌ 특별한 경우가 아니면 안 건드리는 게 좋은 옵션

| 옵션 이름                                       | 이유                          |
| ------------------------------------------- | --------------------------- |
| Skip Creation of FOREIGN KEYS               | 외래 키 생성을 생략 → 권장 X          |
| Add SHOW WARNINGS After Every DDL Statement | 로그 확인용이지만 불필요한 정보 많음        |
| Do Not Create Users. Only Export Privileges | 유저/권한 설정까지 배포할 게 아니라면 의미 없음 |
| Don't create view placeholder tables        | 뷰가 없으면 무의미                  |
| Generate USE statements                     | 여러 DB 작업 시 혼란 줄 수 있음        |



