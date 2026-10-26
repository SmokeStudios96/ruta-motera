// generar_iconos_moto.mjs
import fs from 'node:fs';
import zlib from 'node:zlib';
import path from 'node:path';

function makeCrcTable() {
  let c;
  const table = [];
  for (let n = 0; n < 256; n++) {
    c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    table[n] = c;
  }
  return table;
}
const crcTable = makeCrcTable();
function crc32(buf) {
  let crc = 0 ^ (-1);
  for (let i = 0; i < buf.length; i++) crc = (crc >>> 8) ^ crcTable[(crc ^ buf[i]) & 0xFF];
  return (crc ^ (-1)) >>> 0;
}
function createChunk(type, data) {
  const buf = Buffer.alloc(4 + 4 + data.length + 4);
  buf.writeUInt32BE(data.length, 0);
  buf.write(type, 4);
  data.copy(buf, 8);
  buf.writeUInt32BE(crc32(buf.subarray(4, 8 + data.length)), 8 + data.length);
  return buf;
}
function createIHDR(width, height) {
  const buf = Buffer.alloc(13);
  buf.writeUInt32BE(width, 0);
  buf.writeUInt32BE(height, 4);
  buf[8] = 8;
  buf[9] = 6;
  buf[10] = 0;
  buf[11] = 0;
  buf[12] = 0;
  return createChunk('IHDR', buf);
}
function generateBikerPng(size) {
  const header = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = createIHDR(size, size);
  const stride = 1 + size * 4;
  const raw = Buffer.alloc(stride * size);
  const cx = size / 2;
  const cy = size / 2;

  for (let y = 0; y < size; y++) {
    const rowOffset = y * stride;
    raw[rowOffset] = 0;
    for (let x = 0; x < size; x++) {
      const px = rowOffset + 1 + x * 4;
      const dx = Math.abs(x - cx);
      const dy = Math.abs(y - cy);
      const dist = Math.hypot(x - cx, y - cy);

      const inBadge = dx < size * 0.42 && dy < size * 0.42 &&
        Math.hypot(Math.max(0, dx - size * 0.26), Math.max(0, dy - size * 0.26)) < size * 0.16;

      // Anillo de velocímetro / brújula
      const inRing = dist < size * 0.32 && dist > size * 0.25;
      const inNeedle = dist < size * 0.26 && Math.abs((x - cx) - (y - cy)) < size * 0.04;
      const inCenterPin = dist < size * 0.07;

      if (inBadge) {
        if (inNeedle || inCenterPin) {
          // Verde Menta Neón #00df82
          raw[px] = 0; raw[px + 1] = 223; raw[px + 2] = 130; raw[px + 3] = 255;
        } else if (inRing) {
          // Verde Neón secundario
          raw[px] = 0; raw[px + 1] = 223; raw[px + 2] = 130; raw[px + 3] = 220;
        } else {
          // Verde oscuro Smoke Studios (#022116)
          raw[px] = 2; raw[px + 1] = 33; raw[px + 2] = 22; raw[px + 3] = 255;
        }
      } else {
        // Fondo negro puro #000000
        raw[px] = 0; raw[px + 1] = 0; raw[px + 2] = 0; raw[px + 3] = 255;
      }
    }
  }

  const idat = createChunk('IDAT', zlib.deflateSync(raw));
  const iend = createChunk('IEND', Buffer.alloc(0));
  return Buffer.concat([header, ihdr, idat, iend]);
}

const iconsDir = path.join(process.cwd(), 'frontend', 'public', 'icons');
if (!fs.existsSync(iconsDir)) fs.mkdirSync(iconsDir, { recursive: true });

fs.writeFileSync(path.join(iconsDir, 'icon-192.png'), generateBikerPng(192));
fs.writeFileSync(path.join(iconsDir, 'icon-512.png'), generateBikerPng(512));

console.log('✅ ¡Íconos Biker de RutaMotera generados en frontend/public/icons/: 192x192 y 512x512!');