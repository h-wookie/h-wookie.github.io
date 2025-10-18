#!/usr/bin/env python3
"""
Obsidian to Jekyll Blog Automation Script
Obsidian 노트를 Jekyll 블로그 포스트로 자동 변환 및 배포
"""

import os
import re
import yaml
import shutil
from datetime import datetime
from pathlib import Path
import subprocess

class ObsidianToBlog:
    def __init__(self, obsidian_vault_path, blog_path):
        self.obsidian_path = Path(obsidian_vault_path)
        self.blog_path = Path(blog_path)
        self.posts_path = self.blog_path / "_posts"
        
    def process_obsidian_note(self, note_path):
        """Obsidian 노트를 Jekyll 포스트로 변환"""
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Obsidian 링크 변환: [[링크]] → [링크](링크)
        content = re.sub(r'\[\[([^\]]+)\]\]', r'[\1](\1)', content)
        
        # 이미지 경로 변환
        content = re.sub(r'!\[\[([^\]]+)\]\]', r'![](/assets/images/\1)', content)
        
        # 태그 추출 (#tag → tags: [tag])
        tags = re.findall(r'#(\w+)', content)
        content = re.sub(r'#\w+\s*', '', content)  # 태그 제거
        
        return content, tags
    
    def create_jekyll_post(self, title, content, tags, category="General"):
        """Jekyll 포스트 생성"""
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date}-{title.lower().replace(' ', '-')}.md"
        
        front_matter = {
            'title': title,
            'excerpt': content.split('\n')[0][:100] + "...",
            'categories': [category],
            'tags': tags,
            'toc': True,
            'toc_sticky': True
        }
        
        post_content = f"---\n{yaml.dump(front_matter, allow_unicode=True)}---\n\n{content}"
        
        post_path = self.posts_path / filename
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(post_content)
        
        return post_path
    
    def git_commit_and_push(self, message):
        """Git 커밋 및 푸시"""
        os.chdir(self.blog_path)
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', message])
        subprocess.run(['git', 'push', 'origin', 'main'])

# 사용 예시
if __name__ == "__main__":
    converter = ObsidianToBlog(
        obsidian_vault_path="/path/to/obsidian/vault",
        blog_path="/Users/hyungwook/git-blog-backup"
    )
    
    # 특정 노트 변환
    # content, tags = converter.process_obsidian_note("note.md")
    # converter.create_jekyll_post("제목", content, tags, "Platform Engineering")
    # converter.git_commit_and_push("새 포스트: 제목")
