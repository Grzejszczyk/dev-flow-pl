import assert from 'node:assert/strict';
import test from 'node:test';
import { submitForm } from './form.mjs';

test('formularz pokazuje konflikt i zachowuje wpisany kod', async () => {
  const page = await submitForm('A17', async () => ({ status: 400 }));

  assert.match(page, /Taki kod już istnieje\./);
  assert.match(page, /value="A17"/);
});
