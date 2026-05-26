// ══════════════════════════════════════════════════════════
// FORM.JS — Anamnese HC-FMUSP
// ══════════════════════════════════════════════════════════

// ─── DADOS ESTÁTICOS ──────────────────────────────────────

const MUSCULOS_SUP = [
  'Abdução do braço','Adução do braço','Flexão do antebraço',
  'Extensão do antebraço','Flexão da mão','Extensão da mão',
  'Flexão dos dedos','Extensão dos dedos','Abdução dos dedos',
  'Adução dos dedos','Pinça'
];
const MUSCULOS_INF = [
  'Flexão da coxa','Extensão da coxa','Adução da coxa','Abdução da coxa',
  'Flexão da perna','Extensão da perna','Flexão do pé','Extensão do pé',
  'Flexão dos dedos do pé','Extensão dos dedos do pé'
];
const REFLEXOS = [
  { name:'Patelar',      detail:'L2-L4 · Femoral' },
  { name:'Aquileu',      detail:'S1-S2 · Tibial' },
  { name:'Tricipital',   detail:'C7-C8 · Radial' },
  { name:'Bicipital',    detail:'C5-C6 · Musculocutâneo' },
  { name:'Estilo-radial',detail:'C5-C6 · Radial' },
];
const REFLEX_OPTS = ['Normal','Hipoativo','Abolido','Vivo','Exaltado','Clônus','Não testado'];

const TESTES = {
  'Cervical':    ['Hoffman','Adson','Spurling','Mão na cabeça melhora','Distração'],
  'Ombro':       ['Supra-espinhal (Jobe)','Impacto','Infra-espinhal (Patte)',
                  'Acromioclavicular (Cross arm)','Subescapular (Bear hug)',
                  'Mão na cabeça piora','Cabeça longa bíceps (Speed)'],
  'Mão e Punho': ['Durkan','Finkelstein','Tinel','Phalen'],
  'Lombar':      ['Lasègue','Elevação MMII estendido','Lasègue sentado','Schober'],
  'Quadril':     ['Dor à flexão','Gaenslen','Dor à rotação interna',
                  'Patrick (FABER)','Dor à rotação externa','Trendelenburg'],
  'ATM':         ['Dor à palpação ATM','Crepitação ATM','Subluxação ATM']
};

const SENSIBILIDADE_ITEMS = [
  {name:'Protuberância occipital',        detail:'C2'},
  {name:'Fossa supraclavicular',          detail:'C3'},
  {name:'Articulação acromioclavicular',  detail:'C4'},
  {name:'Fossa antecubital lateral',      detail:'C5'},
  {name:'Polegar',                        detail:'C6'},
  {name:'Dedo médio',                     detail:'C7'},
  {name:'Dedo mínimo',                    detail:'C8'},
  {name:'Fossa antecubital medial',       detail:'T1'},
  {name:'Ápice da axila',                 detail:'T2'},
  {name:'Parte anterosuperior da coxa',   detail:'L1'},
  {name:'Parte anteromedial da coxa',     detail:'L2'},
  {name:'Côndilo femoral medial',         detail:'L3'},
  {name:'Maléolo medial',                detail:'L4'},
  {name:'Dorso 3ª articulação metatarsal',detail:'L5'},
  {name:'Calcanhar lateral',              detail:'S1'},
  {name:'Fossa poplítea',                detail:'S2'},
  {name:'Tuberosidade isquiática',        detail:'S3'},
  {name:'Área perianal',                 detail:'S5'},
  {name:'Parte superior da face',         detail:'V1 Oftálmico'},
  {name:'Parte média da face',            detail:'V2 Maxilar'},
  {name:'Parte inferior da face',         detail:'V3 Mandibular'},
];

const GATILHOS = {
  'Cabeça e Pescoço': [
    'Frontal','Masseter','Temporal','Pterigóideo',
    'Esplênio da cabeça','Esplênio cervical',
    'Semi-espinal da cabeça','Semi-espinal cervical',
    'Sub-occipitais','Elevador da escápula','Escalenos'
  ],
  'Tronco e Ombro': [
    'Trapézio','Supra-espinhal','Infra-espinhal',
    'Redondo maior','Redondo menor','Dorsal','Peitoral','Deltóide'
  ],
  'Membros Superiores': ['Bíceps','Flexores do punho','Intrínsecos da mão'],
  'Região Lombar e Abdome': ['Quadrado lombar','Paravertebral lombar'],
  'Membros Inferiores': [
    'Glúteo máximo','Glúteo médio','Glúteo mínimo','Piriforme',
    'Elevador do ânus','Isquiotibiais','Iliopsoas','Quadríceps',
    'Tríceps sural','Adutores da coxa','Intrínsecos dos pés'
  ]
};

// ─── STATE ────────────────────────────────────────────────
const muscleValues      = {};
const reflexValues      = {};
const testValues        = {};
const sensitivityValues = {};
const triggerValues     = {};
let   currentDraftId    = null; // rascunho sendo editado no painel

// ─── LOCALSTORAGE — HISTÓRICO ─────────────────────────────
const STORAGE_KEY = 'anamnese_hcfmusp_rascunhos';

function getRascunhos() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
  catch { return []; }
}
function saveRascunhos(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}
function salvarRascunho(data) {
  const list = getRascunhos();
  const id   = Date.now().toString();
  const item = {
    id,
    nome:      data.nome || '(sem nome)',
    data:      data.data || new Date().toISOString().split('T')[0],
    vas:       data.vas  || '0',
    savedAt:   new Date().toLocaleString('pt-BR'),
    data_form: data
  };
  list.unshift(item); // mais recente primeiro
  saveRascunhos(list);
  return id;
}
function atualizarRascunho(id, data) {
  const list = getRascunhos();
  const idx  = list.findIndex(r => r.id === id);
  if (idx === -1) return;
  list[idx] = {
    ...list[idx],
    nome:      data.nome || list[idx].nome,
    data:      data.data || list[idx].data,
    vas:       data.vas  || list[idx].vas,
    savedAt:   new Date().toLocaleString('pt-BR'),
    data_form: data
  };
  saveRascunhos(list);
}
function deletarRascunho(id) {
  saveRascunhos(getRascunhos().filter(r => r.id !== id));
}

// ─── CONSTRUTORES DINÂMICOS ───────────────────────────────

function buildMuscleSection(containerId, muscles) {
  const container = document.getElementById(containerId);
  if (!container) return;
  muscles.forEach(muscle => {
    const row = document.createElement('div');
    row.className = 'muscle-row';
    row.innerHTML = `
      <span class="muscle-name">${muscle}</span>
      <div class="scale-buttons">
        ${[0,1,2,3,4,5].map(v =>
          `<button type="button" class="scale-btn" data-muscle="${muscle}" data-val="${v}">${v}</button>`
        ).join('')}
      </div>`;
    container.appendChild(row);
    muscleValues[muscle] = '';
  });
  container.querySelectorAll('.scale-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const m = btn.dataset.muscle;
      container.querySelectorAll(`.scale-btn[data-muscle="${m}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      muscleValues[m] = btn.dataset.val;
    });
  });
}

function buildReflexSection() {
  const container = document.getElementById('reflexos-container');
  if (!container) return;
  REFLEXOS.forEach(r => {
    const row = document.createElement('div');
    row.className = 'reflex-row';
    row.innerHTML = `
      <div class="reflex-name">${r.name}
        <small style="color:var(--text-light);font-weight:400"> ${r.detail}</small>
      </div>
      <div class="reflex-options">
        ${REFLEX_OPTS.map(opt =>
          `<button type="button" class="reflex-opt" data-reflex="${r.name}" data-val="${opt}">${opt}</button>`
        ).join('')}
      </div>`;
    container.appendChild(row);
    reflexValues[r.name] = '';
  });
  container.querySelectorAll('.reflex-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      const reflex = btn.dataset.reflex;
      container.querySelectorAll(`.reflex-opt[data-reflex="${reflex}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      reflexValues[reflex] = btn.dataset.val;
    });
  });
}

function buildTestsSection() {
  const container = document.getElementById('testes-container');
  if (!container) return;
  Object.entries(TESTES).forEach(([group, tests]) => {
    const groupDiv = document.createElement('div');
    groupDiv.className = 'test-group';
    groupDiv.innerHTML = `<div class="test-group-title">${group}</div>
      <div class="test-items-grid" id="tg-${group.replace(/\s+/g,'-')}"></div>`;
    container.appendChild(groupDiv);
    const grid = groupDiv.querySelector('.test-items-grid');
    tests.forEach(test => {
      const row = document.createElement('div');
      row.className = 'test-row';
      row.innerHTML = `
        <span class="test-name">${test}</span>
        <div class="test-options">
          <button type="button" class="test-opt" data-test="${test}" data-val="Positivo">+</button>
          <button type="button" class="test-opt" data-test="${test}" data-val="Negativo">−</button>
          <button type="button" class="test-opt" data-test="${test}" data-val="Não realizado">N/R</button>
        </div>`;
      grid.appendChild(row);
      testValues[test] = '';
    });
  });
  container.querySelectorAll('.test-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      const test = btn.dataset.test;
      container.querySelectorAll(`.test-opt[data-test="${test}"]`).forEach(b => {
        b.classList.remove('active-pos','active-neg');
      });
      if (btn.dataset.val === 'Positivo')      btn.classList.add('active-pos');
      else if (btn.dataset.val === 'Negativo') btn.classList.add('active-neg');
      testValues[test] = btn.dataset.val;
    });
  });
}

function buildSensibilidadeSection() {
  const container = document.getElementById('sensibilidade-container');
  if (!container) return;
  SENSIBILIDADE_ITEMS.forEach(item => {
    const row = document.createElement('div');
    row.className = 'sensitivity-row';
    row.innerHTML = `
      <div class="sensitivity-name">${item.name}
        <span style="color:var(--text-light);font-size:11px"> ${item.detail}</span>
      </div>
      <div class="sensitivity-scale">
        ${[1,2,3,4,5,6,7,8].map(v =>
          `<button type="button" class="sens-btn" data-sens="${item.name}" data-val="${v}">${v}</button>`
        ).join('')}
      </div>`;
    container.appendChild(row);
    sensitivityValues[item.name] = '';
  });
  container.querySelectorAll('.sens-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const s = btn.dataset.sens;
      container.querySelectorAll(`.sens-btn[data-sens="${s}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      sensitivityValues[s] = btn.dataset.val;
    });
  });
}

function buildGatilhoSection() {
  const container = document.getElementById('gatilho-container');
  if (!container) return;
  Object.entries(GATILHOS).forEach(([group, muscles]) => {
    const titleDiv = document.createElement('div');
    titleDiv.className = 'trigger-group-title';
    titleDiv.textContent = group;
    container.appendChild(titleDiv);
    muscles.forEach(m => {
      const row = document.createElement('div');
      row.className = 'trigger-row';
      row.innerHTML = `
        <span class="trigger-name">${m}</span>
        <div class="trigger-options">
          <button type="button" class="trigger-opt" data-trigger="${m}" data-val="Presente">+</button>
          <button type="button" class="trigger-opt" data-trigger="${m}" data-val="Ausente">−</button>
        </div>`;
      container.appendChild(row);
      triggerValues[m] = '';
    });
  });
  container.querySelectorAll('.trigger-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      const t = btn.dataset.trigger;
      container.querySelectorAll(`.trigger-opt[data-trigger="${t}"]`).forEach(b => {
        b.classList.remove('active-pos','active-neg');
      });
      if (btn.dataset.val === 'Presente') btn.classList.add('active-pos');
      else                                btn.classList.add('active-neg');
      triggerValues[t] = btn.dataset.val;
    });
  });
}

// ─── CHIPS ────────────────────────────────────────────────
function initChipGroups() {
  document.querySelectorAll('.chip-group').forEach(group => {
    const name = group.dataset.name;
    const hiddenInput = document.getElementById(`${name}_input`);
    group.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', () => {
        chip.classList.toggle('active');
        const active = Array.from(group.querySelectorAll('.chip.active')).map(c => c.dataset.value);
        if (hiddenInput) hiddenInput.value = active.join(', ');
      });
    });
  });
}

// ─── TOGGLES ──────────────────────────────────────────────
function initToggleGroups() {
  document.querySelectorAll('.toggle-group').forEach(group => {
    const name = group.dataset.name;
    const hiddenInput = document.getElementById(`${name}_input`);
    group.querySelectorAll('.tog').forEach(tog => {
      tog.addEventListener('click', () => {
        group.querySelectorAll('.tog').forEach(t => t.classList.remove('active'));
        tog.classList.add('active');
        if (hiddenInput) hiddenInput.value = tog.dataset.value;
      });
    });
  });
}

// ─── VAS ──────────────────────────────────────────────────
function initVAS() {
  const range   = document.getElementById('vasRange');
  const display = document.getElementById('vasValue');
  if (!range || !display) return;
  function updateColor(v) {
    display.textContent = v;
    if      (v <= 3) display.style.color = '#1a6b3c';
    else if (v <= 6) display.style.color = '#c17f24';
    else             display.style.color = '#9b1c2e';
  }
  range.addEventListener('input', () => updateColor(range.value));
  updateColor(range.value);
}

// ─── NÃO FEZ USO ──────────────────────────────────────────
function initNaoUsouToggles() {
  document.querySelectorAll('.tog-nao-usou').forEach(btn => {
    const targetId = btn.dataset.target;
    const inputId  = btn.dataset.inputid;
    const target   = document.getElementById(targetId);
    const hidden   = inputId ? document.getElementById(inputId) : null;
    btn.addEventListener('click', () => {
      const isActive = btn.classList.toggle('active');
      btn.textContent = isActive ? '✓ Não fez uso' : 'Não fez uso';
      if (hidden) hidden.value = isActive ? 'Não fez uso' : '';
      if (target) target.style.display = isActive ? 'none' : '';
    });
  });
}

// ─── COLETA DE DADOS DO FORMULÁRIO ────────────────────────
function collectFormData() {
  const form = document.getElementById('anamneseForm');
  const data = {};
  form.querySelectorAll('input:not([type=range]):not([type=hidden]), select, textarea').forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  data['vas'] = document.getElementById('vasRange').value;
  form.querySelectorAll('input[type=hidden]').forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  data['regioes_dor'] = document.getElementById('regioes_dor_input')?.value || '';
  Object.entries(muscleValues).forEach(([k,v])      => { data[`forca_${k.replace(/\s+/g,'_').toLowerCase()}`]             = v; });
  Object.entries(reflexValues).forEach(([k,v])      => { data[`reflexo_${k.replace(/\s+/g,'_').toLowerCase()}`]           = v; });
  Object.entries(testValues).forEach(([k,v])        => { data[`teste_${k.replace(/[\s()\/]+/g,'_').toLowerCase()}`]       = v; });
  Object.entries(sensitivityValues).forEach(([k,v]) => { data[`sens_${k.replace(/\s+/g,'_').toLowerCase()}`]              = v; });
  Object.entries(triggerValues).forEach(([k,v])     => { data[`gatilho_${k.replace(/\s+/g,'_').toLowerCase()}`]           = v; });
  return data;
}

// ─── PREENCHE FORMULÁRIO COM DADOS DE UM RASCUNHO ─────────
function preencherFormulario(data) {
  const form = document.getElementById('anamneseForm');
  // inputs normais
  Object.entries(data).forEach(([k, v]) => {
    const el = form.querySelector(`[name="${k}"]`);
    if (!el || el.type === 'hidden') return;
    el.value = v;
  });
  // VAS
  if (data.vas) {
    const r = document.getElementById('vasRange');
    if (r) { r.value = data.vas; r.dispatchEvent(new Event('input')); }
  }
  // hidden inputs
  Object.entries(data).forEach(([k, v]) => {
    const el = document.getElementById(`${k}_input`) || form.querySelector(`input[type=hidden][name="${k}"]`);
    if (el) el.value = v;
  });
  // chips
  document.querySelectorAll('.chip-group').forEach(group => {
    const name = group.dataset.name;
    const val  = data[name] || '';
    const vals = val.split(', ').map(s => s.trim()).filter(Boolean);
    group.querySelectorAll('.chip').forEach(chip => {
      chip.classList.toggle('active', vals.includes(chip.dataset.value));
    });
    const hi = document.getElementById(`${name}_input`);
    if (hi) hi.value = val;
  });
  // toggles
  document.querySelectorAll('.toggle-group').forEach(group => {
    const name = group.dataset.name;
    const val  = data[name] || '';
    group.querySelectorAll('.tog').forEach(t => {
      t.classList.toggle('active', t.dataset.value === val);
    });
    const hi = document.getElementById(`${name}_input`);
    if (hi) hi.value = val;
  });
  // mapa corporal
  if (data.regioes_dor) {
    const regioes = data.regioes_dor.split(', ').map(s => s.trim()).filter(Boolean);
    regioes.forEach(r => {
      _selectedRegions.add(r);
      document.querySelectorAll(`.body-zone[data-region="${r}"]`).forEach(z => z.classList.add('selected'));
    });
    _updateRegionTags();
  }
  // força muscular
  Object.entries(data).filter(([k]) => k.startsWith('forca_')).forEach(([k, v]) => {
    const muscle = k.replace('forca_','').replace(/_/g,' ');
    document.querySelectorAll(`.scale-btn[data-muscle]`).forEach(btn => {
      if (btn.dataset.muscle.toLowerCase().replace(/\s+/g,'_') === k.replace('forca_','')) {
        btn.classList.toggle('active', btn.dataset.val === v);
      }
    });
    muscleValues[muscle] = v;
  });
  // reflexos
  Object.entries(data).filter(([k]) => k.startsWith('reflexo_')).forEach(([k, v]) => {
    document.querySelectorAll(`.reflex-opt`).forEach(btn => {
      if (`reflexo_${btn.dataset.reflex.replace(/\s+/g,'_').toLowerCase()}` === k) {
        btn.classList.toggle('active', btn.dataset.val === v);
      }
    });
  });
  // testes
  Object.entries(data).filter(([k]) => k.startsWith('teste_')).forEach(([k, v]) => {
    document.querySelectorAll(`.test-opt`).forEach(btn => {
      if (`teste_${btn.dataset.test.replace(/[\s()\/]+/g,'_').toLowerCase()}` === k) {
        btn.classList.remove('active-pos','active-neg');
        if (v === 'Positivo') btn.classList.add('active-pos');
        else if (v === 'Negativo') btn.classList.add('active-neg');
      }
    });
  });
}

// ─── PAINEL HISTÓRICO ─────────────────────────────────────
function renderHistorico() {
  const body = document.getElementById('historicoBody');
  const list = getRascunhos();

  if (list.length === 0) {
    body.innerHTML = `
      <div class="historico-empty">
        <div class="empty-icon">📋</div>
        <p>Nenhuma anamnese salva ainda.<br>Preencha o formulário e clique em <strong>Salvar rascunho</strong>.</p>
      </div>`;
    return;
  }

  body.innerHTML = `<div class="historico-lista" id="listaRascunhos"></div>`;
  const lista = document.getElementById('listaRascunhos');

  list.forEach(item => {
    const card = document.createElement('div');
    card.className = 'rascunho-card';
    card.innerHTML = `
      <div class="rascunho-info">
        <div class="rascunho-nome">👤 ${item.nome}</div>
        <div class="rascunho-meta">
          <span>📅 ${item.data}</span>
          <span class="rascunho-vas">VAS ${item.vas}/10</span>
          <span>🕐 Salvo em ${item.savedAt}</span>
        </div>
      </div>
      <div class="rascunho-actions">
        <button type="button" class="btn-card btn-card-primary" data-id="${item.id}" data-action="editar">✏️ Editar</button>
        <button type="button" class="btn-card btn-card-danger"  data-id="${item.id}" data-action="deletar">🗑</button>
      </div>`;
    lista.appendChild(card);
  });

  lista.querySelectorAll('[data-action="editar"]').forEach(btn => {
    btn.addEventListener('click', () => abrirEdicao(btn.dataset.id));
  });
  lista.querySelectorAll('[data-action="deletar"]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (confirm('Excluir esta anamnese?')) {
        deletarRascunho(btn.dataset.id);
        renderHistorico();
      }
    });
  });
}

function abrirHistorico() {
  renderHistorico();
  document.getElementById('historicoModal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}
function fecharHistorico() {
  document.getElementById('historicoModal').style.display = 'none';
  document.body.style.overflow = '';
}

// ─── PAINEL EDIÇÃO ────────────────────────────────────────
const FIELD_LABELS = {
  nome:'Nome', data:'Data', estado_civil:'Estado civil', escolaridade:'Escolaridade',
  mora_em:'Mora em', trabalho:'Trabalho', alergias:'Alergias',
  antecedentes:'Antecedentes patológicos', muc:'MUC', cirurgias:'Cirurgias prévias',
  encaminhamento:'Encaminhamento', tempo_dor:'Tempo de dor', queixa:'Queixa principal',
  regioes_dor:'Regiões de dor',
  qualidade_dor:'Qualidade da dor', componente_emocional:'Componente emocional',
  vas:'VAS (0–10)', frequencia:'Frequência', predominio:'Predomínio', instalacao:'Instalação',
  fatores_melhora:'Fatores de melhora', fatores_piora:'Fatores de piora',
  tratamentos_anteriores:'Tratamentos anteriores', red_flags:'Red Flags',
  med_analgesico_naousou:'Analgésicos', med_analgesico_nome:'Analgésico — nome',
  med_analgesico_dose:'Analgésico — dose', med_analgesico_resp:'Resposta',
  med_analgesico_ec:'Efeitos colaterais', med_analgesico_outros:'Outros analgésicos',
  med_relaxante_naousou:'Relaxantes', med_relaxante_nome:'Relaxante — nome',
  med_relaxante_dose:'Relaxante — dose', med_relaxante_resp:'Resposta',
  med_relaxante_ec:'Efeitos colaterais', med_relaxante_outros:'Outros relaxantes',
  med_anticonv_naousou:'Anticonvulsivantes', med_anticonv_nome:'Anticonv — nome',
  med_anticonv_dose:'Anticonv — dose', med_anticonv_resp:'Resposta',
  med_anticonv_ec:'Efeitos colaterais', med_anticonv_outros:'Outros anticonvulsivantes',
  med_tricilico_naousou:'Tricíclicos', med_tricilico_nome:'Tricíclico — nome',
  med_tricilico_dose:'Dose', med_tricilico_resp:'Resposta',
  med_tricilico_ec:'Efeitos colaterais', med_tricilico_outros:'Outros tricíclicos',
  med_irsn_naousou:'IRSN/ISRS', med_irsn_nome:'IRSN — nome',
  med_irsn_dose:'Dose', med_irsn_resp:'Resposta',
  med_irsn_ec:'Efeitos colaterais', med_irsn_outros:'Outros IRSN/ISRS',
  med_antipsic_naousou:'Antipsicóticos', med_antipsic_nome:'Antipsicótico — nome',
  med_antipsic_dose:'Dose', med_antipsic_resp:'Resposta',
  med_antipsic_ec:'Efeitos colaterais', med_antipsic_outros:'Outros antipsicóticos',
  med_opioide_naousou:'Opioides', med_opioide_nome:'Opioide — nome',
  med_opioide_dose:'Dose/via/freq.', med_opioide_resgate:'Dose resgate',
  med_opioide_resp:'Resposta', med_opioide_depend:'Tolerância/Dependência',
  med_opioide_ec:'Efeitos colaterais', med_opioide_outros:'Outros opioides',
  medicamentos_dor_outros:'Outros medicamentos para dor',
  percepcao_sono:'Percepção do sono', horas_sono:'Horas/noite',
  med_sono:'Med. para dormir', caracteristicas_sono:'Características do sono',
  posicao_dormir:'Posição', travesseiro_aux:'Travesseiro auxiliar',
  altura_travesseiro:'Altura do travesseiro', colchao:'Colchão',
  cafe:'Café da manhã', almoco:'Almoço', jantar:'Jantar',
  intestino:'Hábito intestinal', atividade_fisica:'Atividade física', humor:'Humor',
  inspecao:'Inspeção geral', comportamentos_dolorosos:'Comportamentos dolorosos',
  marcha:'Marcha', marcha_desc:'Descrição marcha', equilibrio:'Equilíbrio',
  tonus:'Tônus', horner:'Horner', reflexos_superficiais:'Reflexos superficiais',
  exames_complementares:'Exames complementares',
  diag_musculo:'Musculoesquelético', diag_neuropatica:'Neuropático',
  diag_visceral:'Visceral/Pélvico', diag_cefaleia:'Cefaleia/Orofacial',
  diag_oncologica:'Oncológico/Misto', cid:'CID', classificacao_dor:'Classificação IASP',
  hipotese_diagnostica_livre:'Hipótese diagnóstica',
  conduta:'Conduta',
};

const LONG_FIELDS = new Set([
  'queixa','antecedentes','muc','cirurgias','fatores_melhora','fatores_piora',
  'inspecao','exames_complementares','hipotese_diagnostica_livre','conduta',
  'med_opioide_outros','medicamentos_dor_outros'
]);

const EDICAO_SECTIONS = [
  { title:'Identificação',     fields:['nome','data','estado_civil','escolaridade','mora_em','trabalho','alergias','antecedentes','muc','cirurgias'] },
  { title:'História',          fields:['encaminhamento','tempo_dor','queixa'] },
  { title:'Localização da Dor',fields:['regioes_dor'] },
  { title:'Caracterização',    fields:['qualidade_dor','componente_emocional','vas','frequencia','predominio','instalacao','fatores_melhora','fatores_piora','tratamentos_anteriores','red_flags'] },
  { title:'Medicamentos',      fields:['med_analgesico_naousou','med_analgesico_nome','med_analgesico_dose','med_analgesico_resp','med_analgesico_ec','med_analgesico_outros','med_relaxante_naousou','med_relaxante_nome','med_relaxante_dose','med_relaxante_resp','med_relaxante_ec','med_relaxante_outros','med_anticonv_naousou','med_anticonv_nome','med_anticonv_dose','med_anticonv_resp','med_anticonv_ec','med_anticonv_outros','med_tricilico_naousou','med_tricilico_nome','med_tricilico_dose','med_tricilico_resp','med_tricilico_ec','med_tricilico_outros','med_irsn_naousou','med_irsn_nome','med_irsn_dose','med_irsn_resp','med_irsn_ec','med_irsn_outros','med_antipsic_naousou','med_antipsic_nome','med_antipsic_dose','med_antipsic_resp','med_antipsic_ec','med_antipsic_outros','med_opioide_naousou','med_opioide_nome','med_opioide_dose','med_opioide_resgate','med_opioide_resp','med_opioide_depend','med_opioide_ec','med_opioide_outros','medicamentos_dor_outros'] },
  { title:'Sono',              fields:['percepcao_sono','horas_sono','med_sono','caracteristicas_sono','posicao_dormir','travesseiro_aux','altura_travesseiro','colchao'] },
  { title:'Hábitos',           fields:['cafe','almoco','jantar','intestino','atividade_fisica','humor'] },
  { title:'Exame Físico',      fields:['inspecao','comportamentos_dolorosos','marcha','marcha_desc','equilibrio','tonus','horner','reflexos_superficiais'] },
  { title:'Exames Complementares', fields:['exames_complementares'] },
  { title:'Hipótese Diagnóstica',  fields:['diag_musculo','diag_neuropatica','diag_visceral','diag_cefaleia','diag_oncologica','cid','classificacao_dor','hipotese_diagnostica_livre'] },
  { title:'Conduta',           fields:['conduta'] },
];

let edicaoData = {};

function abrirEdicao(id) {
  const list = getRascunhos();
  const item = list.find(r => r.id === id);
  if (!item) return;

  currentDraftId = id;
  edicaoData = { ...item.data_form };

  document.getElementById('edicaoTitulo').textContent = `Editando: ${item.nome}`;

  // Renderizar campos
  const body = document.getElementById('edicaoBody');
  body.innerHTML = '';

  EDICAO_SECTIONS.forEach(sec => {
    const hasContent = sec.fields.some(f => edicaoData[f] && String(edicaoData[f]).trim());
    if (!hasContent) return;

    const secEl = document.createElement('div');
    secEl.className = 'review-section';
    secEl.innerHTML = `<div class="review-section-title">${sec.title}</div>`;
    const grid = document.createElement('div');
    grid.className = 'review-grid';

    sec.fields.forEach(fieldName => {
      const val = edicaoData[fieldName];
      if (!val) return;
      const label  = FIELD_LABELS[fieldName] || fieldName;
      const isLong = LONG_FIELDS.has(fieldName);
      const fieldEl = document.createElement('div');
      fieldEl.className = `review-field${isLong ? ' full' : ''}`;
      const labelEl = document.createElement('label');
      labelEl.textContent = label;
      fieldEl.appendChild(labelEl);
      if (isLong) {
        const ta = document.createElement('textarea');
        ta.rows = 3; ta.value = val;
        ta.addEventListener('input', e => { edicaoData[fieldName] = e.target.value; });
        fieldEl.appendChild(ta);
      } else {
        const inp = document.createElement('input');
        inp.type = 'text'; inp.value = val;
        inp.addEventListener('input', e => { edicaoData[fieldName] = e.target.value; });
        fieldEl.appendChild(inp);
      }
      grid.appendChild(fieldEl);
    });

    // exame físico compacto
    if (sec.title === 'Exame Físico') {
      [['Força', 'forca_'],['Reflexos','reflexo_'],['Testes','teste_'],['Sensibilidade','sens_'],['Pontos-gatilho','gatilho_']].forEach(([title, prefix]) => {
        const items = Object.entries(edicaoData).filter(([k,v]) => k.startsWith(prefix) && v);
        if (!items.length) return;
        const sub = document.createElement('div');
        sub.style.cssText = 'grid-column:1/-1;margin-top:12px';
        sub.innerHTML = `<div style="font-size:10px;font-weight:700;text-transform:uppercase;color:var(--text-light);margin-bottom:6px">${title}</div>`;
        const tbl = document.createElement('div');
        tbl.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:5px';
        items.forEach(([k,v]) => {
          const nice = k.replace(prefix,'').replace(/_/g,' ');
          const r = document.createElement('div');
          r.style.cssText = 'display:flex;justify-content:space-between;background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:4px 10px;font-size:12px';
          r.innerHTML = `<span style="color:var(--text-mid)">${nice}</span><strong style="color:var(--accent)">${v}</strong>`;
          tbl.appendChild(r);
        });
        sub.appendChild(tbl);
        grid.appendChild(sub);
      });
    }

    secEl.appendChild(grid);
    body.appendChild(secEl);
  });

  // Mostrar painel de edição
  fecharHistorico();
  document.getElementById('edicaoModal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function fecharEdicao() {
  document.getElementById('edicaoModal').style.display = 'none';
  document.body.style.overflow = '';
  currentDraftId = null;
}

// ─── EVENTOS ──────────────────────────────────────────────

// Salvar rascunho
document.getElementById('btnSalvar').addEventListener('click', () => {
  const data = collectFormData();
  if (!data.nome && !data.queixa) {
    showStatus('⚠️ Preencha pelo menos o nome do paciente antes de salvar.', 'error');
    return;
  }
  const id = salvarRascunho(data);
  currentDraftId = id;
  showStatus(`✅ Rascunho salvo! Acesse o histórico para editar antes de gerar o prontuário.`, 'success');
});

// Abrir histórico
document.getElementById('btnHistorico').addEventListener('click', abrirHistorico);
document.getElementById('historicoClose').addEventListener('click', fecharHistorico);
document.getElementById('historicoOverlay').addEventListener('click', fecharHistorico);
document.getElementById('btnFecharHistorico').addEventListener('click', fecharHistorico);

// Edição — voltar ao histórico
document.getElementById('btnVoltarHistorico').addEventListener('click', () => {
  fecharEdicao();
  abrirHistorico();
});

// Edição — overlay fecha
document.getElementById('edicaoOverlay').addEventListener('click', fecharEdicao);
document.getElementById('edicaoClose').addEventListener('click', fecharEdicao);

// Salvar edição
document.getElementById('btnSalvarEdicao').addEventListener('click', () => {
  if (!currentDraftId) return;
  atualizarRascunho(currentDraftId, edicaoData);
  const statusEl = document.getElementById('edicao-status');
  statusEl.className = 'status-msg success';
  statusEl.textContent = '✅ Edição salva!';
  statusEl.style.display = 'block';
  setTimeout(() => { statusEl.style.display = 'none'; }, 2000);
});

// Gerar prontuário + enviar Sheets
document.getElementById('btnGerarProntuario').addEventListener('click', async () => {
  const btn      = document.getElementById('btnGerarProntuario');
  const statusEl = document.getElementById('edicao-status');
  btn.disabled   = true;
  btn.textContent = '⏳ Enviando...';
  statusEl.style.display = 'none';

  try {
    // 1. Salvar no Google Sheets
    const res = await fetch('/salvar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(edicaoData)
    });
    const result = await res.json();
    if (!res.ok || result.status !== 'ok') throw new Error(result.message || 'Erro ao salvar');

    // 2. Gerar PDF
    const pdfRes = await fetch('/gerar-pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(edicaoData)
    });
    if (pdfRes.ok) {
      const blob = await pdfRes.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      const nome    = (edicaoData.nome || 'paciente').replace(/\s+/g,'_');
      const dataStr = edicaoData.data || new Date().toISOString().split('T')[0];
      a.download = `anamnese_${nome}_${dataStr}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    }

    statusEl.className  = 'status-msg success';
    statusEl.textContent = `✅ Salvo na linha ${result.row}! PDF baixando...`;
    statusEl.style.display = 'block';
    btn.textContent = '✅ Enviado!';

    // Remover do histórico após envio
    if (currentDraftId) deletarRascunho(currentDraftId);

    setTimeout(() => {
      fecharEdicao();
      showStatus(`✅ Prontuário gerado e enviado ao Google Sheets — ${new Date().toLocaleString('pt-BR')}`, 'success');
    }, 2500);

  } catch (err) {
    statusEl.className   = 'status-msg error';
    statusEl.textContent = `❌ Erro: ${err.message}`;
    statusEl.style.display = 'block';
    btn.disabled    = false;
    btn.textContent = '📄 Gerar Prontuário + Enviar Sheets';
  }
});

// ─── HELPER STATUS ────────────────────────────────────────
function showStatus(msg, type) {
  const el = document.getElementById('status-msg');
  el.className   = `status-msg ${type}`;
  el.textContent = msg;
  el.scrollIntoView({ behavior:'smooth', block:'nearest' });
}

// ─── INIT ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initBodyMap();
  initChipGroups();
  initToggleGroups();
  initVAS();
  buildMuscleSection('muscle-sup', MUSCULOS_SUP);
  buildMuscleSection('muscle-inf', MUSCULOS_INF);
  buildReflexSection();
  buildTestsSection();
  buildSensibilidadeSection();
  buildGatilhoSection();
  initNaoUsouToggles();
});
