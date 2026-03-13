---
layout  : post
title   : 왜 gomock 대신 vektra/mockery를 고려하는가
summary : mockery 문서를 기준으로 gomock 대비 장점과 기본 yaml 옵션을 간단히 정리한 노트입니다.
date    : 2026-03-14 01:10:00 +0900
updated : 2026-03-14 01:10:00 +0900
tag     : golang test mockery
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

![](https://velog.velcdn.com/images/haejeonghy/post/a1049bbb-a72a-49d3-88a2-9c900aae72e2/image.png)

# 왜 vektra/mockery인가?

현재 회사에서는 gomock을 사용해서 mock 파일을 생성하고 테스트에 사용한다. 그러던 중 mockery를 사용해서 테스트 작업을 개선해보자는 의견이 나와서 mockery에서 제공하는 문서를 읽고 간략히 정리하며 실습해봤다.

## mockery의 장점

> 왜 gomock 대신 mockery를 쓰나요?
>
> mockery는 훨씬 더 사용자 친화적인 API를 제공하며 사용하기가 덜 혼란스럽습니다.  
> mockery는 견고하고 기능이 풍부한 테스트 프레임워크를 활용합니다.  
> mockery에는 모의가 생성되는 방식을 세부적으로 제어할 수 있는 풍부한 구성 옵션이 있습니다.  
> mockery의 CLI는 더욱 강력하고 사용자 친화적이며 더 많은 옵션을 제공합니다.  
> mockery는 제네릭을 지원합니다.

위 내용은 [mockery 문서](https://vektra.github.io/mockery/latest/)에 명시되어 있다.

1. mockery를 사용할 때는 `gomock.NewController()` 같은 반복되는 초기화 설정이 필요 없고, mockery를 실행해서 자동으로 만들어지는 메서드를 사용할 수 있다. 매번 테스트 코드를 작성할 때마다 필요한 초기화를 한 줄이라도 줄일 수 있다. 또 파일 하나하나에 대한 Mock 파일명 변경 같은 반복작업을 생략할 수 있다.
2. mockery는 yaml 파일을 통해 mocking 옵션을 세세하게 설정할 수 있다.
3. gomock은 아직 제네릭을 완전하게 지원하지 않는데, mockery는 제네릭을 지원한다.

# mockery yaml 옵션

- https://vektra.github.io/mockery/latest/examples/
- https://vektra.github.io/mockery/latest/configuration/

옵션을 보고 있는데, 실제 사용하면서 실용적인 옵션이 생기면 그때 정리하려고 한다.

example 실습하면서 사용한 yaml 옵션은 다음과 같다.

```yaml
quiet: False # mockery 실행 시 출력되는 정보(로그, 진행 상황)를 억제하지 않고 출력
disable-version-string: True # 생성된 모킹 파일 상단에 버전 정보를 포함하지 않음
with-expecter: True # EXPECT() 메서드를 생성하여 기대 동작 설정 가능
outpkg: mocks # 생성된 모킹 코드 패키지 이름을 mocks로 설정
```
