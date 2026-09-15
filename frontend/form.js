const params=new URLSearchParams(location.search); const type=params.get('type')||'public-data'; const id=params.get('id'); const $=name=>document.getElementById(name);
async function api(url,options={}){options.credentials='include';options.headers={'Content-Type':'application/json',...(options.headers||{})};const response=await fetch(url,options);const data=response.status===204?null:await response.json();if(!response.ok)throw new Error(data?.detail||'Ошибка запроса');return data;}
function goBack(){location.href='/';}
async function init(){$('form-title').textContent=id?'Редактирование данных':'Добавление данных';if(id)try{const record=await api(`/api/${type}/${id}`);$('title').value=record.title;$('content').value=record.content;}catch(e){alert(e.message);}}
async function saveRecord(event){event.preventDefault();try{await api(`/api/${type}${id?`/${id}`:''}`,{method:id?'PUT':'POST',body:JSON.stringify({title:$('title').value,content:$('content').value})});goBack();}catch(e){alert(e.message);}}
init();
