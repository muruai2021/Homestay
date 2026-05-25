import React from 'react';

function Sidebar({ agents, currentAgent, onSelectAgent }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">AI 员工</div>
      <ul className="agent-list">
        {agents.map(agent => (
          <li 
            key={agent.id}
            className={`agent-item ${currentAgent?.id === agent.id ? 'active' : ''}`}
            onClick={() => onSelectAgent(agent)}
          >
            <div className="agent-avatar">
              <img src={agent.avatar} alt={agent.name} onError={(e) => e.target.style.display = 'none'} />
            </div>
            <div className="agent-info">
              <div className="agent-name">{agent.name}</div>
              <div className="agent-desc">{agent.desc}</div>
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;
