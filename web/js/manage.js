// 运营管理看板
function openManageDashboard() {
    document.getElementById('portal').style.display = 'none';
    document.getElementById('appContainer').classList.remove('active');
    document.getElementById('manageContainer').classList.add('active');
}

// 关闭管理看板
function closeManageDashboard() {
    document.getElementById('manageContainer').classList.remove('active');
    document.getElementById('portal').style.display = 'flex';
}

// 页面切换
function switchManagePage(pageId) {
    // 更新导航项状态
    document.querySelectorAll('.manage-nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === pageId) {
            item.classList.add('active');
        }
    });

    // 更新页面显示
    document.querySelectorAll('.manage-page').forEach(page => {
        page.classList.remove('active');
        if (page.id === 'page-' + pageId) {
            page.classList.add('active');
        }
    });

    // 更新标题
    const titles = {
        'dashboard': '运营概览',
        'rooms': '房源管理',
        'ops': '运营中心',
        'content': '内容中心',
        'finance': '财务管理',
        'ai': 'AI 洞察'
    };
    document.getElementById('manageTitle').textContent = titles[pageId] || '运营概览';
}

// 暴露到全局作用域
window.openManageDashboard = openManageDashboard;
window.closeManageDashboard = closeManageDashboard;
window.switchManagePage = switchManagePage;

// 初始化时间
document.addEventListener('DOMContentLoaded', () => {
    const timeEl = document.getElementById('manageTime');
    if (timeEl) {
        timeEl.textContent = new Date().toLocaleString('zh-CN', {
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
});
