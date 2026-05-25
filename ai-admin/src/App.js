import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';

const agents = [
  { id: 'xhs', name: '小红书文案', nickname: '南乔', title: '小红书运营专家', desc: '打造爆款种草文案', avatar: '/ai/avatars/ops-manager.png' },
  { id: 'wechat', name: '公众号文案', nickname: '凌冬', title: '公众号运营专家', desc: '生成专业公众号文章', avatar: '/ai/avatars/minsu-assistant.png' },
  { id: 'shortvideo', name: '短视频文案', nickname: '明轩', title: '短视频方案专家', desc: '生成视频脚本和分镜', avatar: '/ai/avatars/ai-architect.png' },
  { id: 'poster', name: '海报设计', nickname: '西柚', title: '海报设计专家', desc: 'AI生成精美海报', avatar: '/ai/avatars/poster-designer.png' },
  { id: 'intelligence', name: '情报分析', nickname: '北辰', title: '情报分析专家', desc: '竞品分析趋势预测', avatar: '/ai/avatars/inteligence-analyst.png' },
  { id: 'knowledge', name: '企业知识库', nickname: '东岳', title: '知识库管家', desc: '企业知识管理和问答', avatar: '/ai/avatars/knowledge-keeper.png' },
];

function App() {
  const [currentAgent, setCurrentAgent] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <div className="app-container">
      {/* 顶部导航栏 */}
      <nav className="top-nav">
        <div className="top-nav-brand">
          <svg viewBox="0 0 56 56" fill="none" width="32" height="32">
            <defs>
              <linearGradient id="navGrad" x1="10" y1="6" x2="46" y2="48">
                <stop stopColor="#c4a35a"/>
                <stop offset="1" stopColor="#d4b96a"/>
              </linearGradient>
            </defs>
            <path d="M28 6L10 20V48H22V34H34V48H46V20L28 6Z" stroke="url(#navGrad)" strokeWidth="1.5" fill="none"/>
            <path d="M34 48V40H42V48" stroke="url(#navGrad)" strokeWidth="1.5" fill="none"/>
            <path d="M14 48V40H22V48" stroke="url(#navGrad)" strokeWidth="1.5" fill="none"/>
          </svg>
          <span>猩伙伴 AI</span>
        </div>
        <div className="top-nav-menu">
          <a href="/" className="top-nav-link">官网</a>
          <button 
            className={`top-nav-link ${!showDashboard ? 'active' : ''}`}
            onClick={() => setShowDashboard(false)}
          >
            AI 员工
          </button>
          <button
            className={`top-nav-link ${showDashboard ? 'active' : ''}`}
            onClick={() => window.location.href = '/ai/manage.html'}
          >
            运营看板
          </button>
        </div>
      </nav>

      {/* 主内容区域 */}
      <div className="main-container" style={{ paddingTop: '60px' }}>
        {!showDashboard && (
          <Sidebar 
            agents={agents} 
            currentAgent={currentAgent} 
            onSelectAgent={setCurrentAgent} 
          />
        )}
        {showDashboard ? (
          <div className="dashboard-view">
            <h2>运营看板</h2>
            <p style={{ color: 'var(--text-muted)', marginTop: '20px' }}>看板功能开发中...</p>
          </div>
        ) : (
          <ChatArea currentAgent={currentAgent} onBack={() => setCurrentAgent(null)} />
        )}
      </div>
    </div>
  );
}

export default App;
