---
title: "플랫폼 엔지니어링과 IDP, 그리고 Backstage 구성 살펴보기"
excerpt: "Platform Engineering이 다시 주목받는 이유, 개발자 포털(IDP)의 역할, Backstage의 핵심 구성 요소와 운영 포인트를 간단히 정리했습니다."
categories:
  - Platform-Engineering
tags:
  - Platform Engineering
  - IDP
  - Backstage
  - DevOps
  - Cloud Native
toc: true
---

플랫폼 엔지니어링(Platform Engineering)은 **제품 팀이 맡은 서비스 개발과 운영에 집중할 수 있도록 내부 플랫폼을 설계·제공하는 일**입니다. DevOps 이후의 대안이 아니라, “실제로 쓰고 싶은 플랫폼을 만드는 방법론”이라는 점이 핵심이죠. 최근 수년간 조직 규모가 커지고, 마이크로서비스와 SaaS 도구가 폭증하면서 개발자들이 감당해야 할 툴과 절차도 복잡해졌습니다.  

이 글에서는 플랫폼 엔지니어링이 왜 다시 주목받는 흐름인지, 그 중심에 있는 **개발자 포털(IDP)** 은 무엇인지, 그리고 우리가 실험하면서 정리한 [Backstage](https://backstage.io/) 구성과 운영 포인트를 공유합니다.

## 1. 플랫폼 엔지니어링이 다시 주목받는 이유

플랫폼 엔지니어링은 다음과 같은 문제를 해결합니다.

- **경험(Developer Experience) 단순화:** 개발자가 서비스를 만들고 배포할 때 필요한 정보를 한곳에서 제공.
- **가이드와 거버넌스:** 표준 인프라, 템플릿, 보안 정책을 일관성 있게 강제.
- **셀프서비스(Self-Service):** 인프라/CI/CD 구성, 문서, 액세스 요청을 자동화하여 플랫폼팀의 반복 작업을 줄임.

DevOps가 “팀 간 협업 문화”였다면, 플랫폼 엔지니어링은 **협업을 가능하게 만드는 제품(Platform)** 을 만드는 일이라고 이해하시면 됩니다.

## 2. IDP(Internal Developer Portal)란?

IDP는 조직 내부 개발자가 사용하는 웹 포털로서, 다음과 같은 기능을 포함합니다.

1. **서비스 카탈로그:** 현재 운영 중인 서비스, 팀, 오너, 린트/정책 상태를 한눈에 확인.
2. **셀프 서비스 템플릿:** Terraform/Helm 등으로 신규 인프라나 애플리케이션을 자동으로 생성.
3. **문서/지식 허브:** 운영 매뉴얼, Runbook, TechDocs를 한 곳에서 검색.
4. **워크플로 집약:** 배포 상태, 모니터링 대시보드, 알림을 포털 내에서 연결.

IDP를 제대로 구축하려면 다양한 시스템을 통합해야 합니다. 직접 모든 것을 만드는 대신, **CNCF가 관리하는 오픈소스 Backstage**를 많이 사용합니다.

### 2-1. 대표 IDP 솔루션 비교

| 제품 | 라이선스/비용 | 제공 방식 | 강점 | 고려사항 |
|------|---------------|-----------|------|----------|
| **Backstage** (Spotify) | 오픈소스 (Apache 2.0) | 자가 호스팅 | 플러그인 생태계, 대규모 커뮤니티, CNCF Incubating | 설치·운영 책임 필요 |
| **Port** | 상용 (SaaS 요금제) | 클라우드 | 직관적 UI, 워크플로 자동화, 빠른 온보딩 | 사용량 기반 과금, 커스터마이징 제약 |
| **HashiCorp Waypoint** | 상용(SaaS 요금제) | 자가 호스팅 | Terraform/Vault 등 HashiCorp 도구와 자연스러운 연동 | Web 포털 기능이 제한적, HashiCorp 에코시스템 의존 |
| **Humanitec Platform Orchestrator** | 상용 | SaaS/Hybrid | 환경·인프라 관리 자동화, RBAC | 비용·벤더 종속성 고려 필요 |

<div style="display:flex; gap:20px; align-items:center; flex-wrap:wrap; margin: 16px 0 8px 0;">
  <img src="https://github.com/cncf/artwork/blob/main/projects/backstage/icon/color/backstage-icon-color.png?raw=true" alt="Backstage Logo" width="100p" />
  
  <img src="https://cdn.prod.website-files.com/622996415264e2107087774c/65f708f88d3d97e8059c6b90_Share%20image.jpg" alt="Port Logo" width="200" />
  <img src="https://www.hashicorp.com/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1714513406-blog-library-product-hcp-waypoint.jpg&w=3840&q=75" alt="HashiCorp Logo" width="150" />
  
  <img src="https://developer.humanitec.com/Humanitec_icon.svg" alt="HashiCorp Logo" width="130" />
</div>

**Backstage를 선택한 이유**

- 오픈소스이면서도 CNCF 생태계를 기반으로 꾸준히 발전하고 있습니다.
- Scaffolder·TechDocs 등 플랫폼 엔지니어링에 필요한 구성 요소가 한 틀 안에 들어 있습니다.
- 우리가 실험 중인 Terraform/GitHub Actions 파이프라인과 쉽게 통합되었습니다.


## 3. Backstage 한눈에 보기

Backstage는 Spotify가 내부 플랫폼을 외부에 공개한 프로젝트로, CNCF Incubating 단계에 있습니다.  
주요 특징은 다음과 같습니다.

- **Software Catalog:** YAML 기반 메타데이터로 시스템/서비스/팀 정보를 관리.
- **Scaffolder:** Software Template을 활용해 Terraform, Helm, 앱 스켈레톤 등을 자동 생성.
- **TechDocs:** Markdown+MkDocs 기반 문서화를 Backstage에서 호스트.
- **Plugin 구조:** Search, Kubernetes, Grafana 등 다양한 플러그인을 붙여서 확장.
- **프론트/백 분리:** `packages/app`(React) + `packages/backend`(Node) 구조로 커스텀 플러그인을 개발하기 쉬움.

Spotify 내부에서 “Golden Path”를 제공하던 노하우가 녹아 있어서 IDP를 빠르게 구축하기에 좋은 출발점이 됩니다.

## 4. Backstage 구성 요소 요약

| 구성 요소 | 역할 | 커스터마이징 포인트 |
|-----------|------|---------------------|
| **App (packages/app)** | React 기반 UI | 라우팅, 메인 페이지, 커스텀 플러그인 |
| **Backend (packages/backend)** | Plugin orchestration, API | `src/index.ts`에서 플러그인 등록, `app-config*.yaml`로 환경 지정 |
| **Software Catalog** | 서비스/팀 메타데이터 저장소 | `catalog-info.yaml` / YAML 스키마 |
| **Scaffolder** | 템플릿을 통한 자원 생성 | `examples/template`와 설정 (`catalog.locations`) |
| **TechDocs** | 개발 문서 뷰어 | Markdown + MkDocs, S3/GCS 등 외부 스토리지 연동 가능 |
| **Plugins** | 검색, 알림, Kubernetes 등 | npm 패키지 설치 후 백엔드/프론트에 로딩 |

우리 저장소에는 Terraform을 이용한 EC2 데모 템플릿을 넣어 두었고, GitHub Actions 파이프라인까지 자동 구성하도록 시연 중입니다.

## 5. 포털 운영 Quick Start

실험하면서 정리해 둔 Markdown 가이드를 바탕으로, Backstage를 로컬에서 올려보려면 아래 순서를 따라가면 됩니다.

```bash
# 의존성 설치 및 백엔드 빌드
yarn install
yarn build:backend

# 로컬 개발 모드
yarn dev
# or Docker 이미지 빌드 후 실행
yarn build-image
docker run -d -p 7007:7007 --name backstage-demo backstage:latest
```

프로덕션 배포나 템플릿 구조, CI/CD 파이프라인 정리는 다음 문서를 참고하세요.

- [② Backstage 설치 & 템플릿 환경 구성](/2025/10/30/backstage-setup-guide/)
- [③ Docker 배포 & 파이프라인 운영](/2025/10/30/backstage-deployment-guide/)

## 6. 마치며

플랫폼 엔지니어링은 “새로운 타이틀”이 아니라 **직접 써보고 싶은 플랫폼을 만드는 실용적인 접근**입니다. Backstage는 IDP를 빠르게 경험해볼 수 있는 좋은 도구이며, 실제 도입 시에는 조직 문화와 거버넌스를 함께 설계해야 완성됩니다.

앞으로는 Backstage를 IDP로 운영하면서 발생한 인사이트와, Terraform 템플릿/CI 파이프라인을 더 고도화한 경험도 공유해볼 예정입니다. 질문이나 피드백은 언제든지 환영합니다!
