#!/bin/bash
# Obsidian + AI + Git 자동화 환경 설정

echo "🚀 Obsidian to Blog 자동화 환경 설정 시작..."

# Python 의존성 설치
pip install pyyaml watchdog

# Obsidian 플러그인 설치 가이드 출력
echo "📱 Obsidian에서 다음 플러그인들을 설치하세요:"
echo "- Templater"
echo "- Git"
echo "- Advanced Tables"
echo "- Dataview (선택사항)"

# GitHub Actions 워크플로우 생성
mkdir -p .github/workflows
cat > .github/workflows/obsidian-sync.yml << 'EOF'
name: Obsidian to Blog Sync
on:
  push:
    paths: ['obsidian-notes/**']
  workflow_dispatch:

jobs:
  convert-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        pip install pyyaml
        
    - name: Convert Obsidian notes
      run: |
        python automation/obsidian-to-blog.py
        
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --staged --quiet || git commit -m "Auto-sync from Obsidian"
        git push
EOF

# 디렉토리 구조 생성
mkdir -p obsidian-notes
mkdir -p assets/images

echo "✅ 설정 완료!"
echo "📝 다음 단계:"
echo "1. Obsidian Vault를 obsidian-notes/ 폴더에 연결"
echo "2. automation/obsidian-to-blog.py 스크립트 경로 수정"
echo "3. 첫 번째 노트 작성 후 테스트"
