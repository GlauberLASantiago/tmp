import pathlib,argparse,json,struct,zlib
from route_fscommands import route_movie,sha
from patch_audio import patch_audio
def tag_leaves(raw):
 b=raw[:8]+zlib.decompress(raw[8:]) if raw[:3]==b'CWS' else raw;assert len(b)==struct.unpack_from('<I',b,4)[0];rootstart=8+(5+4*(b[8]>>3)+7)//8+4;leaves=[]
 def walk(b,p,where):
  ix=0
  while p+2<=len(b):
   h=struct.unpack_from('<H',b,p)[0];p+=2;t=h>>6;n=h&63
   if n==63:n=struct.unpack_from('<I',b,p)[0];p+=4
   d=b[p:p+n];p+=n;assert len(d)==n;loc=where+f'/{ix}';ix+=1
   if t==39:walk(d,4,loc)
   else:leaves.append((loc,t,d))
   if t==0:assert n==0 and p==len(b);return
  raise AssertionError('Missing End')
 walk(b,rootstart,'root');return b[8:rootstart],leaves
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('source',type=pathlib.Path);parser.add_argument('final',type=pathlib.Path);parser.add_argument('--report',type=pathlib.Path);args=parser.parse_args();paths=list(args.final.glob('*.swf'));mapping={p.name.lower():p.name for p in paths};records=[]
 for target in paths:
  original=args.source/target.name
  # Piano is unchanged and may be kept only once when originals contain the 26 routed movies.
  if not original.exists():assert target.name=='PianoMelhor.swf';original=target
  raw=original.read_bytes();expected,route_evidence=route_movie(raw,target.name,mapping);audio_evidence=None
  if target.name=='ArtiAcent.swf':expected,audio_evidence=patch_audio(expected)
  actual=target.read_bytes();assert actual==expected, f'Unexpected bytes in {target.name}'
  oh,ol=tag_leaves(raw);fh,fl=tag_leaves(actual);assert oh==fh;assert [(loc,t) for loc,t,d in ol]==[(loc,t) for loc,t,d in fl]
  unchanged_nonactions=0;audio=0
  for (loc,t,d),(loc2,t2,fd) in zip(ol,fl):
   if t not in (12,34,59):assert d==fd,(target.name,loc,t);unchanged_nonactions+=1
   if t==14:audio+=1;assert d==fd
  records.append({'file':target.name,'original_sha256':sha(raw),'final_sha256':sha(actual),'exact_expected_routes_and_single_audio_fix':True,'original_stage_header_preserved':True,'non_action_tag_payloads_byte_exact':unchanged_nonactions,'DefineSound_payloads_byte_exact':audio,'route_changes':len(route_evidence['changes']),'audio_symbol_fix':audio_evidence is not None})
 result={'files':len(records),'checks':records};assert len(records)==27
 if args.report:args.report.write_text(json.dumps(result,indent=2),encoding='utf8')
 print(json.dumps({'files':len(records),'route_actions':sum(r['route_changes'] for r in records),'sound_payloads':sum(r['DefineSound_payloads_byte_exact'] for r in records),'passed':True},indent=2))
