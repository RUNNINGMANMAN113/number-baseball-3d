/* NUMBER BASEBALL 3D unified shared core v1. No game secrets are shared. */
(function(global){'use strict';
const KEY='nb3d-unified-roster-v1';
const PRESETS={
HT:{label:'KIA 타이거즈',primary:'#bc152b',accent:'#171717'},
SS:{label:'삼성 라이온즈',primary:'#184ea2',accent:'#e8e8eb'},
LG:{label:'LG 트윈스',primary:'#191919',accent:'#c91f35'},
OB:{label:'두산 베어스',primary:'#172750',accent:'#d7243a'},
KT:{label:'KT 위즈',primary:'#141414',accent:'#ea252b'},
SK:{label:'SSG 랜더스',primary:'#c41230',accent:'#f1f1f1'},
LT:{label:'롯데 자이언츠',primary:'#142e50',accent:'#ed7831'},
HH:{label:'한화 이글스',primary:'#f26e21',accent:'#181818'},
NC:{label:'NC 다이노스',primary:'#184e75',accent:'#d7a24c'},
WO:{label:'키움 히어로즈',primary:'#79283f',accent:'#f0e5e9'}};
const DEFAULT_COLORS=[{primary:'#4087c6',accent:'#173e65'},{primary:'#e6b765',accent:'#7d4d1a'}];
const ROLES=['batPositions','pitchPositions','benchNames','benchPositions','teamNames','playerNames','pitcherNames'];
function safeColor(x,def){return typeof x==='string'&&/^#[0-9a-fA-F]{6}$/.test(x)?x.toLowerCase():def;}
function validate(r){return !!(r&&Array.isArray(r.teamNames)&&r.teamNames.length===2&&Array.isArray(r.playerNames)&&r.playerNames.length===2&&r.playerNames.every(x=>Array.isArray(x)&&x.length===9)&&Array.isArray(r.pitcherNames)&&r.pitcherNames.length===2&&r.pitcherNames.every(x=>Array.isArray(x)&&x.length===11));}
function get(){try{const raw=global.localStorage.getItem(KEY);const data=raw?JSON.parse(raw):null;return validate(data)?data:null;}catch(e){return null;}}
function saveRoster(roster,mode){if(!validate(roster))throw Error('공용 선수명단 형식 오류');
  const old=get()||{},next={version:3};
  for(const k of ROLES){const v=roster[k];if(v!==undefined)next[k]=JSON.parse(JSON.stringify(v));}
  next.teamClubCodes=Array.from({length:2},(_,t)=>{const v=roster.teamClubCodes?.[t]??old.teamClubCodes?.[t]??'custom';return PRESETS[v]?v:'custom'});
  next.teamColors=Array.from({length:2},(_,t)=>{const obj=roster.teamColors?.[t]??old.teamColors?.[t]??DEFAULT_COLORS[t];return {primary:safeColor(obj.primary,DEFAULT_COLORS[t].primary),accent:safeColor(obj.accent,DEFAULT_COLORS[t].accent)};});
  next.updatedAt=new Date().toISOString();next.updatedFrom=mode==='classic'?'classic':'fullcount';
  global.localStorage.setItem(KEY,JSON.stringify(next));return next;
}
function readRosterFor(mode){const obj=get();if(!obj)return null;const copy=JSON.parse(JSON.stringify(obj));copy.version=mode==='classic'?2:3;return JSON.stringify(copy);}
function getSummary(){const v=get();return v?{teams:v.teamNames,colors:v.teamColors,clubs:v.teamClubCodes,updatedAt:v.updatedAt,updatedFrom:v.updatedFrom}:null;}
global.NB3DShared=Object.freeze({KEY,KBO_UNIFORM_PRESETS:PRESETS,NB_DEFAULT_COLORS:DEFAULT_COLORS,saveRoster,readRosterFor,getSummary,get,validate});
})(window);
