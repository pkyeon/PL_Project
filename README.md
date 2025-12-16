# PL_Project
# 🐹 두더지 잡기 게임

Python과 tkinter를 활용해 제작한 두더지 잡기 게임입니다.  
난이도, 콤보 시스템, 랭킹 저장 기능 등을 설계하여 구현했습니다.

---

프로그램 기획 의도

강의 중 배운 python을 이용하여 게임을 만들어 보고자 함.

- 시간이 지날수록 빨라지는 난이도
- 두더지를 놓치면 끊기는 콤보 시스템
- 보너스 역할의 황금 두더지와 위험 요소인 폭탄
- 플레이 결과를 저장하는 랭킹 시스템

---

프로그램 기능 설명

1. 난이도 선택
- Easy / Hard 모드 제공
- Hard 모드는 점수 배점이 높고 속도가 더 빠르게 증가

---

2. 두더지 종류

| 🐹 일반 두더지 | 기본 점수 획득 |

| ⭐ 황금 두더지 | 높은 점수 획득 |

| 💣 폭탄 | 클릭 시 점수 감소 |

※ Windows / Linux 환경에서는 문자(M / G / X)와 색상으로 표시됩니다.

---

3. 콤보 시스템
- 일반 두더지를 연속으로 잡으면 콤보 증가
- 일반 두더지를 놓치면 콤보 초기화
- 황금 두더지는 놓쳐도 콤보에 영향 없음

---

4. 랭킹 시스템
- 게임 종료 시 점수를 TOP 5 랭킹으로 저장
- TOP 5에 새로 진입하면 ‘신기록 달성’ 알림 표시

---

5. 효과음 시스템

- 일반 두더지를 잡았을 때: 타격 효과음
- 황금 두더지를 잡았을 때: 보너스 효과음
- 폭탄을 클릭하거나 빈 칸을 클릭했을 때: 경고 효과음
- 게임 종료 시: 종료 알림 효과음

효과음 파일은 sounds 폴더에 포함되어 있으며,  
게임 실행 중 자동으로 재생됩니다.

---
 
6. 실행 환경
- Python 3.x
- macOS / Windows / Linux
- 추가 라이브러리 설치 필요 없음 (tkinter 사용)

---

7. 실행 결과
- 닉네임 설정 화면
<img width="268" height="126" alt="스크린샷 2025-12-16 오후 5 49 28" src="https://github.com/user-attachments/assets/fc947e72-19da-484d-a789-f8e23fdb40ef" />


- 메인 화면
<img width="447" height="423" alt="스크린샷 2025-12-16 오후 5 49 51" src="https://github.com/user-attachments/assets/c20c35d3-95dc-48c0-ae8a-935390fce45d" />


- 게임 실행 화면
<img width="447" height="423" alt="스크린샷 2025-12-16 오후 5 50 04" src="https://github.com/user-attachments/assets/587f73d0-f5b9-482d-8410-d11de736b84e" />



- 신기록 여부에 따른 게임 종료 화면
<img width="393" height="344" alt="스크린샷 2025-12-16 오후 5 52 42" src="https://github.com/user-attachments/assets/68644ca6-cc2e-4490-945c-1e929863d715" />

<img width="393" height="344" alt="스크린샷 2025-12-16 오후 5 51 30" src="https://github.com/user-attachments/assets/8cce1fd9-3d7b-4d8a-8e22-c8e1755cf44d" />


-실행 영상

※ macOS 기본 화면 녹화 기능 특성상 시스템 효과음은 영상에 포함되지 않았으나,
실제 실행 시에는 효과음이 정상적으로 재생됩니다.

https://github.com/user-attachments/assets/8611be89-18b3-417c-be68-002cd520ac22

https://github.com/user-attachments/assets/0bd60852-5691-4d47-b00d-703c4b7aa8e3





