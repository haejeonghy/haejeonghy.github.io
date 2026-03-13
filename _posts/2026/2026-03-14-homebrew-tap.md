---
layout  : post
title   : Homebrew의 brew tap은 왜 필요한가
summary : solidity 설치 과정에서 사용한 brew tap 명령의 역할과 Homebrew repository, formula 구조를 정리합니다.
date    : 2026-03-14 00:50:00 +0900
updated : 2026-03-14 00:50:00 +0900
tag     : homebrew tap macos
toc     : true
comment : false
public  : true
---
* TOC
{:toc}

## 발단

solidity를 설치하는 과정에서 `brew tap ethereum/ethereum` 명령을 실행한 후 solidity를 설치했다. 기존에는 다른 패키지를 `brew install` 명령만 실행하여 설치했는데, `tap` 명령은 어떤 용도로 사용되는지 궁금해 조사하게 되었다.

## 공식 문서

brew 공식 문서에서는 `tap` 명령을 다음과 같이 설명한다.

`brew tap` 명령은 Homebrew에서 추적, 업데이트, 설치하는 공식 목록에 더 많은 repository를 추가한다. 기본적으로 tap repository는 Github에서 가져오지만, 해당 명령은 한 개의 위치로 제한되지 않는다.

`brew tap <user/repo>` 명령은 `https://github.com/<user>/homebrew-<repo>` 의 repository를 `$(brew --repository)/Library/Taps`에 클론한다. 그 후 Homebrew의 `homebrew/core` 정식 저장소에 있는 것처럼 해당 formula로 작업할 수 있다. `[un]install` 을 사용하여 설치 및 제거할 수 있으며, formula는 `brew update` 시 자동으로 업데이트 된다.

## 조사

Homebrew는 macOS 용 패키지 관리 애플리케이션이다. 주로 커맨드 라인 도구나 시스템 패키지를 설치하는 데 사용한다.

그렇다면 brew repository는 뭘까?

Homebrew를 설치하면 기본적으로 Homebrew-core repository가 설치되는데, 이 repository에 `brew install`로 설치할 수 있는 formula가 저장되어 있다.

formula는 ruby로 작성된 패키지 정의로, 해당 ruby 파일의 내용은 다음과 같다.

```ruby
class Foo < Formula
  desc ""
  homepage ""
  url "https://example.com/foo-0.1.tar.gz"
  sha256 "85cc828a96735bdafcf29eb6291ca91bac846579bcef7308536e0c875d6c81d7"
  license ""

  # depends_on "cmake" => :build

  def install
    # ENV.deparallelize
    system "./configure", "--disable-debug",
                          "--disable-dependency-tracking",
                          "--disable-silent-rules",
                          "--prefix=#{prefix}"
    # system "cmake", ".", *std_cmake_args
    system "make", "install"
  end

  test do
    system "false"
  end
end
```

이 formula를 사용하여 패키지를 설치할 수 있다.

그러므로 `brew tap ethereum/ethereum` 명령을 실행하여 `https://github.com/ethereum/homebrew-ethereum` git repository를 Homebrew에서 접근할 수 있는 repository로 추가하고, `brew install solidity`를 실행해 `homebrew-ethereum` repository에 저장된 solidity formula를 통해 solidity 패키지를 설치할 수 있었다.

![homebrew-ethereum repository에서 solidity formula 확인](https://velog.velcdn.com/images/haejeonghy/post/1ec2100d-d4ed-4a2f-ab45-e27bf3907daf/image.png)

## 평가

mac을 사용하기 시작하면서 Homebrew를 자연스럽게 사용하고 있었는데, Homebrew가 어떻게 동작하는지 생각해 본 적이 없었다. 이번에 궁금했던 점을 해결하다 보니 tap을 사용하여 repository를 추가하면 `homebrew/core`에서 패키지 전체를 관리하는 것보다 관리가 편할 것 같다는 생각이 들었다. 갈수록 기술은 편리하고 효율적으로 발전하고 있는 것 같아 재밌었다.

## 참고 문헌

- https://docs.brew.sh/Taps
- https://www.44bits.io/ko/keyword/homebrew
