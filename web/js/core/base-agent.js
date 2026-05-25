/**
 * AI 员工基础类 - 所有智能体的基类
 */
export class BaseAgent {
    constructor(agentId, config) {
        this.agentId = agentId;
        this.config = config;
        this.mode = 'chat'; // chat 或 generate
        this.isLoading = false;
        this.chatHistory = [];
        
        this.initUI();
    }
    
    initUI() {
        // 初始化 UI 事件绑定
        this.bindEvents();
    }
    
    bindEvents() {
        // 绑定模式切换
        const modeToggle = document.getElementById('mode-toggle');
        if (modeToggle) {
            modeToggle.addEventListener('change', (e) => {
                this.mode = e.target.value;
                this.toggleMode();
            });
        }
        
        // 绑定发送按钮
        const sendBtn = document.getElementById('send-btn');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.handleSend());
        }
        
        // 绑定回车发送
        const input = document.getElementById('user-input');
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSend();
                }
            });
        }
        
        // 绑定清空历史
        const clearBtn = document.getElementById('clear-history-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearHistory());
        }
    }
    
    toggleMode() {
        // 切换聊天/生成模式
        const chatPanel = document.getElementById('chat-panel');
        const generatePanel = document.getElementById('generate-panel');
        
        if (this.mode === 'chat') {
            chatPanel.style.display = 'block';
            generatePanel.style.display = 'none';
        } else {
            chatPanel.style.display = 'none';
            generatePanel.style.display = 'block';
        }
    }
    
    async handleSend() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        if (this.mode === 'chat') {
            await this.sendChatMessage(message);
        } else {
            await this.sendGenerateTask(message);
        }
        
        input.value = '';
    }
    
    async sendChatMessage(message) {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading();
        
        try {
            // 显示用户消息
            this.appendMessage('user', message);
            
            // 发送请求
            const response = await this.streamChat(message);
            
            // 显示 AI 响应
            this.appendMessage('assistant', response);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }
    
    async sendGenerateTask(userInput) {
        if (this.isLoading) return;
        
        const taskInput = document.getElementById('task-input');
        const task = taskInput.value.trim();
        
        if (!task) {
            alert('请输入生成任务描述');
            return;
        }
        
        this.isLoading = true;
        this.showLoading();
        
        try {
            // 显示用户输入
            this.appendMessage('user', `任务：${task}\n输入：${userInput}`);
            
            // 发送请求
            const response = await this.streamGenerate(task, userInput);
            
            // 显示 AI 响应
            this.appendMessage('assistant', response);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }
    
    async streamChat(message) {
        const response = await fetch(`${window.CONFIG.API_URL}/api/agent/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                agent_id: this.agentId
            })
        });
        
        if (!response.ok) {
            throw new Error('请求失败');
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            fullText += chunk;
            
            // 实时更新
            this.updateLastMessage(fullText);
        }
        
        return fullText;
    }
    
    async streamGenerate(task, userInput) {
        const response = await fetch(`${window.CONFIG.API_URL}/api/agent/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: task,
                user_input: userInput,
                agent_id: this.agentId
            })
        });
        
        if (!response.ok) {
            throw new Error('请求失败');
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            fullText += chunk;
            
            // 实时更新
            this.updateLastMessage(fullText);
        }
        
        return fullText;
    }
    
    appendMessage(role, content) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.innerHTML = this.formatMessage(content);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        this.chatHistory.push({ role, content });
    }
    
    updateLastMessage(content) {
        const chatMessages = document.getElementById('chat-messages');
        const lastMessage = chatMessages.lastElementChild;
        if (lastMessage && lastMessage.classList.contains('assistant')) {
            lastMessage.innerHTML = this.formatMessage(content);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    formatMessage(content) {
        // 简单的 Markdown 格式化
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }
    
    showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant loading';
        loadingDiv.id = 'loading-message';
        loadingDiv.innerHTML = '<span class="loading-dots">AI 正在思考...</span>';
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideLoading() {
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    showError(message) {
        const chatMessages = document.getElementById('chat-messages');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message error';
        errorDiv.innerHTML = `❌ ${message}`;
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    async clearHistory() {
        if (!confirm('确定要清空对话历史吗？')) return;
        
        try {
            await fetch(`${window.CONFIG.API_URL}/api/agent/${this.agentId}/clear`, {
                method: 'POST'
            });
            
            // 清空 UI
            const chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML = '';
            this.chatHistory = [];
            
            this.showToast('对话历史已清空');
        } catch (error) {
            this.showError('清空失败');
        }
    }
    
    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

export default BaseAgent;
