/**
 * 历史记录管理
 */

class HistoryManager {
    constructor(feature, title) {
        this.feature = feature;
        this.title = title;
        this.maxItems = CONFIG.MAX_HISTORY_ITEMS;
    }

    get key() {
        return `ai_matrix_history_${this.feature}`;
    }

    load() {
        return Storage.get(this.key, []);
    }

    save(item) {
        const history = this.load();
        const newItem = {
            ...item,
            timestamp: new Date().toLocaleString('zh-CN')
        };
        
        history.unshift(newItem);
        if (history.length > this.maxItems) {
            history.pop();
        }
        
        return Storage.set(this.key, history);
    }

    getItem(index) {
        const history = this.load();
        return history[index] || null;
    }

    download() {
        const history = this.load();
        if (history.length === 0) {
            alert('暂无历史记录');
            return;
        }
        
        let content = `${this.title} - 历史记录\n`;
        content += `导出时间：${new Date().toLocaleString('zh-CN')}\n`;
        content += '='.repeat(50) + '\n\n';
        
        history.forEach((item, index) => {
            content += `【记录 ${index + 1}】\n`;
            content += `时间：${item.timestamp}\n`;
            if (item.input) content += `输入：${item.input}\n`;
            if (item.output) content += `输出：\n${item.output}\n`;
            if (item.imageUrl) content += `图片：${item.imageUrl}\n`;
            content += '-'.repeat(30) + '\n\n';
        });
        
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.feature}_history_${Date.now()}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    renderPanel() {
        const history = this.load();
        return `
            <div class="history-panel">
                <div class="history-header">
                    <span class="history-title">📜 历史记录</span>
                    <div class="history-actions">
                        <span class="history-count">${history.length}/${this.maxItems}</span>
                        <button class="history-btn" onclick="window.featureManager.downloadHistory()" title="下载全部记录">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                                <polyline points="7 10 12 15 17 10"/>
                                <line x1="12" y1="15" x2="12" y2="3"/>
                            </svg>
                            下载
                        </button>
                    </div>
                </div>
                ${history.length > 0 ? `
                    <div class="history-list">
                        ${history.map((item, index) => `
                            <div class="history-item" onclick="window.featureManager.loadHistoryItem(${index})">
                                <div class="history-item-title">${item.title || '记录 ' + (index + 1)}</div>
                                <div class="history-item-time">${item.timestamp}</div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<div class="history-empty">暂无历史记录</div>'}
            </div>
        `;
    }
}

window.HistoryManager = HistoryManager;
