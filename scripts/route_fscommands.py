import pathlib,struct,zlib,json,hashlib,argparse
OUT=pathlib.Path(__file__).resolve().parent;SRC=OUT/'Dados';DEST=OUT/'web-routed'
sha=lambda b:hashlib.sha256(b).hexdigest();files={};manifest=[]
def rectend(b,p):return p+(5+4*(b[p]>>3)+7)//8
def cstring(b,p):q=b.index(0,p);return b[p:q],q+1
def patch_actions(b,where,changes):
 p=0;output=[];ops=[];local=[]
 while p<len(b):
  at=p;op=b[p];p+=1;ops.append(op)
  if not op:output.append(b[at:]);break
  n=0
  if op>=128:n=struct.unpack_from('<H',b,p)[0];p+=2
  d=b[p:p+n];p+=n;replacement=None
  if op==0x83:
   url,q=cstring(d,0);target,q=cstring(d,q)
   if target==b'_level0' and url.decode('cp1252').lower() in files:
    canonical=files[url.decode('cp1252').lower()];new=b'FSCommand:loadModule\0'+canonical.encode('cp1252')+b'\0';assert q==len(d)
    replacement=bytes([op])+struct.pack('<H',len(new))+new
    local.append({'location':where,'action_offset_within_block':at,'original_target':url.decode('cp1252'),'module':canonical,'before_hex':b[at:p].hex(),'after_hex':replacement.hex()})
  output.append(replacement if replacement is not None else b[at:p])
 if local:
  # Absolute action positions may change; no branch crosses a changed GetURL.
  assert not any(op in (0x99,0x9d,0x8a,0x8d,0x9b,0x8e) for op in ops),(where,ops)
  result=b''.join(output);changes.extend(local);return result
 return b
def patch_button(d,where,changes):
 off=struct.unpack_from('<H',d,3)[0]
 if not off:return d
 p=3+off;prefix=d[:p];blocks=[]
 while p+4<=len(d):
  size,flags=struct.unpack_from('<HH',d,p);end=p+size if size else len(d);actions=d[p+4:end];patched=patch_actions(actions,where+f'/condition{flags:x}',changes);newsize=4+len(patched) if size else 0;assert newsize<65536
  blocks.append(struct.pack('<HH',newsize,flags)+patched)
  if not size:break
  p=end
 result=prefix+b''.join(blocks);assert result[:3+off]==d[:3+off];return result
def tagencode(code,payload,originalheader):
 oldn=originalheader[0]|(originalheader[1]<<8)
 if len(payload)<63 and oldn&63!=63:return struct.pack('<H',(code<<6)|len(payload))+payload
 return struct.pack('<HI',(code<<6)|63,len(payload))+payload
def patch_tags(b,p,where,changes,audit):
 result=[];index=0
 while p+2<=len(b):
  at=p;h=struct.unpack_from('<H',b,p)[0];p+=2;t=h>>6;n=h&63
  if n==63:n=struct.unpack_from('<I',b,p)[0];p+=4
  header=b[at:p];d=b[p:p+n];p+=n;loc=where+f'/tag{t}[{index}]@{at}';index+=1;before=len(changes)
  if t==39:new=d[:4]+patch_tags(d,4,loc,changes,audit)
  elif t==34:new=patch_button(d,loc+'/button'+str(struct.unpack_from('<H',d)[0]),changes)
  elif t in (12,59):pre=d[:2] if t==59 else b'';new=pre+patch_actions(d[len(pre):],loc,changes)
  else:new=d
  if new!=d:
   assert len(changes)>before; audit.append({'location':loc,'tag':t,'before_payload_sha256':sha(d),'after_payload_sha256':sha(new),'before_payload_size':len(d),'after_payload_size':len(new),'change_kind':'only_GetURL_actions_and_required_container_lengths'})
  else:assert new==d
  result.append(tagencode(t,new,header))
  if t==0:assert p==len(b);return b''.join(result)
 raise ValueError('No End '+where)
def route_movie(raw,name,mapping):
 global files
 files=mapping
 data=raw[:8]+zlib.decompress(raw[8:]) if raw[:3]==b'CWS' else raw;p=rectend(data,8)+4;changes=[];audit=[];tags=patch_tags(data,p,'root',changes,audit)
 if changes:
  finaldata=data[:4]+struct.pack('<I',p+len(tags))+data[8:p]+tags;final=finaldata[:8]+zlib.compress(finaldata[8:],9) if raw[:3]==b'CWS' else finaldata
 else:final=raw
 return final,{'file':name,'original_sha256':sha(raw),'web_sha256':sha(final),'original_size':len(raw),'web_size':len(final),'changes':changes,'changed_tag_payloads':audit,'unchanged_tags_preserved_byte_exact':True,'branch_safety':'changed action blocks have no jumps, if, skip frames or nested function declarations','audio_unchanged':True}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source',type=pathlib.Path,default=SRC);parser.add_argument('--destination',type=pathlib.Path,default=DEST);parser.add_argument('--manifest',type=pathlib.Path,default=OUT/'fscommand-route-manifest.json');args=parser.parse_args();args.destination.mkdir(parents=True,exist_ok=True);mapping={p.name.lower():p.name for p in args.source.glob('*.swf')}
 for path in args.source.glob('*.swf'):
  final,evidence=route_movie(path.read_bytes(),path.name,mapping);(args.destination/path.name).write_bytes(final);manifest.append(evidence)
 args.manifest.write_text(json.dumps(manifest,indent=2),encoding='utf8');print(json.dumps({'files':len(manifest),'changed_files':sum(bool(r['changes']) for r in manifest),'changed_GetURL_actions':sum(len(r['changes']) for r in manifest),'destination':str(args.destination)},indent=2))
