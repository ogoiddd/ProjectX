import { test } from 'node:test';
import assert from 'node:assert/strict';
import { scanHtmlForAddresses } from '../src/parser/siteScan.js';

const USDC = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';
const WSOL = 'So11111111111111111111111111111111111111112';

test('finds CA next to a "Contract Address" label and ranks it first', () => {
  const html = `
    <html><body>
      <p>Some noise ${WSOL}</p>
      <h2>Contract Address</h2>
      <code>${USDC}</code>
    </body></html>`;
  const candidates = scanHtmlForAddresses(html);
  assert.equal(candidates[0].address, USDC);
  assert.equal(candidates[0].nearKeyword, true);
});

test('frequency breaks ties when no keyword is near', () => {
  const html = `${WSOL} ... ${USDC} ... ${USDC} ... ${USDC}`;
  const candidates = scanHtmlForAddresses(html);
  assert.equal(candidates[0].address, USDC);
  assert.equal(candidates[0].occurrences, 3);
});

test('empty/irrelevant html yields no candidates', () => {
  assert.deepEqual(scanHtmlForAddresses(''), []);
  assert.deepEqual(scanHtmlForAddresses('<html><body>hello world</body></html>'), []);
});
