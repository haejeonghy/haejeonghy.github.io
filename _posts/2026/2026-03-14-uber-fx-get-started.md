---
layout  : post
title   : Uber Fx 시작하기와 핵심 개념 정리
summary : Golang 서버에서 의존성 주입 문제를 해결하기 위해 Uber Fx를 조사하며 정리한 시작 가이드와 핵심 개념 노트입니다.
date    : 2026-03-14 14:35:00 +0900
updated : 2026-03-14 14:35:00 +0900
tag     : golang fx dependency-injection
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

![](https://velog.velcdn.com/images/haejeonghy/post/d640a9d8-aa7e-41ea-9578-0ae85239ea38/image.png)

# 서론

현재 내가 일하고 있는 회사에서는 Go 언어(Golang)를 사용해 서버를 운영하고 있다. 하지만 의존성을 주입할 때마다 글로벌 설정 변수를 사용해야 하는 불편함이 있었다. 이 문제를 해결하기 위해 팀 내에서 논의가 이루어졌고, 결과적으로 [Uber의 FX 프레임워크](https://uber-go.github.io/fx/)를 도입하자는 의견에 합의가 이뤄졌다.

잘 모르는 개념을 바로 쓸 수 없으니까, 공식 문서를 읽으면서 정리했다.

# 시작하기

[Uber FX 시작하기](https://uber-go.github.io/fx/get-started/index.html) 페이지에서는 간단한 서버를 실행해 보며 FX 프레임워크를 체험할 수 있는 과정을 제공한다.

나는 이 가이드를 따라가면서 FX의 기능을 체험해 보았고, 기본적인 사용법을 익혔다. 아래는 Get Started 코스에서 제공된 예제 코드에 나의 간단한 주석을 추가한 내용이다.

이 과정은 의존성 주입을 보다 편리하고 효율적으로 관리할 수 있게 도와주며, 기존에 우리가 겪고 있던 불편함을 어떻게 해결할 수 있을지에 대한 좋은 통찰을 제공해 주었다.

## 설치

```bash
go get go.uber.org/fx@latest
```

## main.go

```go
package main

import (
	"context"
	"fmt"
	"io"
	"net"
	"net/http"

	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"
	"go.uber.org/zap"
)

func main() {
	// New() 새로운 앱을 생성하고 초기화한다.
	app := fx.New(
		// WithLogger() 생성자가 제공되거나 함수가 호출되었을 때 기록할 logger 저장
		fx.WithLogger(func(log *zap.Logger) fxevent.Logger {
			return &fxevent.ZapLogger{Logger: log}
		}),
		// Provide() 앱이 다양한 타입을 인스턴스화 하는 방법을 가르치기 위해 여러 개의 생성자 함수를 등록한다.
		fx.Provide(
			NewHTTPServer,
			// Annotate() 함수의 매개변수와 반환값에 어노테이션을 추가할 수 있도록 해주며 별도의 구조체 정의가 필요없다.
			fx.Annotate(
				NewServeMux,
				// ParamTags 명시적으로 routes를 받겠다고 구분
				fx.ParamTags(`group:"routes"`),
			),
		),
		fx.Provide(
			AsRoute(NewEchoHandler),
			AsRoute(NewHelloHandler),
			zap.NewExample,
		),
		// Invoke() 새로운 앱을 생성하는 과정에서 해당 옵션에 등록된 함수가 전부 실행된다.
		fx.Invoke(func(*http.Server) {}),
	)
	app.Run()
}

func AsRoute(f any) any {
	return fx.Annotate(
		f,
		// As() 함수의 반환 타입을 다른 인터페이스 타입으로 제공하도록 지정할 수 있다.
		fx.As(new(Route)),
		// ResultTags 명시적으로 routes를 리턴한다고 선언
		fx.ResultTags(`group:"routes"`),
	)
}

// Lifecycle interface: 앱의 생명 주기 동안 특정 시점에 실행될 콜백 함수를 등록하도록 하는 인터페이스
func NewHTTPServer(lc fx.Lifecycle, mux *http.ServeMux, log *zap.Logger) *http.Server {
	srv := &http.Server{Addr: ":8080", Handler: mux}
	// Append() Hook 타입 객체를 받아 여러 개의 Hook을 등록한다.
	lc.Append(fx.Hook{
		OnStart: func(ctx context.Context) error {
			ln, err := net.Listen("tcp", srv.Addr)
			if err != nil {
				return err
			}
			log.Info("Starting HTTP server", zap.String("addr", srv.Addr))
			go srv.Serve(ln)
			return nil
		},
		OnStop: func(ctx context.Context) error {
			return srv.Shutdown(ctx)
		},
	})
	return srv
}

type EchoHandler struct {
	log *zap.Logger
}

type HelloHandler struct {
	log *zap.Logger
}

type Route interface {
	http.Handler
	Pattern() string
}

func NewHelloHandler(log *zap.Logger) *HelloHandler {
	return &HelloHandler{log: log}
}

func (*HelloHandler) Pattern() string {
	return "/hello"
}

func (h *HelloHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		h.log.Error("request 읽기에 실패했습니다.", zap.Error(err))
		http.Error(w, "internal server error", http.StatusInternalServerError)
	}

	if _, err := fmt.Fprintf(w, "Hello %s\n", body); err != nil {
		h.log.Error("response 작성에 실패했습니다.", zap.Error(err))
		http.Error(w, "Internal 서버 에러 발생", http.StatusInternalServerError)
		return
	}
}

func NewEchoHandler(log *zap.Logger) *EchoHandler {
	return &EchoHandler{log: log}
}

func (h *EchoHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if _, err := io.Copy(w, r.Body); err != nil {
		h.log.Warn("Failed to handle request", zap.Error(err))
	}
}

func (h *EchoHandler) Pattern() string {
	return "/echo"
}

func NewServeMux(routes []Route) *http.ServeMux {
	mux := http.NewServeMux()
	for _, route := range routes {
		mux.Handle(route.Pattern(), route)
	}
	return mux
}
```

# 들어가기

[Introduction](https://uber-go.github.io/fx/intro.html)에서 Fx를 사용하면 다음과 같은 장점이 있다.

> Boilerplate 코드를 줄이기  
> 글로벌 상태 제거  
> 새로운 컴포넌트 추가 시 즉시 접근 가능  
> 일반적인 모듈 만들기

1. Boilerplate는 반복적으로 작성해야 하는 코드를 의미한다. 우리 팀에서 Fx를 도입해서 해결하려는 가장 큰 문제 중 하나이다.
2. 글로벌 상태는 앱 전체에서 접근할 수 있는 변수를 의미하는데, 이는 디버깅이 어렵고 유지보수성을 떨어뜨린다. 테스트 하기도 어려워진다.
3. 새로운 기능을 앱에 추가했을 때 접근해서 사용하는 단계를 줄일 수 있다.
4. 공유 가능한 제너럴한 모듈을 만들어 코드 재사용을 쉽게 한다.

# 개념

## Container

[FX 컨테이너 문서](https://uber-go.github.io/fx/container.html)

컨테이너는 모든 생성자와 값을 보관하는 추상화이다. 컨테이너에 앱의 요구사항, 특정 작업을 수행하는 방법을 알려주고 실제로 앱을 실행하도록 한다.

FX에선 컨테이너에 직접 액세스를 제공하지 않는다.

## Lifecycle

[FX 라이프사이클 문서](https://uber-go.github.io/fx/lifecycle.html)

FX의 앱 라이프사이클은 초기화와 실행이라는 상위 단계로 구성된다.

초기화 시 Fx는 전달된 모든 생성자를 등록한다 (`fx.Provide`), 전달된 모든 데코레이터를 등록한다 (`fx.Decorate`).

### Lifecycle Hook

라이프사이클 훅은 앱이 시작되거나 종료될 때 Fx가 실행할 작업을 예약하는 기능을 제공한다. 다음과 같은 주의사항을 유념하며 사용해야 한다.

- 훅은 장기 실행 작업을 동기적으로 실행하기 위해 메인 스레드를 차단하면 안 된다.
- 훅은 백그라운드 고루틴에서 장기 실행 작업을 예약해야 한다.
- 종료 훅은 시작 훅에서 시작된 백그라운드 작업을 중지해야 한다.

## Module

[FX 모듈 문서](https://uber-go.github.io/fx/modules.html)

Fx 모듈은 Fx 앱에 독립형 기능을 제공하는 공유 가능한 Go 라이브러리나 패키지이다. 이건 쓰다보면 이해하겠지.

# 기능

## Parameter Objects

[Fx 매개변수 객체 문서](https://uber-go.github.io/fx/parameter-objects.html)

매개변수 객체는 특정 함수나 메서드에 대한 매개변수를 전달하는 단일 목적을 가진 객체이다. 객체는 다른 함수와 공유하지 않는다.

```go
type ClientParams struct {
   fx.In

   Config     ClientConfig
   HTTPClient *http.Client
}

func NewClient(p ClientParams) (*Client, error) {
   return &Client{
       url:  p.Config.URL,
       http: p.HTTPClient,
       // ...
   }, nil

 // 이렇게 생성된 매개변수 생성 함수는 Provide에 제공한다.
 fx.Provide(New),
```

## Result Objects

[FX 결과 객체](https://uber-go.github.io/fx/result-objects.html)

결과 객체는 특정 함수나 메서드에 대한 결과를 전달하는 단일 목적을 가진 객체이다.

```go
type ClientResult struct {
   fx.Out

   Client *Client
}

func NewClient() (ClientResult, error) {
   client := &Client{
       // ...
   }
   return ClientResult{Client: client}, nil
}
```

## Annotate

[FX 주석 문서](https://uber-go.github.io/fx/annotate.html)

함수 어노테이션을 사용하면 함수에서 반환된 구조체 값을 다른 함수에서 사용하는 인터페이스로 캐스팅 할 수 있다.

```go
fx.Provide(
    fx.Annotate(
        NewHTTPClient,
        fx.ResultTags(`name:"client"`),
    ),
)
```

# 정리하며

실사용하면서 더 배운 내용이 있다면 추가하겠다. 문서만 보다보니 어떤 내용을 더 연구해야 할지 모르겠다.
