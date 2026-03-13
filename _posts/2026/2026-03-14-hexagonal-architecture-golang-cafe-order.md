---
layout  : post
title   : 헥사고날 아키텍처 핵심 개념과 Golang 카페 주문 시스템 예시
summary : 헥사고날 아키텍처의 코어·포트·어댑터 개념을 정리하고 Golang 카페 주문 시스템 예시로 적용 방식을 설명합니다.
date    : 2026-03-14 00:40:00 +0900
updated : 2026-03-14 00:40:00 +0900
tag     : architecture golang hexagonal
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

> 이 게시글은 AI에게 질문하면서 배운 내용을 AI에게 정리하라고 하여 작성된 글입니다.

현대 소프트웨어 설계에서 헥사고날 아키텍처는 유연하고 확장 가능한 시스템을 구축하는 데 매우 유용한 패턴 중 하나입니다. 이 글에서는 헥사고날 아키텍처의 기본 개념, 핵심 용어, 그리고 Golang을 이용한 카페 주문 시스템의 예시를 통해 실전에서 어떻게 적용할 수 있는지를 살펴보겠습니다.

## 1. 개념

헥사고날 아키텍처(Hexagonal Architecture)란 비즈니스 로직과 외부 시스템을 분리하여 애플리케이션을 설계하는 방법입니다. 흔히 포트-어댑터 아키텍처(Ports and Adapters)라고도 불리며, 비즈니스 로직을 외부 의존성으로부터 독립시켜 유연성과 유지보수성을 높이는 것이 목적입니다.

이 아키텍처에서는 비즈니스 로직을 중심으로, 외부 시스템과의 상호작용을 포트(인터페이스)와 어댑터(구현체)를 통해 처리합니다. 이렇게 하면 외부 시스템(DB, API 등)을 변경해도 비즈니스 로직에는 영향을 최소화할 수 있습니다.

## 2. 핵심 용어

### 1) 코어(Core): 비즈니스 로직

설명: 비즈니스 로직이 담긴 애플리케이션의 핵심 부분으로, 외부 시스템(DB, 외부 API 등)과 독립적으로 동작합니다.

예시: `OrderService`, `Drink`와 같은 비즈니스 규칙을 처리하는 서비스.

```go
type Drink struct {
    Name  string
    Stock int
}
```

### 2) 포트(Ports): 인터페이스

설명: 비즈니스 로직에서 외부 시스템과의 상호작용을 추상화한 인터페이스입니다. 비즈니스 로직은 포트에 정의된 기능을 사용해 외부 시스템과 통신하며, 구체적인 구현은 알지 못합니다.

예시: 외부 시스템으로부터 재고를 확인하는 `StockChecker`, DB에 데이터를 저장하는 `DrinkRepository`.

```go
type StockChecker interface {
    CheckStock(drinkName string) (int, error)
}
```

### 3) 어댑터(Adapters): 외부 통신 구현체

설명: 포트를 구현하여 외부 시스템과의 실제 통신을 담당하는 부분입니다. 포트를 통해 비즈니스 로직이 요청하는 기능을 외부 시스템에서 수행합니다.

예시: 외부 서버에 HTTP 요청을 보내는 `HTTPStockChecker`, DB에 데이터를 저장하는 `SQLDrinkRepository`.

```go
type SQLDrinkRepository struct {
    db *sql.DB
}

func (r *SQLDrinkRepository) Save(drink Drink) error {
    _, err := r.db.Exec("INSERT INTO drinks (name, stock) VALUES (?, ?)", drink.Name, drink.Stock)
    return err
}
```

### 4) Driven (구동됨)

설명: 외부 시스템 요청에 의해 애플리케이션이 동작하는 부분입니다.

예시: DB에 데이터를 저장하는 `SQLDrinkRepository`.

### 5) Driving (구동함)

설명: 애플리케이션이 외부 시스템에 요청을 보내고 결과를 받아오는 역할입니다.

예시: 외부 서버로 재고 확인 요청을 보내는 `HTTPStockChecker`.

## 3. 카페 주문 시스템 예시

카페 주문 시스템을 통해 헥사고날 아키텍처 적용 방법을 살펴보겠습니다. 이 예시에서는 카페 주문 서비스가 외부 서버에서 음료 재고를 확인하고, 그 데이터를 DB에 저장합니다.

### 1) 비즈니스 로직 (코어)

```go
package cafe

type Drink struct {
    ID    int
    Name  string
    Stock int
}

type StockChecker interface {
    CheckStock(drinkName string) (int, error)
}

type DrinkRepository interface {
    Save(drink Drink) error
}

type OrderService struct {
    stockChecker    StockChecker
    drinkRepository DrinkRepository
}

func NewOrderService(stockChecker StockChecker, drinkRepository DrinkRepository) *OrderService {
    return &OrderService{
        stockChecker:    stockChecker,
        drinkRepository: drinkRepository,
    }
}

func (s *OrderService) OrderDrink(drinkName string) error {
    stock, err := s.stockChecker.CheckStock(drinkName)
    if err != nil {
        return err
    }

    drink := Drink{
        Name:  drinkName,
        Stock: stock,
    }

    return s.drinkRepository.Save(drink)
}
```

### 2) 외부 시스템과의 통신 (어댑터)

외부 서버와의 통신 (Driving 어댑터):

```go
package adapter

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type HTTPStockChecker struct {
    apiEndpoint string
}

func NewHTTPStockChecker(apiEndpoint string) *HTTPStockChecker {
    return &HTTPStockChecker{
        apiEndpoint: apiEndpoint,
    }
}

func (h *HTTPStockChecker) CheckStock(drinkName string) (int, error) {
    resp, err := http.Get(fmt.Sprintf("%s/checkStock?drink=%s", h.apiEndpoint, drinkName))
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()

    var result struct {
        Stock int `json:"stock"`
    }
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return 0, err
    }

    return result.Stock, nil
}
```

DB 저장소와의 통신 (Driven 어댑터):

```go
package adapter

import (
    "database/sql"
    "cafe"
)

type SQLDrinkRepository struct {
    db *sql.DB
}

func NewSQLDrinkRepository(db *sql.DB) *SQLDrinkRepository {
    return &SQLDrinkRepository{db: db}
}

func (r *SQLDrinkRepository) Save(drink cafe.Drink) error {
    _, err := r.db.Exec("INSERT INTO drinks (name, stock) VALUES (?, ?)", drink.Name, drink.Stock)
    return err
}
```

### 3) 전체 통합

```go
package main

import (
    "database/sql"
    "fmt"
    "cafe"
    "adapter"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/cafedb")
    if err != nil {
        fmt.Println("Failed to connect to the database:", err)
        return
    }
    defer db.Close()

    stockChecker := adapter.NewHTTPStockChecker("http://inventory.api.com")
    drinkRepository := adapter.NewSQLDrinkRepository(db)

    orderService := cafe.NewOrderService(stockChecker, drinkRepository)

    err = orderService.OrderDrink("Americano")
    if err != nil {
        fmt.Println("Failed to order drink:", err)
    } else {
        fmt.Println("Drink ordered successfully!")
    }
}
```

## 결론

헥사고날 아키텍처는 비즈니스 로직과 외부 시스템의 의존성을 분리하여 시스템의 확장성과 유지보수성을 높여줍니다. 포트(인터페이스)를 통해 외부와의 상호작용을 추상화하고, 어댑터(구현체)를 통해 구체적인 구현을 처리하는 이 방식은 외부 시스템(DB, API 등)을 교체하거나 추가할 때 유연하게 대처할 수 있는 구조를 제공합니다.

카페 주문 시스템 예시를 통해 이러한 설계가 실제로 어떻게 작동하는지를 살펴보았듯이, 헥사고날 아키텍처는 다양한 환경에서 강력한 도구가 될 수 있습니다.
