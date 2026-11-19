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

function grayStats(g) {
  let mn = 255, mx = 0, sum = 0;
  for (let i = 0; i < g.length; i++) {
    const v = g[i];
    if (v < mn) mn = v;
    if (v > mx) mx = v;
    sum += v;
  }
  const mean = sum / Math.max(1, g.length);
  let varSum = 0;
  for (let i = 0; i < g.length; i++) varSum += (g[i] - mean) ** 2;
  return [mn, mx, mean, Math.sqrt(varSum / Math.max(1, g.length))];
}

function applyYuvLumaTransform(id, fn) {
  const { data, width: w, height: h } = id;
  const yArr = toGrayArray(id);
  const yNew = fn(yArr, w, h);
  const out = new Uint8ClampedArray(data.length);
  for (let i = 0, p = 0; i < yArr.length; i++, p += 4) {
    const u = -0.14713 * data[p] - 0.28886 * data[p + 1] + 0.436 * data[p + 2];
    const v = 0.615 * data[p] - 0.51499 * data[p + 1] - 0.10001 * data[p + 2];
    const y = yNew[i];
    out[p] = Math.min(255, Math.max(0, Math.round(y + 1.13983 * v)));
    out[p + 1] = Math.min(255, Math.max(0, Math.round(y - 0.39465 * u - 0.58060 * v)));
    out[p + 2] = Math.min(255, Math.max(0, Math.round(y + 2.03211 * u)));
    out[p + 3] = 255;
  }
  return { imageData: new ImageData(out, w, h), gray: yNew };
}

function adaptiveThresholdGray(g, w, h, block = 35, cBias = 7) {
  const r = Math.floor(block / 2);
  const sat = new Float64Array((w + 1) * (h + 1));
  for (let y = 1; y <= h; y++) {
    let rowSum = 0;
    for (let x = 1; x <= w; x++) {
      rowSum += g[(y - 1) * w + (x - 1)];
      sat[y * (w + 1) + x] = sat[(y - 1) * (w + 1) + x] + rowSum;
    }
  }
  const out = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    const y0 = Math.max(0, y - r), y1 = Math.min(h - 1, y + r);
    for (let x = 0; x < w; x++) {
      const x0 = Math.max(0, x - r), x1 = Math.min(w - 1, x + r);
      const area = (x1 - x0 + 1) * (y1 - y0 + 1);
      const sum = sat[(y1 + 1) * (w + 1) + (x1 + 1)] - sat[y0 * (w + 1) + (x1 + 1)]
                - sat[(y1 + 1) * (w + 1) + x0] + sat[y0 * (w + 1) + x0];
      out[y * w + x] = g[y * w + x] < (sum / area - cBias) ? 255 : 0;
    }
  }
  return out;
}

function detectOrbFast(g, w, h, thr = 28, maxPts = 180) {
  const offs = [[-3,0],[-3,1],[-2,2],[-1,3],[0,3],[1,3],[2,2],[3,1],[3,0],[3,-1],[2,-2],[1,-3],[0,-3],[-1,-3],[-2,-2],[-3,-1]];
  const scores = [];
  for (let y = 5; y < h - 5; y += 2) {
    for (let x = 5; x < w - 5; x += 2) {
      const c = g[y * w + x];
      let hi = 0, lo = 0, s = 0;
      for (const [dy, dx] of offs) {
        const d = g[(y + dy) * w + (x + dx)] - c;
        if (d > thr) hi++; else if (d < -thr) lo++;
        s += Math.abs(d);
      }
      if (hi >= 9 || lo >= 9) scores.push({ x, y, r: s });
    }
  }
  scores.sort((a, b) => b.r - a.r);
  const kept = [];
  for (const pt of scores) {
    if (kept.every(k => Math.hypot(k.x - pt.x, k.y - pt.y) > 8)) {
      kept.push(pt);
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
const visitedLabs = new Set();
const homeView = document.getElementById("home-view");
const wsView = document.getElementById("workspace-view");
const gridEl = document.getElementById("grid");
const searchEl = document.getElementById("search");

function applyTheme(theme, animate = false, originBtn = null) {
  const commit = () => {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("csst106-theme", theme); } catch (_) {}
    document.querySelectorAll(".seg-btn[data-set-theme]").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.setTheme === theme);
    });
    if (onThemeRefresh) onThemeRefresh();
  };

  if (animate && document.startViewTransition && originBtn &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const rect = originBtn.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;
    const endR = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    const vt = document.startViewTransition(commit);
    vt.ready.then(() => {
      document.documentElement.animate(
        { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${endR}px at ${x}px ${y}px)`] },
        { duration: 420, easing: "cubic-bezier(0.22, 1, 0.36, 1)", pseudoElement: "::view-transition-new(root)" }
      );
    }).catch(() => {});
    return;
  }

  if (animate) {
    document.body.classList.remove("theme-switching");
    void document.body.offsetWidth;
    document.body.classList.add("theme-switching");
  }
  commit();
}

document.querySelectorAll(".seg-btn[data-set-theme]").forEach(btn => {
  btn.onclick = () => {
    const next = btn.dataset.setTheme;
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    if (next !== cur) applyTheme(next, true, btn);
  };
});
applyTheme((() => { try { return localStorage.getItem("csst106-theme") || "dark"; } catch (_) { return "dark"; } })(), false);

// Populate category counts on filter chips
document.querySelectorAll(".chip[data-cat]").forEach(chip => {
  const cat = chip.dataset.cat;
  const count = cat === "All" ? LABS.length : LABS.filter(l => l.cat === cat).length;
  chip.textContent = `${cat} (${count})`;
});

function triggerViewAnim(el) {
  el.classList.remove("anim-view");
  void el.offsetWidth;
  el.classList.add("anim-view");
}

function stopCam() {
  if (camRaf) { cancelAnimationFrame(camRaf); camRaf = null; }
  if (camStream) { camStream.getTracks().forEach(t => t.stop()); camStream = null; }
}

function updateTelemetry() {
  const tEl = document.getElementById("telemetry-text");
  if (!tEl) return;
  const doneTxt = visitedLabs.size ? ` • ${visitedLabs.size} Explored` : "";
  tEl.textContent = `${LABS.length} / ${LABS.length} Interactive Labs Ready${doneTxt}`;
}

function makeUtilityCard() {
  const hasOrt = typeof ort !== "undefined";
  const hasWasm = typeof WebAssembly === "object";
  const hasCam = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
  const envItems = [
    ["Canvas 2D", "Ready"],
    ["WebAssembly", hasWasm ? "Supported" : "N/A"],
    ["ONNX Runtime", hasOrt ? "Loaded" : "Pending"],
    ["Camera API", hasCam ? "Available" : "HTTP/No Cam"],
  ];
  const card = document.createElement("article");
  card.className = "card card-util";
  card.style.setProperty("--accent", "#38bdf8");
  card.innerHTML = `
    <div class="card-head">
      <div class="lab-icon" style="color:#38bdf8;border-color:#38bdf8;background:#38bdf81f">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>
      </div>
      <div style="flex:1;min-width:0">
        <div class="card-top">
          <span class="lab-pill">Environment</span>
          <span class="tag">Browser Runtime</span>
          <span class="status-pill">● Online</span>
        </div>
        <h2>Runtime &amp; Course Quick Check</h2>
      </div>
    </div>
    <div class="env-grid">
      ${envItems.map(([k, v]) => `<div class="env-pill">● ${k}: ${v}</div>`).join("")}
    </div>
    <p>All 7 interactive CV labs &amp; Borce_Lab_0X_Report.docx bundles run client-side via Canvas 2D and ONNX Runtime Web.</p>`;
  return card;
}

function renderHome() {
  stopCam();
  onThemeRefresh = null;
  homeView.style.display = "block";
  wsView.style.display = "none";
  triggerViewAnim(homeView);
  updateTelemetry();

  const q = searchEl.value.trim().toLowerCase();
  gridEl.innerHTML = "";
  const filtered = LABS.filter(l => (activeCat === "All" || l.cat === activeCat) &&
    (!q || l.title.toLowerCase().includes(q) || l.desc.toLowerCase().includes(q) ||
      l.num.toLowerCase().includes(q) || l.cat.toLowerCase().includes(q)));

  filtered.forEach(l => {
    const explored = visitedLabs.has(l.id);
    const card = document.createElement("article");
    card.className = "card";
    card.style.setProperty("--accent", l.accent);
    card.innerHTML = `
      <div class="card-head">
        <div class="lab-icon" style="color:${l.accent};border-color:${l.accent};background:${l.accent}1f">${l.icon}</div>
        <div style="flex:1;min-width:0">
          <div class="card-top">
            <span class="lab-pill">${l.num}</span>
            <span class="tag">${l.week}</span>
            <span class="tag">${l.cat}</span>
            <span class="status-pill ${explored ? "active-lab" : ""}">${explored ? "● Active" : "● Ready"}</span>
          </div>
          <h2>${l.title}</h2>
        </div>
      </div>
      <p>${l.desc}</p>
      <div class="card-actions">
        <button class="btn btn-lab" data-open="${l.id}">▶ Launch Lab</button>
        <a class="btn btn-ghost" href="${l.report}">Report (.docx)</a>
        <a class="btn btn-ghost" href="${l.manual}">Manual (.docx)</a>
      </div>`;
    card.querySelector("[data-open]").onclick = () => openLab(l);
    gridEl.appendChild(card);
  });

  if (activeCat === "All" && !q) {
    gridEl.appendChild(makeUtilityCard());
  }
}

document.getElementById("chips").addEventListener("click", (e) => {
  const chip = e.target.closest("[data-cat]");
  if (!chip) return;
  activeCat = chip.dataset.cat;
  document.querySelectorAll("#chips .chip").forEach(c => c.classList.toggle("active", c.dataset.cat === activeCat));
  renderHome();
});
searchEl.addEventListener("input", renderHome);
document.getElementById("back-btn").onclick = renderHome;

async function openLab(lab) {
  stopCam();
  onThemeRefresh = null;
  currentLab = lab;
  visitedLabs.add(lab.id);
  const statusMsg = document.getElementById("status-msg");
  if (statusMsg) statusMsg.textContent = `Last opened ${lab.num}: ${lab.title}`;
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
  const state = { color: "#ff00ff", patch: 25, paintOnClick: false, y0: 22, y1: 82, x0: 22, x1: 70, scale: 50, rot: 90 };

  function paintPatchAt(cy, cx) {
    const rgb = [0, 2, 4].map(i => parseInt(state.color.slice(1 + i, 3 + i), 16));
    const half = Math.floor(state.patch / 2);
    for (let y = Math.max(0, cy - half); y <= Math.min(workId.height - 1, cy + half); y++)
      for (let x = Math.max(0, cx - half); x <= Math.min(workId.width - 1, cx + half); x++) {
        const k = (y * workId.width + x) * 4;
        workId.data[k] = rgb[0]; workId.data[k + 1] = rgb[1]; workId.data[k + 2] = rgb[2];
      }
  }

  function renderControls() {
    const el = document.getElementById("l1-ctrl");
    if (tab === "pixel") {
      el.innerHTML = `
        <label class="chk-row"><input type="checkbox" id="l1-pon" ${state.paintOnClick ? "checked" : ""}> Paint on image click</label>
        <label>Patch Color: <input type="color" id="l1-col" value="${state.color}"></label>
        <label>Patch Size: <span id="l1-psz">${state.patch}px</span><input type="range" id="l1-p" min="1" max="61" step="2" value="${state.patch}"></label>
        <button class="btn btn-primary" id="l1-apply">Apply at (${sel[0]}, ${sel[1]})</button>`;
      el.querySelector("#l1-pon").onchange = e => state.paintOnClick = e.target.checked;
      el.querySelector("#l1-col").oninput = e => state.color = e.target.value;
      el.querySelector("#l1-p").oninput = e => { state.patch = +e.target.value; el.querySelector("#l1-psz").textContent = state.patch + "px"; };
      el.querySelector("#l1-apply").onclick = () => { paintPatchAt(sel[0], sel[1]); update(); };
    } else if (tab === "crop") {
      el.innerHTML = ["y0","y1","x0","x1"].map(k =>
        `<label>${k.toUpperCase()}: <span id="v-${k}">${state[k]}%</span><input type="range" id="s-${k}" min="0" max="100" value="${state[k]}"></label>`).join("");
      ["y0","y1","x0","x1"].forEach(k => el.querySelector(`#s-${k}`).oninput = e => {
        state[k] = +e.target.value; el.querySelector(`#v-${k}`).textContent = state[k] + "%"; update();
      });
    } else if (tab === "resize") {
      el.innerHTML = `
        <div class="chips chips-seg">${[25,50,100,150,200].map(p=>`<button class="chip ${state.scale===p?'active':''}" data-p="${p}">${p}%</button>`).join("")}</div>
        <label>Scale: <span id="v-sc">${state.scale}%</span><input type="range" id="s-sc" min="20" max="200" value="${state.scale}"></label>`;
      el.querySelectorAll("[data-p]").forEach(b => b.onclick = () => { state.scale = +b.dataset.p; renderControls(); update(); });
      el.querySelector("#s-sc").oninput = e => { state.scale = +e.target.value; el.querySelector("#v-sc").textContent = state.scale + "%"; el.querySelectorAll("[data-p]").forEach(b => b.classList.toggle("active", +b.dataset.p === state.scale)); update(); };
    } else if (tab === "rotate") {
      el.innerHTML = `<div class="chips chips-seg">${[90,180,270].map(d=>`<button class="chip ${state.rot===d?'active':''}" data-r="${d}">${d}° CW</button>`).join("")}</div>`;
      el.querySelectorAll("[data-r]").forEach(b => b.onclick = () => { state.rot = +b.dataset.r; renderControls(); update(); });
    } else el.innerHTML = `<div class="tag">Click anywhere on Original image to inspect BGR / RGB / Grayscale pixel values.</div>`;
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
    sel = [y, x];
    if (tab === "pixel") {
      if (state.paintOnClick) paintPatchAt(y, x);
      renderControls();
    }
    update();
  };
  document.getElementById("l1-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]");
    if (!btn) return;
    tab = btn.dataset.t;
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
// LAB 2: EDGE DETECTION (MATCHES lab2_ui.py TABS & PARAMETERS)
// ============================================================================
async function mountLab2(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 560);
  let tab = "compare", blurK = 3, sobelK = 3, t1 = 100, t2 = 200;

  body.innerHTML = `
    <div class="tab-bar" id="l2-tabs">
      ${["compare:Compare (All 3)","blur:Gaussian Blur","sobel:Sobel X / Y","canny:Canny Thresholds","qa:Question & Conclusion"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <label class="btn" style="margin-left:auto">Upload Image<input type="file" id="l2-file" accept="image/*" hidden></label>
      <button class="btn" id="l2-reset">Reset</button>
    </div>
    <div class="ws-split">
      <div>
        <div class="ws-grid-3" id="l2-grid">
          <div class="panel" id="l2-p0"><div class="panel-hdr"><span id="l2-t0">ORIGINAL</span><span id="l2-b0"></span></div><canvas id="l2-c0" class="cv-canvas"></canvas></div>
          <div class="panel" id="l2-p1"><div class="panel-hdr"><span id="l2-t1h">SOBEL</span><span id="l2-b1"></span></div><canvas id="l2-c1" class="cv-canvas"></canvas></div>
          <div class="panel" id="l2-p2"><div class="panel-hdr"><span id="l2-t2h">CANNY</span><span id="l2-b2"></span></div><canvas id="l2-c2" class="cv-canvas"></canvas></div>
        </div>
        <div class="panel qa-scroll" id="l2-qa" style="display:none"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>EDGE PARAMETERS</span></div>
        <div class="ctrl-stack">
          <div>
            <small style="color:var(--muted)">Gaussian Blur Kernel</small>
            <div class="chips chips-seg" style="margin-top:4px">${[1,3,5,7].map(k=>`<button class="chip ${k===3?"active":""}" data-b="${k}">${k===1?"Off":k+"×"+k}</button>`).join("")}</div>
          </div>
          <div>
            <small style="color:var(--muted)">Sobel Kernel Size</small>
            <div class="chips chips-seg" style="margin-top:4px">${[3,5].map(k=>`<button class="chip ${k===3?"active":""}" data-sk="${k}">${k}×${k}</button>`).join("")}</div>
          </div>
          <label>Canny T1 (Low): <span id="l2-t1v">100</span><input type="range" id="l2-t1" min="0" max="255" value="100"></label>
          <label>Canny T2 (High): <span id="l2-t2v">200</span><input type="range" id="l2-t2" min="0" max="255" value="200"></label>
          <pre id="l2-det" class="mono-box"></pre>
        </div>
      </div>
    </div>`;

  function update() {
    const w = srcId.width, h = srcId.height;
    const g = toGrayArray(srcId);
    const bl = gaussianBlurGray(g, w, h, blurK);
    const sobSrc = sobelK === 5 ? gaussianBlurGray(bl, w, h, 3) : bl;
    const sob = computeSobel(sobSrc, w, h);
    const can = computeCanny(bl, w, h, t1, t2);
    let edgePx = 0; for (let i = 0; i < can.length; i++) if (can[i]) edgePx++;
    const edgePct = (edgePx * 100) / can.length;
    const meanMag = sob.mag.reduce((a, b) => a + b, 0) / sob.mag.length;
    const blurTxt = blurK > 1 ? `${blurK}×${blurK}` : "Off";

    if (tab === "qa") {
      body.querySelector("#l2-grid").style.display = "none";
      const qa = body.querySelector("#l2-qa");
      qa.style.display = "block";
      qa.innerHTML = `
        <h3>Question:</h3>
        <p>Compare Sobel and Canny edge detection on <code>input.jpg</code> and explain the differences between their edge maps.</p>
        <h3>Answer — Differences Between Sobel &amp; Canny:</h3>
        <ul>
          <li><b>Output Type &amp; Intensity:</b> <b>Sobel</b> produces continuous grayscale gradient magnitudes (Max=<code>${sob.maxM.toFixed(1)}</code>, Mean=<code>${meanMag.toFixed(1)}</code>). <b>Canny</b> outputs a crisp binary map (<code>0</code> or <code>255</code>), marking <code>${edgePx.toLocaleString()}</code> edge pixels (<code>${edgePct.toFixed(2)}%</code>).</li>
          <li><b>Edge Thickness:</b> Sobel creates thicker ridges; Canny applies <i>non-maximum suppression</i> to thin edges to 1-pixel contours.</li>
          <li><b>Hysteresis Thresholding:</b> Canny uses dual thresholds (<code>T1=${t1}</code>, <code>T2=${t2}</code>) to suppress noise while preserving connected weak edges.</li>
          <li><b>Directional Gradients:</b> Sobel computes separate horizontal (<code>Gx</code>) and vertical (<code>Gy</code>) derivatives (inspect them in the <b>Sobel X / Y</b> tab).</li>
        </ul>
        <h3>Conclusion:</h3>
        <p>Sobel preserves gradient strength and orientation, while Canny produces clean, thin binary contours ideal for shape analysis and segmentation.</p>`;
    } else {
      body.querySelector("#l2-grid").style.display = "grid";
      body.querySelector("#l2-qa").style.display = "none";
      const panels = tab === "compare"
        ? [["ORIGINAL (GRAYSCALE)", `${w}×${h}`, g], ["SOBEL MAGNITUDE", `k=${sobelK}`, sob.u8], ["CANNY EDGES", `T=(${t1}, ${t2})`, can]]
        : tab === "blur"
        ? [["ORIGINAL GRAYSCALE", `${w}×${h}`, g], ["GAUSSIAN BLURRED", blurTxt, bl]]
        : tab === "sobel"
        ? [["SOBEL X (VERTICAL)", `dx=1, k=${sobelK}`, sob.gxU8], ["SOBEL Y (HORIZONTAL)", `dy=1, k=${sobelK}`, sob.gyU8], ["SOBEL COMBINED", "sqrt(Gx² + Gy²)", sob.u8]]
        : [["GAUSSIAN INPUT", blurTxt, bl], ["CANNY BINARY EDGES", `T1=${t1}, T2=${t2}`, can]];

      for (let i = 0; i < 3; i++) {
        const card = body.querySelector(`#l2-p${i}`);
        if (i < panels.length) {
          card.style.display = "flex";
          body.querySelector(`#l2-t${i === 0 ? "0" : i + "h"}`).textContent = panels[i][0];
          body.querySelector(`#l2-b${i}`).textContent = panels[i][1];
          drawImageData(body.querySelector(`#l2-c${i}`), grayToImageData(panels[i][2], w, h));
        } else card.style.display = "none";
      }
    }

    body.querySelector("#l2-det").textContent =
      `Shape  : (${h}, ${w}) gray\nBlur   : ${blurTxt}\nSobel  : k=${sobelK}\n  Max  = ${sob.maxM.toFixed(1)}\n  Mean = ${meanMag.toFixed(1)}\nCanny  : T1=${t1}, T2=${t2}\n  Edge = ${edgePx.toLocaleString()} px (${edgePct.toFixed(2)}%)`;
  }

  body.querySelector("#l2-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l2-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    update();
  });
  body.querySelectorAll("[data-b]").forEach(b => b.onclick = () => {
    blurK = +b.dataset.b; body.querySelectorAll("[data-b]").forEach(x => x.classList.toggle("active", +x.dataset.b === blurK)); update();
  });
  body.querySelectorAll("[data-sk]").forEach(b => b.onclick = () => {
    sobelK = +b.dataset.sk; body.querySelectorAll("[data-sk]").forEach(x => x.classList.toggle("active", +x.dataset.sk === sobelK)); update();
  });
  body.querySelector("#l2-t1").oninput = e => { t1 = +e.target.value; body.querySelector("#l2-t1v").textContent = t1; update(); };
  body.querySelector("#l2-t2").oninput = e => { t2 = +e.target.value; body.querySelector("#l2-t2v").textContent = t2; update(); };
  body.querySelector("#l2-file").onchange = async e => { if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 560); update(); } };
  body.querySelector("#l2-reset").onclick = () => {
    blurK = 3; sobelK = 3; t1 = 100; t2 = 200;
    body.querySelector("#l2-t1").value = 100; body.querySelector("#l2-t1v").textContent = "100";
    body.querySelector("#l2-t2").value = 200; body.querySelector("#l2-t2v").textContent = "200";
    body.querySelectorAll("[data-b]").forEach(x => x.classList.toggle("active", +x.dataset.b === 3));
    body.querySelectorAll("[data-sk]").forEach(x => x.classList.toggle("active", +x.dataset.sk === 3));
    update();
  };
  update();
}

// ============================================================================
// LAB 3: HISTOGRAM EQUALIZATION & CONTRAST (MATCHES lab3_ui.py)
// ============================================================================
async function mountLab3(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 520);
  let tab = "compare", useColor = false, clip = 2.0, tiles = 8, loP = 1, hiP = 99;

  body.innerHTML = `
    <div class="tab-bar" id="l3-tabs">
      ${["compare:Compare (All 3)","global:Global Equalization","stretch:Contrast Stretching","clahe:CLAHE Tuning","qa:Questions & Conclusion"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <label class="btn" style="margin-left:auto">Upload Image<input type="file" id="l3-file" accept="image/*" hidden></label>
    </div>
    <div class="ws-split">
      <div>
        <div class="ws-grid-3" id="l3-grid">
          ${[0,1,2].map(i=>`<div class="panel" id="l3-p${i}"><div class="panel-hdr"><span id="l3-t${i}">VIEW</span><span id="l3-b${i}"></span></div><canvas id="l3-c${i}" class="cv-canvas"></canvas><canvas id="l3-h${i}"></canvas></div>`).join("")}
        </div>
        <div class="panel qa-scroll" id="l3-qa" style="display:none"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>HISTOGRAM &amp; CLAHE PARAMETERS</span></div>
        <div class="ctrl-stack">
          <div>
            <small style="color:var(--muted)">Color Space</small>
            <div class="chips chips-seg" style="margin-top:4px">
              <button class="chip active" data-cm="gray">Grayscale</button>
              <button class="chip" data-cm="yuv">Color (YUV Luma)</button>
            </div>
          </div>
          <div>
            <small style="color:var(--muted)">CLAHE Tile Grid</small>
            <div class="chips chips-seg" style="margin-top:4px">${[4,8,16].map(t=>`<button class="chip ${t===8?"active":""}" data-ti="${t}">${t}×${t}</button>`).join("")}</div>
          </div>
          <label>CLAHE Clip Limit: <span id="l3-cv">2.0</span><input type="range" id="l3-clip" min="1" max="10" step="0.5" value="2.0"></label>
          <label>Stretch Low %: <span id="l3-lov">1%</span><input type="range" id="l3-lo" min="0" max="20" value="1"></label>
          <label>Stretch High %: <span id="l3-hiv">99%</span><input type="range" id="l3-hi" min="80" max="100" value="99"></label>
          <pre id="l3-det" class="mono-box"></pre>
        </div>
      </div>
    </div>`;

  function update() {
    const w = srcId.width, h = srcId.height;
    const origG = toGrayArray(srcId);
    const makeRes = (fn) => useColor
      ? applyYuvLumaTransform(srcId, fn)
      : (() => { const g = fn(origG, w, h); return { imageData: grayToImageData(g, w, h), gray: g }; })();

    const resOrig = useColor ? { imageData: srcId, gray: origG } : { imageData: grayToImageData(origG, w, h), gray: origG };
    const resStr = makeRes(g => contrastStretchGray(g, Math.min(loP, hiP - 1), Math.max(hiP, loP + 1)));
    const resGlob = makeRes(g => histEqualizeGray(g));
    const resCl = makeRes((g, iw, ih) => applyCLAHEGray(g, iw, ih, clip, tiles));

    const sO = grayStats(resOrig.gray), sS = grayStats(resStr.gray), sG = grayStats(resGlob.gray), sC = grayStats(resCl.gray);

    if (tab === "qa") {
      body.querySelector("#l3-grid").style.display = "none";
      const qa = body.querySelector("#l3-qa");
      qa.style.display = "block";
      qa.innerHTML = `
        <h3>Part 4 — Observations (${useColor ? "Color YUV Luma" : "Grayscale"}):</h3>
        <ul>
          <li><b>Contrast Spread:</b> Original intensity range is <code>[${sO[0]}, ${sO[1]}]</code> (σ=<code>${sO[3].toFixed(1)}</code>). Linear Stretch expands it to <code>[${sS[0]}, ${sS[1]}]</code> (σ=<code>${sS[3].toFixed(1)}</code>), Global Equalization to <code>[${sG[0]}, ${sG[1]}]</code> (σ=<code>${sG[3].toFixed(1)}</code>), and CLAHE achieves σ=<code>${sC[3].toFixed(1)}</code>.</li>
          <li><b>Global vs. CLAHE:</b> <code>equalizeHist()</code> applies one global CDF mapping, which can wash out skies; <b>CLAHE</b> works on local <code>${tiles}×${tiles}</code> tiles with <code>clipLimit=${clip.toFixed(1)}</code> to recover local detail cleanly.</li>
        </ul>
        <h3>Questions to Answer:</h3>
        <p><b>1. What is histogram equalization?</b> A point-processing contrast technique that redistributes pixel intensities so the histogram spreads across <code>0–255</code>.</p>
        <p><b>2. Why do we need it?</b> Low-light or narrow-exposure photos cluster intensities together; equalization separates tones for better visibility and downstream vision tasks.</p>
        <p><b>3. How does it work?</b> Computes histogram → PDF → CDF → maps <i>r</i> to <code>round(255 × CDF(r))</code> (on Y luma in YUV for color images so hues stay intact).</p>
        <p><b>4. How does CLAHE work?</b> Divides image into <code>${tiles}×${tiles}</code> tiles, clips peaks at <code>clipLimit</code> to limit noise, redistributes clipped counts, equalizes per tile, and bilinearly blends tile boundaries.</p>
        <p><b>5. Real-world applications:</b> X-ray/CT/MRI medical enhancement, underwater/foggy dashcams, aerial imagery, and low-light OCR.</p>`;
    } else {
      body.querySelector("#l3-grid").style.display = "grid";
      body.querySelector("#l3-qa").style.display = "none";
      const panels = tab === "compare"
        ? [["ORIGINAL", `σ=${sO[3].toFixed(1)}`, resOrig, "#94a3b8"], ["GLOBAL EQUALIZATION", `σ=${sG[3].toFixed(1)}`, resGlob, "#38bdf8"], [`CLAHE (clip=${clip.toFixed(1)}, ${tiles}×${tiles})`, `σ=${sC[3].toFixed(1)}`, resCl, "#34d399"]]
        : tab === "global"
        ? [["ORIGINAL", `σ=${sO[3].toFixed(1)}`, resOrig, "#94a3b8"], ["GLOBAL EQUALIZATION", `σ=${sG[3].toFixed(1)}`, resGlob, "#38bdf8"]]
        : tab === "stretch"
        ? [["ORIGINAL", `σ=${sO[3].toFixed(1)}`, resOrig, "#94a3b8"], [`LINEAR STRETCH (${loP}%–${hiP}%)`, `σ=${sS[3].toFixed(1)}`, resStr, "#fbbf24"]]
        : [["GLOBAL EQUALIZATION", `σ=${sG[3].toFixed(1)}`, resGlob, "#38bdf8"], [`CLAHE (clip=${clip.toFixed(1)}, ${tiles}×${tiles})`, `σ=${sC[3].toFixed(1)}`, resCl, "#34d399"]];

      for (let i = 0; i < 3; i++) {
        const card = body.querySelector(`#l3-p${i}`);
        if (i < panels.length) {
          card.style.display = "flex";
          const [t, bdg, resObj, col] = panels[i];
          body.querySelector(`#l3-t${i}`).textContent = t;
          body.querySelector(`#l3-b${i}`).textContent = bdg;
          drawImageData(body.querySelector(`#l3-c${i}`), resObj.imageData);
          drawHistCanvas(body.querySelector(`#l3-h${i}`), resObj.gray, col);
        } else card.style.display = "none";
      }
    }

    body.querySelector("#l3-det").textContent =
      `Space   : ${useColor ? "YUV (Y-luma)" : "Grayscale"} (${w}×${h})\nMin..Max | Mean | Std:\n` +
      `  Orig  : ${sO[0]}..${sO[1]} | ${sO[2].toFixed(1)} | ${sO[3].toFixed(1)}\n` +
      `  Strch : ${sS[0]}..${sS[1]} | ${sS[2].toFixed(1)} | ${sS[3].toFixed(1)}\n` +
      `  Glob  : ${sG[0]}..${sG[1]} | ${sG[2].toFixed(1)} | ${sG[3].toFixed(1)}\n` +
      `  CLAHE : ${sC[0]}..${sC[1]} | ${sC[2].toFixed(1)} | ${sC[3].toFixed(1)}`;
  }

  body.querySelector("#l3-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l3-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    update();
  });
  body.querySelectorAll("[data-cm]").forEach(b => b.onclick = () => {
    useColor = b.dataset.cm === "yuv";
    body.querySelectorAll("[data-cm]").forEach(x => x.classList.toggle("active", x.dataset.cm === b.dataset.cm));
    update();
  });
  body.querySelectorAll("[data-ti]").forEach(b => b.onclick = () => {
    tiles = +b.dataset.ti;
    body.querySelectorAll("[data-ti]").forEach(x => x.classList.toggle("active", +x.dataset.ti === tiles));
    update();
  });
  body.querySelector("#l3-clip").oninput = e => { clip = +e.target.value; body.querySelector("#l3-cv").textContent = clip.toFixed(1); update(); };
  body.querySelector("#l3-lo").oninput = e => { loP = +e.target.value; body.querySelector("#l3-lov").textContent = loP + "%"; update(); };
  body.querySelector("#l3-hi").oninput = e => { hiP = +e.target.value; body.querySelector("#l3-hiv").textContent = hiP + "%"; update(); };
  body.querySelector("#l3-file").onchange = async e => { if (e.target.files[0]) { srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 520); update(); } };
  onThemeRefresh = update;
  update();
}

// ============================================================================
// LAB 4: FEATURE DETECTION, MATCHING & COMPARISON (MATCHES lab4_ui.py)
// ============================================================================
async function mountLab4(lab, body) {
  let id1 = imgToImageData(await loadHTMLImage(lab.sample), 480);
  let id2 = imgToImageData(await loadHTMLImage(lab.sample2), 480);
  let tab = "keypoints", detector = "sift", maxKp = 110, fastThr = 28, upright = false;

  body.innerHTML = `
    <div class="tab-bar" id="l4-tabs">
      ${["keypoints:Keypoints","matching:Feature Matching","compare:SIFT vs ORB (SURF)","qa:Questions & Notes"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <label class="btn" style="margin-left:auto">Upload Img 1<input type="file" id="l4-f1" accept="image/*" hidden></label>
      <label class="btn">Upload Img 2<input type="file" id="l4-f2" accept="image/*" hidden></label>
    </div>
    <div class="ws-split">
      <div>
        <div class="ws-grid-2" id="l4-grid">
          <div class="panel" id="l4-p0"><div class="panel-hdr"><span id="l4-t0">VIEW 1</span><span id="l4-b0"></span></div><canvas id="l4-c0" class="cv-canvas"></canvas></div>
          <div class="panel" id="l4-p1"><div class="panel-hdr"><span id="l4-t1">VIEW 2</span><span id="l4-b1"></span></div><canvas id="l4-c1" class="cv-canvas"></canvas></div>
        </div>
        <div class="panel qa-scroll" id="l4-qa" style="display:none"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>FEATURE PARAMETERS</span></div>
        <div class="ctrl-stack">
          <div>
            <small style="color:var(--muted)">Active Detector</small>
            <div class="chips chips-seg" style="margin-top:4px">
              <button class="chip active" data-det="sift">SIFT-style</button>
              <button class="chip" data-det="orb">ORB (FAST)</button>
            </div>
          </div>
          <label class="chk-row"><input type="checkbox" id="l4-up"> Upright Mode (U-SURF / No Rot.)</label>
          <label>Max Keypoints (Hessian Cap): <span id="l4-mkpv">110</span><input type="range" id="l4-mkp" min="25" max="240" step="5" value="110"></label>
          <label>FAST / Corner Sensitivity: <span id="l4-thv">28</span><input type="range" id="l4-th" min="12" max="60" value="28"></label>
          <pre id="l4-det" class="mono-box"></pre>
        </div>
      </div>
    </div>`;

  function patchDesc(g, w, h, x, y) {
    const v = []; let mean = 0;
    for (let dy = -6; dy <= 6; dy += 2) for (let dx = -6; dx <= 6; dx += 2) {
      const val = g[Math.min(h - 1, Math.max(0, y + dy)) * w + Math.min(w - 1, Math.max(0, x + dx))];
      v.push(val); mean += val;
    }
    mean /= v.length;
    return v.map(z => z - mean);
  }

  function runDet(g, w, h, kind) {
    const t0 = performance.now();
    const kp = kind === "orb" ? detectOrbFast(g, w, h, fastThr, maxKp) : detectCornersHarris(g, w, h, maxKp);
    return { kp, ms: performance.now() - t0 };
  }

  function drawKpCanvas(canvas, g, w, h, kp, color) {
    drawImageData(canvas, grayToImageData(g, w, h));
    const ctx = canvas.getContext("2d");
    ctx.strokeStyle = color; ctx.lineWidth = 1.6;
    kp.forEach(p => {
      ctx.beginPath(); ctx.arc(p.x, p.y, 4.5, 0, Math.PI * 2); ctx.stroke();
      if (!upright) {
        const ang = (p.x * 0.13 + p.y * 0.07) % (Math.PI * 2);
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.cos(ang) * 7, p.y + Math.sin(ang) * 7); ctx.stroke();
      }
    });
  }

  function update() {
    const g1 = toGrayArray(id1), g2 = toGrayArray(id2);
    const resSift = runDet(g1, id1.width, id1.height, "sift");
    const resOrb = runDet(g1, id1.width, id1.height, "orb");
    const resAct = detector === "orb" ? resOrb : resSift;
    const kp2 = runDet(g2, id2.width, id2.height, detector).kp;

    const d1 = resAct.kp.map(p => patchDesc(g1, id1.width, id1.height, p.x, p.y));
    const d2 = kp2.map(p => patchDesc(g2, id2.width, id2.height, p.x, p.y));
    const matches = [];
    for (let i = 0; i < d1.length; i++) {
      let bestJ = -1, b1 = 1e18, b2 = 1e18;
      for (let j = 0; j < d2.length; j++) {
        let dist = 0; for (let k = 0; k < d1[i].length; k++) dist += (d1[i][k] - d2[j][k]) ** 2;
        if (dist < b1) { b2 = b1; b1 = dist; bestJ = j; } else if (dist < b2) b2 = dist;
      }
      if (bestJ >= 0 && b1 < 0.74 * b2) matches.push([resAct.kp[i], kp2[bestJ]]);
    }

    const grid = body.querySelector("#l4-grid"), qa = body.querySelector("#l4-qa");
    if (tab === "qa") {
      grid.style.display = "none"; qa.style.display = "block";
      qa.innerHTML = `
        <h3>Questions for Students (Lab 4):</h3>
        <p><b>1. What effect does changing the threshold have on keypoints?</b><br>Stricter thresholds keep fewer, stronger corners/blobs; lower thresholds capture more keypoints along minor textures.</p>
        <p><b>2. Why are descriptors important?</b><br>Descriptors encode local gradient patterns (64-D SURF, 128-D SIFT, 32-B binary ORB) so keypoints can be matched reliably across transformed views.</p>
        <p><b>3. SURF vs. SIFT vs. ORB Comparison:</b></p>
        <ul>
          <li><b>SURF vs. SIFT:</b> SURF uses box filters &amp; integral images (~3× faster); SIFT excels under large scale/affine changes.</li>
          <li><b>ORB:</b> Uses FAST + binary BRIEF descriptors—much faster &amp; patent-free.</li>
          <li><b>Current Image:</b> SIFT-style = <code>${resSift.kp.length} kp</code> (${resSift.ms.toFixed(1)} ms) • ORB-FAST = <code>${resOrb.kp.length} kp</code> (${resOrb.ms.toFixed(1)} ms).</li>
        </ul>
        <h3>U-SURF (Upright Mode):</h3>
        <p>When <code>Upright Mode</code> is enabled (${upright ? "ON" : "OFF"}), orientation vectors are skipped for faster detection when camera roll is minimal.</p>`;
    } else {
      grid.style.display = "grid"; qa.style.display = "none";
      const p0 = body.querySelector("#l4-p0"), p1 = body.querySelector("#l4-p1");
      const c0 = body.querySelector("#l4-c0"), c1 = body.querySelector("#l4-c1");
      if (tab === "keypoints") {
        p0.style.display = "flex"; p1.style.display = "flex";
        body.querySelector("#l4-t0").textContent = "INPUT IMAGE 1";
        body.querySelector("#l4-b0").textContent = `${id1.width}×${id1.height} gray`;
        drawImageData(c0, grayToImageData(g1, id1.width, id1.height));
        body.querySelector("#l4-t1").textContent = `${detector.toUpperCase()} RICH KEYPOINTS`;
        body.querySelector("#l4-b1").textContent = `${resAct.kp.length} kp • ${resAct.ms.toFixed(1)} ms`;
        drawKpCanvas(c1, g1, id1.width, id1.height, resAct.kp, "#fbbf24");
      } else if (tab === "matching") {
        p0.style.display = "flex"; p1.style.display = "none";
        body.querySelector("#l4-t0").textContent = `FEATURE MATCHING (${detector.toUpperCase()}: Img 1 ↔ Img 2)`;
        body.querySelector("#l4-b0").textContent = `${matches.length} good matches`;
        c0.width = id1.width + id2.width; c0.height = Math.max(id1.height, id2.height);
        const ctx = c0.getContext("2d");
        ctx.putImageData(grayToImageData(g1, id1.width, id1.height), 0, 0);
        ctx.putImageData(grayToImageData(g2, id2.width, id2.height), id1.width, 0);
        ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 1.4;
        matches.slice(0, 45).forEach(([a, b]) => { ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(id1.width + b.x, b.y); ctx.stroke(); });
      } else {
        p0.style.display = "flex"; p1.style.display = "flex";
        body.querySelector("#l4-t0").textContent = "SIFT-STYLE KEYPOINTS";
        body.querySelector("#l4-b0").textContent = `${resSift.kp.length} kp • ${resSift.ms.toFixed(1)} ms`;
        drawKpCanvas(c0, g1, id1.width, id1.height, resSift.kp, "#38bdf8");
        body.querySelector("#l4-t1").textContent = "ORB-FAST KEYPOINTS";
        body.querySelector("#l4-b1").textContent = `${resOrb.kp.length} kp • ${resOrb.ms.toFixed(1)} ms`;
        drawKpCanvas(c1, g1, id1.width, id1.height, resOrb.kp, "#34d399");
      }
    }

    body.querySelector("#l4-det").textContent =
      `Mode    : ${upright ? "Upright (U-SURF)" : "Rotation-Invariant"}\n` +
      `Active  : ${detector.toUpperCase()} (${resAct.kp.length} kp)\nMatches : ${matches.length} good\n\n` +
      `Benchmark (Img 1):\n  SIFT : ${resSift.kp.length} kp | ${resSift.ms.toFixed(1)} ms\n  ORB  : ${resOrb.kp.length} kp | ${resOrb.ms.toFixed(1)} ms`;
  }

  body.querySelector("#l4-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l4-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    update();
  });
  body.querySelectorAll("[data-det]").forEach(b => b.onclick = () => {
    detector = b.dataset.det;
    body.querySelectorAll("[data-det]").forEach(x => x.classList.toggle("active", x.dataset.det === detector));
    update();
  });
  body.querySelector("#l4-up").onchange = e => { upright = e.target.checked; update(); };
  body.querySelector("#l4-mkp").oninput = e => { maxKp = +e.target.value; body.querySelector("#l4-mkpv").textContent = maxKp; update(); };
  body.querySelector("#l4-th").oninput = e => { fastThr = +e.target.value; body.querySelector("#l4-thv").textContent = fastThr; update(); };
  body.querySelector("#l4-f1").onchange = async e => { if (e.target.files[0]) { id1 = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480); update(); } };
  body.querySelector("#l4-f2").onchange = async e => { if (e.target.files[0]) { id2 = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480); update(); } };
  update();
}

// ============================================================================
// LAB 5: PCA EIGENFACES (MATCHES lab5_ui.py TABS, PARAMETERS & CLASSIFICATION REPORT)
// ============================================================================
async function mountLab5(lab, body) {
  const d = await getLab5Data();
  let tab = "eigenfaces", selK = 150, whiten = true, failOnly = true, selSample = 0;

  body.innerHTML = `
    <div class="tab-bar" id="l5-tabs">
      ${["eigenfaces:Eigenfaces","variance:Variance Curve","failures:Predictions & Failures","reconstruct:Reconstruction","qa:Analysis & Q&A"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <button class="btn" id="l5-reset" style="margin-left:auto">Reset Defaults</button>
    </div>
    <div class="ws-split">
      <div class="panel" id="l5-main-card">
        <div class="panel-hdr"><span id="l5-hdr">EIGENFACES GALLERY (TOP 9 VS. LAST 3)</span><span id="l5-sub">n_components=150</span></div>
        <div id="l5-body"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>PCA &amp; SVM PARAMETERS</span></div>
        <div class="ctrl-stack">
          <label>PCA n_components: <span id="l5-kval">150</span><input type="range" id="l5-k" min="1" max="150" value="150"></label>
          <label class="chk-row"><input type="checkbox" id="l5-whiten" checked> whiten=True (unit variance components)</label>
          <label class="chk-row"><input type="checkbox" id="l5-failonly" checked> Show misclassified faces only (Failures tab)</label>
          <label>Reconstruction Sample #: <span id="l5-sval">0 (${d.recons[0].name})</span>
            <input type="range" id="l5-s" min="0" max="${d.recons.length - 1}" value="0">
          </label>
          <pre id="l5-report" class="mono-box" style="font-size:11px;line-height:1.4"></pre>
        </div>
      </div>
    </div>`;

  function makeFaceCanvas(pixels, label, color) {
    const wrap = document.createElement("div"); wrap.className = "face-item";
    const c = document.createElement("canvas"); c.width = d.w; c.height = d.h;
    c.getContext("2d").putImageData(grayToImageData(pixels, d.w, d.h), 0, 0);
    const cap = document.createElement("small");
    cap.style.color = color || "var(--text)";
    cap.textContent = label;
    wrap.append(c, cap);
    return wrap;
  }

  function formatReport() {
    const acc = whiten ? d.acc_whiten : d.acc_no_whiten;
    const retVar = d.cum_var[selK - 1];
    const errs = whiten ? d.mis_count : Math.round((100 - d.acc_no_whiten) * d.n_test / 100);
    let txt = `LFW (min_faces=70, resize=0.4)\nSamples : ${d.n_samples} (${d.n_train} train / ${d.n_test} test)\nImage   : ${d.h}×${d.w} (${d.n_features} features)\nClasses : ${d.report.length}\n\n`;
    txt += `PCA (k=${selK}, whiten=${whiten}):\n  Retained Var : ${retVar}%\n  90% Var at k : ${d.k90}\nSVM Accuracy   : ${acc}% (${errs} errors)\n\n`;
    txt += `Class            prec  rec   f1  sup\n`;
    txt += d.report.map(r => `${r.name.padEnd(16)} ${r.precision.toFixed(2)} ${r.recall.toFixed(2)} ${r.f1.toFixed(2)}  ${String(r.support).padStart(3)}`).join("\n");
    body.querySelector("#l5-report").textContent = txt;
  }

  function renderMain() {
    const host = body.querySelector("#l5-body");
    const hdr = body.querySelector("#l5-hdr");
    const sub = body.querySelector("#l5-sub");
    host.innerHTML = "";

    if (tab === "eigenfaces") {
      hdr.textContent = "EIGENFACES GALLERY (TOP 9 VS. LAST 3)";
      sub.textContent = `Top 9 + Tail 3 of ${selK} components`;
      const fg = document.createElement("div"); fg.className = "face-grid";
      d.eigenfaces.forEach(ef => fg.appendChild(makeFaceCanvas(ef.pixels, `${ef.tag}: Eigenface ${ef.idx}`)));
      host.appendChild(fg);
    } else if (tab === "variance") {
      hdr.textContent = "CUMULATIVE EXPLAINED VARIANCE CURVE";
      sub.textContent = `k=${selK} → ${d.cum_var[selK - 1]}% (90% @ k=${d.k90})`;
      const cvs = document.createElement("canvas");
      cvs.style.width = "100%";
      host.appendChild(cvs);
      const w = cvs.width = host.clientWidth || 640, h = cvs.height = 310;
      const ctx = cvs.getContext("2d");
      ctx.fillStyle = getCanvasBg(); ctx.fillRect(0, 0, w, h);
      const y90 = h - 26 - 0.90 * (h - 46), x90 = 38 + ((d.k90 - 1) / 149) * (w - 56);
      ctx.setLineDash([5, 4]); ctx.strokeStyle = "#fbbf24";
      ctx.beginPath(); ctx.moveTo(38, y90); ctx.lineTo(w - 18, y90); ctx.stroke();
      ctx.strokeStyle = "#34d399";
      ctx.beginPath(); ctx.moveTo(x90, 20); ctx.lineTo(x90, h - 26); ctx.stroke();
      ctx.setLineDash([]);
      ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.6; ctx.beginPath();
      d.cum_var.forEach((v, i) => {
        const x = 38 + (i / 149) * (w - 56), y = h - 26 - (v / 100) * (h - 46);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.stroke();
      const xSel = 38 + ((selK - 1) / 149) * (w - 56), ySel = h - 26 - (d.cum_var[selK - 1] / 100) * (h - 46);
      ctx.fillStyle = "#f472b6"; ctx.beginPath(); ctx.arc(xSel, ySel, 5.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#94a3b8"; ctx.font = "11px Consolas, monospace";
      ctx.fillText(`90% Threshold @ k=${d.k90}`, x90 + 6, h - 34);
      ctx.fillText(`Selected k=${selK}: ${d.cum_var[selK - 1]}%`, 44, 30);
    } else if (tab === "failures") {
      hdr.textContent = failOnly ? "PROGRAMMATIC FAILURE ANALYSIS (MISCLASSIFIED FACES)" : "TEST SET SAMPLE PREDICTIONS";
      sub.textContent = `${d.mis_count} errors out of ${d.n_test} test faces`;
      const fg = document.createElement("div"); fg.className = "face-grid";
      const list = failOnly ? d.failures : [...d.failures].reverse();
      list.forEach(f => fg.appendChild(makeFaceCanvas(f.pixels, `True: ${f.true.split(" ").pop()}\nPred: ${f.pred.split(" ").pop()}`, "#f87171")));
      host.appendChild(fg);
    } else if (tab === "reconstruct") {
      hdr.textContent = `PCA RECONSTRUCTION ACROSS k COMPONENTS — #${selSample}: ${d.recons[selSample].name}`;
      sub.textContent = "Original vs k=5..150";
      const chips = document.createElement("div"); chips.className = "chips chips-seg"; chips.style.marginBottom = "10px";
      chips.innerHTML = d.recons.map((r, i) => `<button class="chip ${i===selSample?"active":""}" data-rs="${i}">#${i} ${r.name}</button>`).join("");
      chips.querySelectorAll("[data-rs]").forEach(b => b.onclick = () => {
        selSample = +b.dataset.rs;
        body.querySelector("#l5-s").value = selSample;
        body.querySelector("#l5-sval").textContent = `${selSample} (${d.recons[selSample].name})`;
        renderMain();
      });
      host.appendChild(chips);
      const fg = document.createElement("div"); fg.className = "face-grid";
      const item = d.recons[selSample];
      fg.appendChild(makeFaceCanvas(item.orig, "Original", "#38bdf8"));
      d.k_steps.forEach(k => fg.appendChild(makeFaceCanvas(item.steps[String(k)], `k=${k}`)));
      host.appendChild(fg);
    } else {
      hdr.textContent = "LAB 5 — POST-LAB ANALYSIS & FOLLOW-UP QUESTIONS";
      sub.textContent = `LFW ${d.n_samples} faces`;
      const qa = document.createElement("div"); qa.className = "qa-scroll";
      qa.innerHTML = `
        <h3>Post-Lab Analysis (Tasks 1–4):</h3>
        <p><b>Q1. Dimensionality vs. Variance:</b> With <code>n_components=${selK}</code> on LFW (<code>${d.n_features}</code> raw features), PCA retains <code>${d.cum_var[selK - 1]}%</code> variance. Reaching <b>90%</b> variance takes <b><code>k=${d.k90}</code></b> components (~95% reduction).</p>
        <p><b>Q2. First 3 vs. Last 3 Eigenfaces:</b> First Eigenfaces capture global lighting direction and face oval geometry; tail Eigenfaces capture fine high-frequency edge textures and noise.</p>
        <p><b>Q3. Importance of Whitening (<code>whiten=True</code>):</b> Scales each component by 1/√λᵢ so RBF SVM treats all 150 facial components evenly instead of letting top illumination PCs dominate distances (${d.acc_whiten}% with whiten vs. ${d.acc_no_whiten}% without).</p>
        <p><b>Q4. Failure Analysis (${d.mis_count} / ${d.n_test} test errors):</b> Misclassifications stem from extreme off-axis profiles, harsh lighting shadows, glasses/occlusions, and class imbalance.</p>
        <h3>Follow-Up Questions:</h3>
        <p><b>1. Why dimensionality reduction?</b> Removes redundant pixel correlation ("curse of dimensionality"), prevents overfitting, and speeds up classification.</p>
        <p><b>2. PC1 vs. PC2?</b> PC1 points along maximum dataset variance; PC2 is orthogonal to PC1 and captures maximum remaining variance.</p>
        <p><b>3. What is lost (1,000 → 100 PCs)?</b> High-frequency textures, sharp edges, subtle facial expressions, and noise.</p>
        <p><b>4. PCA for face recognition?</b> Faces are centered and projected onto top-<i>k</i> Eigenfaces; test faces project to the same subspace for SVM/NN matching.</p>
        <p><b>5. Why center features?</b> Subtracting the mean face ensures components capture variance <i>among</i> faces rather than average brightness.</p>`;
      host.appendChild(qa);
    }
    formatReport();
  }

  body.querySelector("#l5-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l5-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    renderMain();
  });
  body.querySelector("#l5-k").oninput = e => { selK = +e.target.value; body.querySelector("#l5-kval").textContent = selK; renderMain(); };
  body.querySelector("#l5-whiten").onchange = e => { whiten = e.target.checked; formatReport(); renderMain(); };
  body.querySelector("#l5-failonly").onchange = e => { failOnly = e.target.checked; if (tab === "failures") renderMain(); };
  body.querySelector("#l5-s").oninput = e => { selSample = +e.target.value; body.querySelector("#l5-sval").textContent = `${selSample} (${d.recons[selSample].name})`; if (tab === "reconstruct") renderMain(); };
  body.querySelector("#l5-reset").onclick = () => {
    selK = 150; whiten = true; failOnly = true; selSample = 0;
    body.querySelector("#l5-k").value = 150; body.querySelector("#l5-kval").textContent = "150";
    body.querySelector("#l5-whiten").checked = true; body.querySelector("#l5-failonly").checked = true;
    body.querySelector("#l5-s").value = 0; body.querySelector("#l5-sval").textContent = `0 (${d.recons[0].name})`;
    renderMain();
  };
  onThemeRefresh = renderMain;
  renderMain();
}

// ============================================================================
// LAB 6: YOLOV11 OBJECT DETECTION (MATCHES lab6_ui.py TABS & INSPECTOR)
// ============================================================================
async function mountLab6(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 640);
  let tab = "detect", conf = 0.25, fileName = "sample_scene.jpg";

  body.innerHTML = `
    <div class="tab-bar" id="l6-tabs">
      ${["detect:Object Detection","dataset:Dataset & Training Guide","qa:Question & Notes"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <label class="btn" style="margin-left:auto">Upload Image<input type="file" id="l6-file" accept="image/*" hidden></label>
      <button class="btn btn-primary" id="l6-cam">Start Live Webcam</button>
    </div>
    <div class="ws-split">
      <div>
        <div class="ws-grid-2" id="l6-grid">
          <div class="panel"><div class="panel-hdr"><span id="l6-in-t">INPUT (${fileName})</span><span id="l6-in-dim"></span></div><canvas id="l6-c0" class="cv-canvas"></canvas></div>
          <div class="panel"><div class="panel-hdr"><span>YOLOv11n BROWSER DETECTIONS</span><span id="l6-stat">Loading ONNX...</span></div><canvas id="l6-c" class="cv-canvas"></canvas><video id="l6-vid" autoplay playsinline hidden></video></div>
        </div>
        <div class="panel qa-scroll" id="l6-text" style="display:none"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>YOLO PARAMETERS &amp; DETECTIONS</span></div>
        <div class="ctrl-stack">
          <label>Confidence Threshold: <span id="l6-cv">0.25</span><input type="range" id="l6-conf" min="0.10" max="0.90" step="0.05" value="0.25"></label>
          <pre id="l6-list" class="mono-box"></pre>
        </div>
      </div>
    </div>`;

  const c0 = body.querySelector("#l6-c0"), cvs = body.querySelector("#l6-c");

  function renderTextTab() {
    const grid = body.querySelector("#l6-grid"), txt = body.querySelector("#l6-text");
    if (tab === "detect") {
      grid.style.display = "grid"; txt.style.display = "none";
      return;
    }
    grid.style.display = "none"; txt.style.display = "block";
    if (tab === "dataset") {
      txt.innerHTML = `
        <h3>Part 2: Preparing a Custom Dataset</h3>
        <p>Annotate images using <b>LabelImg</b> or <b>Roboflow</b> in YOLO format (one <code>.txt</code> per image):</p>
        <pre>class_id x_center y_center width height</pre>
        <pre>/dataset
├── /images/{train, val}
├── /labels/{train, val}
└── data.yaml  (train, val, nc, names)</pre>
        <h3>Part 3: Training YOLOv11</h3>
        <pre>yolo task=detect mode=train model=yolo11n.pt data=data.yaml epochs=100 imgsz=640</pre>
        <h3>Part 4: Validation &amp; Inference</h3>
        <pre>yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=data.yaml</pre>`;
    } else {
      txt.innerHTML = `
        <h3>Question:</h3>
        <p><i>What is object detection in computer vision, and how does it differ from image classification? Explain with a real-world example.</i></p>
        <h3>Answer:</h3>
        <p><b>Image classification</b> assigns a single overall label to an image without localization.</p>
        <p><b>Object detection</b> performs both <b>classification</b> and <b>localization</b> simultaneously, predicting <code>(x1, y1, x2, y2)</code> bounding boxes, class labels, and confidence scores for every object instance.</p>
        <p><b>Real-World Example (Autonomous Driving / Traffic Monitoring):</b> A classifier labels a dashcam frame simply <code>"street"</code>, whereas <b>YOLOv11</b> draws boxes around every <i>person</i>, <i>car</i>, <i>bus</i>, and <i>traffic light</i> in real time so a vehicle can estimate distance and brake safely.</p>`;
    }
  }

  async function runOn(id) {
    body.querySelector("#l6-in-t").textContent = `INPUT (${fileName})`;
    body.querySelector("#l6-in-dim").textContent = `${id.width}×${id.height}`;
    drawImageData(c0, id);
    body.querySelector("#l6-stat").textContent = "Running YOLOv11n ONNX...";
    const { detections, ms } = await runYoloOnImageData(id, conf);
    drawImageData(cvs, id);
    const ctx = cvs.getContext("2d");
    ctx.lineWidth = 2.5; ctx.font = "bold 14px Segoe UI, sans-serif";
    const counts = {};
    detections.forEach(d => {
      counts[d.cls] = (counts[d.cls] || 0) + 1;
      const [x1, y1, x2, y2] = d.box;
      ctx.strokeStyle = "#fb7185"; ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
      const lbl = `${d.cls} ${d.conf.toFixed(2)}`;
      const tw = ctx.measureText(lbl).width + 10;
      ctx.fillStyle = "#fb7185"; ctx.fillRect(x1, Math.max(0, y1 - 20), tw, 20);
      ctx.fillStyle = "#0f172a"; ctx.fillText(lbl, x1 + 5, Math.max(14, y1 - 5));
    });
    body.querySelector("#l6-stat").textContent = `${detections.length} objects • ${ms.toFixed(0)} ms`;
    const clsLines = Object.entries(counts).sort().map(([k, v]) => `  ${k.padEnd(13)}: ${v}`).join("\n");
    const boxLines = detections.slice(0, 12).map(d => `  ${d.cls} (${d.conf.toFixed(2)}) [${d.box.map(Math.round).join(",")}]`).join("\n");
    body.querySelector("#l6-list").textContent =
      `Model   : yolo11n.onnx (WASM)\nInput   : ${fileName} (${id.width}×${id.height})\nConf    : ${conf.toFixed(2)}\nLatency : ${ms.toFixed(1)} ms\nObjects : ${detections.length}\n` +
      (clsLines ? `\nClass Counts:\n${clsLines}\n\nBoxes:\n${boxLines}` : "\nNo objects above threshold.");
  }

  body.querySelector("#l6-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l6-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    renderTextTab();
  });
  body.querySelector("#l6-conf").oninput = e => { conf = +e.target.value; body.querySelector("#l6-cv").textContent = conf.toFixed(2); if (!camStream) runOn(srcId); };
  body.querySelector("#l6-file").onchange = async e => {
    stopCam();
    if (e.target.files[0]) {
      fileName = e.target.files[0].name;
      srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 640);
      runOn(srcId);
    }
  };
  body.querySelector("#l6-cam").onclick = async () => {
    const btn = body.querySelector("#l6-cam");
    if (camStream) {
      stopCam(); btn.textContent = "Start Live Webcam";
      btn.classList.remove("btn-danger"); btn.classList.add("btn-primary");
      runOn(srcId); return;
    }
    try {
      camStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
      const vid = body.querySelector("#l6-vid"); vid.srcObject = camStream;
      fileName = "Live Webcam";
      btn.textContent = "Stop Webcam";
      btn.classList.remove("btn-primary"); btn.classList.add("btn-danger");
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
    } catch (_) {
      body.querySelector("#l6-stat").textContent = "Webcam blocked/unavailable";
    }
  };
  await runOn(srcId);
}

// ============================================================================
// LAB 7: SEGMENTATION (MATCHES lab7_ui.py TABS, PARAMETERS & Q&A)
// ============================================================================
async function mountLab7(lab, body) {
  let srcId = imgToImageData(await loadHTMLImage(lab.sample), 480);
  let tab = "compare", seed = [145, 155], tol = 30, c1 = 50, c2 = 140;
  let semanticId = null, semanticClasses = [], semanticStatus = "Pending (click Run DeepLabV3)";

  body.innerHTML = `
    <div class="tab-bar" id="l7-tabs">
      ${["compare:Compare All 4","threshold:Thresholding","region:Region-Based","edge:Edge-Based","semantic:Semantic (DeepLabV3)","qa:Question & Conclusion"].map((s,i)=>{
        const [k,v] = s.split(":"); return `<button class="tab ${i===0?"active":""}" data-t="${k}">${v}</button>`;
      }).join("")}
      <div class="chips chips-seg" id="l7-sample-chips" style="margin-left:auto">
        <button class="chip active" id="l7-obj">Objects Sample</button>
        <button class="chip" id="l7-scn">Scene Sample</button>
      </div>
      <label class="btn">Upload Image<input type="file" id="l7-file" accept="image/*" hidden></label>
    </div>
    <div class="ws-split">
      <div>
        <div class="ws-grid-2" id="l7-grid">
          ${[0,1,2,3].map(i=>`<div class="panel" id="l7-p${i}"><div class="panel-hdr"><span id="l7-t${i}">VIEW</span><span id="l7-b${i}"></span></div><canvas id="l7-c${i}" class="cv-canvas"></canvas></div>`).join("")}
        </div>
        <div class="panel qa-scroll" id="l7-qa" style="display:none"></div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><span>SEGMENTATION PARAMETERS</span></div>
        <div class="ctrl-stack">
          <label>Region Grow Tolerance: <span id="l7-tv">30</span><input type="range" id="l7-tol" min="5" max="80" value="30"></label>
          <label>Canny Edge T1: <span id="l7-c1v">50</span><input type="range" id="l7-c1s" min="10" max="200" value="50"></label>
          <label>Canny Edge T2: <span id="l7-c2v">140</span><input type="range" id="l7-c2s" min="50" max="255" value="140"></label>
          <button class="btn btn-primary" id="l7-sem">Run DeepLabV3 ONNX</button>
          <pre id="l7-det" class="mono-box"></pre>
        </div>
      </div>
    </div>`;

  function setSampleActive(activeId) {
    ["l7-obj", "l7-scn"].forEach(id => {
      const el = body.querySelector(`#${id}`);
      if (el) el.classList.toggle("active", id === activeId);
    });
  }

  function computeClassical() {
    const w = srcId.width, h = srcId.height, g = toGrayArray(srcId);
    const ot = otsuThreshold(g);
    const adap = adaptiveThresholdGray(g, w, h, 35, 7);

    // Seed Region Growing
    const sy = Math.min(h - 1, Math.max(0, seed[0])), sx = Math.min(w - 1, Math.max(0, seed[1]));
    const sv = g[sy * w + sx], rg = new Uint8Array(w * h), vis = new Uint8Array(w * h);
    const q = [[sy, sx]]; vis[sy * w + sx] = 1;
    let grownPx = 0;
    while (q.length) {
      const [y, x] = q.pop();
      if (Math.abs(g[y * w + x] - sv) <= tol) {
        rg[y * w + x] = 255; grownPx++;
        for (const [dy, dx] of [[-1,0],[1,0],[0,-1],[0,1]]) {
          const ny = y + dy, nx = x + dx;
          if (ny >= 0 && ny < h && nx >= 0 && nx < w && !vis[ny * w + nx]) { vis[ny * w + nx] = 1; q.push([ny, nx]); }
        }
      }
    }

    const edge = computeCanny(gaussianBlurGray(g, w, h, 5), w, h, c1, c2);
    const inMarked = cloneImageData(srcId);
    const tmpC = document.createElement("canvas"); tmpC.width = w; tmpC.height = h;
    const tctx = tmpC.getContext("2d"); tctx.putImageData(inMarked, 0, 0);
    tctx.strokeStyle = "#fbbf24"; tctx.lineWidth = 2.2;
    tctx.beginPath(); tctx.arc(sx, sy, 6, 0, Math.PI * 2); tctx.stroke();

    return {
      w, h,
      markedInput: tctx.getImageData(0, 0, w, h),
      otsuId: grayToImageData(ot.mask, w, h), otsuThr: ot.thr,
      adapId: grayToImageData(adap, w, h),
      rgId: grayToImageData(rg, w, h), grownPx,
      edgeId: grayToImageData(edge, w, h),
    };
  }

  function renderAll() {
    const res = computeClassical();
    const semView = semanticId || res.markedInput;
    const grid = body.querySelector("#l7-grid"), qa = body.querySelector("#l7-qa");

    if (tab === "qa") {
      grid.style.display = "none"; qa.style.display = "block";
      qa.innerHTML = `
        <h3>Answer — 4 Segmentation Techniques Compared:</h3>
        <p><b>1. Thresholding Segmentation (Global Otsu / Adaptive):</b> Partitions pixels by comparing intensities against global (<code>T=${res.otsuThr}</code>) or local 35×35 thresholds.<br><i>Advantage:</i> Very fast &amp; simple. <i>Limitation:</i> Fails when foreground &amp; background share similar intensities.</p>
        <p><b>2. Region-Based Segmentation (Region Growing / Watershed):</b> Groups neighboring pixels by similarity from a seed or watershed topography.<br><i>Advantage:</i> Produces connected regions &amp; splits touching objects. <i>Limitation:</i> Sensitive to seed point &amp; noise.</p>
        <p><b>3. Edge-Based Segmentation (Canny + Contours):</b> Detects sharp gradient boundaries (<code>T=(${c1}, ${c2})</code>).<br><i>Advantage:</i> Effective with strong boundary contrast. <i>Limitation:</i> Broken edge chains fail to close contours.</p>
        <p><b>4. Semantic Segmentation (DeepLabV3 ONNX):</b> Deep CNN classifying every pixel into semantic categories (21 PASCAL VOC classes).<br><i>Advantage:</i> Understands complex scenes. <i>Limitation:</i> Heavier compute &amp; large labeled dataset requirements.</p>
        <h3>Conclusion:</h3>
        <p>Classical methods excel on lightweight high-contrast tasks, while DeepLabV3 provides robust semantic understanding on complex natural scenes.</p>`;
    } else {
      grid.style.display = "grid"; qa.style.display = "none";
      const panels = tab === "compare"
        ? [["1. OTSU THRESHOLDING", `T=${res.otsuThr}`, res.otsuId, false], ["2. REGION GROWING (CLICK SEED)", `Seed=(${seed[0]},${seed[1]}) tol=${tol}`, res.rgId, true], ["3. CANNY EDGES", `T=(${c1}, ${c2})`, res.edgeId, false], ["4. SEMANTIC (DEEPLABV3)", semanticStatus, semView, false]]
        : tab === "threshold"
        ? [["OTSU GLOBAL THRESHOLD", `T=${res.otsuThr}`, res.otsuId, false], ["ADAPTIVE MEAN (35×35)", "Local lighting", res.adapId, false]]
        : tab === "region"
        ? [["INPUT (CLICK SEED)", `Seed=(${seed[0]},${seed[1]})`, res.markedInput, true], ["SEED REGION GROWING", `${res.grownPx.toLocaleString()} px (tol=${tol})`, res.rgId, false]]
        : tab === "edge"
        ? [["INPUT IMAGE", `${res.w}×${res.h}`, res.markedInput, false], ["CANNY EDGE BOUNDARIES", `T=(${c1}, ${c2})`, res.edgeId, false]]
        : [["INPUT IMAGE", `${res.w}×${res.h}`, res.markedInput, false], ["DEEPLABV3 (PASCAL VOC)", semanticStatus, semView, false]];

      for (let i = 0; i < 4; i++) {
        const card = body.querySelector(`#l7-p${i}`), cvs = body.querySelector(`#l7-c${i}`);
        if (i < panels.length) {
          card.style.display = "flex";
          const [t, bdg, id, isClickable] = panels[i];
          body.querySelector(`#l7-t${i}`).textContent = t;
          body.querySelector(`#l7-b${i}`).textContent = bdg;
          cvs.classList.toggle("clickable", isClickable);
          cvs.onclick = isClickable ? (e => {
            const r = e.target.getBoundingClientRect();
            seed = [Math.floor((e.clientY - r.top) * srcId.height / r.height), Math.floor((e.clientX - r.left) * srcId.width / r.width)];
            renderAll();
          }) : null;
          drawImageData(cvs, id);
        } else card.style.display = "none";
      }
    }

    body.querySelector("#l7-det").textContent =
      `Image   : ${res.w}×${res.h}\nSeed    : (${seed[0]}, ${seed[1]})\nOtsu T  : ${res.otsuThr}\nRegion  : ${res.grownPx.toLocaleString()} px (tol=${tol})\nCanny   : (${c1}, ${c2})\nSemantic: ${semanticStatus}`;
  }

  async function runSemantic() {
    const semBtn = body.querySelector("#l7-sem");
    if (semBtn) { semBtn.classList.add("is-busy"); semBtn.textContent = "Running DeepLabV3..."; }
    semanticStatus = "Running DeepLabV3...";
    renderAll();
    try {
      const { imageData, classes } = await runDeepLabOnImageData(srcId);
      semanticId = imageData; semanticClasses = classes;
      semanticStatus = classes.length ? classes.join(", ") : "background";
    } finally {
      if (semBtn) { semBtn.classList.remove("is-busy"); semBtn.textContent = "Run DeepLabV3 ONNX"; }
    }
    renderAll();
  }

  body.querySelector("#l7-tabs").addEventListener("click", e => {
    const btn = e.target.closest("[data-t]"); if (!btn) return;
    tab = btn.dataset.t;
    body.querySelectorAll("#l7-tabs .tab").forEach(b => b.classList.toggle("active", b.dataset.t === tab));
    renderAll();
  });
  body.querySelector("#l7-tol").oninput = e => { tol = +e.target.value; body.querySelector("#l7-tv").textContent = tol; renderAll(); };
  body.querySelector("#l7-c1s").oninput = e => { c1 = +e.target.value; body.querySelector("#l7-c1v").textContent = c1; renderAll(); };
  body.querySelector("#l7-c2s").oninput = e => { c2 = +e.target.value; body.querySelector("#l7-c2v").textContent = c2; renderAll(); };
  body.querySelector("#l7-obj").onclick = async () => {
    setSampleActive("l7-obj");
    srcId = imgToImageData(await loadHTMLImage(lab.sample), 480);
    seed = [145, 155]; semanticId = null; semanticClasses = []; semanticStatus = "Pending (click Run DeepLabV3)";
    renderAll();
  };
  body.querySelector("#l7-scn").onclick = async () => {
    setSampleActive("l7-scn");
    srcId = imgToImageData(await loadHTMLImage(lab.sample2), 480);
    seed = [Math.floor(srcId.height / 2), Math.floor(srcId.width / 2)];
    semanticId = null; renderAll();
    await runSemantic();
  };
  body.querySelector("#l7-file").onchange = async e => {
    if (e.target.files[0]) {
      setSampleActive(null);
      srcId = imgToImageData(await loadHTMLImage(URL.createObjectURL(e.target.files[0])), 480);
      seed = [Math.floor(srcId.height / 2), Math.floor(srcId.width / 2)];
      semanticId = null; semanticStatus = "Pending (click Run DeepLabV3)";
      renderAll();
    }
  };
  body.querySelector("#l7-sem").onclick = runSemantic;
  renderAll();
}

renderHome();
