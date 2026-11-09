# NUMBER BASEBALL 3D 통합판 v1 — 검증 기록

## 통과한 검사

1. 통합 메뉴에서 CLASSIC은 2인용·1인 공격, FULL COUNT는 2인용·AI 대전·1인 공격을 제공함.
2. 6개 경기 HTML의 자바스크립트 문법 검사(`node --check`) 완료.
3. 통합 메뉴 및 6개 경기 HTML의 공용 에셋·메뉴 복귀 링크 확인.
4. `shared/runtime.js` 선수명단·구단 색상 데이터의 CLASSIC→FULL COUNT 및 FULL COUNT→CLASSIC 양방향 직렬화 테스트 통과.
5. FULL COUNT의 홈런 승리 규칙과 CLASSIC의 득점 승리 규칙이 각기 독립된 엔진에 보존된 구조 정적 검사 통과.
6. 공통 애니메이션 파일은 `shared/animation_engine.html` 하나로 합침.

## 남은 검증

- 이 환경의 Chromium 브라우저에서는 `http://127.0.0.1` 및 `file://` 주소가 `ERR_BLOCKED_BY_ADMINISTRATOR`로 차단됨. 브라우저 실화면 동작 검증, Three.js 3D 렌더링, 저장한 경기를 끝까지 진행하는 기능 테스트는 진행하지 못함.
- CLASSIC v42가 FULL COUNT v3.1에서 확장된 공용 3D 엔진의 모든 장면을 정상 재생하는지 실제 WebGL 테스트가 필요함.
- 통산 기록은 모드별로 분리하며 다른 버전의 이미 진행 중인 저장 게임 데이터를 자동 변환하지 않음.

## 범위

이 버전은 사용자 관점에서 하나의 메인 메뉴·공용 선수명단·공용 유니폼 설정·공용 애니메이션을 제공하며, 모드별 규칙 로직은 의도적으로 분리하여 보존합니다. 향후 공용 게임 판정 로직과 AI 코드 모듈화는 별도 리팩터링 단계입니다.

## v1.1 수정 검증

- CLASSIC AI 메뉴 및 인게임 링크 제거
- `classic/ai.html` 통합 배포 제외
- FULL COUNT AI 대전과 나머지 경기 기능 유지
- 통합 메뉴에서 모드 변경 시 표시되는 버튼 수 및 URL 검사
