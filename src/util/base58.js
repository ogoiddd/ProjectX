// Base58 (Bitcoin/Solana alphabet) encode/decode. Zero-dependency on purpose:
// this project may handle a wallet key, so we keep the supply chain empty.

const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
const CHAR_MAP = new Map([...ALPHABET].map((c, i) => [c, BigInt(i)]));

/**
 * @param {string} str
 * @returns {Buffer}
 */
export function b58decode(str) {
  if (typeof str !== 'string' || str.length === 0) {
    throw new Error('base58: empty input');
  }
  let num = 0n;
  for (const c of str) {
    const v = CHAR_MAP.get(c);
    if (v === undefined) throw new Error(`base58: invalid character "${c}"`);
    num = num * 58n + v;
  }
  const bytes = [];
  while (num > 0n) {
    bytes.push(Number(num & 0xffn));
    num >>= 8n;
  }
  for (const c of str) {
    if (c === '1') bytes.push(0);
    else break;
  }
  return Buffer.from(bytes.reverse());
}

/**
 * @param {Uint8Array} buf
 * @returns {string}
 */
export function b58encode(buf) {
  let num = 0n;
  for (const byte of buf) num = (num << 8n) + BigInt(byte);
  let out = '';
  while (num > 0n) {
    out = ALPHABET[Number(num % 58n)] + out;
    num /= 58n;
  }
  for (const byte of buf) {
    if (byte === 0) out = '1' + out;
    else break;
  }
  return out;
}

/**
 * A Solana address is base58 text that decodes to exactly 32 bytes
 * (ed25519 public key). Length in text form is 32-44 chars.
 * @param {string} str
 */
export function isSolanaAddress(str) {
  if (typeof str !== 'string' || str.length < 32 || str.length > 44) return false;
  try {
    return b58decode(str).length === 32;
  } catch {
    return false;
  }
}
