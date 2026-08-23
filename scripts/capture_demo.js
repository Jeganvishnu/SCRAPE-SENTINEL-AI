import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

const screenshotsDir = path.join(rootDir, 'demo', 'screenshots');
const videoDir = path.join(rootDir, 'demo', 'video');

// Ensure directories exist
fs.mkdirSync(screenshotsDir, { recursive: true });
fs.mkdirSync(videoDir, { recursive: true });

async function runDemoCapture() {
  console.log('🚀 Starting Scrape Sentinel AI Automated Demo & Screenshot Capture...');
  
  const browser = await chromium.launch({
    headless: true,
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: videoDir,
      size: { width: 1920, height: 1080 }
    }
  });

  const page = await context.newPage();
  const baseUrl = 'http://localhost:5173';

  try {
    // 1. Dashboard Overview
    console.log('📸 Capturing Dashboard Overview (01_dashboard_overview.png)...');
    await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '01_dashboard_overview.png'), fullPage: false });

    // 2. Sources List
    console.log('📸 Capturing Target Sources (02_sources_list.png)...');
    await page.goto(`${baseUrl}/sources`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '02_sources_list.png'), fullPage: false });

    // 3. Scrape Runs History
    console.log('📸 Capturing Scrape Runs History (03_scrape_runs.png)...');
    await page.goto(`${baseUrl}/runs`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '03_scrape_runs.png'), fullPage: false });

    // 4. Healing Queue
    console.log('📸 Capturing Self-Healing Queue (04_healing_queue.png)...');
    await page.goto(`${baseUrl}/healing`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '04_healing_queue.png'), fullPage: false });

    // 5. AI Scraper Intelligence Panel
    console.log('📸 Capturing AI Scraper Intelligence Panel (05_ai_insights.png)...');
    await page.goto(`${baseUrl}/insights`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '05_ai_insights.png'), fullPage: false });

    // 6. System Settings
    console.log('📸 Capturing Settings & Config (06_settings_config.png)...');
    await page.goto(`${baseUrl}/settings`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(screenshotsDir, '06_settings_config.png'), fullPage: false });

    // 7. Complete Walkthrough Recording Loop
    console.log('🎬 Recording interactive demo workflow...');
    await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.goto(`${baseUrl}/insights`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    await page.goto(`${baseUrl}/healing`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    console.log('✅ Demo capture & workflow walkthrough completed successfully!');
  } catch (err) {
    console.error('❌ Error during demo capture:', err);
  } finally {
    const video = page.video();
    await context.close();
    await browser.close();

    if (video) {
      const videoPath = await video.path();
      const targetVideoPath = path.join(videoDir, 'demo_walkthrough.webm');
      if (fs.existsSync(videoPath)) {
        fs.copyFileSync(videoPath, targetVideoPath);
        console.log(`🎥 Demo video saved to: ${targetVideoPath}`);
      }
    }
  }
}

runDemoCapture();
