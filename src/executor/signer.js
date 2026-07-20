// Loads a burner-wallet keypair from a base58 secret (env var only — never a
// file in the repo) and signs Solana versioned transactions, using only
// node:crypto's ed25519 support. No third-party crypto dependencies.

import { createPrivateKey, createPublicKey, sign as edSign } from 'node:crypto';
import { b58decode, b58encode } from '../util/base58.js';

// PKCS8 DER prefix for a raw 32-byte ed25519 seed.
const PKCS8_ED25519_PREFIX = Buffer.from('302e020100300506032b657004220420', 'hex');

/**
 * Accepts the standard Solana 64-byte secret key (seed || pubkey, e.g. a
 * Phantom/solana-keygen export) or a bare 32-byte seed, base58-encoded.
 * @param {string} base58Secret
 */
export function loadKeypair(base58Secret) {
  const raw = b58decode(base58Secret.trim());
  let seed;
  let expectedPub = null;
  if (raw.length === 64) {
    seed = raw.subarray(0, 32);
    expectedPub = raw.subarray(32);
  } else if (raw.length === 32) {
    seed = raw;
  } else {
    throw new Error(`invalid private key length ${raw.length} (expected 32 or 64 bytes)`);
  }

  const privateKey = createPrivateKey({
    key: Buffer.concat([PKCS8_ED25519_PREFIX, seed]),
    format: 'der',
    type: 'pkcs8',
  });
  const spki = createPublicKey(privateKey).export({ format: 'der', type: 'spki' });
  const publicKeyBytes = Buffer.from(spki.subarray(spki.length - 32));
  if (expectedPub && !publicKeyBytes.equals(expectedPub)) {
    throw new Error('secret key is corrupt: derived public key does not match embedded one');
  }
  return { privateKey, publicKeyBytes, publicKey: b58encode(publicKeyBytes) };
}

/** Solana compact-u16 ("shortvec") decoding. Returns [value, bytesRead]. */
export function readShortVec(buf, offset) {
  let value = 0;
  let shift = 0;
  let i = offset;
  for (;;) {
    const byte = buf[i];
    if (byte === undefined) throw new Error('shortvec: buffer too short');
    value |= (byte & 0x7f) << shift;
    i += 1;
    if ((byte & 0x80) === 0) break;
    shift += 7;
    if (shift > 14) throw new Error('shortvec: value too large');
  }
  return [value, i - offset];
}

/** First static account key of a (possibly versioned) message = fee payer. */
export function feePayerOfMessage(message) {
  let o = 0;
  if ((message[0] & 0x80) !== 0) o = 1; // versioned message prefix byte
  o += 3; // message header (3 u8s)
  const [numKeys, read] = readShortVec(message, o);
  if (numKeys < 1) throw new Error('message has no account keys');
  o += read;
  return message.subarray(o, o + 32);
}

/**
 * Signs a serialized (base64) transaction as returned by Jupiter's /swap.
 * The burner wallet must be the fee payer (signature slot 0) — which it is
 * for Jupiter swaps where userPublicKey is our wallet.
 *
 * @param {string} txBase64
 * @param {ReturnType<typeof loadKeypair>} keypair
 * @returns {{ signedTxBase64: string, signatureBase58: string }}
 */
export function signTransaction(txBase64, keypair) {
  const tx = Buffer.from(txBase64, 'base64');
  const [numSignatures, sigLenBytes] = readShortVec(tx, 0);
  if (numSignatures < 1) throw new Error('transaction has no signature slots');
  const messageStart = sigLenBytes + numSignatures * 64;
  if (tx.length <= messageStart) throw new Error('malformed transaction: no message');
  const message = tx.subarray(messageStart);

  const feePayer = feePayerOfMessage(message);
  if (!feePayer.equals(keypair.publicKeyBytes)) {
    throw new Error('refusing to sign: burner wallet is not the transaction fee payer');
  }

  const signature = edSign(null, message, keypair.privateKey);
  signature.copy(tx, sigLenBytes); // fee payer signature is slot 0
  return { signedTxBase64: tx.toString('base64'), signatureBase58: b58encode(signature) };
}
