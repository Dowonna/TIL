## 📑커리큘럼

|     시간     |     과목     |
|:------------|:-----------:|
| 10~11시 | **KT Cloud 서비스 컴포넌트 소개** <br> KT Cloud 개요, 주요 컴포넌트 별 서비스 라인업 소개 |
| 11~12시 | **KT Cloud Hands On(UI/Open API기반 서비스 사용법 소개 및 시연)①** <br> 포탈 콘솔 사용법 소개 및 기본실습(서버/NW설정), 고가용성 웹서비스(LB기반) 구성 실습 |
| 12~13시 | <점심시간> |
| 13~15시 | **KT Cloud Hands On(UI/Open API기반 서비스 사용법 소개 및 시연)②** <br> 포탈 콘솔 사용법 소개 및 기본실습(서버/NW설정), 고가용성 웹서비스(LB기반) 구성 실습 |
| 15~16시 | **KT Cloud와 함께하는 SW 개발(DevTools)** <br> DevOps 개념 및 KT Cloud DevTools 소개 |
| 16~18시 | **KT Cloud Container Essential** <br> 컨테이너 기반 기술(컨테이너 전반 소개, Docker 및 K8S 이론/시연) & KT Cloud 컨테이너 Deep Dive(CaaS, DevOps Suite) |

---

## 1. KT Cloud 서비스 컴포넌트 소개

### KT Cloud Overview

- 대한민국 Cloud의 역사를 만들며 DX Platform Builder로 진화

- KT Cloud의 핵심 강점 3가지
    - KT만이 가능한 「Cloud + IDC + NW」 통합 서비스
    - 업종 별 특화된 E2E 맞춤 서비스
    - 10년 간 축적되어 성장해온 대규모 설계/운영 역량

- 다양한 산업 군의 7,000여 고객 사 이용 중

- 산업 영역 특성/다양한 사업 니즈에 유연하게 대응하기 위해, '고객 맞춤형' Cloud 서비스 제공 중

- 코로나19 이후를 위한 KT Cloud의 준비 = DX Platform

- DX로인한 고객 니즈 변화(플랫폼 수요)에 대응

- KT DX플랫폼의 차별점 - 검증된 솔루션, 사용자 편의성

- 참고. KT DX Core 플랫폼 Overview - AI Studio

- 참고. KT DX Core 플랫폼 Overview - Datalake

- 참고. KT DX Core 플랫폼 Overview - IoT

- 참고. KT DX Core 플랫폼 Overview - DevOps Suite

- KT Cloud가 걸어온 길, 나아갈 방향

### KT Cloud의 서비스 라인업을 소개합니다!

- KT Cloud 서비스 라인업(Computing, Storage, Network, VMware Cloud, Container...)

- KT Cloud 주요 서비스 컴포넌트

- Computing 서비스 라인업
    - KT Cloud가 제공해드리는 고품질/가성비 있는 가상화 서버

    - AMD EPYC 프로세서 기반, 성능/비용 혜택 Upgrade된 가상화 서버

    - 수요에 따라 탄력적(주기, 이벤트)으로 KT Cloud Server를 확장/축소

- Storage 서비스 라인업
    - **SSD Volume** | 다양한 워크로드의 요구 사항을 충족시킬 수 있는 SSD기반 Block Storage
    - **NAS** | S고성능 NAS를 KT Cloud Server와 함께 이용하도록 제공
    - **Object Storage** | 장기 백업/보관에 적합한 높은 확장성을 가진 스토리지 서비스

- Network 서비스 라인업
    - **VR** | 가상 서버의 안전한 NW 이용을 위한 서비스(모든 고객에 기본 제공)
    - **LB(Load Balancer)** | 특정 가상 서버에 트래픽이 집중되지 않도록 부하 분산 기능을 제공
    - **GSLB** | 멀티 존/서로 다른 물리적 사이트간의 가용성을 보장하기 위한 서비스
    - 참고. NW 서비스로 할 수 있는 것

- DB 서비스 라인업
    - **DBaaS for MySQL/MariaDB** | 관리 노력을 최소화하며 데이터 베이스(RDB)를 이용할 수 있는 서비스
    - 참고. DB 서비스 구성

- Management & Monitoring 서비스 라인업
    - **Infra Formation** | 가상서버/애플리케이션 구성 내역을 코드로 표현하고/자동 생성해주는 서비스
    - **Watch** | KT CLoud 인프라에 대한 감시/탐지/트리거 기능을 제공하는 모니터링 서비스
    - 참고. Watch에 기반한 서비스 시나리오

### KT Cloud Arch. Work Book

- 성능 효율성(탄력, 확장성)
    - Case: 온라인 이벤트 대응을 위한 Cloud 아키텍처
    - Architecture Sample

- 안정성 및 신뢰성(고가용성)
    - Case: 고가용성 보장이 가능한 웹 애플리케이션 아키텍처
    - Architecture Sample

### KT Cloud Hands-on(기본)

- 고객 시스템 환경 이해

- 시스템 부하 변동에 따른 Scaling 정책

- 이중화 전략 - VM 이중화

- 시스템 부하 변동에 따른 Scaling 정책

- 이중화 전략 - VM 이중화

- 이중화 전략 - VM 이중화(LB 사용)

- 이중화 전략 - Multi 계정을 통한 이중화(그룹 계정)

- 계정의 이중화/다중화, 그룹 계정

- 이중화 전략 - Multi Zone을 통한 이중화

- 