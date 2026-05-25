// 猩伙伴民宿 - 房源数据
// 注意：图片已从Word文档提取到images/properties/目录

const communities = [
  {
    id: 'baoli',
    name: '保利国际广场',
    nameShort: '保利',
    area: '天心区',
    metro: '碧沙湖站',
    address: '长沙天心区保利国际广场',
    description: '位于长沙天心区，一线江景，紧邻碧沙湖地铁站，出行便利',
    propertyCount: 5
  },
  {
    id: 'jianfayangyun',
    name: '建发养云',
    nameShort: '建发养云',
    area: '开福区',
    metro: '开福寺站',
    address: '长沙开福区新河街道潘家坪路建发养云',
    description: '开福区核心地段，步行可达开福寺，一线江景体验',
    propertyCount: 9
  },
  {
    id: 'beichen',
    name: '北辰三角洲',
    nameShort: '北辰',
    area: '开福区',
    metro: '北辰三角洲站',
    address: '长沙开福区沅浦路28号北辰三角洲',
    description: '北辰三角洲核心区，靠近北辰荟购物中心，一线江景',
    propertyCount: 7
  }
];

const properties = [
  // 保利国际广场（5套）
  {
    id: 1,
    name: '复兴基地',
    community: 'baoli',
    communityName: '保利国际广场',
    type: '两卧大床房',
    capacity: '4大人2小孩',
    area: '约80㎡',
    price: '电询',
    tags: ['江景', '艺术设计'],
    isLuxury: false,
    features: '由伦敦艺术大学设计师设计的中古现代风格，一线江景房，从房间内可看到橘子洲头青年毛泽东雕像，晨享湘江水波雾面，傍晚赏江面落日熔金，夜间俯瞰城市霓虹',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾'],
    transport: {
      airport: '44分钟',
      highSpeedRail: '36分钟',
      trainStation: '27分钟',
      metro: '地铁4号线碧沙湖站3C出口步行580米'
    },
    address: '长沙天心区保利国际广场-B1栋2607室',
    image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'
  },
  {
    id: 2,
    name: '时空胶囊',
    community: 'baoli',
    communityName: '保利国际广场',
    type: '两卧大床房',
    capacity: '4大人2小孩',
    area: '约80㎡',
    price: '电询',
    tags: ['江景', '复古科技'],
    isLuxury: true,
    features: '由海归青年设计师设计的一间复古科技风双卧民宿，推窗就是一线橘洲江景，从房间内可看到橘子洲头青年毛泽东雕像，白日观湘江水波雾面，傍晚赏江面落日熔金，夜间俯瞰城市霓虹',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾'],
    transport: {
      airport: '44分钟',
      highSpeedRail: '36分钟',
      trainStation: '27分钟',
      metro: '地铁4号线碧沙湖站3C出口步行580米'
    },
    address: '长沙天心区保利国际广场-B1栋4709室',
    image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'
  },
  {
    id: 3,
    name: '润之江阁',
    community: 'baoli',
    communityName: '保利国际广场',
    type: '两卧大床房',
    capacity: '4大人2小孩',
    area: '约80㎡',
    price: '电询',
    tags: ['江景', '东方美学'],
    isLuxury: true,
    features: '由青年设计师打造的一间兼具现代舒适与东方意境的美学居所，江景与古韵巧妙融合，营造出松弛又高级的氛围。推窗就是一线橘洲江景，从房间内可看到橘子洲头青年毛泽东雕像',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾'],
    transport: {
      airport: '44分钟',
      highSpeedRail: '36分钟',
      trainStation: '27分钟',
      metro: '地铁4号线碧沙湖站3C出口步行580米'
    },
    address: '长沙天心区保利国际广场-B1栋4708室',
    image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800'
  },
  {
    id: 4,
    name: '童趣江境',
    community: 'baoli',
    communityName: '保利国际广场',
    type: '两卧大床房',
    capacity: '4大人2小孩',
    area: '约80㎡',
    price: '电询',
    tags: ['江景', '童趣'],
    isLuxury: true,
    features: '由伦敦艺术大学硕士设计师设计的一间童趣风民宿，以大胆的波普艺术元素和流畅的空间动线，打造出兼具视觉冲击力与舒适住宿体验的居住空间。推窗就是一线橘洲江景',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾'],
    transport: {
      airport: '44分钟',
      highSpeedRail: '36分钟',
      trainStation: '27分钟',
      metro: '地铁4号线碧沙湖站3C出口步行580米'
    },
    address: '长沙天心区保利国际广场-B1栋2407室',
    image: 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800'
  },
  {
    id: 5,
    name: '麓江别苑',
    community: 'baoli',
    communityName: '保利国际广场',
    type: '两卧大床房',
    capacity: '4大人2小孩',
    area: '约80㎡',
    price: '电询',
    tags: ['江景', '东方美学'],
    isLuxury: true,
    features: '由青年设计师设计的一间藏于都市中的东方美学居所，兼具艺术美感与舒适度。推窗就是一线橘洲江景，从房间内可看到橘子洲头青年毛泽东雕像，远眺麓山，绿意环绕',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾'],
    transport: {
      airport: '44分钟',
      highSpeedRail: '36分钟',
      trainStation: '27分钟',
      metro: '地铁4号线碧沙湖站3C出口步行580米'
    },
    address: '长沙天心区保利国际广场-B1栋4706室',
    image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'
  },
  // 建发养云（9套）
  {
    id: 6,
    name: '梵高小窝',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '一卧一卫',
    capacity: '2大人+1幼儿',
    area: '70㎡',
    price: '电询',
    tags: ['艺术设计', 'Loft'],
    isLuxury: false,
    features: '当梵高的笔触跃入居所，艺术便成了生活的日常。一层客厅以梵高《星月夜》巨幅壁画为灵魂，搭配条纹艺术椅、米色沙发与原木茶几。民宿配备高清可投屏电视，落地窗将城市景观尽收眼底',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '可投屏电视'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼3315室',
    image: 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800'
  },
  {
    id: 7,
    name: '摩登剧场',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '一卧一卫',
    capacity: '2大人+1幼儿',
    area: '75㎡',
    price: '电询',
    tags: ['江景', 'Loft'],
    isLuxury: false,
    features: '以"红磨坊"为主题设计的75㎡轻奢江景loft，一楼定制浴缸嵌在望江落地窗边，让您享受"一线江景泡澡自由"。配备极米投影仪，清晰度堪比私人影院',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '极米投影仪', '浴缸'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼2833室',
    image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'
  },
  {
    id: 8,
    name: '江鸢小筑',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '两卧一卫',
    capacity: '4人',
    area: '约90㎡',
    price: '电询',
    tags: ['江景', '艺术设计'],
    isLuxury: false,
    features: '整面楼梯侧墙采用梵高《鸢尾花》手绘壁画，蓝绿撞色强烈。双层挑高设计，楼梯带感应灯带；上层为主卧江景房，下层为客餐厨+次卧，卫浴干湿分离',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼2127室',
    image: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800'
  },
  {
    id: 9,
    name: '悬浮星宫',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '三卧一卫',
    capacity: '6大人',
    area: '130㎡',
    price: '电询',
    tags: ['江景', 'Loft'],
    isLuxury: true,
    features: '推开房门，首先映入眼帘的是充满盎然生机的仙人掌植物置景。一楼开放式餐厨与悬浮楼梯构成几何美感，定制麻将机承包娱乐活动，定制高奢导台满足您的晨咖夜酒',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '麻将机'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼3301室',
    image: 'https://images.unsplash.com/photo-1602002418816-5c0aeef426aa?w=800'
  },
  {
    id: 10,
    name: '天空牧场',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '三卧两卫',
    capacity: '6大人',
    area: '约150㎡',
    price: '电询',
    tags: ['江景', '童趣'],
    isLuxury: true,
    features: '由伦艺硕士海归青年设计师打造的现代童趣风美学居所，拥有270度的一线环绕江景。房间里随处可见设计巧思：与窗边江景融为一体的艺术展品骏马，沙发上毛茸茸的北极熊',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼2331室',
    image: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800'
  },
  {
    id: 11,
    name: '江天木舍',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '三卧三卫',
    capacity: '6大人',
    area: '180㎡',
    price: '电询',
    tags: ['江景', '艺术设计'],
    isLuxury: true,
    features: '由伦艺青年海归设计师打造的180㎡中古现代美学居所：开放式餐厨，原木长桌配藤编椅，艺术吊灯如编织的云朵。透过玻璃窗，江景与落日同框，星城的脉络在眼前铺展',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼2926室',
    image: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800'
  },
  {
    id: 12,
    name: '粉墨',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '三卧一卫',
    capacity: '6大人',
    area: '150㎡',
    price: '电询',
    tags: ['江景', '艺术设计'],
    isLuxury: true,
    features: '由格拉斯哥大学毕业海归青年女设计师亲手打造，肃穆神秘的黑色与甜美梦幻粉色碰撞出来的150㎡空间美学，落雪的圣诞树缀着魔镜粉调，巨型Labubu躲在楼梯角，毛绒绒的粉色抱枕卧在奶油沙发上',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '麻将机'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼1631室',
    image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800'
  },
  {
    id: 13,
    name: '鹤隐',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '一卧一卫',
    capacity: '2大人+1幼儿',
    area: '70㎡',
    price: '电询',
    tags: ['艺术设计', '新中式'],
    isLuxury: false,
    features: '新中式融合现代风雅居。一层客厅以青绿鹤鸣壁画为视觉焦点，搭配米白色慵懒沙发与艺术感吊灯。沿着木质楼梯而上，二层圆形拱窗设计的卧室别出心裁',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云S1号楼3317室',
    image: 'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800'
  },
  {
    id: 14,
    name: '宋韵璟庭',
    community: 'jianfayangyun',
    communityName: '建发养云',
    type: '两卧一卫',
    capacity: '4大人',
    area: '约100㎡',
    price: '电询',
    tags: ['江景', '新中式'],
    isLuxury: false,
    features: '整体空间以新中式风格为基调，古雅的宋式山水壁画与简约现代的家具相得益彰。270度全景落地窗，白天可俯瞰江水流淌、城市天际线，傍晚看晚霞染江，夜晚赏万家灯火',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '40分钟',
      highSpeedRail: '41分钟',
      trainStation: '20分钟',
      metro: '地铁1号线开福寺站3号出口步行791米'
    },
    address: '长沙开福区新河街道潘家坪路建发养云',
    image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800'
  },
  // 北辰三角洲（7套）
  {
    id: 15,
    name: '摩卡',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '两卧大床房',
    capacity: '2-4大人',
    area: '80㎡',
    price: '电询',
    tags: ['江景', '创意'],
    isLuxury: false,
    features: '颇具创意与趣味性的咖啡主题民宿，面积80㎡，房间内充斥着各种咖啡元素，住客将收获民宿+咖啡馆的双重体验。江景视野开阔，晚上可看到赛博灯光秀',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋3204室',
    image: 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800'
  },
  {
    id: 16,
    name: '星光',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '两卧大床房',
    capacity: '3-6大人+2小孩',
    area: '130㎡',
    price: '电询',
    tags: ['江景', '家庭优选'],
    isLuxury: false,
    features: '面积130㎡的宽敞空间，家庭亲子出行优选，临江大平层，带高清投影，可做饭，有儿童房，视野开阔。步行7分钟可达北辰荟',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '高清投影', '可做饭'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '45分钟',
      highSpeedRail: '43分钟',
      trainStation: '26分钟',
      metro: '地铁1号线北辰三角洲站2出口步行716米'
    },
    address: '长沙开福区北辰三角洲D3区8栋1单元1002房',
    image: 'https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800'
  },
  {
    id: 17,
    name: '江檀谧屿',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '两卧一厅',
    capacity: '2-4大人',
    area: '100㎡',
    price: '电询',
    tags: ['江景', '法式'],
    isLuxury: false,
    features: '江景环绕的100㎡轻奢法式松弛慵懒居所，房间配备定制麻将机。黑色皮质沙发搭配暖绒抱枕，增添复古质感。裹着慵懒与松弛住进这里，推窗就见烟波绿意',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '麻将机'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋608室',
    image: 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800'
  },
  {
    id: 18,
    name: '空中楼阁',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '两卧大床房',
    capacity: '2-4大人',
    area: '70㎡',
    price: '电询',
    tags: ['江景', 'Loft'],
    isLuxury: false,
    features: '由伦敦艺术大学室内设计师亲自操刀设计的70㎡包豪斯艺术空间，极简几何线条搭配高级金属质感，诠释轻奢美学。挑高LOFT结构，解锁室内玻璃栈道游玩体验，仿佛悬浮于云端之上',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋1909室',
    image: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800'
  },
  {
    id: 19,
    name: '花间',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '两卧大床房',
    capacity: '2-4大人',
    area: '80㎡',
    price: '电询',
    tags: ['江景', 'Loft'],
    isLuxury: false,
    features: '颇具设计感的80㎡现代美学空间，挑高LOFT结构，一楼休闲娱乐区，二楼静谧休憩区。步行5分钟可达北辰荟、一线江景，晚上可看到赛博灯光秀',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋3203室',
    image: 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800'
  },
  {
    id: 20,
    name: '禅意町屋',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '三卧一卫',
    capacity: '6大人',
    area: '150㎡',
    price: '电询',
    tags: ['江景', '禅意'],
    isLuxury: true,
    features: '伦艺设计师亲手打造的禅意空间，面积150㎡的江景环绕式三卧套间。房间配备全木定制麻将机，禅意绿植与日式布帘在暖黄的障子灯下更添氛围',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '麻将机'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋2704室',
    image: 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800'
  },
  {
    id: 21,
    name: '秘密基地',
    community: 'beichen',
    communityName: '北辰三角洲',
    type: '三卧两卫',
    capacity: '6大人',
    area: '150㎡',
    price: '电询',
    tags: ['江景', '艺术设计'],
    isLuxury: true,
    features: '国际设计奖拿到手软的设计师民宿，面积150㎡的江景环绕式三卧套间。在新中式与现代风格的融合中，点缀了些许童趣元素，视觉造型吸睛',
    amenities: ['冷暖空调', '电梯', '无线网', '落地窗', '麻将机'],
    bathroom: ['热水', '独立卫浴', '电吹风', '洗浴用品', '牙具', '浴巾', '拖鞋'],
    transport: {
      airport: '50分钟',
      highSpeedRail: '32分钟',
      trainStation: '23分钟',
      metro: '地铁1号线北辰三角洲站3C1出口步行585米'
    },
    address: '长沙开福区沅浦路28号北辰三角洲C1区北辰府3栋3109室',
    image: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800'
  }
];

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { communities, properties };
}
