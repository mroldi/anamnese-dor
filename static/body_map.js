// ══════════════════════════════════════════════════════════
// BODY MAP — Mapa interativo de dor
// ══════════════════════════════════════════════════════════

const _selectedRegions = new Set();

function initBodyMap() {
  document.querySelectorAll('.body-zone').forEach(zone => {
    const region = zone.getAttribute('data-region');
    zone.setAttribute('title', region);
    zone.addEventListener('click', () => {
      if (_selectedRegions.has(region)) {
        _selectedRegions.delete(region);
        // deseleciona todos os SVG com esse data-region (frente e costas)
        document.querySelectorAll(`.body-zone[data-region="${region}"]`).forEach(z => z.classList.remove('selected'));
      } else {
        _selectedRegions.add(region);
        document.querySelectorAll(`.body-zone[data-region="${region}"]`).forEach(z => z.classList.add('selected'));
      }
      _updateRegionTags();
    });
  });
}

function _updateRegionTags() {
  const container = document.getElementById('selected-tags');
  const input = document.getElementById('regioes_dor_input');
  if (!container) return;

  if (_selectedRegions.size === 0) {
    container.innerHTML = '<span class="no-region">Nenhuma região selecionada</span>';
    if (input) input.value = '';
    return;
  }

  container.innerHTML = '';
  _selectedRegions.forEach(region => {
    const tag = document.createElement('span');
    tag.className = 'region-tag';
    // escape region name for use in onclick
    const escaped = region.replace(/'/g, "\\'");
    tag.innerHTML = `${region} <button type="button" onclick="_removeRegion('${escaped}')" title="Remover">×</button>`;
    container.appendChild(tag);
  });

  if (input) input.value = Array.from(_selectedRegions).join(', ');
}

function _removeRegion(region) {
  _selectedRegions.delete(region);
  document.querySelectorAll(`.body-zone[data-region="${region}"]`).forEach(z => z.classList.remove('selected'));
  _updateRegionTags();
}
