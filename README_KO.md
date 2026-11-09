# NUMBER BASEBALL 3D — UNIFIED EDITION v1

이 패키지는 기존 **CLASSIC v42**와 **FULL COUNT v3.1**을 하나의 메인 메뉴 안에 통합한 브라우저 게임입니다.

## 시작하기

압축을 해제한 뒤 **최상위 `index.html`**을 실행하세요. CLASSIC / FULL COUNT 모드와 2인용 대전 / AI 대전 / 1인 공격을 선택할 수 있습니다. 파일 하나만 따로 옮기면 공용 자산을 찾지 못할 수 있으므로 **전체 폴더 구조를 유지**하세요. 저장소 기능이 정상적으로 작동하지 않는 브라우저에서는 로컬 웹 서버로 실행하면 안정적입니다. 고화질 3D는 인터넷 연결을 사용합니다.

## 통합 구조

```text
index.html             통합 메인 메뉴
shared/runtime.js      공용 KBO 팀 색상 / 팀 선수명단 저장 및 버전 호환
shared/animation_engine.html 공용 3D 경기장 · 애니메이션
shared/KBO_2026_3games_roster_checked.csv 참고 데이터
classic/index.html     기존 v42 2인용 경기
classic/ai.html        기존 v42 AI 대전
classic/attack.html    기존 v42 1인 공격
fullcount/index.html   FULL COUNT v3.1 2인용 경기
fullcount/ai.html      FULL COUNT v3.1 AI 대전
fullcount/attack.html  FULL COUNT v3.1 1인 공격
```

## 규칙 차이

- CLASSIC은 원래 v42 **일반 득점** 승리 규칙을 유지합니다.
- FULL COUNT는 **3S 홈런 개수**로 승패를 결정하고 일반 득점은 경기 정보로 표시합니다.
- FULL COUNT는 볼넷 후 부분 숫자 변경이 없으며, 홈런 후 수비 3자리 변경권·누적 6F 추가 아웃 폐지·피치클락 첫 60초/이후 45초를 유지합니다.
- CLASSIC은 FULL COUNT 전용 규칙을 강제로 적용하지 않았습니다.

## 공용 설정과 독립 데이터

- **공유**: 공용 선수명단, 구단 색상 프리셋, 최신 통합 3D 중계 엔진.
- **분리**: 2인용/AI/1인 게임 로직, 경기 저장, 통산 기록, 모드별 숫자 판정과 승리 조건. 두 게임의 인게임 비밀 숫자는 공유하지 않습니다.
- 어느 모드에서든 **선수명단 저장**을 누르면 통합 저장소 `nb3d-unified-roster-v1`도 갱신됩니다. 다음 모드의 선수명단 준비 화면에서 같은 내용을 확인할 수 있습니다.
- 이전 CLASSIC·FULL COUNT 명단은 통합 메뉴의 **이전 버전 명단 가져오기** 버튼을 통해 가져올 수 있습니다. 과거 게임 저장·통산 기록은 기존 키를 유지합니다.
- 최신 FULL COUNT에서 제작한 팀 색상 설정을 CLASSIC 선발명단 화면에도 이식했습니다. 공통 3D 엔진으로 두 모드에 같은 팀 색상을 전달합니다.

## 개발 방식

규칙과 AI 설계가 상당히 다른 두 버전은 현재 각각의 **모드 엔진**으로 분리하고, 공용 UI·설정·데이터·애니메이션을 중앙화했습니다. 따라서 단일 엔진으로 100% 재작성한 형태는 아니며, 향후 공통 게임 로직을 단계적으로 별도 모듈로 추출하기 위한 안정적인 통합판입니다.

## 기술/검증 유의 사항

모든 HTML 게임은 외부 Three.js 로딩에 의존합니다. 로컬 브라우저의 `file://` 환경에 따라 저장소 접근이 다르게 처리될 수 있습니다. 이 경우 `python -m http.server 8000`을 통합판 폴더에서 실행하고 `http://localhost:8000`을 열어주세요. 예전 저장 파일은 자동 삭제하지 않습니다.
