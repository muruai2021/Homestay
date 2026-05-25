import React, { useState, useRef, useEffect } from 'react';

// 简单 Markdown 解析
const parseMarkdown = (text) => {
  if (!text) return '';
  let html = text;
  // 代码块
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
  // 行内代码
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  // 标题
  html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>');
  // 加粗
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // 列表
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
  // 数字列表
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
  // 换行
  html = html.replace(/\n\n/g, '</p><p>');
  html = html.replace(/\n/g, '<br/>');
  return `<p>${html}</p>`;
};

function ChatArea({ currentAgent, onBack }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  // 加载历史记录
  useEffect(() => {
    if (currentAgent) {
      setMessages([]);
      fetch(`/api/agent/${currentAgent.id}/history?limit=50`)
        .then(r => r.json())
        .then(data => {
          if (data.history && data.history.length > 0) {
            setMessages(data.history);
          }
        })
        .catch(() => {});
    }
  }, [currentAgent]);

  const sendMessage = async () => {
    if (!input.trim() || !currentAgent) return;
    
    const userMsg = input.trim();
    setInput('');
    setLoading(true);

    // 添加用户消息
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);

    try {
      const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          agent_id: currentAgent.id, 
          message: userMsg 
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      // 添加AI消息占位
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        fullContent += chunk;
        setMessages(prev => {
          const newMsgs = [...prev];
          newMsgs[newMsgs.length - 1].content = fullContent;
          return newMsgs;
        });
      }
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: '抱歉，服务暂时不可用。' }]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 未选择 AI 员工
  if (!currentAgent) {
    return (
      <div className="chat-area">
        <div className="chat-messages">
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <p>您好！请选择左侧的 AI 员工开始对话</p>
            </div>
          </div>
        </div>
        <div className="chat-input-area">
          <div className="chat-input-wrapper">
            <textarea 
              className="chat-input" 
              placeholder="输入消息..." 
              rows="1"
              disabled
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-area">
      <div className="chat-header">
        <div className="chat-header-info">
          <button className="back-btn" onClick={onBack} title="返回">
            ←
          </button>
          <div className="chat-header-avatar">
            <img src={currentAgent.avatar} alt={currentAgent.name} onError={(e) => e.target.style.display = 'none'} />
          </div>
          <div>
            <div className="chat-header-title">{currentAgent.name}</div>
            <div className="chat-header-desc">{currentAgent.title}</div>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {/* 欢迎消息（无历史时） */}
        {messages.length === 0 && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <p>您好！我是{currentAgent.name}，有什么可以帮您的？</p>
            </div>
          </div>
        )}
        {/* 历史消息 + 新消息 */}
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'assistant' ? '🤖' : '👤'}
            </div>
            <div className="message-content" dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.content) }} />
          </div>
        ))}
        {/* 加载中 */}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <p>AI 思考中...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea 
            className="chat-input" 
            placeholder={`对 ${currentAgent.name} 说...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows="1"
          />
          <button className="chat-send-btn" onClick={sendMessage}>发送</button>
        </div>
      </div>
    </div>
  );
}

export default ChatArea;
