// 猩伙伴民宿官网 - 房源详情页逻辑

document.addEventListener('DOMContentLoaded', function() {
  loadPropertyDetail();
  initChat();
});

// 房源图片映射 - 从Word文档提取的真实图片
const propertyImages = {
  1: 'images/properties/1-fuxing.jpg',      // 复兴基地
  2: 'images/properties/2-shikong.jpg',     // 时空胶囊
  3: 'images/properties/3-runzhi.jpg',       // 润之江阁
  4: 'images/properties/4-tongqu.jpg',       // 童趣江境
  5: 'images/properties/5-lujiang.jpg',      // 麓江别苑
  6: 'images/properties/6-fangao.jpg',       // 梵高小窝
  7: 'images/properties/7-moden.jpg',        // 摩登剧场
  8: 'images/properties/8-jiangyuan.jpg',    // 江鸢小筑
  9: 'images/properties/9-xuanfu.jpg',       // 悬浮星宫
  10: 'images/properties/10-tiankong.jpg',   // 天空牧场
  11: 'images/properties/11-jiangtian.jpg',  // 江天木舍
  12: 'images/properties/12-fenmo.jpg',      // 粉墨
  13: 'images/properties/13-heyin.jpg',      // 鹤隐
  14: 'images/properties/14-songyun.jpg',    // 宋韵璟庭
  15: 'images/properties/15-moka.jpg',       // 摩卡
  16: 'images/properties/16-xingguang.jpg',  // 星光
  17: 'images/properties/17-jiangtan.jpg',   // 江檀谧屿
  18: 'images/properties/18-kongzhong.jpg',  // 空中楼阁
  19: 'images/properties/19-huajian.jpg',     // 花间
  20: 'images/properties/20-chanyi.jpg',      // 禅意町屋
  21: 'images/properties/21-mimi.jpg'        // 秘密基地
};

// 加载房源详情
function loadPropertyDetail() {
  const urlParams = new URLSearchParams(window.location.search);
  const propertyId = parseInt(urlParams.get('id'));

  if (!propertyId) {
    window.location.href = 'index.html';
    return;
  }

  const property = properties.find(p => p.id === propertyId);

  if (!property) {
    window.location.href = 'index.html';
    return;
  }

  // 设置页面标题
  document.title = `猩伙伴·${property.name} - 猩伙伴民宿`;

  // Hero背景图 - 使用从Word文档提取的真实图片
  const hero = document.getElementById('propertyHero');
  const realImage = propertyImages[propertyId] || property.image;
  hero.style.backgroundImage = `url(${realImage})`;

  // 基本信息
  document.getElementById('propertyName').textContent = `猩伙伴·${property.name}`;
  document.getElementById('propertyPrice').textContent = property.price;
  document.getElementById('propertyFeatures').textContent = property.features;

  // 标签
  const tagsContainer = document.getElementById('propertyTags');
  const tagClass = property.isLuxury ? '' : (property.tags.includes('江景') ? 'river' : (property.tags.includes('艺术设计') ? 'art' : ''));
  const tagText = property.isLuxury ? '顶奢' : property.tags[0] || '';

  if (property.isLuxury || property.tags.includes('江景') || property.tags.includes('艺术设计')) {
    tagsContainer.innerHTML = `<span class="property-tag-large ${tagClass}">${tagText}</span>`;
  }

  // 侧边栏信息
  document.getElementById('infoCommunity').textContent = property.communityName;
  document.getElementById('infoType').textContent = property.type;
  document.getElementById('infoCapacity').textContent = property.capacity;
  document.getElementById('infoArea').textContent = property.area;
  document.getElementById('infoAddress').textContent = property.address;

  // 基础设施
  const amenitiesContainer = document.getElementById('propertyAmenities');
  amenitiesContainer.innerHTML = property.amenities.map(amenity => `
    <div class="amenity-item">
      <span class="amenity-icon">&#x2714;</span>
      <span>${amenity}</span>
    </div>
  `).join('');

  // 卫浴设施
  const bathroomContainer = document.getElementById('propertyBathroom');
  bathroomContainer.innerHTML = property.bathroom.map(item => `
    <div class="amenity-item">
      <span class="amenity-icon">&#x2714;</span>
      <span>${item}</span>
    </div>
  `).join('');

  // 交通信息
  const transportContainer = document.getElementById('propertyTransport');
  transportContainer.innerHTML = `
    <div class="transport-item">
      <span class="transport-icon">&#x2708;</span>
      <div class="transport-info">
        <p class="transport-label">距离机场</p>
        <p class="transport-value">长沙黄花机场约${property.transport.airport}车程</p>
      </div>
    </div>
    <div class="transport-item">
      <span class="transport-icon">&#x1F682;</span>
      <div class="transport-info">
        <p class="transport-label">距离高铁南站</p>
        <p class="transport-value">约${property.transport.highSpeedRail}车程</p>
      </div>
    </div>
    <div class="transport-item">
      <span class="transport-icon">&#x1F68C;</span>
      <div class="transport-info">
        <p class="transport-label">距离火车站</p>
        <p class="transport-value">约${property.transport.trainStation}车程</p>
      </div>
    </div>
    <div class="transport-item">
      <span class="transport-icon">&#x1F687;</span>
      <div class="transport-info">
        <p class="transport-label">地铁</p>
        <p class="transport-value">${property.transport.metro}</p>
      </div>
    </div>
  `;

  // 相册 - 使用从Word文档提取的真实图片作为主图
  const galleryContainer = document.getElementById('propertyGallery');
  const galleryImages = [
    realImage,
    realImage,
    realImage,
    realImage,
    realImage,
    realImage
  ];

  galleryContainer.innerHTML = galleryImages.map(img => `
    <div class="gallery-item">
      <img src="${img}" alt="房源图片" loading="lazy">
    </div>
  `).join('');

  // 更新meta description
  const metaDesc = document.querySelector('meta[name="description"]') || document.createElement('meta');
  metaDesc.name = 'description';
  metaDesc.content = property.features.substring(0, 150);
}

// AI客服（与首页共用逻辑）
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

  const sendMessage = () => {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    chatInput.value = '';

    setTimeout(() => {
      const reply = getAIResponse(message);
      addMessage(reply, 'bot');
    }, 500);
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

  if (lowerMessage.includes('位置') || lowerMessage.includes('在哪') || lowerMessage.includes('地址')) {
    return '我们的房源分布在长沙三个小区：<br>• 保利国际广场（天心区，碧沙湖地铁站）<br>• 建发养云（开福区，开福寺地铁站）<br>• 北辰三角洲（开福区，北辰三角洲地铁站）<br>距地铁站步行10分钟以内，一线江景。';
  }

  if (lowerMessage.includes('户型') || lowerMessage.includes('几卧') || lowerMessage.includes('多少人')) {
    return '我们有21套房源，户型从一卧到三卧不等：<br>• 一卧：可住2大人+1幼儿<br>• 两卧：可住4大人或4大人2小孩<br>• 三卧：可住6大人<br>适合情侣、家庭、闺蜜聚会。';
  }

  if (lowerMessage.includes('价格') || lowerMessage.includes('多少钱') || lowerMessage.includes('报价')) {
    return '价格根据房型和日期不同，请拨打 <strong>15874818550</strong> 咨询，我们会给您最优惠的报价！';
  }

  if (lowerMessage.includes('预订') || lowerMessage.includes('预定') || lowerMessage.includes('预约') || lowerMessage.includes('订房')) {
    return '预订请致电 <strong>15874818550</strong>（微信同号），我们会为您安排好一切！';
  }

  if (lowerMessage.includes('联系') || lowerMessage.includes('电话') || lowerMessage.includes('微信')) {
    return '客服电话：<strong>15874818550</strong><br>微信：同手机号<br>24小时在线为您服务！';
  }

  if (lowerMessage.includes('特色') || lowerMessage.includes('特点') || lowerMessage.includes('有什么')) {
    return '我们的房源由伦敦艺术大学、格拉斯哥大学等国际设计师打造，每间都有独特风格：<br>• 一线江景，可看橘子洲头<br>• 艺术风格设计，拍照超美<br>• 五星床品、极米投影、麻将机<br>• 步行可达地铁站和商圈';
  }

  if (lowerMessage.includes('顶奢') || lowerMessage.includes('高端')) {
    return '我们有9套顶奢系列房源，特点包括：<br>• 更大的空间（130-180㎡）<br>• 三卧配置，可住6人<br>• 独特设计风格（童趣、法式、中古等）<br>• 部分配备麻将机、按摩椅等';
  }

  return '您好！我是猩伙伴AI客服。<br>您可以问我：<br>• 房源位置分布<br>• 户型和人数<br>• 价格咨询<br>• 如何预订<br>• 房源特色介绍<br><br>或直接拨打 <strong>15874818550</strong> 人工服务~';
}
