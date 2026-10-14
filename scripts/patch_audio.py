import pathlib,struct,zlib,json,hashlib,argparse
BAD=b'ArtiAcent1.wav';GOOD=b'ArtiAcen1.wav'
def sha(b):return hashlib.sha256(b).hexdigest()
def patch_audio(raw):
 data=raw[:8]+zlib.decompress(raw[8:]) if raw[:3]==b'CWS' else raw;p=8+(5+4*(data[8]>>3)+7)//8+4;head=data[:p];parts=[];changes=[];frame=1
 while p+2<=len(data):
  at=p;h=struct.unpack_from('<H',data,p)[0];p+=2;t=h>>6;n=h&63
  if n==63:n=struct.unpack_from('<I',data,p)[0];p+=4
  payload=data[p:p+n];p+=n;new=payload
  if t==12 and frame==4:
   q=0;blocks=[]
   while q<len(payload):
    a=q;op=payload[q];q+=1
    if not op:blocks.append(payload[a:]);break
    size=0
    if op>=128:size=struct.unpack_from('<H',payload,q)[0];q+=2
    d=payload[q:q+size];q+=size;replacement=payload[a:q]
    if op==0x88 and BAD+b'\0' in d:
     assert d.count(BAD+b'\0')==1;nd=d.replace(BAD+b'\0',GOOD+b'\0');replacement=bytes([op])+struct.pack('<H',len(nd))+nd
     changes.append({'root_frame':frame,'tag':t,'tag_offset_before':at,'action_offset_within_tag':a,'opcode':'0x88','before_symbol':BAD.decode(),'after_symbol':GOOD.decode(),'before_action_hex':payload[a:q].hex(),'after_action_hex':replacement.hex(),'before_payload_sha256':sha(payload),'before_payload_size':len(payload)})
    blocks.append(replacement)
   new=b''.join(blocks)
   if new!=payload:changes[-1].update({'after_payload_sha256':sha(new),'after_payload_size':len(new)})
  if new==payload:parts.append(data[at:p])
  elif len(new)<63 and h&63!=63:parts.append(struct.pack('<H',(t<<6)|len(new))+new)
  else:parts.append(struct.pack('<HI',(t<<6)|63,len(new))+new)
  if t==1:frame+=1
  if t==0:assert p==len(data);break
 assert len(changes)==1,changes;body=b''.join(parts);finaldata=head[:4]+struct.pack('<I',len(head)+len(body))+head[8:]+body;final=finaldata[:8]+zlib.compress(finaldata[8:],9) if raw[:3]==b'CWS' else finaldata
 return final,{'before_sha256':sha(raw),'after_sha256':sha(final),'before_size':len(raw),'after_size':len(final),'changes':changes,'only_constant_pool_symbol_and_required_lengths_changed':True,'all_DefineSound_bytes_preserved':True,'restore': 'Rerun route_fscommands.py from the preserved original to recover the pre-audio-patch variant.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('input',type=pathlib.Path);parser.add_argument('output',type=pathlib.Path);parser.add_argument('manifest',type=pathlib.Path);args=parser.parse_args();result,manifest=patch_audio(args.input.read_bytes());args.output.write_bytes(result);args.manifest.write_text(json.dumps(manifest,indent=2),encoding='utf8');print(json.dumps(manifest,indent=2))
