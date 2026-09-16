let selectedType = 'public-data';
const $ = id => document.getElementById(id);
function show(message) { if (message !== 'Требуется access-токен') alert(message); }
async function api(url, options = {}) {
  options.credentials = 'include';
  options.headers = {'Content-Type': 'application/json', ...(options.headers || {})};
  const response = await fetch(url, options);
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || 'Ошибка запроса');
  return data;
}
function credentials() {
  const username = $('username').value;
  const password = $('password').value;
  if (!username || !password) { show('Заполните имя пользователя и пароль'); return null; }
  return {username, password};
}
async function register() { const dataInput=credentials(); if(!dataInput) return; try { await api('/api/auth/register',{method:'POST',body:JSON.stringify(dataInput)}); await openApp(); } catch(e) { show(e.message); } }
async function login() { const dataInput=credentials(); if(!dataInput) return; try { await api('/api/auth/login',{method:'POST',body:JSON.stringify(dataInput)}); await openApp(); } catch(e) { show(e.message); } }
async function logout() { try { await api('/api/auth/logout',{method:'POST'}); } catch(e) {} $('app-section').hidden=true; $('auth-section').hidden=false; document.body.classList.add('auth-page'); }
async function openApp() { try { const user=await api('/api/auth/me'); $('current-user').textContent=`Добро пожаловать, ${user.username}`; $('auth-section').hidden=true; $('app-section').hidden=false; document.body.classList.remove('auth-page'); selectTab('public-data'); } catch(e) { show(e.message); } }
function selectTab(type) { selectedType=type; $('tab-public').classList.toggle('active',type==='public-data'); $('tab-confidential').classList.toggle('active',type==='confidential'); $('panel-title').textContent=type==='public-data'?'Неконфиденциальные данные':'Конфиденциальные данные'; $('search').value=''; loadData(); }
function addRecord() { location.href=`/data-form.html?type=${selectedType}`; }
async function loadData() { try { const records=await api(`/api/${selectedType}?search=${encodeURIComponent($('search').value)}`); $('records').innerHTML=records.map(r=>`<article class="record"><div><h3>${escapeHtml(r.title)}</h3><p>${escapeHtml(r.content)}</p></div><div class="record-actions"><button onclick="editRecord(${r.id})">Отредактировать</button><button class="danger" onclick="deleteRecord(${r.id})">Удалить</button></div></article>`).join('')||'<p class="empty">Записей нет.</p>'; } catch(e) { show(e.message); } }
function editRecord(id) { location.href=`/data-form.html?type=${selectedType}&id=${id}`; }
async function deleteRecord(id) { try { await api(`/api/${selectedType}/${id}`,{method:'DELETE'}); loadData(); } catch(e) { show(e.message); } }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])); }
openApp();
