'use strict';
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const page = document.body.dataset.page;
const state = {skip: 0, limit: 20, search: '', forecasts: [], products: [], customers: []};
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num = v => v == null ? '—' : Number(v).toLocaleString('ko-KR', {maximumFractionDigits: 1});
const money = v => `${num(v)}원`;
const badge = (text, type = '') => `<span class="tag ${type}">${esc(text)}</span>`;
const productName = p => `<strong>${esc(p.name)}</strong><small>${esc(p.sku)}</small>`;
const statusTag = s => s === 'urgent' ? badge('긴급', 'danger') : s === 'order_now' ? badge('발주 필요', 'warn') : badge('정상');
const empty = (message = '아직 등록된 데이터가 없습니다.') => `<div class="empty">${esc(message)}</div>`;
function table(headers, rows) {return rows.length ? `<div class="table-wrap"><table><thead><tr>${headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>`<td>${v}</td>`).join('')}</tr>`).join('')}</tbody></table></div>` : empty();}
function showError(error, target = '#error') {const el=$(target); el.textContent=error.message || String(error); el.hidden=false;}
function clearError(target = '#error') {$(target).hidden=true;}
function toast(message) {$('#toast').textContent=message; $('#toast').hidden=false; clearTimeout(state.toastTimer); state.toastTimer=setTimeout(()=>$('#toast').hidden=true, 4000);}
async function api(path, options = {}) {
 const response = await fetch(path, options);
 const text = await response.text(); let data;
 try {data=text ? JSON.parse(text) : null;} catch {throw new Error(`응답을 읽을 수 없습니다. 서버 상태를 확인하세요. (${response.status})`);}
 if(!response.ok) {
  const detail=data?.detail;
  const message=Array.isArray(detail) ? detail.map(e=>`${e.loc?.slice(1).join('.') || '입력값'}: ${e.msg}`).join('\n') : (typeof detail==='string' ? detail : `요청에 실패했습니다. (${response.status})`);
  throw new Error(message);
 }
 return data;
}
const json = (method, data) => ({method, headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)});
async function all(path) {let rows=[]; for(let skip=0;;skip+=100) {const batch=await api(`${path}?skip=${skip}&limit=100`); rows.push(...batch); if(batch.length<100) return rows;}}
async function catalog() {const [p,c]=await Promise.all([all('/products'), all('/customers')]); state.products=p; state.customers=c;}
const customerLabel = id => state.customers.find(c=>c.id===id)?.company_name || `거래처 #${id}`;
const orderStatus = s => s === 'confirmed' ? badge('확정') : badge(s);
function orderRows(rows) {return rows.map(o=>[`<strong>#${o.id}</strong>`,esc(customerLabel(o.customer_id)),esc(new Date(o.ordered_at.endsWith('Z') || /[+-]\d\d:\d\d$/.test(o.ordered_at) ? o.ordered_at : o.ordered_at+'Z').toLocaleString('ko-KR')),`${o.items.length}개 품목`,money(o.total_amount),orderStatus(o.status),`<button class="secondary row-action" data-detail="${o.id}">상세</button>`]);}
function bindOrderDetails(rows) {$$('[data-detail]').forEach(b=>b.onclick=()=>{const o=rows.find(x=>x.id===Number(b.dataset.detail));openModal(`주문 #${o.id} 상세`, `<p>${esc(customerLabel(o.customer_id))} · ${money(o.total_amount)}</p>${table(['상품','수량','단가'],o.items.map(i=>[esc(state.products.find(p=>p.id===i.product_id)?.name || `상품 #${i.product_id}`),num(i.quantity),money(i.unit_price)]))}`,null);});}
async function overview() {
 const [summary, inventory, orders, customers, products]=await Promise.all([api('/dashboard/summary'),api('/inventory?low_stock_only=true'),api('/orders?limit=5'),all('/customers'),all('/products')]);
 state.customers=customers; state.products=products;
 $$('[data-metric]').forEach(el=>el.textContent=num(summary[el.dataset.metric]));
 $('#low-stock').innerHTML=inventory.length ? table(['상품','현재 재고','재주문 기준','상태'],inventory.map(p=>[productName(p),`<strong>${num(p.quantity)}</strong>`,num(p.reorder_point),badge(p.quantity===0?'품절':'재고 부족',p.quantity===0?'danger':'warn')])) : empty('현재 재고 부족 상품이 없습니다.');
 $('#recent-orders').innerHTML=table(['주문','거래처','주문 일시','품목','주문 금액','상태',''],orderRows(orders));bindOrderDetails(orders);
}
async function listing() {
 let path=`/${page}`;
 if(page==='inventory') path+=`?low_stock_only=${$('#low-only').checked}`;
 else path+=`?skip=${state.skip}&limit=${state.limit+1}${page==='products'?`&search=${encodeURIComponent(state.search)}`:''}`;
 if(page==='orders') await catalog();
 const raw=await api(path), hasNext=page!=='inventory'&&raw.length>state.limit;
 const rows=page==='inventory'?raw:raw.slice(0,state.limit);
 $('#list-count').textContent=`${rows.length}개${page==='inventory'?'': ' · 현재 페이지'}`;
 if(page==='products') $('#list').innerHTML=table(['상품','단가','현재 재고','재주문 기준','상태'],rows.map(p=>[productName(p),money(p.unit_price),num(p.stock_quantity),num(p.reorder_point),p.stock_quantity<=p.reorder_point?badge('재고 부족','warn'):badge('정상')]));
 if(page==='customers') $('#list').innerHTML=table(['거래처','사업자번호','담당자','이메일'],rows.map(c=>[`<strong>${esc(c.company_name)}</strong><small>#${c.id}</small>`,esc(c.business_number),esc(c.contact_name||'—'),esc(c.contact_email||'—')]));
 if(page==='orders') {$('#list').innerHTML=table(['주문','거래처','주문 일시','품목','주문 금액','상태',''],orderRows(rows));bindOrderDetails(rows);}
 if(page==='inventory') {
  $('#list').innerHTML=table(['상품','현재 재고','재주문 기준','상태',''],rows.map(p=>[productName(p),`<strong>${num(p.quantity)}</strong>`,num(p.reorder_point),p.needs_reorder?badge('재고 부족','warn'):badge('정상'),`<button class="secondary row-action" data-adjust="${p.product_id}">재고 조정</button>`]));
  $$('[data-adjust]').forEach(b=>b.onclick=()=>{const p=rows.find(x=>x.product_id===Number(b.dataset.adjust));openModal('재고 조정',`<p>${esc(p.name)} · 현재 ${num(p.quantity)}개</p><div class="form-grid" style="margin-top:18px">${field('amount','조정 수량','number','', 'required step="1"', '입고 +10 / 출고 -10처럼 입력하세요.')}</div>`,async data=>{if(Number(data.amount)===0)throw new Error('0 이외의 조정 수량을 입력하세요.');await api(`/inventory/${p.product_id}`,json('PATCH',{amount:Number(data.amount)}));});});
 }
 if(page!=='inventory') {$('#prev').disabled=state.skip===0;$('#next').disabled=!hasNext;$('#page-number').textContent=`${state.skip/state.limit+1} 페이지`;}
}
function field(name,label,type='text',value='',attrs='',hint='') {return `<label>${esc(label)}<input name="${name}" type="${type}" value="${esc(value)}" ${attrs}>${hint?`<small>${esc(hint)}</small>`:''}</label>`;}
function openModal(title, html, onSave) {
 $('#modal-title').textContent=title;$('#modal-fields').innerHTML=html;clearError('#modal-error');$('#save-modal').hidden=!onSave;$('#cancel-modal').textContent=onSave?'취소':'닫기';$('#modal-form').onsubmit=async e=>{
  e.preventDefault();if(!onSave)return;clearError('#modal-error');const button=$('#save-modal');button.disabled=true;
  try {await onSave(Object.fromEntries(new FormData(e.target)));$('#modal').close();toast('저장되었습니다.');await reload();}catch(error){showError(error,'#modal-error');}finally{button.disabled=false;}
 };$('#modal').showModal();
}
async function create() {
 if(page==='products')openModal('상품 등록',`<div class="form-grid">${field('sku','SKU','text','','required maxlength="50"')}${field('name','상품명','text','','required maxlength="200"')}${field('unit_price','판매 단가 (원)','number','','required min="0.01" step="0.01"')}${field('initial_stock','시작 재고','number','0','required min="0" step="1"')}${field('reorder_point','재주문 기준','number','10','required min="0" step="1"')}</div>`,async d=>{await api('/products',json('POST',{...d,initial_stock:Number(d.initial_stock),reorder_point:Number(d.reorder_point)}));});
 if(page==='customers')openModal('거래처 등록',`<div class="form-grid">${field('company_name','거래처명','text','','required maxlength="200"')}${field('business_number','사업자번호','text','','required maxlength="20"')}${field('contact_name','담당자','text','','maxlength="100"')}${field('contact_email','이메일','email','','maxlength="200"')}</div>`,async d=>{await api('/customers',json('POST',{...d,contact_name:d.contact_name||null,contact_email:d.contact_email||null}));});
 if(page==='orders') {
  await catalog();if(!state.products.length||!state.customers.length)throw new Error('상품과 거래처를 먼저 등록하세요.');
  openModal('주문 등록',`<label>거래처<select name="customer_id" required><option value="">거래처 선택</option>${state.customers.map(c=>`<option value="${c.id}">${esc(c.company_name)}</option>`).join('')}</select></label><div class="order-items"><h3>주문 상품</h3><div id="order-rows"></div><button class="secondary" type="button" id="add-item">+ 상품 추가</button></div><div class="order-note">주문 예상 금액 <strong id="order-total">0원</strong><br>등록 시 재고가 자동 차감됩니다.</div>`,async d=>{const items=$$('.order-row').map(r=>({product_id:Number($('select',r).value),quantity:Number($('input',r).value)}));await api('/orders',json('POST',{customer_id:Number(d.customer_id),items}));});
  $('#add-item').onclick=addOrderItem;addOrderItem();
 }
}
function addOrderItem() {
 const div=document.createElement('div');div.className='order-row';
 div.innerHTML=`<select aria-label="주문 상품" required><option value="">상품 선택</option>${state.products.map(p=>`<option value="${p.id}">${esc(p.name)} · ${esc(p.sku)} · 재고 ${num(p.stock_quantity)}</option>`).join('')}</select><input aria-label="주문 수량" type="number" min="1" step="1" value="1" required><button class="secondary" type="button" aria-label="품목 제거">×</button>`;
 $('button',div).onclick=()=>{if($$('.order-row').length>1){div.remove();orderTotal();}};div.oninput=orderTotal;$('#order-rows').append(div);orderTotal();
}
function orderTotal() {$('#order-total').textContent=money($$('.order-row').reduce((sum,r)=>sum+Number(state.products.find(p=>p.id===Number($('select',r).value))?.unit_price||0)*Number($('input',r).value||0),0));}
function formQuery(selector) {const data=new FormData($(selector));const params=new URLSearchParams(data);if(selector==='#replenishment-filter')params.set('needs_order_only',$('[name=needs_order_only]').checked);return params.toString();}
async function forecasts() {
 const result=await api('/forecasts?'+formQuery('#forecast-filter'));state.forecasts=result.forecasts;
 $('#forecast-product').innerHTML=result.forecasts.map(p=>`<option value="${p.product_id}">${esc(p.name)} · ${esc(p.sku)}</option>`).join('');$('#forecast-product').disabled=!result.forecasts.length;
 $('#forecast-list').innerHTML=table(['상품','예측 기간 총 수요','모델','WAPE','주문 활성 비율'],result.forecasts.map(p=>[productName(p),num(p.forecast.reduce((s,x)=>s+x.quantity,0)),esc(p.model),p.backtest_wape==null?'—':`${num(p.backtest_wape*100)}%`,`${num(p.active_week_ratio*100)}%`]));
 $('#excluded-list').innerHTML=result.excluded.length?table(['상품','주문 활성 비율','제외 사유'],result.excluded.map(p=>[productName(p),`${num(p.active_week_ratio*100)}%`,`<div class="detail">${esc(p.reason)}</div>`])):empty('예측 제외 상품이 없습니다.');
 drawForecast(result.forecasts[0]);
}
function drawForecast(p) {
 if(!p){$('#forecast-chart').innerHTML=empty('예측 대상 상품이 없습니다.');return;}
 const points=[...p.history,...p.forecast],w=900,h=280,left=50,right=25,top=25,bottom=45,max=Math.max(1,...points.map(x=>x.quantity))*1.15;
 const x=i=>left+i*(w-left-right)/Math.max(1,points.length-1),y=v=>h-bottom-v*(h-top-bottom)/max;
 const line=(start,values)=>values.map((v,i)=>`${i?'L':'M'}${x(start+i).toFixed(1)},${y(v.quantity).toFixed(1)}`).join(' ');
 let grid='';for(let i=0;i<5;i++){const v=max*i/4;grid+=`<line x1="${left}" y1="${y(v)}" x2="${w-right}" y2="${y(v)}" stroke="#e9eee9"/><text x="${left-10}" y="${y(v)+4}" text-anchor="end" fill="#87998d" font-size="11">${num(v)}</text>`;}
 let labels='';points.forEach((pt,i)=>{if(i%Math.max(1,Math.ceil(points.length/7))===0||i===points.length-1)labels+=`<text x="${x(i)}" y="${h-15}" text-anchor="middle" fill="#87998d" font-size="11">${esc(pt.week_start.slice(5))}</text>`;});
 const forecastPoints=p.history.length?[p.history.at(-1),...p.forecast]:p.forecast, start=p.history.length? p.history.length-1:0;
 $('#forecast-chart').innerHTML=`<div class="chart-box"><div class="chart-stats"><span>${esc(p.name)}</span><span>예측 수요 <strong>${num(p.forecast.reduce((s,x)=>s+x.quantity,0))}개</strong></span><span>WAPE <strong>${p.backtest_wape==null?'—':num(p.backtest_wape*100)+'%'}</strong></span></div><svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(p.name)} 주간 실적과 예측 그래프">${grid}${labels}<path d="${line(0,p.history)}" fill="none" stroke="#9baea1" stroke-width="3"/><path d="${line(start,forecastPoints)}" fill="none" stroke="#087f68" stroke-width="3" stroke-dasharray="7 4"/>${points.map((pt,i)=>`<circle cx="${x(i)}" cy="${y(pt.quantity)}" r="4" fill="${i<p.history.length?'#9baea1':'#087f68'}"><title>${esc(pt.week_start)}: ${num(pt.quantity)}개</title></circle>`).join('')}</svg><div class="legend"><span>주간 실적</span><span>주간 예측</span></div>${table(['구분','주 시작일','수량'],points.map((pt,i)=>[i<p.history.length?'실적':'예측',esc(pt.week_start),num(pt.quantity)]))}</div>`;
}
async function forecastDetail() {const id=$('#forecast-product').value;if(!id)return;const p=await api(`/forecasts/products/${id}?${formQuery('#forecast-filter')}`);drawForecast(p);}
async function replenishment() {
 const result=await api('/replenishment?'+formQuery('#replenishment-filter'));
 $('#plan-summary').innerHTML=`<span>기준일 <strong>${esc(result.as_of)}</strong></span><span>예측 범위 <strong>${result.horizon_weeks}주</strong></span><span>긴급 <strong>${result.items.filter(p=>p.status==='urgent').length}개</strong></span><span>발주 필요 <strong>${result.items.filter(p=>p.status==='order_now').length}개</strong></span>`;
 $('#plan-list').innerHTML=table(['상품','상태','판단 방식','현재 재고','추천 발주량','예상 품절일','발주 기한','안전재고','재주문 수준','설명'],result.items.map(p=>[productName(p),statusTag(p.status),p.method==='forecast'?'수요예측':'재주문 기준',num(p.current_stock),p.recommended_qty==null?'계산 대상 아님':num(p.recommended_qty),esc(p.stockout_date||'—'),esc(p.order_by_date||'—'),num(p.safety_stock),num(p.reorder_level),`<div class="detail">${esc(p.note||'입고까지 예상 수요 '+num(p.lead_time_demand)+'개')}</div>`]));
}
async function upload(e) {
 e.preventDefault();clearError();$('#import-result').innerHTML='';const form=e.target,button=$('button[type=submit]',form),file=form.file.files[0];if(file.size>10*1024*1024){showError(new Error('파일은 10MB 이하여야 합니다.'));return;}
 button.disabled=true;button.textContent='가져오는 중…';
 try {const data=new FormData();data.append('file',file);const result=await api(`/imports/orders?initial_stock=${encodeURIComponent(form.initial_stock.value)}`,{method:'POST',body:data});$('#import-result').innerHTML=`<div class="result-box"><h3>주문 데이터를 가져왔습니다.</h3><p>총 ${num(result.total_rows)}행 · 주문 ${num(result.orders_created)}건 등록</p><p>새 상품 ${num(result.products_created)}개 · 새 거래처 ${num(result.customers_created)}곳</p><a class="text-link" href="/ui/orders">주문 내역 확인 ↗</a></div>`;form.file.value='';toast('가져오기가 완료되었습니다.');}catch(error){showError(error);}finally{button.disabled=false;button.textContent='주문 데이터 가져오기';}
}
async function reload() {
 clearError();const button=$('#refresh');button.disabled=true;button.textContent='불러오는 중…';
 try {if(page==='overview')await overview();else if(['products','customers','orders','inventory'].includes(page))await listing();else if(page==='forecasts')await forecasts();else if(page==='replenishment')await replenishment();}
 catch(error){showError(error);if(page==='forecasts'){$('#forecast-chart').innerHTML=empty('현재 예측을 표시할 수 없습니다.');$('#forecast-list').innerHTML='';$('#excluded-list').innerHTML='';$('#forecast-product').innerHTML='';}if(page==='replenishment'){$('#plan-summary').innerHTML='';$('#plan-list').innerHTML=empty('현재 추천을 표시할 수 없습니다.');}}
 finally{button.disabled=false;button.textContent='↻ 새로고침';}
}
$('#today').textContent=new Date().toLocaleDateString('ko-KR',{year:'numeric',month:'long',day:'numeric'});
$('#refresh').onclick=reload;$('#close-modal').onclick=$('#cancel-modal').onclick=()=>$('#modal').close();
$('.mobile-menu').onclick=e=>{const open=$('#sidebar').classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',open);};
$('#create')?.addEventListener('click',async()=>{try{await create();}catch(error){showError(error);}});
$('#search-form')?.addEventListener('submit',e=>{e.preventDefault();state.search=e.target.search.value.trim();state.skip=0;reload();});
$('#low-only')?.addEventListener('change',reload);
$('#prev')?.addEventListener('click',()=>{state.skip=Math.max(0,state.skip-state.limit);reload();});
$('#next')?.addEventListener('click',()=>{state.skip+=state.limit;reload();});
for(const selector of ['#forecast-filter','#replenishment-filter'])$(selector)?.addEventListener('submit',e=>{e.preventDefault();reload();});
$('#forecast-product')?.addEventListener('change',async()=>{try{clearError();await forecastDetail();}catch(error){showError(error);}});
$('#import-form')?.addEventListener('submit',upload);
reload();
