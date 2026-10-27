from __future__ import annotations

import argparse, csv, hashlib, json, math, os, statistics, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; GEO=DATA/'geografia'
QUEUE=GEO/'fila_roteamento_sede.csv'; RESULT=GEO/'sede_para_locais.csv'; CACHE=GEO/'cache_tomtom_routing.json'; CHECKPOINT=GEO/'checkpoint_roteamento.json'; AUDIT=GEO/'auditoria_roteamento.csv'; QA=GEO/'qa_roteamento.csv'; STATS=GEO/'estatisticas_roteamento.json'
LAT0,LON0=-23.1800797,-45.8808507; QPS=2; INTERVAL=0.5; RETRIES=3; BACKOFF=[2,5,15]

def hav(lat1,lon1,lat2,lon2):
 r=6371.0088;p1,p2=math.radians(lat1),math.radians(lat2);dp=math.radians(lat2-lat1);dl=math.radians(lon2-lon1);a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return r*2*math.atan2(math.sqrt(a),math.sqrt(1-a))
def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(p,rows,fields):
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def key():
 return os.environ.get('SAFEFLOW_TOMTOM_API_KEY') or os.environ.get(r'SAFEFLOW\_TOMTOM\_API\_KEY') or ''
def route(api_key,lat,lon):
 loc=f'{LAT0},{LON0}:{lat},{lon}'
 params=urllib.parse.urlencode({'key':api_key,'travelMode':'car','traffic':'false','routeType':'fastest','computeTravelTimeFor':'all','routeRepresentation':'summaryOnly'})
 url=f'https://api.tomtom.com/routing/1/calculateRoute/{loc}/json?{params}'
 req=urllib.request.Request(url,headers={'User-Agent':'SafeFlow-Sprint11/1.0'})
 with urllib.request.urlopen(req,timeout=30) as resp:data=json.load(resp)
 summary=data['routes'][0]['summary']; seconds=summary.get('noTrafficTravelTimeInSeconds',summary['travelTimeInSeconds'])
 return round(summary['lengthInMeters']/1000,3),round(seconds/60,2)
def save_checkpoint(processed,total,calls,retries,errors):
 CHECKPOINT.write_text(json.dumps({'processados':processed,'total':total,'chamadas_reais':calls,'retries':retries,'erros':errors,'atualizado_utc':datetime.now(timezone.utc).isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');ap.add_argument('--confirmed-quota',type=int,default=0);args=ap.parse_args()
 api_key=key().strip(); queue=read_csv(QUEUE); cache=json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}; existing={r['ID_ENDERECO']:r for r in read_csv(RESULT)} if RESULT.exists() else {}
 if not args.execute: print(json.dumps({'fila':len(queue),'cache':len(cache),'concluidos':len(existing)},ensure_ascii=False));return
 if not api_key: raise SystemExit('BLOQUEADO: chave TomTom ausente')
 needed=sum(r['ID_ENDERECO'] not in existing or existing[r['ID_ENDERECO']]['STATUS']!='CALCULADO' for r in queue)
 if args.confirmed_quota < needed: raise SystemExit(f'BLOQUEADO: cota confirmada {args.confirmed_quota} menor que chamadas necessárias {needed}')
 calls=retry_count=error_count=0; audit=[]; fields=['ID_RELACAO','ID_ORIGEM','ID_ENDERECO','LAT_ORIGEM','LON_ORIGEM','LAT_DESTINO','LON_DESTINO','MUNICIPIO','DISTANCIA_RETA_KM','DISTANCIA_RODOVIARIA_KM','TEMPO_ESTIMADO_MIN','FATOR_RODOVIARIO','PROVEDOR','PERFIL','TIPO_TEMPO','DATA_CALCULO_UTC','STATUS','ERRO','CACHE_KEY','QA_STATUS']
 for idx,q in enumerate(queue,1):
  ident=q['ID_ENDERECO']; lat,lon=float(q['LAT']),float(q['LON']); ck=q['CACHE_KEY']
  if ident in existing and existing[ident]['STATUS']=='CALCULADO': continue
  straight=round(hav(LAT0,LON0,lat,lon),3); road=duration='';status='PENDENTE';err='';source='CHAMADA'
  if ck in cache: road=cache[ck]['distancia_rodoviaria_km'];duration=cache[ck]['tempo_estimado_min'];status='CALCULADO';source='CACHE'
  else:
   for attempt in range(RETRIES+1):
    try:
     road,duration=route(api_key,lat,lon);calls+=1;status='CALCULADO';cache[ck]={'distancia_rodoviaria_km':road,'tempo_estimado_min':duration,'data_calculo_utc':datetime.now(timezone.utc).isoformat(),'provedor':'TOMTOM_ROUTING_API','perfil':'CARRO'};CACHE.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8');break
    except urllib.error.HTTPError as e:
     calls+=1;err=f'HTTP_{e.code}'; transient=e.code in (408,429,500,502,503,504)
     if e.code==429: save_checkpoint(idx-1,len(queue),calls,retry_count,error_count); raise SystemExit('BLOQUEADO_HTTP_429')
     if transient and attempt<RETRIES: retry_count+=1;time.sleep(BACKOFF[attempt]);continue
     status='SEM_ROTA' if e.code in (400,404) else 'ERRO_PROVEDOR';error_count+=1;break
    except Exception as e:
     err=f'{type(e).__name__}: {str(e)[:160]}'
     if attempt<RETRIES:retry_count+=1;time.sleep(BACKOFF[attempt]);continue
     status='ERRO_PROVEDOR';error_count+=1;break
   time.sleep(INTERVAL)
  factor=round(float(road)/straight,3) if status=='CALCULADO' and straight>0 else ''
  qa='REVISAR' if status=='CALCULADO' and (float(road)<=0 or float(duration)<=0 or float(road)<straight*.85 or factor>3) else ('OK' if status=='CALCULADO' else 'INCOMPLETO')
  row={'ID_RELACAO':f'SEDE_001__{ident}','ID_ORIGEM':'SEDE_001','ID_ENDERECO':ident,'LAT_ORIGEM':LAT0,'LON_ORIGEM':LON0,'LAT_DESTINO':lat,'LON_DESTINO':lon,'MUNICIPIO':q['MUNICIPIO'],'DISTANCIA_RETA_KM':straight,'DISTANCIA_RODOVIARIA_KM':road,'TEMPO_ESTIMADO_MIN':duration,'FATOR_RODOVIARIO':factor,'PROVEDOR':'TOMTOM_ROUTING_API','PERFIL':'CARRO','TIPO_TEMPO':'NO_TRAFFIC_TRAVEL_TIME_CURRENT_GRAPH','DATA_CALCULO_UTC':cache.get(ck,{}).get('data_calculo_utc',datetime.now(timezone.utc).isoformat()),'STATUS':status,'ERRO':err,'CACHE_KEY':ck,'QA_STATUS':qa}
  existing[ident]=row;audit.append({'ID_ENDERECO':ident,'FONTE':source,'STATUS':status,'TENTATIVAS':attempt+1 if source=='CHAMADA' else 0,'ERRO':err})
  ordered=[existing[x['ID_ENDERECO']] for x in queue if x['ID_ENDERECO'] in existing];write_csv(RESULT,ordered,fields);save_checkpoint(len(ordered),len(queue),calls,retry_count,error_count)
  if idx%50==0 or idx==len(queue): print(f'Processados: {idx}/{len(queue)} | Calculados: {sum(r["STATUS"]=="CALCULADO" for r in ordered)} | Erros: {error_count} | Chamadas: {calls}',flush=True)
 rows=[existing[x['ID_ENDERECO']] for x in queue if x['ID_ENDERECO'] in existing]; write_csv(AUDIT,audit,['ID_ENDERECO','FONTE','STATUS','TENTATIVAS','ERRO']); qa_rows=[r for r in rows if r['QA_STATUS']!='OK'];write_csv(QA,qa_rows,fields)
 calc=[r for r in rows if r['STATUS']=='CALCULADO']
 def metrics(field):
  v=sorted(float(r[field]) for r in calc);return {'MIN':min(v),'MEDIANA':round(statistics.median(v),3),'MEDIA':round(statistics.mean(v),3),'P90':v[math.ceil(.9*len(v))-1],'MAX':max(v)} if v else {}
 stats={'TOTAL_PONTOS':1583,'TOTAL_CALCULADO':len(calc),'TOTAL_SEM_ROTA':sum(r['STATUS']=='SEM_ROTA' for r in rows),'TOTAL_ERROS':sum(r['STATUS']=='ERRO_PROVEDOR' for r in rows),'TOTAL_PENDENTE':1583-len(rows),'COBERTURA_PCT':round(100*len(calc)/1583,3),'DIST_RETA':metrics('DISTANCIA_RETA_KM'),'DIST_RODOVIARIA':metrics('DISTANCIA_RODOVIARIA_KM'),'TEMPO':metrics('TEMPO_ESTIMADO_MIN'),'CACHE_HITS':sum(a['FONTE']=='CACHE' for a in audit),'CHAMADAS_REAIS':calls,'RETRIES':retry_count,'QA_REVISAR':sum(r['QA_STATUS']=='REVISAR' for r in rows),'QPS_CONFIGURADO':QPS}
 STATS.write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
