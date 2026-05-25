// 猩伙伴民宿官网 - 首页交互逻辑

document.addEventListener('DOMContentLoaded', function() {
  initNavbar();
  initCommunities();
  initPropertyScroll();
  initModal();
  initChat();
  initScrollAnimations();
  initAdminLoginModal();
});

// 导航栏滚动效果
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });

  // 点击导航链接关闭移动端菜单
  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('active');
    });
  });
}

// 小区背景图片映射
const communityImages = {
  'baoli': 'images/baoli.jpg',
  'jianfayangyun': 'images/jianfa.jpg',
  'beichen': 'images/beichen.jpg'
};

// 房源图片映射 - 从Word文档提取的真实图片
const propertyImages = {
  1: 'images/properties/1-fuxing.jpg',      // 复兴基地
  2: 'images/properties/2-shikong.jpg',     // 时空胶囊
  3: 'images/properties/3-runzhi.jpg',     // 润之江阁
  4: 'images/properties/4-tongqu.jpg',      // 童趣江境
  5: 'images/properties/5-lujiang.jpg',     // 麓江别苑
  6: 'images/properties/6-fangao.jpg',      // 梵高小窝
  7: 'images/properties/7-moden.jpg',        // 摩登剧场
  8: 'images/properties/8-jiangyuan.jpg',   // 江鸢小筑
  9: 'images/properties/9-xuanfu.jpg',      // 悬浮星宫
  10: 'images/properties/10-tiankong.jpg',  // 天空牧场
  11: 'images/properties/11-jiangtian.jpg',  // 江天木舍
  12: 'images/properties/12-fenmo.jpg',      // 粉墨
  13: 'images/properties/13-heyin.jpg',      // 鹤隐
  14: 'images/properties/14-songyun.jpg',    // 宋韵璟庭
  15: 'images/properties/15-moka.jpg',       // 摩卡
  16: 'images/properties/16-xingguang.jpg',  // 星光
  17: 'images/properties/17-jiangtan.jpg',   // 江檀谧屿
  18: 'images/properties/18-kongzhong.jpg',  // 空中楼阁
  19: 'images/properties/19-huajian.jpg',    // 花间
  20: 'images/properties/20-chanyi.jpg',     // 禅意町屋
  21: 'images/properties/21-mimi.jpg'        // 秘密基地
};

// 渲染小区卡片
function initCommunities() {
  const grid = document.getElementById('communitiesGrid');
  if (!grid) return;

  const icons = ['🏠', '🏢', '🏙️']; // 房子图标

  grid.innerHTML = communities.map((community, index) => {
    const communityProperties = properties.filter(p => p.community === community.id);
    const bgImage = communityImages[community.id] || '';
    return `
      <div class="community-card" data-community="${community.id}">
        <div class="community-bg" style="background-image: url('${bgImage}'); background-size: cover; background-position: center;"></div>
        <div class="community-overlay">
          <div class="community-icon">${icons[index]}</div>
          <h3 class="community-name">${community.name}</h3>
          <p class="community-area">${community.area} · ${community.metro}</p>
          <span class="community-count">${community.propertyCount}套房源</span>
          <div class="community-action">
            <button class="btn btn-small btn-outline">点击查看</button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // 点击小区卡片打开弹窗
  grid.querySelectorAll('.community-card').forEach(card => {
    card.addEventListener('click', () => {
      const communityId = card.dataset.community;
      openCommunityModal(communityId);
    });
  });
}

// 渲染精选房源滚动
function initPropertyScroll() {
  const track = document.getElementById('propertyTrack');
  const prevBtn = document.getElementById('scrollPrev');
  const nextBtn = document.getElementById('scrollNext');
  const scrollContainer = document.getElementById('propertyScroll');

  if (!track) return;

  track.innerHTML = properties.map(property => {
    const tagClass = property.isLuxury ? '' : (property.tags.includes('江景') ? 'river' : (property.tags.includes('艺术设计') ? 'art' : ''));
    const tagText = property.isLuxury ? '顶奢' : (property.tags[0] || '');
    const featurePreview = property.features.substring(0, 60) + '...';
    // 使用从Word文档提取的真实图片
    const realImage = propertyImages[property.id] || property.image;

    return `
      <div class="property-card" data-id="${property.id}">
        <div class="property-image">
          <img src="${realImage}" alt="${property.name}" loading="lazy">
          <span class="property-tag ${tagClass}">${tagText}</span>
        </div>
        <div class="property-info">
          <h3 class="property-name">猩伙伴·${property.name}</h3>
          <div class="property-meta">
            <span class="property-community">${property.communityName}</span>
            <span>${property.type}</span>
          </div>
          <div class="property-hover">
            <p class="property-feature">${featurePreview}</p>
            <div class="property-actions">
              <button class="btn-detail" onclick="window.location.href='property.html?id=${property.id}'">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // 滚动按钮事件
  if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      scrollContainer.scrollBy({ left: -320, behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', () => {
      scrollContainer.scrollBy({ left: 320, behavior: 'smooth' });
    });
  }

  // 卡片点击跳转到详情页
  track.querySelectorAll('.property-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (!e.target.closest('.btn-detail')) {
        const id = card.dataset.id;
        window.location.href = `property.html?id=${id}`;
      }
    });
  });
}

// 小区弹窗
function initModal() {
  const modal = document.getElementById('communityModal');
  const overlay = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalClose');

  if (closeBtn) {
    closeBtn.addEventListener('click', closeCommunityModal);
  }

  if (overlay) {
    overlay.addEventListener('click', closeCommunityModal);
  }

  // ESC键关闭
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCommunityModal();
      closeAdminLoginModal();
    }
  });
}

// 管理员登录弹窗
function initAdminLoginModal() {
  const loginBtn = document.getElementById('adminLoginBtn');
  const modal = document.getElementById('adminLoginModal');
  const overlay = document.getElementById('adminModalOverlay');
  const closeBtn = document.getElementById('adminLoginClose');
  const loginForm = document.getElementById('adminLoginForm');

  if (!loginBtn || !modal) return;

  // 打开弹窗
  loginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  });

  // 关闭弹窗
  if (closeBtn) {
    closeBtn.addEventListener('click', closeAdminLoginModal);
  }

  if (overlay) {
    overlay.addEventListener('click', closeAdminLoginModal);
  }

  // 登录表单提交
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const phone = document.getElementById('adminPhone').value;
      const password = document.getElementById('adminPassword').value;

      if (phone === '15874818550' && password === '123456') {
        localStorage.setItem('xinghuoban_admin', phone);
        closeAdminLoginModal();
        window.location.href = 'admin.html';
      } else {
        alert('手机号或密码错误');
      }
    });
  }
}

function closeAdminLoginModal() {
  const modal = document.getElementById('adminLoginModal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function openCommunityModal(communityId) {
  const modal = document.getElementById('communityModal');
  const title = document.getElementById('modalTitle');
  const subtitle = document.getElementById('modalSubtitle');
  const propertiesList = document.getElementById('modalProperties');

  const community = communities.find(c => c.id === communityId);
  const communityProperties = properties.filter(p => p.community === communityId);

  if (!community) return;

  title.textContent = community.name;
  subtitle.textContent = `${community.area} · ${community.metro} · ${community.propertyCount}套房源`;

  propertiesList.innerHTML = communityProperties.map(property => {
    const tagClass = property.isLuxury ? '' : (property.tags.includes('江景') ? 'river' : '');
    const tagText = property.isLuxury ? '顶奢' : (property.tags[0] || '');
    // 使用从Word文档提取的真实图片
    const realImage = propertyImages[property.id] || property.image;

    return `
      <div class="modal-property" onclick="window.location.href='property.html?id=${property.id}'">
        <div class="modal-property-img">
          <img src="${realImage}" alt="${property.name}">
        </div>
        <div class="modal-property-info">
          <h4 class="modal-property-name">猩伙伴·${property.name}</h4>
          <p class="modal-property-meta">
            <span class="property-tag ${tagClass}" style="display: inline-block; margin-right: 5px;">${tagText}</span>
            ${property.type} · 可住${property.capacity}
          </p>
          <p class="modal-property-capacity">${property.area}</p>
        </div>
      </div>
    `;
  }).join('');

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeCommunityModal() {
  const modal = document.getElementById('communityModal');
  modal.classList.remove('active');
  document.body.style.overflow = '';
}

// AI客服
function initChat() {
  const chatToggle = document.getElementById('chatToggle');
  const chatBox = document.getElementById('chatBox');
  const chatClose = document.getElementById('chatClose');
  const chatInput = document.getElementById('chatInput');
  const chatSend = document.getElementById('chatSend');
  const chatMessages = document.getElementById('chatMessages');

  if (!chatToggle) return;

  chatToggle.addEventListener('click', () => {
    chatBox.classList.toggle('active');
  });

  if (chatClose) {
    chatClose.addEventListener('click', () => {
      chatBox.classList.remove('active');
    });
  }

  const sendMessage = async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    // 添加用户消息
    addMessage(message, 'user');
    chatInput.value = '';

    // 创建AI消息容器（流式输出）
    const chatMessages = document.getElementById('chatMessages');
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message bot';
    aiMessageDiv.innerHTML = '<p></p>';
    chatMessages.appendChild(aiMessageDiv);
    const aiContentP = aiMessageDiv.querySelector('p');
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_id: 'customer', message: message })
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        fullContent += chunk;
        aiContentP.innerHTML = fullContent.replace(/\n/g, '<br>');
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    } catch (e) {
      aiContentP.innerHTML = '抱歉，服务暂时不可用，请稍后再试。';
    }
  };

  if (chatSend) {
    chatSend.addEventListener('click', sendMessage);
  }

  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  }
}

function addMessage(text, type) {
  const messagesContainer = document.getElementById('chatMessages');
  if (!messagesContainer) return;

  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.innerHTML = `<p>${text}</p>`;
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function getAIResponse(message) {
  const lowerMessage = message.toLowerCase();

  // 房源位置
  if (lowerMessage.includes('位置') || lowerMessage.includes('在哪') || lowerMessage.includes('地址')) {
    return '我们的房源分布在长沙三个小区：<br>• 保利国际广场（天心区，碧沙湖地铁站）<br>• 建发养云（开福区，开福寺地铁站）<br>• 北辰三角洲（开福区，北辰三角洲地铁站）<br>距地铁站步行10分钟以内，一线江景。';
  }

  // 房源户型
  if (lowerMessage.includes('户型') || lowerMessage.includes('几卧') || lowerMessage.includes('多少人')) {
    return '我们有21套房源，户型从一卧到三卧不等：<br>• 一卧：可住2大人+1幼儿<br>• 两卧：可住4大人或4大人2小孩<br>• 三卧：可住6大人<br>适合情侣、家庭、闺蜜聚会。';
  }

  // 价格
  if (lowerMessage.includes('价格') || lowerMessage.includes('多少钱') || lowerMessage.includes('报价')) {
    return '价格根据房型和日期不同，请拨打 <strong>15874818550</strong> 咨询，我们会给您最优惠的报价！';
  }

  // 预订
  if (lowerMessage.includes('预订') || lowerMessage.includes('预定') || lowerMessage.includes('预约') || lowerMessage.includes('订房')) {
    return '预订请致电 <strong>15874818550</strong>（微信同号），我们会为您安排好一切！';
  }

  // 联系方式
  if (lowerMessage.includes('联系') || lowerMessage.includes('电话') || lowerMessage.includes('微信')) {
    return '客服电话：<strong>15874818550</strong><br>微信：同手机号<br>24小时在线为您服务！';
  }

  // 特色
  if (lowerMessage.includes('特色') || lowerMessage.includes('特点') || lowerMessage.includes('有什么')) {
    return '我们的房源由伦敦艺术大学、格拉斯哥大学等国际设计师打造，每间都有独特风格：<br>• 一线江景，可看橘子洲头<br>• 艺术风格设计，拍照超美<br>• 五星床品、极米投影、麻将机<br>• 步行可达地铁站和商圈';
  }

  // 顶奢
  if (lowerMessage.includes('顶奢') || lowerMessage.includes('高端')) {
    return '我们有9套顶奢系列房源，特点包括：<br>• 更大的空间（130-180㎡）<br>• 三卧配置，可住6人<br>• 独特设计风格（童趣、法式、中古等）<br>• 部分配备麻将机、按摩椅等';
  }

  // 默认回复
  return '您好！我是猩伙伴AI客服。<br>您可以问我：<br>• 房源位置分布<br>• 户型和人数<br>• 价格咨询<br>• 如何预订<br>• 房源特色介绍<br><br>或直接拨打 <strong>15874818550</strong> 人工服务~';
}

// 滚动动画
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.feature-card, .community-card, .property-card').forEach(el => {
    observer.observe(el);
  });
}
