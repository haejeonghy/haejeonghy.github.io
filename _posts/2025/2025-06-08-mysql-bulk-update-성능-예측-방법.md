---
layout  : post
title   : MySQL Bulk Update 성능 예측 방법
summary : '선임이 “프로덕션 DB 테이블에 bulk update 하면 얼마나 빨라?”라고 질문함. >'
date    : 2025-06-08 15:40:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : database
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# MySQL Bulk Update 성능 예측 방법
Created: 2025년 6월 8일 오후 3:40
Tags: Database
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

## **📌 MySQL Bulk Update 성능 예측 방법 정리**

### **❓ 상황**

> 선임이 “프로덕션 DB 테이블에 bulk update 하면 얼마나 빨라?”라고 질문함.
> 

> → Staging 환경에서 테스트한 결과가 유의미한가?
> 

> → 어떻게 성능을 파악해야 하는가?
> 

---

### **✅ 선임에게 이렇게 대답한다**

> “Staging 환경은 데이터 양과 설정이 달라서 성능 테스트 결과가 과소평가될 수 있습니다.
> 

> 정확한 예측을 위해서는 아래 항목들을 확인해야 합니다.”
> 

---

### **🔍 실무적으로 확인해야 할 항목**

1. **대상 row 수 추정**
    - SELECT COUNT(*) WHERE 조건
2. **인덱스 유무 확인**
    - EXPLAIN UPDATE ... → full scan이면 성능 저하
3. **트랜잭션 배치 테스트**
    - LIMIT 1000 단위로 나눠서 ROLLBACK 테스트
4. **슬로우 쿼리, 락 대기 확인**
    - SHOW PROCESSLIST, SHOW ENGINE INNODB STATUS
5. **MySQL 설정 차이 고려**
    - staging은 sync_binlog, innodb_flush_log_at_trx_commit이 완화되어 있어 정확한 비교 어려움

---

### **❌ Staging에서 성능 테스트의 한계**

| **항목** | **Staging 테스트 결과 유의미함?** | **이유** |
| --- | --- | --- |
| 인덱스 사용 여부 | ✅ | EXPLAIN으로 확인 가능 |
| Deadlock 가능성 | ✅ | row-level lock 충돌 확인 |
| 전체 update 시간 | ❌ | 데이터 양, I/O, buffer pool 상황 다름 |
| 트랜잭션 압박 | ❌ | 로그, flush 설정이 다름 |

---

### **🎯 현실적인 접근**

- **prod에서 제한된 범위로 ROLLBACK 테스트**

```
START TRANSACTION;
UPDATE your_table SET col = 'value' WHERE 조건 LIMIT 10000;
ROLLBACK;
```

- **성능 이슈 없도록 배치 처리 설계**
- **pt-archiver / chunk update 도구 활용 고려**

---
