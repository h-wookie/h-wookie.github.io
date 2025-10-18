document.addEventListener('DOMContentLoaded', function() {
  const toc = document.querySelector('.toc');
  
  if (toc) {
    // TOC 제목에 숨기기 버튼 추가
    const tocTitle = toc.querySelector('.toc__title');
    if (tocTitle) {
      const hideBtn = document.createElement('button');
      hideBtn.className = 'toc-hide-btn';
      hideBtn.innerHTML = '✕';
      hideBtn.title = 'TOC 숨기기';
      tocTitle.appendChild(hideBtn);
      
      hideBtn.addEventListener('click', function() {
        toc.classList.add('hidden');
        toggleBtn.classList.add('show');
      });
    }
    
    // 플로팅 토글 버튼 생성
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toc-toggle';
    toggleBtn.innerHTML = '📋';
    toggleBtn.title = 'TOC 보기';
    document.body.appendChild(toggleBtn);
    
    toggleBtn.addEventListener('click', function() {
      toc.classList.remove('hidden');
      toggleBtn.classList.remove('show');
    });
    
    // 반응형: 태블릿/모바일에서는 기본적으로 TOC 숨김
    function checkScreenSize() {
      if (window.innerWidth <= 1024) {
        toc.classList.add('hidden');
        toggleBtn.classList.add('show');
      } else {
        toc.classList.remove('hidden');
        toggleBtn.classList.remove('show');
      }
    }
    
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
  }
});
