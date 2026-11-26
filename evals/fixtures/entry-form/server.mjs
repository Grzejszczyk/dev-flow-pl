import { createServer } from 'node:http';
import { pathToFileURL } from 'node:url';
import { renderForm, submitForm } from './form.mjs';

async function readCode(request) {
  request.setEncoding('utf8');
  let body = '';
  for await (const chunk of request) body += chunk;
  return new URLSearchParams(body).get('code') ?? '';
}

export function createApp() {
  const entries = new Set();
  const server = createServer(async (request, response) => {
    if (request.url === '/' && request.method === 'GET') {
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' }).end(renderForm());
    } else if (request.url === '/' && request.method === 'POST') {
      const api = `http://127.0.0.1:${server.address().port}/api/entries`;
      const page = await submitForm(await readCode(request), code =>
        fetch(api, { method: 'POST', body: new URLSearchParams({ code }) })
      );
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' }).end(page);
    } else if (request.url === '/api/entries' && request.method === 'GET') {
      response.writeHead(200, { 'Content-Type': 'application/json' }).end(JSON.stringify([...entries]));
    } else if (request.url === '/api/entries' && request.method === 'POST') {
      const code = await readCode(request);
      if (!code) {
        response.writeHead(400).end();
      } else if (entries.has(code)) {
        response.writeHead(409).end();
      } else {
        entries.add(code);
        response.writeHead(201).end();
      }
    } else {
      response.writeHead(404).end();
    }
  });
  return server;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = createApp();
  server.listen(0, '127.0.0.1', () => {
    console.log(`http://127.0.0.1:${server.address().port}/`);
  });
}
