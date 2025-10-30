---
title: "Backstage 실험 기록 ③ - Docker 배포와 파이프라인 운영"
excerpt: "Backstage를 Docker 이미지로 빌드해 운영 환경에 배포하고, Terraform 데모 워크플로를 검증하는 과정을 정리했습니다."
categories:
  - Platform-Engineering
tags:
  - Backstage
  - Deployment
  - Docker
  - CI/CD
  - Terraform
  - Platform Engineering
  - IDP
toc: true
---

> **Backstage 실험 기록 시리즈**
> ① 플랫폼 & IDP 소개 · ② 설치/환경 구성 · **③ Docker 배포 & 파이프라인 운영** (현재 글)

## 1. 사전 준비

| 항목 | 버전/설명 |
|------|-----------|
| Node.js | 22.x (또는 20.x) |
| Yarn | 4.4.x |
| Docker | 최신 |
| GitHub PAT | `repo`, `workflow` 권한 |

로컬에서 템플릿을 테스트하려면 [설치 가이드(2편)](/2025/10/30/backstage-setup-guide/)를 먼저 완료하세요.

## 2. Docker 이미지 빌드

```bash
# 백엔드 번들 작성
yarn build:backend

# Docker 이미지 생성
yarn build-image

# 확인
docker images | grep backstage
```

빌드된 이미지는 `backstage:latest` 이름으로 로컬에 저장됩니다.

## 3. 컨테이너 실행 & 점검

```bash
# 실행
docker run -d -p 7007:7007 --name backstage-demo backstage:latest

# 로그 모니터링
docker logs -f backstage-demo

# 상태 체크
curl -I http://localhost:7007
```

정상적으로 올라오면 `Listening on :7007` 로그가 출력되고, 브라우저에서 `http://localhost:7007`으로 접속할 수 있습니다.

## 4. Terraform 데모 파이프라인 복습

Backstage에서 템플릿을 실행하면 `terraform.yml` GitHub Actions 워크플로가 함께 생성됩니다.

| 액션 | 트리거 | 설명 |
|------|--------|------|
| `plan` | PR 또는 수동 실행 | 포맷/검증 후 Plan 수행, PR에 결과 코멘트 |
| `apply` | main 브랜치 push, `workflow_dispatch` + `action=apply` | Plan 아티팩트를 내려받아 실제 배포 수행 |
| `destroy` | `workflow_dispatch` + `action=destroy` | Plan 없이 즉시 Destroy 수행 |

Secrets(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)가 구성돼 있지 않으면 `aws-actions/configure-aws-credentials` 단계에서 실패합니다.

## 5. 문제 해결 메모

| 증상 | 조치 |
|------|------|
| `Region is not valid: {{ values.aws_region }}` | 템플릿에서 `${{ ... }}` 패턴을 유지했는지 확인 |
| `Credentials could not be loaded` | GitHub Org/Repo Secrets 상속 여부 점검 |
| 템플릿 repo를 덮어쓰지 못함 | `github:repo:push` 사용 (이미 템플릿에 적용됨) |
| 반복 테스트가 번거롭다 | `./reset-terraform-demo.sh`로 repo 초기화 |

## 6. 다음 단계

- **EC2 데모 템플릿 커스터마이징:** Terraform 모듈·워크플로에 원하는 리소스를 추가해 보세요.
- **TechDocs 도입:** 엔지니어링 Runbook을 Markdown으로 작성해 Backstage에서 바로 열람.
- **Kubernetes / Observability 플러그인 연동:** 플랫폼 가시성을 높여 개발팀 경험을 개선.

---

> 시리즈 정리
> - [① 플랫폼 엔지니어링과 Backstage 소개](/2025/10/30/platform-engineering-idp-backstage/)
> - [② Backstage 설치 & 템플릿 환경 구성](/2025/10/30/backstage-setup-guide/)
> - **③ Docker 배포 & 파이프라인 운영 (현재 글)**
