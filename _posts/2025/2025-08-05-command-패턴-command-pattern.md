---
layout  : post
title   : Command 패턴(Command Pattern)
summary : 'type Command interface { Before() Execute() After() }'
date    : 2025-08-05 23:16:00 +0900
updated : 2026-03-14 01:08:00 +0900
tag     : notion import
toc     : true
comment : false
public  : true
---
* TOC
{:toc}
# Command 패턴(Command Pattern)
Created: 2025년 8월 5일 오후 11:16
보관소: No
최종 편집 일시: 2026년 3월 14일 오전 1:08

- before, execute, after 식으로 **명령 실행 전후의 로직을 분리해 제어 흐름을 일관되게 관리**할 때 쓰는 구조예요.
- 명령(=Command)을 객체로 캡슐화해서, 실행자(Invoker)가 구체적인 동작을 모르고도 Execute()만 호출하게 하는 방식입니다.

- 실행을 지연시키거나 큐잉할 때,
- 실행 취소(Undo) 기능을 붙일 때,
- 트랜잭션 같은 일관된 실행 단위를 만들 때
    
    활용됩니다.
    

```go
type Command interface {
    Before()
    Execute()
    After()
}

type MakeLatte struct{}
func (m MakeLatte) Before() { fmt.Println("컵을 데웁니다") }
func (m MakeLatte) Execute() { fmt.Println("라떼를 내립니다") }
func (m MakeLatte) After() { fmt.Println("컵을 닦습니다") }

func RunCommand(cmd Command) {
    cmd.Before()
    cmd.Execute()
    cmd.After()
}
```
