(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.SafeFlowFilters = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  function normalize(value) { return String(value ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim(); }
  function haversineKm(origin, destination) { const toRad = (degrees) => (degrees * Math.PI) / 180; const radius = 6371.0088; const dLat = toRad(destination.lat - origin.lat); const dLon = toRad(destination.lon - origin.lon); const lat1 = toRad(origin.lat); const lat2 = toRad(destination.lat); const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2; return 2 * radius * Math.asin(Math.sqrt(a)); }
  function includesNormalized(values, expected) { return !expected || (values || []).some((item) => normalize(item) === normalize(expected)); }
  function dateMatches(dates, start, end) { return (!start && !end) || (dates || []).some((date) => (!start || date >= start) && (!end || date <= end)); }
  function searchMatches(properties, term) { if (!term) return true; const haystack = [properties.id_endereco, properties.endereco, ...(properties.estabelecimentos || [])].map(normalize).join(" | "); return normalize(term).split(/\s+/).filter(Boolean).every((token) => haystack.includes(token)); }
  function fiscalYearRows(data, year, group) {
    return (data?.status === "VERIFICADO" ? data.por_fiscal_ano : []).filter(r => (!year || String(r.ano) === String(year)) && (!group || (group === "um" ? r.apenas_um_dia : !r.apenas_um_dia)));
  }
  function individualMatches(feature, filters, data) {
    if (!filters.anoFiscal && !filters.grupoFiscal) return true;
    if (data?.status !== "VERIFICADO") return false;
    const eligible = fiscalYearRows(data, filters.anoFiscal, filters.grupoFiscal);
    return (data.por_id_endereco[feature.properties.id_endereco] || []).some(pair =>
      (!filters.fiscal || normalize(pair.fiscal) === normalize(filters.fiscal)) &&
      (!filters.dataInicial || pair.data >= filters.dataInicial) && (!filters.dataFinal || pair.data <= filters.dataFinal) &&
      eligible.some(row => row.fiscal === pair.fiscal && String(row.ano) === pair.data.slice(0, 4)));
  }
  function municipalityMask(feature) {
    const polygons = feature.geometry.type === "Polygon" ? [feature.geometry.coordinates] : feature.geometry.coordinates;
    // Even-odd fill: municipality exteriors cut holes; interior holes remain dimmed.
    return { type: "Feature", properties: {}, geometry: { type: "Polygon", coordinates: [
      [[-180,-85],[180,-85],[180,85],[-180,85],[-180,-85]], ...polygons.flatMap(polygon => polygon)
    ] } };
  }
  function matchesFeature(feature, filters, sedeCoordinates) { const p = feature.properties; if (!includesNormalized(p.fiscais, filters.fiscal)) return false; if (!includesNormalized(p.motoristas, filters.motorista)) return false; if (filters.municipio && normalize(p.municipio) !== normalize(filters.municipio)) return false; if (!dateMatches(p.datas_historicas, filters.dataInicial, filters.dataFinal)) return false; if (!searchMatches(p, filters.busca)) return false; if (filters.raioSede) { if (!sedeCoordinates) return false; const [lon, lat] = feature.geometry.coordinates; if (haversineKm(sedeCoordinates, { lat, lon }) > Number(filters.raioSede)) return false; } return true; }
  function filterFeatures(features, filters, sedeCoordinates) { return features.filter((feature) => matchesFeature(feature, filters, sedeCoordinates)); }
  function markerState(filters) { if (filters.busca) return "search"; if (filters.fiscal) return "fiscal"; if (filters.motorista || filters.municipio || filters.dataInicial || filters.dataFinal || filters.raioSede) return "filtered"; return "general"; }
  return { normalize, haversineKm, dateMatches, searchMatches, matchesFeature, filterFeatures, markerState, fiscalYearRows, individualMatches, municipalityMask };
});
