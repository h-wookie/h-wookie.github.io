---
title: "Backstage 실험 기록 ② - 설치와 템플릿 환경 구성"
excerpt: "Backstage 개발 환경을 빠르게 올리고, Terraform EC2 데모 템플릿을 셀프서비스로 제공하기까지 필요한 설정을 정리했습니다."
categories:
  - Platform-Engineering
tags:
  - Backstage
  - Setup
  - Scaffolder
  - Terraform
  - Platform Engineering
  - IDP
toc: true
---

> **Backstage 실험 기록 시리즈**
> ① 플랫폼 엔지니어링 & IDP 개요 · **② 설치/환경 구성** · ③ Docker 배포 & 파이프라인 운영

## 1. 준비물 체크리스트

| 항목 | 권장 버전 | 메모 |
|------|-----------|------|
| Node.js | 22.x (20 이상) | `nvm install 22`로 손쉽게 설치 |
| Yarn | 4.4.x | `corepack enable && corepack prepare yarn@4.4.1 --activate` |
| Docker | 최신 버전 | 이미지 빌드 및 실행에 사용 |
| Git / jq | 최신 | GitHub API 스크립트 실행, 템플릿 자동화 |

GitHub Personal Access Token(PAT)은 로컬 환경 변수로만 주입합니다.

```bash
export GITHUB_TOKEN="ghp_xxx"          # repo, delete_repo, workflow 권한 필요
export GITHUB_OWNER="kr-backstage"     # 조직 또는 사용자
export GITHUB_OWNER_TYPE="org"         # 개인 계정이면 user
```

## 2. Backstage 프로젝트 생성 & 로컬 실행

```bash
npx @backstage/create-app@latest my-backstage-app
cd my-backstage-app

# 의존성 설치 후 로컬 개발 서버 실행 (프론트 3000 / 백엔드 7007)
yarn install
yarn dev
```

백엔드만 확인하고 싶다면 `yarn start-backend`를 사용하세요.

## 3. Docker 이미지 빌드와 검증

```bash
yarn build:backend
yarn build-image

docker run -d -p 7007:7007 --name backstage-demo backstage:latest
docker logs -f backstage-demo
```

이미지 빌드 전 `app-config.production.yaml`이 실제 템플릿 경로(`./examples/...`)를 가리키는지 확인하세요.

## 4. GitHub 저장소 자동화 스크립트

데모를 반복하기 위해 repo를 지우고 다시 만드는 작업을 자동화했습니다.

```bash
./reset-terraform-demo.sh          # terraform-demo (기본값)
./reset-terraform-demo.sh my-repo  # 원하는 이름으로 생성
```

필수 환경 변수는 앞서 설정한 `GITHUB_*` 값을 사용합니다. 스크립트는 기존 repo 삭제 → 새 public repo 생성 → 기본 브랜치 초기화를 처리합니다.

## 5. 필수 설정 정리

### 5.1 `app-config.yaml`
```yaml
catalog:
  locations:
    - type: file
      target: ../../examples/template/terraform-template.yaml
      rules:
        - allow: [Template]
```
`integrations.github[0].token`은 `${GITHUB_TOKEN}`으로 두고, 실제 값은 환경 변수로 주입합니다.

### 5.2 `app-config.production.yaml`
- 컨테이너 경로 기준으로 동일한 카탈로그 위치
- 데모 환경은 SQLite 인메모리를 사용하도록 유지 (`better-sqlite3`)

### 5.3 백엔드 플러그인 (`packages/backend/src/index.ts`)
- Scaffolder, GitHub, Notifications 등 주요 플러그인이 미리 활성화돼 있습니다.
- 플러그인을 추가/제거하면 `yarn build:backend`로 다시 번들링해야 합니다.

## 6. Terraform 템플릿 사용 가이드

Backstage UI → **Create Component** → `Terraform EC2 Demo with CI/CD` 템플릿 선택 후 아래 항목을 입력합니다.

| 입력 값 | 설명 |
|---------|------|
| Project Name | GitHub repo 및 AWS 자원 prefix (20자 이내, 영문/숫자/하이픈) |
| Description | 생성할 인프라 설명 |
| AWS Region | 드롭다운에서 `ap-northeast-2` 등 선택 |
| Repository | `RepoUrlPicker`로 조직 내 비어 있는 repo 지정 |

### 6.1 템플릿 치환 규칙 체크

- `${{ ... }}` 패턴은 Nunjucks가 값을 치환합니다. (`aws-region: '${{ values.aws_region }}'` → `'ap-northeast-2'`)
- GitHub Expression이 그대로 남아야 할 때는 `{% raw %}...{% endraw %}` 로 감쌉니다.
- `secrets.*` 접근도 동일한 규칙을 따릅니다.

### 6.2 GitHub Actions 요약

`terraform.yml` 워크플로는

1. `plan` (PR 코멘트 포함) → 2. `apply` → 3. `destroy` 의 패턴으로 동작합니다.
2. `workflow_dispatch`에서 `action=destroy`를 선택하면 Plan/Apply 없이 Destroy만 실행됩니다.
3. AWS 시크릿(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)이 상속돼 있지 않으면 1단계에서 즉시 실패합니다.

## 7. 마치며

여기까지 설정하면 Terraform EC2 데모 템플릿을 Backstage에서 셀프서비스로 제공할 수 있습니다. 다음 글에서는 Docker 이미지 배포와 파이프라인 운영 팁을 정리합니다.

- [시리즈 ① 플랫폼 엔지니어링과 Backstage 개요]( /2025/10/30/platform-engineering-idp-backstage/ )
- [시리즈 ③ Backstage Docker 배포 & 파이프라인 운영]( /2025/10/30/backstage-deployment-guide/ )
