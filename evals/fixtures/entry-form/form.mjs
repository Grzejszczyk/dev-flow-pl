export function renderForm(code = '', message = '') {
  const value = code.replaceAll('&', '&amp;').replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;').replaceAll('>', '&gt;');

  return `<!doctype html>
<html lang="pl"><meta charset="utf-8"><title>Wpisy</title>
<form method="post" action="/">
  <label>Kod <input name="code" value="${value}" required></label>
  <button>Zapisz</button>
</form>
<p role="status">${message}</p></html>`;
}

export async function submitForm(code, createEntry) {
  const response = await createEntry(code);
  if (response.status === 201) return renderForm('', 'Zapisano.');
  if (response.status === 400) return renderForm(code, 'Taki kod już istnieje.');
  return renderForm(code, 'Nie udało się zapisać.');
}
