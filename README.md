YOLO11 + VLM(언어 생성 보조) 하이브리드 구조 기반 AI CCTV 통합 관제 시스템 연구 (안정화 작업)</br>
</br>
주요 작업 내용</br>
① 영상 분석 엔진 개발</br>
  - 6채널 CCTV 영상 동시 처리</br>
  - YOLO기반 객체 탐지(비전영역)를 활용하여 사람 및 객체 인식</br>
  - 탐지 결과(인원 수 등)를 기반으로 이벤트 감지 로직 수행</br>
  - 이벤트 발생 시 이미지 캡쳐 및 로그 기록</br>
</br>
② VLM 기반 상황 설명 생성</br>
   - YOLO로 분석된 결과를 입력으로 활용</br>
   - VLM(Visual-Language Model)을 통해 자연어 설명 생성</br>
   - 단순 이벤트 데이터를 사람이 이해하기 쉬운 문장으로 변환</br>
</br>  
③ 관제 대시보드 개발</br>
   - Streamlit 기반 실시간 UI 구성</br>
   - 6채널 CCTV 영상 실시간 표시</br>
   - 이벤트 로그(CSV) 표시</br>
   - 이벤트 선택 시 이미지 및 상세 분석 결과 확인</br>
   - 이벤트 통계 제공</br>
</br>
④ 시스템 안정화 및 성능 개선</br>
   - 이미지 저장 충돌 문제 해결 (파일 구조 개선)</br>
   - CSV 동시 접근 안정화</br>
   - 실시간 영상 갱신 구조 개선</br>
   - 예외 처리 및 오류 복구 로직 추가</br>
</br>
결론</br>
   - YOLO를 활용한 빠른 실시간 객체 탐지를 통해 영상 내 객체를 신속하게 인식</br>
   - VLM을 활용한 지능형 상황 설명 생성을 통해 분석 결과를 자연어로 해석 및 전달</br>
   - 6채널 멀티 CCTV 실시간 관제를 통해 다양한 영상 소스를 동시에 통합 관리</br>
   - 이벤트 기반 로그 및 통계 관리를 통해 발생 상황을 체계적으로 기록 및 분석</br>
</br>
실행</br>
   ① 6채널 CCTV 영상을 실시간으로 분석하여 객체 탐지(YOLO), 이벤트 판단, VLM 기반 상황 설명 생성 및 로그 저장을 수행하는 관제 엔진 실행</br>
     - CCTV 영상(6채널)을 입력받아 ai_engine_multi.py에서 실시간으로 프레임을 처리</br>
     - YOLO 기반 객체 탐지를 통해 사람 및 객체를 인식하고 인원 수를 계산</br>
     - 탐지 결과를 기반으로 이벤트 발생 여부를 판단 (예: 인원 과다 등)</br>
     - 이벤트 발생 시 해당 프레임을 이미지로 저장하고 이벤트 로그(CSV)에 기록</br>
     - VLM을 활용하여 이벤트 상황을 자연어 형태로 설명 생성</br>
     - 처리된 최신 프레임을 관제용 이미지로 저장하여 대시보드에서 활용</br>
   </br>
   python ai_engine_multi.py</br>
   </br>
   <img width="699" height="314" alt="image" src="https://github.com/user-attachments/assets/f9fa6ae4-4d86-44b6-9f3f-488faa189dbf" />
   </br>
   <img width="1908" height="747" alt="image" src="https://github.com/user-attachments/assets/50d64914-eb14-4ed1-ba00-72a9a0adbd64" /></br>
   </br> 
   ② 관제 대시보드</br> 
     - dashboard.py를 실행하여 Streamlit 기반 관제 화면 구동</br>
     - 저장된 최신 CCTV 이미지(6채널)를 불러와 실시간으로 화면에 표시</br>
     - 이벤트 로그(CSV)를 읽어 이벤트 리스트 및 상세 정보 출력</br>
     - 사용자가 이벤트를 선택하면 해당 이미지와 VLM 분석 결과를 확인</br>
     - 이벤트 데이터 기반 통계(유형별, 카메라별)를 시각화하여 제공</br>
     - 일정 주기로 자동 새로고침하여 실시간 관제 환경 유지</br>
   </br>
   </br>
   streamlit-autorefresh 패키지 설치 후 실행</br> 
   pip install streamlit-autorefres</br> 
   </br>
   streamlit run dashboard.py</br>   
   </br>
   외부 접근 명령어 : ngrok http 8501</br>
   https://khalilah-implacental-kimora.ngrok-free.dev/</br>
   </br>
   <img width="1109" height="627" alt="image" src="https://github.com/user-attachments/assets/14887f1a-6fda-4cab-8fe4-92abbd4642b0" /></br>
   </br>
   </br>
   <img width="796" height="126" alt="image" src="https://github.com/user-attachments/assets/a5dec09a-55be-43fa-82aa-f3fb1c39bc03" /></br>
   </br>
   <img width="1911" height="981" alt="image" src="https://github.com/user-attachments/assets/9e3c551c-009c-494d-8701-6cedfb4b8efd" /></br>
   </br>
   <img width="1780" height="400" alt="image" src="https://github.com/user-attachments/assets/5c9bf3d0-333f-48d5-a25b-44c8a44f2b11" /></br>
   </br>
   <img width="1765" height="408" alt="image" src="https://github.com/user-attachments/assets/d2410fec-9c8e-47db-8a8f-aab948f8b0e3" /></br>
   </br>
   </br>
   </br>
   ※ YOLO와 같은 경량 객체 탐지 모델을 사용하지 않고, VLM(Visual-Language Model)기반 컴퓨터 비전만으로 6개 채널 CCTV 영상을 실시간 분석하여 객체 탐지 및 이벤트 판단을 수행하려 하였으나, 프레임 단위로 발생하는 대량의 API 호출로 인해 쿼터 초과(비용 및 호출 제한) 문제가 발생하였다. 이로 인해 VLM 단독으로는 다채널 실시간 영상 분석을 안정적으로 처리하기 어려워, 해당 방식은 실질적인 운영이 불가능한 것으로 판단된다.</br>
   </br>
   <img width="1258" height="176" alt="image" src="https://github.com/user-attachments/assets/e620c684-70da-43eb-8eb9-ccbadd1b1602" />
   </br>
   - 해결방법</br>
     ① API 정싱 시용할려면 OpenAPI 유료 결재하고 Billing 등록 후 해결하는 방법</br>
     ② 구조적으로 해결</br>
       방법 A : 호출 제한</br>
       방법 B : 테스트 모드</br>
                (vlm_model.py 임시 변경)</br>
       방법 C : 이벤트 기반 호출</br>
                영상 → 변화 감지 (Motion) → 이상 상황 발생 시만 → VLM 호출</br>
       방법 D : 로컬 VLM (API 제거)</br>
            - LLaVA</br>
            - BLIP-2</br> 
            </br> 
            → C 방법으로 적용</br>
              VLM 역할은 이미지 이해 (사람 있음 / 상황 설명), 자연어 생성</br>
                 ※  VLM은 “객체를 정밀하게 추출하는 모델”이 아니라 “장면을 이해하고 설명하는 모델”입니다.</br>
                 ※  OpenAI API 없이 “VLM만으로 객체 추출(탐지)”은 제한적으로만 가능하며, YOLO 수준의 정확한 객체 탐지는 사실상 어렵습니다.</br>
                 </br>
               <img width="1252" height="189" alt="image" src="https://github.com/user-attachments/assets/34e82578-92b2-402f-9ea2-78b3f3eacbaa" /></br>
   
