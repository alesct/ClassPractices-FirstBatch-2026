# ────────୨ৎ────────
# FastAPI & Gradio: Quotes 프로젝트
# ────────୨ৎ────────

이 프로젝트는 FastAPI를 백엔드로 사용하고, Gradio를 이용해 사용자에게 친숙한 인터페이스를 제공하는 
명언 관리 및 조회 애플리케이션입니다.

## ╰┈➤.시작하기
VS Code를 사용하여 프로젝트를 설정하는 방법입니다.

## 𝟙.프로젝트 폴더 열기
VS Code를 실행하고 프로젝트 폴더를 엽니다.


## 𝟚.가상 환경 설정

프로젝트의 의존성을 분리하기 위해 가상 환경을 생성하고 활성화합니다.

터미널 열기: `Ctrl + Shift + `` (또는 상단 메뉴의 Terminal > New Terminal)

가상 환경 생성:
⋆python -m venv venv

가상 환경 활성화:
⋆.\venv\Scripts\activate

##𝟛. 필수 라이브러리 설치

FastAPI와 Gradio를 설치합니다.
⋆pip install fastapi uvicorn gradio

## 𝟜. 프로젝트 실행을 위한 파일 구성

### ᯓ★.  app.py              # Gradio UI 및 FastAPI 통합 메인 실행 파일
### ᯓ★.  client.py           # 클라이언트 요청 테스트 스크립트
### ᯓ★.  main_CRUD.py        # 데이터베이스 생성 및 CRUD 로직
### ᯓ★.  main_server.py      # FastAPI 서버 인스턴스 및 라우팅 설정
### ᯓ★.  quotes.db           # SQLite 데이터베이스 파일
### ᯓ★.  packages.txt        # 시스템 패키지 목록
### ᯓ★.  requirements.txt    # Python 라이브러리 의존성 파일

## 𝟝. 실행 및 배포

로컬 환경 실행 
로컬에서 프로젝트를 실행하면 http://127.0.0.1:8000 (localhost) 주소가 생성됩니다. 
이 주소는 개인 PC 내부에서만 접속이 가능하며 외부 공유는 불가능합니다.

↬가상 환경 활성화 후 python app.py 실행.

↬터미널에 나타나는 로컬 링크를 클릭하여 접속.

 ### 🤗Hugging Face 배포 
교수님과 동료들이 어디서든 접속할 수 있도록 Hugging Face Spaces를 통해 프로젝트를 배포하였습니다. 
아래 링크를 통해 실시간으로 시스템을 확인할 수 있습니다.

### ꩜실시간 데모 보기:
메인 사용자 인터페이스: [https://alesct1-midterm2555041.hf.space](https://alesct1-midterm2555041.hf.space)

명언 조회, 단어 수 확인 및 실시간 다국어 번역 기능을 제공합니다.

API 명세서 및 데이터 관리: [https://alesct1-midterm2555041.hf.space/docs](https://alesct1-midterm2555041.hf.space/docs)

명언의 생성, 수정, 삭제 등 백엔드 기능을 시각적으로 테스트할 수 있습니다.

## 𝟟. 결론

이 프로젝트는 고성능 FastAPI 백엔드와 직관적인 Gradio 인터페이스를 성공적으로 결합하여, 
누구나 쉽게 글로벌 명언을 분석하고 번역할 수 있는 환경을 구축하였습니다. 
특히 로컬 개발 환경의 한계를 넘어 Hugging Face 클라우드 배포를 통해 접근성을 극대화함으로써, 
사용자에게 별도의 설치 과정 없이도 실시간 데이터를 제공할 수 있는 완성도 높은 서비스를 구현했습니다. 
결과적으로 본 시스템은 효율적인 데이터 관리와 다국어 지원 기술이 조화를 이룬 스마트한 플랫폼으로서, 
향후 다양한 기능 확장을 위한 견고한 기반이 될 것입니다.




