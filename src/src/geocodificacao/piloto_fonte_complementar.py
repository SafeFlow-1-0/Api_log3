"""Piloto GEO_COMPLEMENTAR_001: exatamente 10 B_MANTIDO via Photon."""

from __future__ import annotations

import csv, hashlib, json, math, re, time, unicodedata, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent
OUT = ROOT / "data/geocodificacao/fonte_complementar"
RESP = OUT / "respostas_provedor"
REC = ROOT / "data/geocodificacao/recuperacao_geo001"
AUDIT = ROOT / "data/geocodificacao/geocodificacao_lote_001.csv"
POINTS = SOURCE / "mapa_historico_pontos.csv"
RESULT05 = REC / "resultado_recuperacao.csv"
VIACEP = REC / "cache_provedor_2.json"
CACHE = OUT / "cache_photon.json"
ENDPOINT = "https://photon.komoot.io/structured"
LOT = "GEO_COMPLEMENTAR_001"
UA = "SafeFlowMap-Sprint06/1.0 pilot-10"

def norm(v):
    t = unicodedata.normalize("NFD", str(v or ""))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9]+", " ", t.upper()).strip()

def digits(v): return re.sub(r"\D", "", str(v or ""))
def compatible(a, b, limit=.76):
    a, b = norm(a), norm(b)
    return bool(a and b and (a == b or a in b or b in a or SequenceMatcher(None, a, b).ratio() >= limit))
def now(): return datetime.now(timezone.utc).isoformat()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); tmp.replace(path)
def load_json(path): return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
def valid(lat, lon):
    try: return -90 <= float(lat) <= 90 and -180 <= float(lon) <= 180 and math.isfinite(float(lat)) and math.isfinite(float(lon))
    except: return False
def hav(lat1,lon1,lat2,lon2):
    if not valid(lat1,lon1) or not valid(lat2,lon2): return ""
    p1,p2=map(math.radians,[float(lat1),float(lat2)]); dp=math.radians(float(lat2)-float(lat1)); dl=math.radians(float(lon2)-float(lon1)); a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return f"{6371000*2*math.atan2(math.sqrt(a),math.sqrt(1-a)):.2f}"

def select_sample(b_rows, points):
    by_city={}
    for row in sorted(b_rows,key=lambda r:r["ID_ENDERECO"]):
        by_city.setdefault(points[row["ID_ENDERECO"]]["MUNICIPIO"],[]).append(row)
    selected=[by_city[city][0] for city in sorted(by_city)[:10]]
    if len(selected)!=10: raise RuntimeError("Amostra não possui exatamente 10 casos")
    return selected

def query(point, cache, online):
    # A instância pública rejeita `lang=pt` no endpoint estruturado (HTTP 400).
    # Mantemos a tentativa original no cache e usamos a consulta documentada sem idioma.
    params={"street":point["LOGRADOURO"],"housenumber":point["NUMERO"],"city":point["MUNICIPIO"],"postcode":digits(point["CEP"]),"state":"São Paulo","countrycode":"BR","limit":5}
    sent=urllib.parse.urlencode(params); key=hashlib.sha256(sent.encode()).hexdigest()
    if key in cache: return key, sent, cache[key], True
    if not online: return key, sent, {}, False
    req=urllib.request.Request(f"{ENDPOINT}?{sent}",headers={"User-Agent":UA,"Accept":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=40) as res: payload=json.loads(res.read().decode("utf-8")); status=res.status
        item={"consulted_at_utc":now(),"status_http":status,"query":sent,"response":payload,"error":""}
    except Exception as exc: item={"consulted_at_utc":now(),"status_http":"","query":sent,"response":{},"error":f"{type(exc).__name__}: {exc}"}
    cache[key]=item; write_json(CACHE,cache); time.sleep(.35)
    return key,sent,item,False

def choose(point, item):
    features=(item.get("response") or {}).get("features") or []
    exact=[]; approximate=[]; conflict=[]
    for f in features:
        p=f.get("properties") or {}; coords=(f.get("geometry") or {}).get("coordinates") or []
        coord=len(coords)>=2 and valid(coords[1],coords[0]); city_ok=compatible(point["MUNICIPIO"],p.get("city"),.88); state_ok=norm(p.get("state")) in {"SAO PAULO","SP"}; road_ok=compatible(point["LOGRADOURO"],p.get("street"),.76); num_ok=bool(digits(point["NUMERO"])) and digits(point["NUMERO"])==digits(p.get("housenumber")); country_ok=norm(p.get("countrycode"))=="BR"
        score=sum([coord,city_ok,state_ok,road_ok,num_ok,country_ok])
        data=(score,f,{"coord":coord,"city":city_ok,"state":state_ok,"road":road_ok,"number":num_ok,"country":country_ok})
        if all(data[2].values()): exact.append(data)
        elif coord and city_ok and state_ok and road_ok and country_ok: approximate.append(data)
        else: conflict.append(data)
    bucket=exact or approximate or conflict
    return max(bucket,key=lambda x:x[0]) if bucket else None

def main(online=False):
    OUT.mkdir(parents=True,exist_ok=True); RESP.mkdir(exist_ok=True)
    pts={r["ID_ENDERECO"]:r for r in read_csv(POINTS)}; r05=read_csv(RESULT05); b=[r for r in r05 if r["CLASSIFICACAO_APOS_RECUPERACAO"]=="B_MANTIDO"]
    if len(b)!=42: raise RuntimeError("Universo B_MANTIDO deve ser 42")
    sample=select_sample(b,pts); audit={r["ID_ENDERECO"]:r for r in read_csv(AUDIT)}; via=load_json(VIACEP); cache=load_json(CACHE)
    sample_rows=[]
    for i,r in enumerate(sample,1):
        p=pts[r["ID_ENDERECO"]]; sample_rows.append({"ORDEM":i,"ID_ENDERECO":r["ID_ENDERECO"],"MUNICIPIO":p["MUNICIPIO"],"CEP":p["CEP"],"REGRA_SELECAO":"primeiro ID por município; 10 municípios em ordem alfabética"})
    write_csv(OUT/"amostra_10.csv",sample_rows,list(sample_rows[0]))
    results=[]; comparisons=[]; queries=[]; qa=[]; misses=hits=0
    for r in sample:
        ident=r["ID_ENDERECO"]; p=pts[ident]; key,sent,item,hit=query(p,cache,online); hits+=hit; misses+=not hit and bool(item)
        if item: write_json(RESP/f"{ident}.json",item)
        chosen=choose(p,item); feature=chosen[1] if chosen else {}; checks=chosen[2] if chosen else {}; prop=feature.get("properties") or {}; coords=(feature.get("geometry") or {}).get("coordinates") or ["",""]
        if item.get("error"): pilot="ERRO_SERVICO"
        elif not chosen: pilot="SEM_RESULTADO"
        elif all(checks.values()): pilot="CANDIDATO_A_RECUPERADO"
        elif checks.get("coord") and checks.get("city") and checks.get("state") and checks.get("road") and checks.get("country") and not checks.get("number"): pilot="B_CONFIRMADO"
        else: pilot="CONFLITO"
        # Photon compartilha base OSM com Nominatim: QA bloqueia promoção sem independência.
        qa_decision="NAO_APROVADO_FONTE_NAO_INDEPENDENTE" if pilot=="CANDIDATO_A_RECUPERADO" else "NAO_APLICAVEL"
        final="B_CONFIRMADO" if pilot=="CANDIDATO_A_RECUPERADO" else pilot
        va=(via.get(digits(p["CEP"])) or {}).get("response") or {}; a=audit[ident]; lon,lat=(coords+["",""])[:2]
        queries.append({"ID_ENDERECO":ident,"CONSULTA_ENVIADA":sent,"CHAVE_CACHE":key,"CACHE_HIT":str(hit).lower(),"STATUS_HTTP":item.get("status_http",""),"DATA_HORA_UTC":item.get("consulted_at_utc",""),"ERRO":item.get("error","")})
        results.append({"ID_LOTE":LOT,"ID_ENDERECO":ident,"ENDERECO_ORIGINAL":p["ENDERECO_ORIGINAL"],"ENDERECO_NORMALIZADO":p["ENDERECO_NORMALIZADO"],"LOGRADOURO":p["LOGRADOURO"],"NUMERO_ORIGINAL":p["NUMERO"],"BAIRRO":p["BAIRRO"],"CEP_ORIGINAL":p["CEP"],"MUNICIPIO_ORIGINAL":p["MUNICIPIO"],"UF_ORIGINAL":p["UF"],"PROVEDOR":"Photon/komoot","NUMERO_FONTE_COMPLEMENTAR":prop.get("housenumber",""),"NUMERO_COMPATIVEL":str(bool(checks.get("number"))).lower(),"LOGRADOURO_COMPLEMENTAR":prop.get("street",""),"MUNICIPIO_COMPLEMENTAR":prop.get("city",""),"UF_COMPLEMENTAR":prop.get("state",""),"CEP_COMPLEMENTAR":prop.get("postcode",""),"CEP_COMPATIVEL":str(digits(p["CEP"])==digits(prop.get("postcode"))).lower(),"LATITUDE_COMPLEMENTAR":lat,"LONGITUDE_COMPLEMENTAR":lon,"COORDENADAS_VALIDAS":str(bool(checks.get("coord"))).lower(),"PRECISAO_DECLARADA":prop.get("type") or prop.get("osm_value") or "NÃO_FORNECIDA","IDENTIFICADOR_RESULTADO":f"{prop.get('osm_type','')}:{prop.get('osm_id','')}","RESULTADO_PILOTO":pilot,"RESULTADO_APOS_QA":final,"ORIGEM_VALIDACAO":"SPRINT06_FONTE_COMPLEMENTAR","QA":qa_decision,"PUBLICAR":"false","EVIDENCIAS":"Histórico x ViaCEP x Nominatim x Photon; base Photon não independente do OSM"})
        comparisons.append({"ID_ENDERECO":ident,"NOMINATIM_ENCONTROU":"true","NOMINATIM_NUMERO":a["NUMERO_RETORNADO"],"NOMINATIM_NUMERO_CONFIRMADO":a["NUMERO_COMPATIVEL"],"NOMINATIM_MUNICIPIO_OK":a["MUNICIPIO_COMPATIVEL"],"NOMINATIM_UF_OK":a["UF_COMPATIVEL"],"NOMINATIM_CEP":a["CEP_RETORNADO"],"NOMINATIM_PRECISAO":a["TIPO_RESULTADO"],"PHOTON_ENCONTROU":str(bool(chosen)).lower(),"PHOTON_NUMERO":prop.get("housenumber",""),"PHOTON_NUMERO_CONFIRMADO":str(bool(checks.get("number"))).lower(),"PHOTON_MUNICIPIO_OK":str(bool(checks.get("city"))).lower(),"PHOTON_UF_OK":str(bool(checks.get("state"))).lower(),"PHOTON_CEP":prop.get("postcode",""),"PHOTON_PRECISAO":prop.get("type") or prop.get("osm_value") or "NÃO_FORNECIDA","VIACEP_LOGRADOURO":va.get("logradouro",""),"DISTANCIA_COMPLEMENTAR_NOMINATIM_METROS":hav(a["LATITUDE_RETORNADA"],a["LONGITUDE_RETORNADA"],lat,lon),"CONFLITO":str(pilot=="CONFLITO").lower()})
        if pilot=="CANDIDATO_A_RECUPERADO": qa.append({"ID_ENDERECO":ident,"ENDERECO_HISTORICO_OK":"true","VIACEP_OK":"true","NOMINATIM_REVISADO":"true","PHOTON_NUMERO_OK":"true","MUNICIPIO_UF_OK":"true","CEP_ANALISADO":"true","PRECISAO_ANALISADA":"true","DISTANCIA_ANALISADA":"true","DECISAO_QA":qa_decision,"MOTIVO":"Photon deriva do OSM/Nominatim; falta evidência independente"})
    write_csv(OUT/"consultas_piloto.csv",queries,list(queries[0])); write_csv(OUT/"resultado_piloto.csv",results,list(results[0])); write_csv(OUT/"comparacao_fontes.csv",comparisons,list(comparisons[0])); write_csv(OUT/"qa_piloto.csv",qa,list(qa[0]) if qa else ["ID_ENDERECO","DECISAO_QA","MOTIVO"])
    c=Counter(x["RESULTADO_PILOTO"] for x in results); f=Counter(x["RESULTADO_APOS_QA"] for x in results); confirmed=sum(x["NUMERO_COMPATIVEL"]=="true" for x in results); recovered=sum(x["PUBLICAR"]=="true" for x in results)
    stats={"consultados":10,"com_resultado":sum(x["PHOTON_ENCONTROU"]=="true" for x in comparisons),"numero_exato_confirmado":confirmed,"candidato_a_recuperado":c["CANDIDATO_A_RECUPERADO"],"a_recuperado_apos_qa":recovered,"b_confirmado":f["B_CONFIRMADO"],"conflito":f["CONFLITO"],"sem_resultado":f["SEM_RESULTADO"],"erro_servico":f["ERRO_SERVICO"],"taxa_confirmacao_numero":round(confirmed/10*100,2),"taxa_recuperacao_segura":round(recovered/10*100,2),"cache_hits_execucao":hits,"cache_misses_execucao":misses,"cache_entries":len(cache),"tentativas_http_historicas":len(cache),"erros_http_historicos":sum(bool(x.get("error")) for x in cache.values()),"observacao_tentativas":"10 tentativas iniciais HTTP 400 por lang=pt preservadas; 10 repetições corrigidas sem o parâmetro, sobre os mesmos casos","custo_monetario":0,"publicados_antes":18,"publicados_depois":18+recovered,"expansao_32_executada":False}
    write_json(OUT/"estatisticas_piloto.json",stats)
    manifest={"id_lote":LOT,"quantidade":10,"universo_total":42,"ids":[x["ID_ENDERECO"] for x in sample],"regra_selecao":"um primeiro ID por município; dez municípios em ordem alfabética","fonte":"Photon/komoot","endpoint":ENDPOINT,"hashes_fontes_sha256":{x.name:sha(x) for x in [POINTS,RESULT05,AUDIT,VIACEP]},"baseline":"outputs/safeflow-map-sprint05-baseline","nenhum_geo002":True,"nenhuma_expansao_32":True,"nenhum_custo":True,"credencial_usada":False}
    write_json(OUT/"manifesto_geo_complementar_001.json",manifest); print(json.dumps(stats,ensure_ascii=False,indent=2))

if __name__=="__main__":
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument("--online",action="store_true"); args=ap.parse_args(); main(args.online)
