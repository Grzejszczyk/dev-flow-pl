import assert from 'node:assert/strict';
import test from 'node:test';
import { createApp } from './server.mjs';

test('API zapisuje nowy kod', async t => {
  const server = createApp();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));

  const url = `http://127.0.0.1:${server.address().port}/api/entries`;
  const response = await fetch(url, { method: 'POST', body: new URLSearchParams({ code: 'A17' }) });

  assert.equal(response.status, 201);
  assert.deepEqual(await (await fetch(url)).json(), ['A17']);
});
