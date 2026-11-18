/* CSST 106 — Interactive Browser Suite (GitHub Pages) */

const REPO_URL = "https://github.com/BorceKhen/CSST106-4B-AY2627";

const COCO_CLASSES = [
  "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light",
  "fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow",
  "elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee",
  "skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard",
  "tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
  "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch",
  "potted plant","bed","dining table","toilet","tv","laptop","mouse","remote","keyboard","cell phone",
  "microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear",
  "hair drier","toothbrush"
];

const VOC_CLASSES = [
  "background","aeroplane","bicycle","bird","boat","bottle","bus","car","cat","chair","cow",
  "diningtable","dog","horse","motorbike","person","pottedplant","sheep","sofa","train","tvmonitor"
];

const VOC_PALETTE = [
  [15,23,42],[128,0,0],[0,128,0],[128,128,0],[0,0,128],[128,0,128],[0,128,128],[128,128,128],
  [64,0,0],[192,0,0],[64,128,0],[192,128,0],[64,0,128],[192,0,128],[64,128,128],[56,189,248],
  [0,64,0],[128,64,0],[0,192,0],[128,192,0],[0,64,128]
];

const LABS = [
  {
    id: "lab1", num: "Lab 01", week: "Week 1–2", cat: "Image Processing", accent: "#38bdf8",
    title: "Image Representation & Manipulation",
    desc: "Explore 2D/3D pixel arrays, BGR vs. grayscale, pixel editing, ROI cropping, resizing, and 90° rotation.",
    sample: "./Lab_01_Images/sample_image.png",
    report: "./Lab_01_Images/Borce_Lab_01_Report.docx",
    manual: "./Lab_01_Images/CSST106_Lab_Experiment_01_Images.docx",
    code: "Lab_01_Images/lab1_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5" fill="currentColor"/><path d="M21 16l-5-5-4 4-3-3-6 6"/></svg>`
  },
  {
    id: "lab2", num: "Lab 02", week: "Week 3–4", cat: "Image Processing", accent: "#a78bfa",
    title: "Edge Detection (Sobel vs. Canny)",
    desc: "Gaussian smoothing, Sobel directional X/Y gradients & magnitude, Canny hysteresis (T1/T2), and Q&A.",
    sample: "./Lab_02_Edge_Detection/input.jpg",
    report: "./Lab_02_Edge_Detection/Borce_Lab_02_Report.docx",
    manual: "./Lab_02_Edge_Detection/CSST106_Lab_Experiment_02_Edge_Detection.docx",
    code: "Lab_02_Edge_Detection/lab2_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l5-10 4 9 4-11 5 8"/></svg>`
  },
  {
    id: "lab3", num: "Lab 03", week: "Week 4–5", cat: "Image Processing", accent: "#34d399",
    title: "Histogram Equalization & Contrast",
    desc: "Global equalizeHist (Gray & YUV), linear contrast stretch, adaptive CLAHE tuning, and live histograms.",
    sample: "./Lab_03_Histogram/sample_low_contrast.png",
    report: "./Lab_03_Histogram/Borce_Lab_03_Report.docx",
    manual: "./Lab_03_Histogram/CSST106_Lab_Experiment_03_Histogram.docx",
    code: "Lab_03_Histogram/lab3_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="12" width="3" height="8" rx="1"/><rect x="9" y="7" width="3" height="13" rx="1"/><rect x="14" y="4" width="3" height="16" rx="1"/><rect x="19" y="10" width="3" height="10" rx="1"/></svg>`
  },
  {
    id: "lab4", num: "Lab 04", week: "Week 6", cat: "Features & ML", accent: "#fbbf24",
    title: "SURF, SIFT & ORB Feature Matching",
    desc: "Rich keypoint detection, two-image descriptor matching, SIFT vs. ORB benchmark, and U-SURF notes.",
    sample: "./Lab_04_SURF_Feature_Detection/sample_image.jpg",
    sample2: "./Lab_04_SURF_Feature_Detection/sample_image_transformed.jpg",
    report: "./Lab_04_SURF_Feature_Detection/Borce_Lab_04_Report.docx",
    manual: "./Lab_04_SURF_Feature_Detection/CSST106_Lab_Experiment_04_SURF_Feature_Detection.docx",
    code: "Lab_04_SURF_Feature_Detection/lab4_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="7" r="2" fill="currentColor"/><circle cx="18" cy="6" r="2" fill="currentColor"/><circle cx="12" cy="13" r="2" fill="currentColor"/><circle cx="6" cy="18" r="2" fill="currentColor"/><circle cx="18" cy="17" r="2" fill="currentColor"/><path d="M7.5 8l3 4M16.5 7l-3 5M7.5 17l3-3M16.5 16l-3-2"/></svg>`
  },
  {
    id: "lab5", num: "Lab 05", week: "Week 7–8", cat: "Features & ML", accent: "#f472b6",
    title: "PCA Facial Recognition (Eigenfaces)",
    desc: "LFW faces, Eigenfaces gallery, 90% variance curve, whitening comparison, RBF SVM, and failure analysis.",
    report: "./Lab_05_PCA_in_CV/Borce_Lab_05_Report.docx",
    manual: "./Lab_05_PCA_in_CV/CSST106_Lab_Experiment_05_PCA_in_CV.docx",
    code: "Lab_05_PCA_in_CV/lab5_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="3" width="14" height="18" rx="5"/><circle cx="9.5" cy="10" r="1" fill="currentColor"/><circle cx="14.5" cy="10" r="1" fill="currentColor"/><path d="M9 15c1.5 1.5 4.5 1.5 6 0"/></svg>`
  },
  {
    id: "lab6", num: "Lab 06", week: "Week 8–9", cat: "Deep Learning", accent: "#fb7185",
    title: "YOLOv11 Real-Time Object Detection",
    desc: "Browser ONNX YOLOv11n inference on images & live webcam, confidence tuning, and custom dataset setup.",
    sample: "./Lab_06_YOLO_Object_Detection/sample_scene.jpg",
    report: "./Lab_06_YOLO_Object_Detection/Borce_Lab_06_Report.docx",
    manual: "./Lab_06_YOLO_Object_Detection/CSST106_Lab_Experiment_06_YOLOV8_Object_Detection.docx",
    code: "Lab_06_YOLO_Object_Detection/lab6_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 8V4h4M20 8V4h-4M4 16v4h4M20 16v4h-4"/><circle cx="12" cy="12" r="3"/></svg>`
  },
  {
    id: "lab7", num: "Lab 07", week: "Week 13", cat: "Deep Learning", accent: "#2dd4bf",
    title: "Image Segmentation Techniques",
    desc: "Otsu/Adaptive thresholding, Region Growing & Watershed, Canny contours, DeepLabV3 ONNX, and IoU metrics.",
    sample: "./Lab_07_Segmentation/sample_objects.png",
    sample2: "./Lab_07_Segmentation/sample_scene.jpg",
    report: "./Lab_07_Segmentation/Borce_Lab_07_Report.docx",
    manual: "./Lab_07_Segmentation/CSST106_Lab_Experiment_07_Segmetation.docx",
    code: "Lab_07_Segmentation/lab7_ui.py",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9.5" cy="10" r="5" fill="currentColor" fill-opacity="0.25"/><circle cx="14.5" cy="14" r="5" fill="currentColor" fill-opacity="0.55"/></svg>`
  }
];

// ============================================================================
// IMAGE / CV HELPERS (PURE JS + ONNX)
// ============================================================================
const offCvs = document.createElement("canvas");
const offCtx = offCvs.getContext("2d", { willReadFrequently: true });

function loadHTMLImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

function imgToImageData(img, maxDim = 720) {
  let w = img.naturalWidth || img.width;
  let h = img.naturalHeight || img.height;
  if (Math.max(w, h) > maxDim) {
    const sc = maxDim / Math.max(w, h);
    w = Math.round(w * sc);
    h = Math.round(h * sc);
  }
  offCvs.width = w;
  offCvs.height = h;
  offCtx.drawImage(img, 0, 0, w, h);
  return offCtx.getImageData(0, 0, w, h);
}

function cloneImageData(id) {
  return new ImageData(new Uint8ClampedArray(id.data), id.width, id.height);
}

function toGrayArray(id) {
  const { data, width: w, height: h } = id;
  const g = new Uint8Array(w * h);
  for (let i = 0, j = 0; i < data.length; i += 4, j++) {
    g[j] = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
  }
  return g;
}

function grayToImageData(g, w, h) {
  const out = new Uint8ClampedArray(w * h * 4);
  for (let i = 0, j = 0; i < g.length; i++, j += 4) {
    const v = g[i];
    out[j] = v; out[j + 1] = v; out[j + 2] = v; out[j + 3] = 255;
  }
  return new ImageData(out, w, h);
}

function drawImageData(canvas, id) {
  canvas.width = id.width;
  canvas.height = id.height;
  canvas.getContext("2d").putImageData(id, 0, 0);
}

function gaussianBlurGray(g, w, h, ksize) {
  if (ksize <= 1) return new Uint8Array(g);
  const kernels = {
    3: [1, 2, 1, 2, 4, 2, 1, 2, 1],
    5: [1,4,6,4,1, 4,16,24,16,4, 6,24,36,24,6, 4,16,24,16,4, 1,4,6,4,1],
    7: [0,0,1,2,1,0,0, 0,3,13,22,13,3,0, 1,13,59,97,59,13,1, 2,22,97,159,97,22,2, 1,13,59,97,59,13,1, 0,3,13,22,13,3,0, 0,0,1,2,1,0,0]
  };
  const ker = kernels[ksize] || kernels[3];
  const sum = ker.reduce((a, b) => a + b, 0);
  const r = (ksize - 1) >> 1;
  const out = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      let acc = 0, ki = 0;
      for (let dy = -r; dy <= r; dy++) {
        const yy = Math.min(h - 1, Math.max(0, y + dy));
        for (let dx = -r; dx <= r; dx++) {
          const xx = Math.min(w - 1, Math.max(0, x + dx));
          acc += g[yy * w + xx] * ker[ki++];
        }
      }
      out[y * w + x] = Math.round(acc / sum);
    }
  }
  return out;
}

function computeSobel(g, w, h) {
  const gx = new Float32Array(w * h);
  const gy = new Float32Array(w * h);
  const mag = new Float32Array(w * h);
  let maxM = 1;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const vx = -g[(y-1)*w+x-1] + g[(y-1)*w+x+1] - 2*g[y*w+x-1] + 2*g[y*w+x+1] - g[(y+1)*w+x-1] + g[(y+1)*w+x+1];
      const vy = -g[(y-1)*w+x-1] - 2*g[(y-1)*w+x] - g[(y-1)*w+x+1] + g[(y+1)*w+x-1] + 2*g[(y+1)*w+x] + g[(y+1)*w+x+1];
      gx[i] = vx; gy[i] = vy;
      const m = Math.hypot(vx, vy);
      mag[i] = m;
      if (m > maxM) maxM = m;
    }
  }
  const u8 = new Uint8Array(w * h);
  const gxU8 = new Uint8Array(w * h);
  const gyU8 = new Uint8Array(w * h);
  for (let i = 0; i < w * h; i++) {
    u8[i] = Math.min(255, Math.round((mag[i] / maxM) * 255));
    gxU8[i] = Math.min(255, Math.abs(Math.round(gx[i])));
    gyU8[i] = Math.min(255, Math.abs(Math.round(gy[i])));
  }
  return { gx, gy, mag, maxM, u8, gxU8, gyU8 };
}

function computeCanny(g, w, h, t1, t2) {
  const low = Math.min(t1, t2), high = Math.max(t1, t2);
  const { gx, gy, mag } = computeSobel(g, w, h);
  const nms = new Float32Array(w * h);
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const m = mag[i];
      if (m === 0) continue;
      let ang = (Math.atan2(gy[i], gx[i]) * 180) / Math.PI;
      if (ang < 0) ang += 180;
      let m1 = 0, m2 = 0;
      if (ang < 22.5 || ang >= 157.5) { m1 = mag[i - 1]; m2 = mag[i + 1]; }
      else if (ang < 67.5) { m1 = mag[(y - 1) * w + x + 1]; m2 = mag[(y + 1) * w + x - 1]; }
      else if (ang < 112.5) { m1 = mag[(y - 1) * w + x]; m2 = mag[(y + 1) * w + x]; }
      else { m1 = mag[(y - 1) * w + x - 1]; m2 = mag[(y + 1) * w + x + 1]; }
      if (m >= m1 && m >= m2) nms[i] = m;
    }
  }
  const out = new Uint8Array(w * h);
  const stack = [];
  for (let i = 0; i < w * h; i++) {
    if (nms[i] >= high) { out[i] = 255; stack.push(i); }
    else if (nms[i] >= low) out[i] = 128;
  }
  while (stack.length) {
    const idx = stack.pop();
    const x = idx % w, y = (idx - x) / w;
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const nx = x + dx, ny = y + dy;
        if (nx >= 0 && nx < w && ny >= 0 && ny < h) {
          const ni = ny * w + nx;
          if (out[ni] === 128) { out[ni] = 255; stack.push(ni); }
        }
      }
    }
  }
  for (let i = 0; i < w * h; i++) if (out[i] !== 255) out[i] = 0;
  return out;
}

function histEqualizeGray(g) {
  const hist = new Uint32Array(256);
  for (let i = 0; i < g.length; i++) hist[g[i]]++;
  const cdf = new Uint32Array(256);
  let acc = 0, cdfMin = 0;
  for (let i = 0; i < 256; i++) {
    acc += hist[i];
    cdf[i] = acc;
    if (cdfMin === 0 && acc > 0) cdfMin = acc;
  }
  const denom = Math.max(1, g.length - cdfMin);
  const lut = new Uint8Array(256);
  for (let i = 0; i < 256; i++) lut[i] = Math.round(((cdf[i] - cdfMin) / denom) * 255);
  const out = new Uint8Array(g.length);
  for (let i = 0; i < g.length; i++) out[i] = lut[g[i]];
  return out;
}

function contrastStretchGray(g, loP, hiP) {
  const hist = new Uint32Array(256);
  for (let i = 0; i < g.length; i++) hist[g[i]]++;
  const loCount = (loP / 100) * g.length, hiCount = (hiP / 100) * g.length;
  let acc = 0, lo = 0, hi = 255;
  for (let i = 0; i < 256; i++) {
    acc += hist[i];
    if (acc >= loCount) { lo = i; break; }
  }
  acc = 0;
  for (let i = 0; i < 256; i++) {
    acc += hist[i];
    if (acc >= hiCount) { hi = i; break; }
  }
  const out = new Uint8Array(g.length);
  if (hi <= lo) { out.set(g); return out; }
  const scale = 255 / (hi - lo);
  for (let i = 0; i < g.length; i++) out[i] = Math.min(255, Math.max(0, Math.round((g[i] - lo) * scale)));
  return out;
}

function applyCLAHEGray(g, w, h, clipLimit, tiles) {
  const tx = tiles, ty = tiles;
  const tileW = w / tx, tileH = h / ty;
  const luts = Array.from({ length: ty }, () => Array(tx));
  for (let r = 0; r < ty; r++) {
    const y0 = Math.floor(r * tileH), y1 = Math.min(h, Math.floor((r + 1) * tileH));
    for (let c = 0; c < tx; c++) {
      const x0 = Math.floor(c * tileW), x1 = Math.min(w, Math.floor((c + 1) * tileW));
      const hist = new Float32Array(256);
      let n = 0;
      for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) { hist[g[y * w + x]]++; n++; }
      const limit = Math.max(1, (clipLimit * n) / 256);
      let excess = 0;
      for (let i = 0; i < 256; i++) {
        if (hist[i] > limit) { excess += hist[i] - limit; hist[i] = limit; }
      }
      const add = excess / 256;
      const lut = new Uint8Array(256);
      let cdf = 0;
      for (let i = 0; i < 256; i++) {
        cdf += hist[i] + add;
        lut[i] = Math.min(255, Math.round((cdf / Math.max(1, n)) * 255));
      }
      luts[r][c] = lut;
    }
  }
  const out = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    const gy = (y + 0.5) / tileH - 0.5;
    const r0 = Math.max(0, Math.min(ty - 1, Math.floor(gy)));
    const r1 = Math.min(ty - 1, r0 + 1);
    const fy = Math.max(0, Math.min(1, gy - r0));
    for (let x = 0; x < w; x++) {
      const gx = (x + 0.5) / tileW - 0.5;
      const c0 = Math.max(0, Math.min(tx - 1, Math.floor(gx)));
      const c1 = Math.min(tx - 1, c0 + 1);
      const fx = Math.max(0, Math.min(1, gx - c0));
      const v = g[y * w + x];
      const top = luts[r0][c0][v] * (1 - fx) + luts[r0][c1][v] * fx;
      const bot = luts[r1][c0][v] * (1 - fx) + luts[r1][c1][v] * fx;
      out[y * w + x] = Math.round(top * (1 - fy) + bot * fy);
    }
  }
  return out;
}

function getCanvasBg() {
  return getComputedStyle(document.documentElement).getPropertyValue("--canvas-bg").trim() || "#0b1120";
}

function drawHistCanvas(canvas, g, color) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width = canvas.clientWidth || 260;
  const h = canvas.height = 92;
  ctx.fillStyle = getCanvasBg();
  ctx.fillRect(0, 0, w, h);
  const hist = new Uint32Array(256);
  for (let i = 0; i < g.length; i++) hist[g[i]]++;
  const sorted = Array.from(hist).sort((a, b) => a - b);
  const cap = Math.max(sorted[251] || 1, Math.max(...hist) * 0.35, 1);
  ctx.beginPath();
  ctx.moveTo(0, h - 14);
  for (let i = 0; i < 256; i++) {
    const x = (i / 255) * w;
    const norm = Math.min(1, hist[i] / cap);
    ctx.lineTo(x, h - 14 - norm * (h - 20));
  }
  ctx.lineTo(w, h - 14);
  ctx.closePath();
  ctx.fillStyle = color + "55";
  ctx.fill();
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.stroke();
  ctx.fillStyle = "#64748b";
  ctx.font = "10px Consolas, monospace";
  ctx.fillText("0", 4, h - 3);
  ctx.fillText("128", w / 2 - 10, h - 3);
  ctx.fillText("255", w - 24, h - 3);
}

function otsuThreshold(g) {
  const hist = new Uint32Array(256);
  for (let i = 0; i < g.length; i++) hist[g[i]]++;
  let sum = 0;
  for (let i = 0; i < 256; i++) sum += i * hist[i];
  let sumB = 0, wB = 0, maxVar = -1, thr = 127;
  const total = g.length;
  for (let t = 0; t < 256; t++) {
    wB += hist[t];
    if (wB === 0) continue;
    const wF = total - wB;
    if (wF === 0) break;
    sumB += t * hist[t];
    const mB = sumB / wB, mF = (sum - sumB) / wF;
    const v = wB * wF * (mB - mF) ** 2;
    if (v > maxVar) { maxVar = v; thr = t; }
  }
  const out = new Uint8Array(total);
  for (let i = 0; i < total; i++) out[i] = g[i] > thr ? 255 : 0;
  return { thr, mask: out };
}

function detectCornersHarris(g, w, h, maxPts = 120) {
  const { gx, gy } = computeSobel(g, w, h);
  const scores = [];
  const step = 3;
  for (let y = 8; y < h - 8; y += step) {
    for (let x = 8; x < w - 8; x += step) {
      let ixx = 0, iyy = 0, ixy = 0;
      for (let dy = -2; dy <= 2; dy++) {
        for (let dx = -2; dx <= 2; dx++) {
          const k = (y + dy) * w + (x + dx);
          ixx += gx[k] * gx[k];
          iyy += gy[k] * gy[k];
          ixy += gx[k] * gy[k];
        }
      }
      const det = ixx * iyy - ixy * ixy;
      const tr = ixx + iyy;
      const r = det - 0.04 * tr * tr;
      if (r > 1e7) scores.push({ x, y, r });
    }
  }
  scores.sort((a, b) => b.r - a.r);
  const kept = [];
  for (const s of scores) {
    if (kept.every(k => Math.hypot(k.x - s.x, k.y - s.y) > 10)) {
      kept.push(s);
      if (kept.length >= maxPts) break;
    }
  }
  return kept;
}

// ============================================================================
// ONNX SESSIONS (LAZY LOADED)
// ============================================================================
let yoloSess = null, deeplabSess = null, lab5Data = null;

async function getYoloSession() {
  if (!yoloSess) yoloSess = await ort.InferenceSession.create("./web_assets/yolo11n.onnx", { executionProviders: ["wasm"] });
  return yoloSess;
}
async function getDeepLabSession() {
  if (!deeplabSess) deeplabSess = await ort.InferenceSession.create("./web_assets/deeplabv3_voc.onnx", { executionProviders: ["wasm"] });
  return deeplabSess;
}
async function getLab5Data() {
  if (!lab5Data) lab5Data = await (await fetch("./web_assets/lab5_data.json")).json();
  return lab5Data;
}

function iou(a, b) {
  const x1 = Math.max(a[0], b[0]), y1 = Math.max(a[1], b[1]);
  const x2 = Math.min(a[2], b[2]), y2 = Math.min(a[3], b[3]);
  const inter = Math.max(0, x2 - x1) * Math.max(0, y2 - y1);
  const ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter;
  return ua > 0 ? inter / ua : 0;
}

async function runYoloOnImageData(id, confThr = 0.25) {
  const sess = await getYoloSession();
  const S = 640;
  const scale = Math.min(S / id.width, S / id.height);
  const nw = Math.round(id.width * scale), nh = Math.round(id.height * scale);
  const padX = Math.floor((S - nw) / 2), padY = Math.floor((S - nh) / 2);

  const tmp = document.createElement("canvas");
  tmp.width = S; tmp.height = S;
  const tctx = tmp.getContext("2d");
  tctx.fillStyle = "rgb(114,114,114)";
  tctx.fillRect(0, 0, S, S);
  const srcC = document.createElement("canvas");
  srcC.width = id.width; srcC.height = id.height;
  srcC.getContext("2d").putImageData(id, 0, 0);
  tctx.drawImage(srcC, padX, padY, nw, nh);

  const px = tctx.getImageData(0, 0, S, S).data;
  const inp = new Float32Array(3 * S * S);
  for (let i = 0, p = 0; i < S * S; i++, p += 4) {
    inp[i] = px[p] / 255;
    inp[S * S + i] = px[p + 1] / 255;
    inp[2 * S * S + i] = px[p + 2] / 255;
  }

  const t0 = performance.now();
  const res = await sess.run({ [sess.inputNames[0]]: new ort.Tensor("float32", inp, [1, 3, S, S]) });
  const ms = performance.now() - t0;
  const out = res[sess.outputNames[0]].data; // [1, 84, 8400]
  const N = 8400;
  const cand = [];
  for (let i = 0; i < N; i++) {
    let bestC = -1, bestS = 0;
    for (let c = 0; c < 80; c++) {
      const s = out[(4 + c) * N + i];
      if (s > bestS) { bestS = s; bestC = c; }
    }
    if (bestS >= confThr) {
      const cx = out[0 * N + i], cy = out[1 * N + i], bw = out[2 * N + i], bh = out[3 * N + i];
      const x1 = Math.max(0, (cx - bw / 2 - padX) / scale);
      const y1 = Math.max(0, (cy - bh / 2 - padY) / scale);
      const x2 = Math.min(id.width, (cx + bw / 2 - padX) / scale);
      const y2 = Math.min(id.height, (cy + bh / 2 - padY) / scale);
      cand.push({ cls: COCO_CLASSES[bestC], clsId: bestC, conf: bestS, box: [x1, y1, x2, y2] });
    }
  }
  cand.sort((a, b) => b.conf - a.conf);
  const kept = [];
  for (const d of cand) {
    if (kept.every(k => k.clsId !== d.clsId || iou(k.box, d.box) < 0.45)) kept.push(d);
  }
  return { detections: kept, ms };
}

async function runDeepLabOnImageData(id) {
  const sess = await getDeepLabSession();
  const S = 384;
  const tmp = document.createElement("canvas");
  tmp.width = S; tmp.height = S;
  const srcC = document.createElement("canvas");
  srcC.width = id.width; srcC.height = id.height;
  srcC.getContext("2d").putImageData(id, 0, 0);
  tmp.getContext("2d").drawImage(srcC, 0, 0, S, S);
  const px = tmp.getContext("2d").getImageData(0, 0, S, S).data;
  const inp = new Float32Array(3 * S * S);
  const mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225];
  for (let i = 0, p = 0; i < S * S; i++, p += 4) {
    inp[i] = (px[p] / 255 - mean[0]) / std[0];
    inp[S * S + i] = (px[p + 1] / 255 - mean[1]) / std[1];
    inp[2 * S * S + i] = (px[p + 2] / 255 - mean[2]) / std[2];
  }
  const out = (await sess.run({ input: new ort.Tensor("float32", inp, [1, 3, S, S]) })).output.data;
  const maskSmall = new ImageData(S, S);
  const found = new Set();
  for (let i = 0; i < S * S; i++) {
    let bestC = 0, bestV = -1e9;
    for (let c = 0; c < 21; c++) {
      const v = out[c * S * S + i];
      if (v > bestV) { bestV = v; bestC = c; }
    }
    if (bestC > 0) found.add(VOC_CLASSES[bestC]);
    const col = VOC_PALETTE[bestC];
    const p = i * 4;
    maskSmall.data[p] = col[0]; maskSmall.data[p + 1] = col[1]; maskSmall.data[p + 2] = col[2]; maskSmall.data[p + 3] = 255;
  }
  const mc = document.createElement("canvas");
  mc.width = S; mc.height = S;
  mc.getContext("2d").putImageData(maskSmall, 0, 0);
  const outC = document.createElement("canvas");
  outC.width = id.width; outC.height = id.height;
  const octx = outC.getContext("2d");
  octx.putImageData(id, 0, 0);
  octx.globalAlpha = 0.55;
  octx.drawImage(mc, 0, 0, id.width, id.height);
  return { imageData: octx.getImageData(0, 0, id.width, id.height), classes: Array.from(found) };
}

// ============================================================================
// UI CONTROLLER
// ============================================================================
let activeCat = "All", currentLab = null, camStream = null, camRaf = null, onThemeRefresh = null;
const homeView = document.getElementById("home-view");
const wsView = document.getElementById("workspace-view");
const gridEl = document.getElementById("grid");
const searchEl = document.getElementById("search");

const SUN_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>`;
const MOON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

function applyTheme(theme, animate = false) {
  if (animate) {
    document.body.classList.remove("theme-switching");
    void document.body.offsetWidth;
    document.body.classList.add("theme-switching");
  }
  document.documentElement.setAttribute("data-theme", theme);
  try { localStorage.setItem("csst106-theme", theme); } catch (_) {}
  const html = theme === "dark" ? `${SUN_SVG}<span>Light</span>` : `${MOON_SVG}<span>Dark</span>`;
  ["theme-toggle-home", "theme-toggle-ws"].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.innerHTML = html;
  });
  if (onThemeRefresh) onThemeRefresh();
}

function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme") || "dark";
  applyTheme(cur === "dark" ? "light" : "dark", true);
}

["theme-toggle-home", "theme-toggle-ws"].forEach(id => {
  const btn = document.getElementById(id);
  if (btn) btn.onclick = toggleTheme;
});
applyTheme((() => { try { return localStorage.getItem("csst106-theme") || "dark"; } catch (_) { return "dark"; } })(), false);

function triggerViewAnim(el) {
  el.classList.remove("anim-view");
  void el.offsetWidth;
  el.classList.add("anim-view");
}

function stopCam() {
  if (camRaf) { cancelAnimationFrame(camRaf); camRaf = null; }
  if (camStream) { camStream.getTracks().forEach(t => t.stop()); camStream = null; }
}

function renderHome() {
  stopCam();
  onThemeRefresh = null;
  homeView.style.display = "block";
  wsView.style.display = "none";
  triggerViewAnim(homeView);
  const q = searchEl.value.trim().toLowerCase();
  gridEl.innerHTML = "";
  LABS.filter(l => (activeCat === "All" || l.cat === activeCat) &&
    (!q || l.title.toLowerCase().includes(q) || l.desc.toLowerCase().includes(q) || l.num.toLowerCase().includes(q)))
    .forEach(l => {
      const card = document.createElement("article");
      card.className = "card";
      card.style.setProperty("--accent", l.accent);
      card.innerHTML = `
        <div class="card-head">
          <div class="lab-icon" style="color:${l.accent};border-color:${l.accent};background:${l.accent}1f">${l.icon}</div>
          <div>
            <div class="card-top">
              <span class="lab-pill">${l.num}</span>
              <span class="tag">${l.week}</span>
              <span class="tag">${l.cat}</span>
            </div>
            <h2>${l.title}</h2>
          </div>
        </div>
        <p>${l.desc}</p>
        <div class="card-actions">
          <button class="btn btn-lab" data-open="${l.id}">▶ Launch Lab</button>
          <a class="btn" href="${l.report}">Report (.docx)</a>
          <a class="btn" href="${l.manual}">Manual (.docx)</a>
        </div>`;
      card.querySelector("[data-open]").onclick = () => openLab(l);
      gridEl.appendChild(card);
    });
}

document.getElementById("chips").addEventListener("click", (e) => {
  if (!e.target.dataset.cat) return;
  activeCat = e.target.dataset.cat;
  document.querySelectorAll(".chip").forEach(c => c.classList.toggle("active", c.dataset.cat === activeCat));
  renderHome();
});
searchEl.addEventListener("input", renderHome);
document.getElementById("back-btn").onclick = renderHome;

async function openLab(lab) {
  stopCam();
  onThemeRefresh = null;
  currentLab = lab;
  homeView.style.display = "none";
  wsView.style.display = "block";
  triggerViewAnim(wsView);
  document.getElementById("ws-pill").textContent = lab.num;
  document.getElementById("ws-pill").style.background = lab.accent;
  document.getElementById("ws-title").textContent = lab.title;
  document.getElementById("ws-report").href = lab.report;
  document.getElementById("ws-code").href = `${REPO_URL}/blob/main/${lab.code}`;

  const body = document.getElementById("ws-body");
  body.innerHTML = `<div class="panel">Loading ${lab.num}...</div>`;

  if (lab.id === "lab1") await mountLab1(lab, body);
  else if (lab.id === "lab2") await mountLab2(lab, body);
  else if (lab.id === "lab3") await mountLab3(lab, body);
  else if (lab.id === "lab4") await mountLab4(lab, body);
  else if (lab.id === "lab5") await mountLab5(lab, body);
  else if (lab.id === "lab6") await mountLab6(lab, body);
  else if (lab.id === "lab7") await mountLab7(lab, body);
}

// ============================================================================
// LAB 1: IMAGE MANIPULATION
// ============================================================================
async function mountLab1(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample));
  let workId = cloneImageData(srcId);
  let tab = "properties", sel = [Math.min(95, srcId.height - 1), Math.min(520, srcId.width - 1)];

  body.innerHTML = `
    <div class="tab-bar" id="l1-tabs">
      ${["properties:Properties","grayscale:Grayscale","pixel:Modify Pixel","crop:Crop (ROI)","resize:Resize","rotate:Rotate"].map((s,i)=>{
        const [k,v]=s.split(":"); return `<button class="tab ${i===0?'active':''}" data-t="${k}">${v}</button>`;
      }).join("")}
      <label class="btn" style="margin-left:auto">Upload Image<input type="file" id="l1-file" accept="image/*" hidden></label>
      <button class="btn" id="l1-reset">Reset</button>
    </div>
    <div class="ws-grid-2">
      <div class="panel">
        <div class="panel-hdr"><span>ORIGINAL (CLICK PIXEL)</span><span id="l1-orig-dim"></span></div>
        <canvas id="l1-c1" class="cv-canvas clickable"></canvas>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span id="l1-out-hdr">OUTPUT</span><span id="l1-out-dim"></span></div>
        <canvas id="l1-c2" class="cv-canvas"></canvas>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>CONTROLS &amp; DETAILS</span></div>
        <div id="l1-ctrl" class="ctrl-stack"></div>
        <pre id="l1-info" class="mono-box"></pre>
      </div>
    </div>`;

  const c1 = document.getElementById("l1-c1"), c2 = document.getElementById("l1-c2");
  const state = { color: "#ff00ff", patch: 25, y0: 22, y1: 82, x0: 22, x1: 70, scale: 50, rot: 90 };

  function renderControls() {
    const el = document.getElementById("l1-ctrl");
    if (tab === "pixel") {
      el.innerHTML = `
        <label>Patch Color: <input type="color" id="l1-col" value="${state.color}"></label>
        <label>Patch Size: <span id="l1-psz">${state.patch}px</span><input type="range" id="l1-p" min="1" max="61" step="2" value="${state.patch}"></label>
        <button class="btn btn-primary" id="l1-apply">Apply at (${sel[0]}, ${sel[1]})</button>`;
      el.querySelector("#l1-col").oninput = e => state.color = e.target.value;
      el.querySelector("#l1-p").oninput = e => { state.patch = +e.target.value; el.querySelector("#l1-psz").textContent = state.patch + "px"; };
      el.querySelector("#l1-apply").onclick = () => {
        const rgb = [0,2,4].map(i => parseInt(state.color.slice(1+i,3+i),16));
        const half = Math.floor(state.patch / 2);
        for (let y = Math.max(0, sel[0]-half); y <= Math.min(workId.height-1, sel[0]+half); y++)
          for (let x = Math.max(0, sel[1]-half); x <= Math.min(workId.width-1, sel[1]+half); x++) {
            const k = (y * workId.width + x) * 4;
            workId.data[k]=rgb[0]; workId.data[k+1]=rgb[1]; workId.data[k+2]=rgb[2];
          }
        update();
      };
    } else if (tab === "crop") {
      el.innerHTML = ["y0","y1","x0","x1"].map(k =>
        `<label>${k.toUpperCase()}: <span id="v-${k}">${state[k]}%</span><input type="range" id="s-${k}" min="0" max="100" value="${state[k]}"></label>`).join("");
      ["y0","y1","x0","x1"].forEach(k => el.querySelector(`#s-${k}`).oninput = e => {
        state[k] = +e.target.value; el.querySelector(`#v-${k}`).textContent = state[k] + "%"; update();
      });
    } else if (tab === "resize") {
      el.innerHTML = `<label>Scale: <span id="v-sc">${state.scale}%</span><input type="range" id="s-sc" min="20" max="200" value="${state.scale}"></label>`;
      el.querySelector("#s-sc").oninput = e => { state.scale = +e.target.value; el.querySelector("#v-sc").textContent = state.scale + "%"; update(); };
    } else if (tab === "rotate") {
      el.innerHTML = `<div class="chips">${[90,180,270].map(d=>`<button class="chip ${state.rot===d?'active':''}" data-r="${d}">${d}° CW</button>`).join("")}</div>`;
      el.querySelectorAll("[data-r]").forEach(b => b.onclick = () => { state.rot = +b.dataset.r; renderControls(); update(); });
    } else el.innerHTML = "";
  }

  function update() {
    const h = workId.height, w = workId.width;
    drawImageData(c1, workId);
    const ctx1 = c1.getContext("2d");
    ctx1.strokeStyle = "#38bdf8"; ctx1.lineWidth = 2;
    ctx1.beginPath(); ctx1.arc(sel[1], sel[0], 6, 0, Math.PI * 2); ctx1.stroke();

    const kpx = (sel[0] * w + sel[1]) * 4;
    const r = workId.data[kpx], g = workId.data[kpx+1], b = workId.data[kpx+2];
    const grayPx = Math.round(0.299*r + 0.587*g + 0.114*b);
    document.getElementById("l1-orig-dim").textContent = `${w}×${h} • (3ch)`;

    let outId = cloneImageData(workId);
    if (tab === "grayscale") {
      outId = grayToImageData(toGrayArray(workId), w, h);
      document.getElementById("l1-out-hdr").textContent = "GRAYSCALE (2D)";
    } else if (tab === "crop") {
      const y0 = Math.floor(h * Math.min(state.y0, state.y1)/100), y1 = Math.max(y0+1, Math.floor(h * Math.max(state.y0, state.y1)/100));
      const x0 = Math.floor(w * Math.min(state.x0, state.x1)/100), x1 = Math.max(x0+1, Math.floor(w * Math.max(state.x0, state.x1)/100));
      ctx1.setLineDash([6, 4]); ctx1.strokeStyle = "#fbbf24"; ctx1.strokeRect(x0, y0, x1-x0, y1-y0); ctx1.setLineDash([]);
      c1.getContext("2d");
      const tmp = document.createElement("canvas"); tmp.width = x1-x0; tmp.height = y1-y0;
      const srcC = document.createElement("canvas"); srcC.width = w; srcC.height = h; srcC.getContext("2d").putImageData(workId,0,0);
      tmp.getContext("2d").drawImage(srcC, x0, y0, x1-x0, y1-y0, 0, 0, x1-x0, y1-y0);
      outId = tmp.getContext("2d").getImageData(0,0,x1-x0,y1-y0);
      document.getElementById("l1-out-hdr").textContent = "CROPPED ROI";
    } else if (tab === "resize") {
      const nw = Math.max(1, Math.round(w * state.scale / 100)), nh = Math.max(1, Math.round(h * state.scale / 100));
      const tmp = document.createElement("canvas"); tmp.width = nw; tmp.height = nh;
      const srcC = document.createElement("canvas"); srcC.width = w; srcC.height = h; srcC.getContext("2d").putImageData(workId,0,0);
      tmp.getContext("2d").drawImage(srcC, 0, 0, nw, nh);
      outId = tmp.getContext("2d").getImageData(0,0,nw,nh);
      document.getElementById("l1-out-hdr").textContent = `RESIZED (${state.scale}%)`;
    } else if (tab === "rotate") {
      const tmp = document.createElement("canvas"), tctx = tmp.getContext("2d");
      const srcC = document.createElement("canvas"); srcC.width = w; srcC.height = h; srcC.getContext("2d").putImageData(workId,0,0);
      if (state.rot === 180) { tmp.width = w; tmp.height = h; } else { tmp.width = h; tmp.height = w; }
      tctx.translate(tmp.width/2, tmp.height/2); tctx.rotate((state.rot * Math.PI)/180);
      tctx.drawImage(srcC, -w/2, -h/2);
      outId = tctx.getImageData(0,0,tmp.width,tmp.height);
      document.getElementById("l1-out-hdr").textContent = `ROTATED ${state.rot}°`;
    } else document.getElementById("l1-out-hdr").textContent = "PREVIEW";

    drawImageData(c2, outId);
    document.getElementById("l1-out-dim").textContent = `${outId.width}×${outId.height}`;
    document.getElementById("l1-info").textContent =
      `Original : (${h}, ${w}, 3) uint8\nOutput   : (${outId.height}, ${outId.width}, ${tab==='grayscale'?1:3})\n` +
      `Selected : (y=${sel[0]}, x=${sel[1]})\n  BGR    = [${b}, ${g}, ${r}]\n  RGB    = (${r}, ${g}, ${b})\n  Gray   = ${grayPx}`;
  }

  c1.onclick = e => {
    const rect = c1.getBoundingClientRect();
    const x = Math.min(workId.width-1, Math.max(0, Math.floor((e.clientX-rect.left)*workId.width/rect.width)));
    const y = Math.min(workId.height-1, Math.max(0, Math.floor((e.clientY-rect.top)*workId.height/rect.height)));
    sel = [y, x]; if (tab==="pixel") renderControls(); update();
  };
  document.getElementById("l1-tabs").addEventListener("click", e => {
    if (!e.target.dataset.t) return;
    tab = e.target.dataset.t;
    document.querySelectorAll("#l1-tabs .tab").forEach(b=>b.classList.toggle("active", b.dataset.t===tab));
    renderControls(); update();
  });
  document.getElementById("l1-file").onchange = async e => {
    if (!e.target.files[0]) return;
    srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])));
    workId = cloneImageData(srcId); sel = [Math.floor(workId.height/2), Math.floor(workId.width/2)];
    renderControls(); update();
  };
  document.getElementById("l1-reset").onclick = () => { workId = cloneImageData(srcId); renderControls(); update(); };
  renderControls(); update();
}

// ============================================================================
// LAB 2: EDGE DETECTION
// ============================================================================
async function mountLab2(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 560);
  let blurK = 3, t1 = 100, t2 = 200;

  body.innerHTML = `
    <div class="toolbar">
      <div class="chips">
        <span>Blur:</span>
        ${[1,3,5,7].map(k=>`<button class="chip ${k===3?'active':''}" data-b="${k}">${k===1?'Off':k+'×'+k}</button>`).join("")}
      </div>
      <label>Canny T1: <span id="l2-t1v">100</span> <input type="range" id="l2-t1" min="0" max="255" value="100"></label>
      <label>Canny T2: <span id="l2-t2v">200</span> <input type="range" id="l2-t2" min="0" max="255" value="200"></label>
      <label class="btn">Upload Image<input type="file" id="l2-file" accept="image/*" hidden></label>
    </div>
    <div class="ws-grid-3">
      <div class="panel"><div class="panel-hdr"><span>ORIGINAL (GRAYSCALE)</span></div><canvas id="l2-c1" class="cv-canvas"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>SOBEL MAGNITUDE</span><span id="l2-sm"></span></div><canvas id="l2-c2" class="cv-canvas"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>CANNY EDGES</span><span id="l2-cn"></span></div><canvas id="l2-c3" class="cv-canvas"></canvas></div>
    </div>
    <div class="panel qa-box">
      <h3>Question &amp; Conclusion</h3>
      <p><b>Differences between Sobel &amp; Canny:</b> Sobel produces continuous grayscale gradient magnitudes with thicker edge ridges and directional components (Gx, Gy), whereas Canny adds non-maximum suppression and dual hysteresis thresholds (<code>T1</code>, <code>T2</code>) to produce crisp 1-pixel-wide binary contours.</p>
    </div>`;

  function update() {
    const g = toGrayArray(srcId);
    const bl = gaussianBlurGray(g, srcId.width, srcId.height, blurK);
    const sob = computeSobel(bl, srcId.width, srcId.height);
    const can = computeCanny(bl, srcId.width, srcId.height, t1, t2);
    let nz = 0; for (let i=0;i<can.length;i++) if (can[i]) nz++;
    drawImageData(document.getElementById("l2-c1"), grayToImageData(g, srcId.width, srcId.height));
    drawImageData(document.getElementById("l2-c2"), grayToImageData(sob.u8, srcId.width, srcId.height));
    drawImageData(document.getElementById("l2-c3"), grayToImageData(can, srcId.width, srcId.height));
    document.getElementById("l2-sm").textContent = `Max=${sob.maxM.toFixed(0)}`;
    document.getElementById("l2-cn").textContent = `${nz.toLocaleString()} px (${(nz*100/can.length).toFixed(2)}%)`;
  }

  body.querySelectorAll("[data-b]").forEach(b => b.onclick = () => {
    blurK = +b.dataset.b;
    body.querySelectorAll("[data-b]").forEach(x => x.classList.toggle("active", +x.dataset.b === blurK));
    update();
  });
  body.querySelector("#l2-t1").oninput = e => { t1 = +e.target.value; body.querySelector("#l2-t1v").textContent = t1; update(); };
  body.querySelector("#l2-t2").oninput = e => { t2 = +e.target.value; body.querySelector("#l2-t2v").textContent = t2; update(); };
  body.querySelector("#l2-file").onchange = async e => { if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 560); update(); } };
  update();
}

// ============================================================================
// LAB 3: HISTOGRAM EQUALIZATION & CONTRAST
// ============================================================================
async function mountLab3(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 520);
  let clip = 2.0, tiles = 8;

  body.innerHTML = `
    <div class="toolbar">
      <label>CLAHE Clip Limit: <span id="l3-cv">2.0</span> <input type="range" id="l3-clip" min="1" max="10" step="0.5" value="2.0"></label>
      <div class="chips"><span>Tiles:</span>${[4,8,16].map(t=>`<button class="chip ${t===8?'active':''}" data-ti="${t}">${t}×${t}</button>`).join("")}</div>
      <label class="btn">Upload Image<input type="file" id="l3-file" accept="image/*" hidden></label>
    </div>
    <div class="ws-grid-4">
      <div class="panel"><div class="panel-hdr"><span>ORIGINAL</span></div><canvas id="l3-c1" class="cv-canvas"></canvas><canvas id="l3-h1"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>LINEAR STRETCH</span></div><canvas id="l3-c2" class="cv-canvas"></canvas><canvas id="l3-h2"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>GLOBAL EQUALIZATION</span></div><canvas id="l3-c3" class="cv-canvas"></canvas><canvas id="l3-h3"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>CLAHE</span></div><canvas id="l3-c4" class="cv-canvas"></canvas><canvas id="l3-h4"></canvas></div>
    </div>
    <div class="panel qa-box">
      <h3>Observations &amp; Key Concepts</h3>
      <p>Global equalization stretches the full 0–255 dynamic range via the CDF but can amplify noise in uniform regions; <b>CLAHE</b> operates on local <code>${tiles}×${tiles}</code> tiles with histogram clipping to enhance local detail without blowing out highlights.</p>
    </div>`;

  function update() {
    const g = toGrayArray(srcId);
    const lin = contrastStretchGray(g, 1, 99);
    const glob = histEqualizeGray(g);
    const cl = applyCLAHEGray(g, srcId.width, srcId.height, clip, tiles);
    [[g,"#l3-c1","#l3-h1","#94a3b8"],[lin,"#l3-c2","#l3-h2","#fbbf24"],[glob,"#l3-c3","#l3-h3","#38bdf8"],[cl,"#l3-c4","#l3-h4","#34d399"]].forEach(([arr,cid,hid,col])=>{
      drawImageData(body.querySelector(cid), grayToImageData(arr, srcId.width, srcId.height));
      drawHistCanvas(body.querySelector(hid), arr, col);
    });
  }
  body.querySelector("#l3-clip").oninput = e => { clip = +e.target.value; body.querySelector("#l3-cv").textContent = clip.toFixed(1); update(); };
  body.querySelectorAll("[data-ti]").forEach(b => b.onclick = () => {
    tiles = +b.dataset.ti;
    body.querySelectorAll("[data-ti]").forEach(x => x.classList.toggle("active", +x.dataset.ti === tiles));
    update();
  });
  body.querySelector("#l3-file").onchange = async e => { if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 520); update(); } };
  update();
}

// ============================================================================
// LAB 4: FEATURE DETECTION & MATCHING
// ============================================================================
async function mountLab4(lab, body) {
  let id1 = imgToImageData(await loadHTMLImage(lab.sample), 480);
  let id2 = imgToImageData(await loadHTMLImage(lab.sample2), 480);

  body.innerHTML = `
    <div class="toolbar">
      <span class="tag">Browser Harris/FAST Keypoint Matcher + OpenCV SIFT/ORB Notes</span>
      <label class="btn">Upload Image 1<input type="file" id="l4-f1" accept="image/*" hidden></label>
      <label class="btn">Upload Image 2<input type="file" id="l4-f2" accept="image/*" hidden></label>
    </div>
    <div class="ws-grid-2">
      <div class="panel"><div class="panel-hdr"><span>DETECTED KEYPOINTS (IMAGE 1)</span><span id="l4-kcnt"></span></div><canvas id="l4-c1" class="cv-canvas"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>PATCH DESCRIPTOR MATCHING (IMG 1 ↔ IMG 2)</span><span id="l4-mcnt"></span></div><canvas id="l4-c2" class="cv-canvas"></canvas></div>
    </div>
    <div class="panel qa-box">
      <h3>SURF vs. SIFT vs. ORB Summary</h3>
      <p><b>Hessian Threshold:</b> Higher thresholds keep only strong, prominent keypoints; lower thresholds yield more keypoints. <b>Descriptors:</b> Encode local gradient patterns (64-D in SURF, 128-D in SIFT, 32-B binary in ORB) for cross-view matching. <b>Speed:</b> ORB (~5.6 ms) is fastest and patent-free, SIFT (~50.1 ms) is highest precision; U-SURF skips orientation for speed on upright views.</p>
    </div>`;

  function patchDesc(g, w, h, x, y) {
    const v = [];
    let mean = 0;
    for (let dy = -6; dy <= 6; dy += 2) for (let dx = -6; dx <= 6; dx += 2) {
      const val = g[Math.min(h-1,Math.max(0,y+dy))*w + Math.min(w-1,Math.max(0,x+dx))];
      v.push(val); mean += val;
    }
    mean /= v.length;
    return v.map(z => z - mean);
  }

  function update() {
    const g1 = toGrayArray(id1), g2 = toGrayArray(id2);
    const kp1 = detectCornersHarris(g1, id1.width, id1.height, 90);
    const kp2 = detectCornersHarris(g2, id2.width, id2.height, 90);
    const c1 = body.querySelector("#l4-c1");
    drawImageData(c1, grayToImageData(g1, id1.width, id1.height));
    const ctx1 = c1.getContext("2d");
    ctx1.strokeStyle = "#fbbf24"; ctx1.lineWidth = 1.5;
    kp1.forEach(p => { ctx1.beginPath(); ctx1.arc(p.x, p.y, 5, 0, Math.PI*2); ctx1.stroke(); });

    const d1 = kp1.map(p => patchDesc(g1, id1.width, id1.height, p.x, p.y));
    const d2 = kp2.map(p => patchDesc(g2, id2.width, id2.height, p.x, p.y));
    const matches = [];
    for (let i = 0; i < d1.length; i++) {
      let bestJ = -1, b1 = 1e18, b2 = 1e18;
      for (let j = 0; j < d2.length; j++) {
        let dist = 0; for (let k=0;k<d1[i].length;k++) dist += (d1[i][k]-d2[j][k])**2;
        if (dist < b1) { b2 = b1; b1 = dist; bestJ = j; } else if (dist < b2) b2 = dist;
      }
      if (bestJ >= 0 && b1 < 0.72 * b2) matches.push([kp1[i], kp2[bestJ]]);
    }

    const c2 = body.querySelector("#l4-c2");
    c2.width = id1.width + id2.width; c2.height = Math.max(id1.height, id2.height);
    const ctx2 = c2.getContext("2d");
    ctx2.putImageData(grayToImageData(g1, id1.width, id1.height), 0, 0);
    ctx2.putImageData(grayToImageData(g2, id2.width, id2.height), id1.width, 0);
    ctx2.strokeStyle = "#38bdf8"; ctx2.lineWidth = 1.4;
    matches.slice(0, 35).forEach(([a, b]) => {
      ctx2.beginPath(); ctx2.moveTo(a.x, a.y); ctx2.lineTo(id1.width + b.x, b.y); ctx2.stroke();
    });
    body.querySelector("#l4-kcnt").textContent = `${kp1.length} kp`;
    body.querySelector("#l4-mcnt").textContent = `${matches.length} matches`;
  }
  body.querySelector("#l4-f1").onchange = async e => { if (e.target.files[0]) { id1 = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480); update(); } };
  body.querySelector("#l4-f2").onchange = async e => { if (e.target.files[0]) { id2 = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480); update(); } };
  update();
}

// ============================================================================
// LAB 5: PCA EIGENFACES (PRE-EXPORTED REAL LFW RESULTS)
// ============================================================================
async function mountLab5(lab, body) {
  const d = await getLab5Data();
  let selK = 150, selSample = 0;

  body.innerHTML = `
    <div class="toolbar">
      <span class="tag">LFW (${d.n_samples} faces • ${d.h}×${d.w})</span>
      <span class="tag">SVM Accuracy: ${d.acc_whiten}% (whiten=True) vs ${d.acc_no_whiten}%</span>
      <span class="tag">90% Variance @ k=${d.k90}</span>
    </div>
    <div class="ws-grid-2">
      <div class="panel">
        <div class="panel-hdr"><span>TOP 9 VS LAST 3 EIGENFACES</span></div>
        <div id="l5-ef" class="face-grid"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>CUMULATIVE EXPLAINED VARIANCE</span><span id="l5-kv">k=150 → ${d.cum_var[149]}%</span></div>
        <canvas id="l5-var" height="220"></canvas>
        <input type="range" id="l5-k" min="1" max="150" value="150" style="width:100%;margin-top:8px">
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>PROGRAMMATIC FAILURE ANALYSIS (${d.mis_count} ERRORS)</span></div>
        <div id="l5-fail" class="face-grid"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>PCA RECONSTRUCTION ACROSS k COMPONENTS</span></div>
        <div class="chips" id="l5-sbtns">${d.recons.map((r,i)=>`<button class="chip ${i===0?'active':''}" data-s="${i}">${r.name}</button>`).join("")}</div>
        <div id="l5-rec" class="face-grid" style="margin-top:10px"></div>
      </div>
    </div>`;

  function makeFaceCanvas(pixels, label, color="#cbd5e1") {
    const wrap = document.createElement("div"); wrap.className = "face-item";
    const c = document.createElement("canvas"); c.width = d.w; c.height = d.h;
    c.getContext("2d").putImageData(grayToImageData(pixels, d.w, d.h), 0, 0);
    const cap = document.createElement("small"); cap.style.color = color; cap.textContent = label;
    wrap.append(c, cap);
    return wrap;
  }

  const efBox = body.querySelector("#l5-ef");
  d.eigenfaces.forEach(ef => efBox.appendChild(makeFaceCanvas(ef.pixels, `${ef.tag} #${ef.idx}`)));

  const failBox = body.querySelector("#l5-fail");
  d.failures.slice(0, 8).forEach(f => failBox.appendChild(makeFaceCanvas(f.pixels, `T:${f.true.split(" ").pop()} / P:${f.pred.split(" ").pop()}`, "#f87171")));

  function drawVariance() {
    const cvs = body.querySelector("#l5-var");
    const w = cvs.width = cvs.clientWidth || 480, h = cvs.height = 220;
    const ctx = cvs.getContext("2d");
    ctx.fillStyle = getCanvasBg(); ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "#fbbf24"; ctx.setLineDash([5, 4]);
    const y90 = h - 20 - 0.90 * (h - 35);
    ctx.beginPath(); ctx.moveTo(30, y90); ctx.lineTo(w - 10, y90); ctx.stroke();
    const x90 = 30 + ((d.k90 - 1) / 149) * (w - 40);
    ctx.strokeStyle = "#34d399";
    ctx.beginPath(); ctx.moveTo(x90, 15); ctx.lineTo(x90, h - 20); ctx.stroke();
    ctx.setLineDash([]);

    ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    d.cum_var.forEach((v, i) => {
      const x = 30 + (i / 149) * (w - 40), y = h - 20 - (v / 100) * (h - 35);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();

    const xSel = 30 + ((selK - 1) / 149) * (w - 40), ySel = h - 20 - (d.cum_var[selK - 1] / 100) * (h - 35);
    ctx.fillStyle = "#f472b6"; ctx.beginPath(); ctx.arc(xSel, ySel, 5, 0, Math.PI * 2); ctx.fill();
    body.querySelector("#l5-kv").textContent = `k=${selK} → ${d.cum_var[selK - 1]}%`;
  }

  function drawRecon() {
    const box = body.querySelector("#l5-rec"); box.innerHTML = "";
    const item = d.recons[selSample];
    box.appendChild(makeFaceCanvas(item.orig, "Original", "#38bdf8"));
    d.k_steps.forEach(k => box.appendChild(makeFaceCanvas(item.steps[String(k)], `k=${k}`)));
  }

  body.querySelector("#l5-k").oninput = e => { selK = +e.target.value; drawVariance(); };
  body.querySelectorAll("[data-s]").forEach(b => b.onclick = () => {
    selSample = +b.dataset.s;
    body.querySelectorAll("[data-s]").forEach(x => x.classList.toggle("active", +x.dataset.s === selSample));
    drawRecon();
  });
  onThemeRefresh = drawVariance;
  drawVariance(); drawRecon();
}

// ============================================================================
// LAB 6: YOLOV11 OBJECT DETECTION (LIVE ONNX IN BROWSER)
// ============================================================================
async function mountLab6(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 640);
  let conf = 0.25;

  body.innerHTML = `
    <div class="toolbar">
      <label>Confidence: <span id="l6-cv">0.25</span> <input type="range" id="l6-conf" min="0.10" max="0.90" step="0.05" value="0.25"></label>
      <label class="btn">Upload Image<input type="file" id="l6-file" accept="image/*" hidden></label>
      <button class="btn btn-primary" id="l6-cam">Start Live Webcam</button>
    </div>
    <div class="ws-grid-2">
      <div class="panel"><div class="panel-hdr"><span>YOLOv11n BROWSER DETECTIONS</span><span id="l6-stat">Loading ONNX...</span></div><canvas id="l6-c" class="cv-canvas"></canvas><video id="l6-vid" autoplay playsinline hidden></video></div>
      <div class="panel"><div class="panel-hdr"><span>DETECTED OBJECTS &amp; QUESTION</span></div><pre id="l6-list" class="mono-box"></pre>
        <div class="qa-box"><b>Object Detection vs Classification:</b> Classification assigns one label to the whole image; Object Detection predicts both bounding-box coordinates and class labels for every instance (e.g., locating each <i>bus</i> and <i>person</i> in traffic).</div>
      </div>
    </div>`;

  const cvs = body.querySelector("#l6-c");

  async function runOn(id) {
    body.querySelector("#l6-stat").textContent = "Running YOLOv11n ONNX...";
    const { detections, ms } = await runYoloOnImageData(id, conf);
    drawImageData(cvs, id);
    const ctx = cvs.getContext("2d");
    ctx.lineWidth = 2.5; ctx.font = "bold 14px Segoe UI, sans-serif";
    detections.forEach(d => {
      const [x1, y1, x2, y2] = d.box;
      ctx.strokeStyle = "#fb7185"; ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
      const lbl = `${d.cls} ${d.conf.toFixed(2)}`;
      const tw = ctx.measureText(lbl).width + 10;
      ctx.fillStyle = "#fb7185"; ctx.fillRect(x1, Math.max(0, y1 - 20), tw, 20);
      ctx.fillStyle = "#0f172a"; ctx.fillText(lbl, x1 + 5, Math.max(14, y1 - 5));
    });
    body.querySelector("#l6-stat").textContent = `${detections.length} objects • ${ms.toFixed(0)} ms`;
    body.querySelector("#l6-list").textContent = detections.length
      ? detections.map(d => `${d.cls.padEnd(14)} ${d.conf.toFixed(2)}  [${d.box.map(Math.round).join(", ")}]`).join("\n")
      : "No objects above confidence threshold.";
  }

  body.querySelector("#l6-conf").oninput = e => { conf = +e.target.value; body.querySelector("#l6-cv").textContent = conf.toFixed(2); if (!camStream) runOn(srcId); };
  body.querySelector("#l6-file").onchange = async e => {
    stopCam();
    if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 640); runOn(srcId); }
  };
  body.querySelector("#l6-cam").onclick = async () => {
    const btn = body.querySelector("#l6-cam");
    if (camStream) { stopCam(); btn.textContent = "Start Live Webcam"; runOn(srcId); return; }
    try {
      camStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
      const vid = body.querySelector("#l6-vid"); vid.srcObject = camStream;
      btn.textContent = "Stop Webcam";
      const tick = async () => {
        if (!camStream) return;
        if (vid.readyState >= 2) {
          offCvs.width = vid.videoWidth || 640; offCvs.height = vid.videoHeight || 480;
          offCtx.drawImage(vid, 0, 0, offCvs.width, offCvs.height);
          await runOn(offCtx.getImageData(0, 0, offCvs.width, offCvs.height));
        }
        camRaf = requestAnimationFrame(tick);
      };
      tick();
    } catch (err) {
      body.querySelector("#l6-stat").textContent = "Webcam blocked/unavailable";
    }
  };
  await runOn(srcId);
}

// ============================================================================
// LAB 7: SEGMENTATION (CLASSICAL JS + DEEPLABV3 ONNX)
// ============================================================================
async function mountLab7(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 480);
  let seed = [145, 155], tol = 30;

  body.innerHTML = `
    <div class="toolbar">
      <button class="chip active" id="l7-obj">Objects Sample</button>
      <button class="chip" id="l7-scn">Scene Sample</button>
      <label>Region Grow Tol: <span id="l7-tv">30</span> <input type="range" id="l7-tol" min="5" max="80" value="30"></label>
      <label class="btn">Upload Image<input type="file" id="l7-file" accept="image/*" hidden></label>
      <button class="btn btn-primary" id="l7-sem">Run DeepLabV3 ONNX</button>
    </div>
    <div class="ws-grid-4">
      <div class="panel"><div class="panel-hdr"><span>INPUT (CLICK SEED)</span></div><canvas id="l7-c1" class="cv-canvas clickable"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>1. OTSU THRESHOLD</span><span id="l7-ot"></span></div><canvas id="l7-c2" class="cv-canvas"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>2. SEED REGION GROW</span></div><canvas id="l7-c3" class="cv-canvas"></canvas></div>
      <div class="panel"><div class="panel-hdr"><span>3. EDGE + 4. DEEPLABV3</span><span id="l7-dl"></span></div><canvas id="l7-c4" class="cv-canvas"></canvas></div>
    </div>`;

  function runClassical() {
    const w = srcId.width, h = srcId.height, g = toGrayArray(srcId);
    const c1 = body.querySelector("#l7-c1");
    drawImageData(c1, srcId);
    const ctx1 = c1.getContext("2d"); ctx1.strokeStyle = "#fbbf24"; ctx1.lineWidth = 2;
    ctx1.beginPath(); ctx1.arc(seed[1], seed[0], 6, 0, Math.PI * 2); ctx1.stroke();

    const ot = otsuThreshold(g);
    drawImageData(body.querySelector("#l7-c2"), grayToImageData(ot.mask, w, h));
    body.querySelector("#l7-ot").textContent = `T=${ot.thr}`;

    // BFS Region growing
    const sy = Math.min(h - 1, Math.max(0, seed[0])), sx = Math.min(w - 1, Math.max(0, seed[1]));
    const sv = g[sy * w + sx], rg = new Uint8Array(w * h), vis = new Uint8Array(w * h);
    const q = [[sy, sx]]; vis[sy * w + sx] = 1;
    while (q.length) {
      const [y, x] = q.pop();
      if (Math.abs(g[y * w + x] - sv) <= tol) {
        rg[y * w + x] = 255;
        for (const [dy, dx] of [[-1,0],[1,0],[0,-1],[0,1]]) {
          const ny = y + dy, nx = x + dx;
          if (ny >= 0 && ny < h && nx >= 0 && nx < w && !vis[ny * w + nx]) { vis[ny * w + nx] = 1; q.push([ny, nx]); }
        }
      }
    }
    drawImageData(body.querySelector("#l7-c3"), grayToImageData(rg, w, h));

    const edge = computeCanny(gaussianBlurGray(g, w, h, 5), w, h, 50, 140);
    drawImageData(body.querySelector("#l7-c4"), grayToImageData(edge, w, h));
    body.querySelector("#l7-dl").textContent = "Canny Edges (click Run DeepLabV3)";
  }

  async function runSemantic() {
    body.querySelector("#l7-dl").textContent = "Running DeepLabV3...";
    const { imageData, classes } = await runDeepLabOnImageData(srcId);
    drawImageData(body.querySelector("#l7-c4"), imageData);
    body.querySelector("#l7-dl").textContent = classes.length ? classes.join(", ") : "background";
  }

  body.querySelector("#l7-c1").onclick = e => {
    const r = e.target.getBoundingClientRect();
    seed = [Math.floor((e.clientY-r.top)*srcId.height/r.height), Math.floor((e.clientX-r.left)*srcId.width/r.width)];
    runClassical();
  };
  body.querySelector("#l7-tol").oninput = e => { tol = +e.target.value; body.querySelector("#l7-tv").textContent = tol; runClassical(); };
  body.querySelector("#l7-obj").onclick = async () => { srcId = imgToImageData(await loadHTMLImage(lab.sample), 480); seed=[145,155]; runClassical(); };
  body.querySelector("#l7-scn").onclick = async () => { srcId = imgToImageData(await loadHTMLImage(lab.sample2), 480); runClassical(); await runSemantic(); };
  body.querySelector("#l7-file").onchange = async e => { if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480); runClassical(); } };
  body.querySelector("#l7-sem").onclick = runSemantic;
  runClassical();
}

renderHome();
