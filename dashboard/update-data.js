const puppeteer = require('puppeteer-core');
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  CDP_PORT: 18800,
  MYHOSTEX_URL: 'https://www.myhostex.com',
  DATA_FILE: 'myhostex_all_orders.json',
  BACKUP_FILE: 'myhostex_all_orders.backup.json',
  STATUS_FILE: 'scrape_status.json',
  LAST_UPDATED_FILE: 'last_updated.txt',
  ERROR_LOG: 'error.log',
  MAX_RETRIES: 3,
  RETRY_DELAY: 30000,
  ROOM_COUNT: 34
};

function log(msg) {
  const ts = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  console.log(`[${ts}] ${msg}`);
}

function logError(msg, err) {
  const ts = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const entry = `[${ts}] ${msg}: ${err?.message || err}\n`;
  fs.appendFileSync(CONFIG.ERROR_LOG, entry);
  console.error(`❌ ${msg}:`, err?.message || err);
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function getStatus() {
  try {
    if (fs.existsSync(CONFIG.STATUS_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG.STATUS_FILE, 'utf-8'));
    }
  } catch(e) {}
  return { consecutiveFailures: 0, lastError: null };
}

function saveStatus(status) {
  fs.writeFileSync(CONFIG.STATUS_FILE, JSON.stringify(status, null, 2));
}

function updateLastUpdated() {
  const ts = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  fs.writeFileSync(CONFIG.LAST_UPDATED_FILE, ts);
}

async function backupData() {
  if (fs.existsSync(CONFIG.DATA_FILE)) {
    fs.copyFileSync(CONFIG.DATA_FILE, CONFIG.BACKUP_FILE);
    log('📦 数据已备份');
  }
}

async function restoreFromBackup() {
  if (fs.existsSync(CONFIG.BACKUP_FILE)) {
    fs.copyFileSync(CONFIG.BACKUP_FILE, CONFIG.DATA_FILE);
    log('♻️ 已从备份恢复数据');
  }
}

async function scrapeOrders() {
  let browser;
  for (let attempt = 1; attempt <= CONFIG.MAX_RETRIES; attempt++) {
    try {
      log(`🔄 第 ${attempt} 次尝试连接浏览器...`);
      browser = await puppeteer.connect({
        browserURL: `http://localhost:${CONFIG.CDP_PORT}`,
        defaultViewport: { width: 1280, height: 800 }
      });
      break;
    } catch(err) {
      if (attempt === CONFIG.MAX_RETRIES) throw new Error(`无法连接浏览器: ${err.message}`);
      log(`⚠️ 连接失败，${CONFIG.RETRY_DELAY/1000}秒后重试...`);
      await sleep(CONFIG.RETRY_DELAY);
    }
  }

  const page = await browser.newPage();
  const orders = [];

  try {
    log('🌐 访问百居易订单页面...');
    await page.goto(`${CONFIG.MYHOSTEX_URL}/admin/orders`, { waitUntil: 'networkidle2', timeout: 60000 });

    // 检查登录状态
    const title = await page.title();
    if (title.includes('登录') || title.includes('login')) {
      throw new Error('浏览器未登录百居易，请先在浏览器中登录');
    }

    // 隐藏表格列（避免渲染阻塞）
    await page.addStyleTag({ content: '.col-actions,.col-operate { display: none !important; }' });

    // 提取订单数据
    const rawOrders = await page.evaluate(() => {
      const rows = document.querySelectorAll('table tbody tr');
      return Array.from(rows).map(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length < 6) return null;
        const guest = cells[1]?.textContent?.trim() || '';
        const room = cells[2]?.textContent?.trim() || '';
        const checkIn = cells[3]?.textContent?.trim() || '';
        const checkOut = cells[4]?.textContent?.trim() || '';
        const price = parseFloat(cells[5]?.textContent?.replace(/[^\d.]/g, '')) || 0;
        return { guest, room, checkIn, checkOut, price };
      }).filter(Boolean);
    });

    log(`📋 获取到 ${rawOrders.length} 条原始订单`);

    // 填充详细信息（从订单详情）
    for (const order of rawOrders) {
      try {
        // 查找对应的订单行并点击
        const orderRow = await page.locator('table tbody tr').filter({ hasText: order.guest }).first();
        await orderRow.click();
        await page.waitForTimeout(500);

        const detail = await page.evaluate(() => {
          const modal = document.querySelector('.order-detail, .modal, [class*="detail"]');
          if (!modal) return {};
          const getVal = label => {
            const el = modal.querySelector(`[class*="label"]:contains("${label}")`) ||
                       Array.from(modal.querySelectorAll('*')).find(e => e.textContent.includes(label));
            if (!el) return '';
            const next = el.nextElementSibling || el.parentElement?.nextElementSibling;
            return next?.textContent?.trim() || '';
          };
          return {
            commission: parseFloat(getVal('佣金')?.replace(/[^\d.]/g, '') || '0'),
            netPrice: parseFloat(getVal('净房费')?.replace(/[^\d.]/g, '') || '0'),
            status: document.querySelector('[class*="status"]')?.textContent?.includes('取消') ? 'cancelled' : 'accepted'
          };
        });

        orders.push({ ...order, ...detail, orderTime: new Date().toLocaleString('zh-CN') });
        await page.keyboard.press('Escape');
        await sleep(100);
      } catch(e) {
        // 单条失败不影响整体
        orders.push({ ...order, commission: 0, netPrice: order.price, status: 'accepted', orderTime: '-' });
      }
    }

  } finally {
    await page.close();
    await browser.disconnect();
  }

  return orders;
}

async function exportToExcel(orders) {
  try {
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(orders);
    XLSX.utils.book_append_sheet(wb, ws, '订单');
    const date = new Date().toISOString().substring(0, 10);
    const xlsxFile = `myhostex_orders_${date}.xlsx`;
    XLSX.writeFile(wb, xlsxFile);
    log(`📊 已导出 Excel: ${xlsxFile}`);
  } catch(e) {
    logError('Excel导出失败', e);
  }
}

async function main() {
  log('🚀 开始抓取百居易订单数据...');
  const status = getStatus();

  try {
    const orders = await scrapeOrders();

    // 保存数据
    await backupData();
    fs.writeFileSync(CONFIG.DATA_FILE, JSON.stringify(orders, null, 2));
    updateLastUpdated();

    // 导出 Excel
    await exportToExcel(orders);

    // 更新状态
    status.lastRun = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    status.lastSuccess = status.lastRun;
    status.consecutiveFailures = 0;
    status.lastError = null;
    saveStatus(status);

    log(`✅ 抓取完成，共 ${orders.length} 条订单`);
  } catch(err) {
    status.consecutiveFailures++;
    status.lastError = err.message;
    status.lastRun = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    saveStatus(status);

    logError('抓取失败', err);

    if (status.consecutiveFailures >= 3) {
      log('⚠️ 连续失败3次，从备份恢复数据');
      await restoreFromBackup();
    }

    process.exit(1);
  }
}

main();