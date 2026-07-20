import { test } from 'node:test';
import assert from 'node:assert/strict';
import { randomBytes, verify as edVerify, createPublicKey } from 'node:crypto';
import { loadKeypair, signTransaction, readShortVec } from '../src/executor/signer.js';
import { b58encode } from '../src/util/base58.js';

function makeKeypair() {
  const seed = randomBytes(32);
  return loadKeypair(b58encode(seed));
}

/** Minimal legacy-format transaction: 1 sig slot + message with 1 static key. */
function makeUnsignedTx(feePayerBytes) {
  const sigSection = Buffer.concat([Buffer.from([1]), Buffer.alloc(64)]);
  const message = Buffer.concat([
    Buffer.from([1, 0, 1]), // header
    Buffer.from([1]), // 1 static account key
    feePayerBytes,
    Buffer.alloc(32), // recent blockhash
    Buffer.from([0]), // 0 instructions
  ]);
  return { txBase64: Buffer.concat([sigSection, message]).toString('base64'), message };
}

test('loadKeypair accepts 32-byte seed and 64-byte secret key', () => {
  const seed = randomBytes(32);
  const kp32 = loadKeypair(b58encode(seed));
  const kp64 = loadKeypair(b58encode(Buffer.concat([seed, kp32.publicKeyBytes])));
  assert.equal(kp32.publicKey, kp64.publicKey);
});

test('loadKeypair rejects a 64-byte key whose halves do not match', () => {
  const seed = randomBytes(32);
  const wrongPub = randomBytes(32);
  assert.throws(() => loadKeypair(b58encode(Buffer.concat([seed, wrongPub]))), /corrupt/);
});

test('signTransaction places a valid ed25519 signature in slot 0', () => {
  const kp = makeKeypair();
  const { txBase64, message } = makeUnsignedTx(kp.publicKeyBytes);
  const { signedTxBase64 } = signTransaction(txBase64, kp);

  const signed = Buffer.from(signedTxBase64, 'base64');
  const [numSigs, read] = readShortVec(signed, 0);
  assert.equal(numSigs, 1);
  const signature = signed.subarray(read, read + 64);
  const publicKey = createPublicKey(kp.privateKey);
  assert.equal(edVerify(null, message, publicKey, signature), true);
});

test('signTransaction refuses when the wallet is not the fee payer', () => {
  const kp = makeKeypair();
  const other = makeKeypair();
  const { txBase64 } = makeUnsignedTx(other.publicKeyBytes);
  assert.throws(() => signTransaction(txBase64, kp), /not the transaction fee payer/);
});
