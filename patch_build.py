from pathlib import Path
import re
root=Path('/mnt/data/NB3D_FULL_COUNT_HR_WIN_v1')
for name in ['index.html','ai.html','attack.html']:
 p=root/name
 s=p.read_text()
 is_ai=name=='ai.html'; is_attack=name=='attack.html'
 def exact(old,new,expected=1):
  global s
  k=s.count(old)
  if k!=expected: raise Exception(f'{name}: expected {expected} occurrence, saw {k}: {old[:80]}')
  s=s.replace(old,new)
 def one_regex(pat,repl):
  global s
  s,n=re.subn(pat,repl,s,count=1,flags=re.S)
  if n!=1: raise Exception(f'{name}: no regex {pat[:80]}')
 s=s.replace('<title>NUMBER BASEBALL | 3D Broadcast</title>','<title>FULL COUNT | HOME RUNS WIN</title>').replace('<title>NUMBER BASEBALL | AI SOLO · LIVE</title>','<title>FULL COUNT | HOME RUNS WIN · AI</title>')
 # separate storage to protect the v42 game history, include historical info for compatibility
 exact("const CAREER_KEY='number-baseball-career-v23';" if not is_attack else "const CAREER_KEY='number-baseball-career-v35-attack';", "const CAREER_KEY='nb3d-full-count-hr-v1-career-'+('"+('attack' if is_attack else 'ai' if is_ai else 'versus')+"');")
 exact("const SAVE_KEY='number-baseball-3d-v7-match';" if name=='index.html' else "const SAVE_KEY='number-baseball-3d-v7-ai-match';" if is_ai else "const SAVE_KEY='number-baseball-3d-v35-attack-match';", "const SAVE_KEY='nb3d-full-count-hr-v1-'+('"+('attack' if is_attack else 'ai' if is_ai else 'versus')+"')+'-match';")
 # replace unique index UI headings and make objective visible
 exact('<h1>⚾ NUMBER BASEBALL · 공격모드</h1>' if is_attack else '<h1>⚾ NUMBER BASEBALL</h1>', '<h1>⚾ FULL COUNT <small style="font-size:.48em;color:#ffd082">HR WINS</small></h1>')
 exact('⚾ NUMBER BASEBALL · LIVE SCORE', '🏆 FULL COUNT · HOME RUNS WIN · RUNS FOR FUN')
 exact('<section class="panel"><h2>경기 현황</h2>', '<section class="panel"><h2>🏆 홈런으로 승부 · 경기 현황</h2><div class="fc-primary-board" id="fcPrimaryBoard" aria-live="polite">원정 HR <strong>0</strong> : <strong>0</strong> HR 홈</div><div class="fc-subline">승패는 홈런 개수로만 결정 · 일반 득점은 참고 기록</div>')
 exact('<section class="panel"><h2>타석 조작</h2>', '<section class="panel"><h2>타석 조작</h2><div class="fc-clock-strip"><span>⏱️ 피치클락 <strong id="fcClock">01:00</strong></span><span id="fcClockInfo">첫 추리 60초 · 이후 45초</span></div><div class="fc-foul-strip" id="fcFoulStatus">투수 누적 F 0/6 · 2S에서 6F 도달 시 특별 아웃</div>')
 # explanation, setup screen, instructions
 exact('⚾ 3S 홈런 · 3F 즉시 아웃 · 누적 3S 삼진 · 4B 출루(조건부 1루타 기록)', '🏆 3S 홈런이 승패를 결정합니다 · 4B 출루는 득점에만 영향 · 누적 F 6개는 2S에서 특별 아웃')
 exact('🤖 컴퓨터가 수비 · 투수 교체 시에만 비밀 숫자 교체 가능' if is_attack else '비밀 숫자는 수비팀만 설정 · 교체 시에만 변경', '🏆 홈런 수로 승리 · 볼넷 후 강제 숫자 변경 없음')
 # Add standalone css before closing style
 css='''
/* FULL COUNT HR WINS v1: preserve the v42 layout while elevating the win condition */
.fc-primary-board{font-size:clamp(17px,2vw,25px);font-weight:900;border:1px solid #e7b95c;background:linear-gradient(125deg,#1c3447,#3e301f);color:#ffe0a0;border-radius:12px;padding:13px;margin:2px 0 8px;text-align:center;letter-spacing:.5px}
.fc-primary-board strong{font-size:1.35em;color:#fff5cc;padding:0 7px}
.fc-subline{color:#bed3dc;font-size:12px;margin:0 0 8px}
.fc-clock-strip{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:7px;padding:10px;background:#162c40;border:1px solid #41657b;border-radius:10px;margin-bottom:7px}
.fc-clock-strip strong{font-size:22px;color:#f9cf75;font-variant-numeric:tabular-nums}
.fc-clock-strip strong.fc-urgent{color:#ff695d;animation:fc-flash .72s infinite alternate}
.fc-clock-strip span:last-child,.fc-foul-strip{color:#bdd3df;font-size:12px}
.fc-foul-strip{padding:7px 10px;background:#092838;border:1px solid #35556d;border-radius:9px;margin-bottom:10px}
@keyframes fc-flash{from{opacity:1}to{opacity:.42}}
.fc-note{padding:9px 12px;border-radius:9px;background:#263322;color:#ffe6b1;margin:10px 0;font-weight:700;font-size:13px}
'''
 exact('</style></head><body class="nb-attack">' if is_attack else '</style></head><body>', css+('</style></head><body class="nb-attack">' if is_attack else '</style></head><body>'))
 # fresh state fields
 exact('bases:[false,false,false],score:[0,0],batterIndex:', 'bases:[false,false,false],score:[0,0],homeRuns:[0,0],batterIndex:')
 exact('secret:null,consecutiveWalks:0,changeRight:false,starterChanges:0,starterSecrets:[]','secret:null,consecutiveWalks:0,changeRight:false,foulDigits:0,starterChanges:0,starterSecrets:[]',2)
 # Global helpers before fresh()
 key='const fresh=()=>'
 helper='''// FULL COUNT v1 — home runs, not runs, determine the match winner.
const FC_FOUL_TIP_DIGITS=6;
function fcHR(t){return Number(game?.homeRuns?.[t]||0)}
function fcWinner(){if(game?.concession)return game.concession.winner;return fcHR(0)===fcHR(1)?null:fcHR(0)>fcHR(1)?0:1}
// A 3S HR earns one HR regardless of baserunner count or runs batted in.
function fcDisplayWinner(){const w=fcWinner();return w===null?'홈런 동률 · 무승부':game?.concession?`${teamNames[w]} 기권 승리!`:`${teamNames[w]} 홈런 승리!`}
'''
 exact(key,helper+key)
 exact('// A 3S HR earns one HR regardless of baserunner count or runs batted in.', '// A 3S HR earns one HR regardless of baserunner count or runs batted in.\nfunction fcThreeChanged(oldValue,newValue){return typeof oldValue==="string"&&typeof newValue==="string"&&oldValue.length===3&&newValue.length===3&&[0,1,2].every(i=>oldValue[i]!==newValue[i])}')
 # After a HR, a chosen full-secret change must alter all three positions; leaving it unchanged is allowed.
 exact('if(!nbCanRefreshStarter(t)||', 'if(t.fcHomerSecret&&!fcThreeChanged(t.fcHomerSecret,newSecret))return false;\n if(!nbCanRefreshStarter(t)||')
 exact('t.starterSecrets=[...history,newSecret];t.secret=newSecret;', 't.starterSecrets=[...history,newSecret];t.secret=newSecret;t.fcHomerSecret=null;')
 exact('if(!seen.has(value))return value;', 'if(!seen.has(value)&&(!t.fcHomerSecret||fcThreeChanged(t.fcHomerSecret,value)))return value;')
 # pitcher replaced: reset foul count only when actual pitcher changes, not starter secret changes
 s=re.sub(r'(t\.pitcherNumber\+\+;t\.pitchCount=0;)',r'\1t.foulDigits=0;',s)
 # Explicit rule: walks do NOT award new number-change rights, including v42 consecutive-walk unlocks.
 exact('return !!t&&(t.changeRight||t.pitchCount>=25||(t.pitchCount>=15&&t.consecutiveWalks>=1))', 'return !!t&&(t.changeRight||t.pitchCount>=25)')
 exact('staff().consecutiveWalks++;if(staff().consecutiveWalks>=2)staff().changeRight=true;', 'staff().consecutiveWalks++; // Walks never grant a number-change right in FULL COUNT HR WINS.')

 # 6F outs are already earned by number logic; only their recorded kind and camera scene vary.
 exact("if(effect==='homer')frame.scene=", "if(effect==='out'&&game.fcLast6FScene)frame.scene=game.fcLast6FScene;\n   else if(effect==='homer')frame.scene=")
 exact("finalTie:'무승부'", "sixF_foulTip:'포수 파울팁 삼진',sixF_firstSolo:'1루수 직접 아웃',sixF_firstPitcher:'1루수→투수 커버',sixF_pitcherLiner:'투수 직선타 아웃',finalTie:'무승부'")
 # Defense can retain the prior secret after a HR, but if they choose to change it, all 3 positions differ.
 exact("staff().changeRight=true;staff().consecutiveWalks=0;", "staff().changeRight=true;staff().fcHomerSecret=staff().secret;staff().consecutiveWalks=0;")
 exact("const t=staff(),allowed=nbHasChangeRight(t)||guardReason==='inning'||guardReason==='start';\n if(secretEntryAction==='starter')", "const t=staff(),allowed=nbHasChangeRight(t)||guardReason==='inning'||guardReason==='start';\n if(t.fcHomerSecret&&secretEntryAction!=='first'&&!fcThreeChanged(t.fcHomerSecret,v)){$('guardHelp').textContent='홈런 후 숫자 변경은 기존 숫자와 세 위치가 모두 달라야 합니다. 유지하려면 투수 유지 버튼을 선택하세요.';return;}\n if(secretEntryAction==='starter')")
 exact('t.secret=v;pendingManagerVisit=true;', 't.secret=v;t.fcHomerSecret=null;pendingManagerVisit=true;')
 exact('t.pitcherNumber++;t.pitchCount=0;', 't.pitcherNumber++;t.pitchCount=0;', expected=s.count('t.pitcherNumber++;t.pitchCount=0;')) if False else None
 # Retaining an unchanged secret with a new pitcher is a permitted defensive bluff.
 s=s.replace('t.pitcherNumber++;t.pitchCount=0;t.foulDigits=0;', 't.pitcherNumber++;t.pitchCount=0;t.foulDigits=0;t.fcHomerSecret=null;')
 # home run tally
 exact('let bs=batterStat();bs.pa++;bs.ab++;bs.h++;\n staff().changeRight=true;', 'let bs=batterStat();bs.pa++;bs.ab++;bs.h++;bs.hr=(bs.hr||0)+1;game.homeRuns[game.half]++;\n staff().changeRight=true;')
 exact('function newBatter(){return {pa:0,ab:0,r:0,rbi:0,h:0,k:0,bb:0}}','function newBatter(){return {pa:0,ab:0,r:0,rbi:0,h:0,hr:0,k:0,bb:0}}')
 # Reward individual three-strike knowledge in the MVP selection too.
 exact('let value=p.rbi*4+p.h*2+p.r*2+p.bb;', 'let value=(p.hr||0)*100+p.rbi*4+p.h*2+p.r*2+p.bb;')

 if is_attack:
  # Retain the post-HR constraint before replacing a real pitcher.
  exact('const oldName=currentPitcherName(),oldSecret=t.secret;', 'const oldName=currentPitcherName(),oldSecret=t.secret,oldHomer=t.fcHomerSecret;')
  exact('let candidate=randSecret();', 'let candidate=randSecret();')
  exact("if(!keepNumber){for(let attempt=0;attempt<20&&candidate===oldSecret;attempt++)candidate=randSecret();if(candidate===oldSecret)candidate=oldSecret.split('').reverse().join('')}", 'if(!keepNumber){for(let attempt=0;attempt<100&&(oldHomer?!fcThreeChanged(oldHomer,candidate):candidate===oldSecret);attempt++)candidate=randSecret();}')
  exact('t.secret=keepNumber?oldSecret:candidate;', 't.secret=keepNumber?oldSecret:candidate;t.fcHomerSecret=null;')
 elif is_ai:
  # Computer defense: any changed secret after HR must change all three positions.
  exact('const old=currentPitcherName(),oldSecret=t.secret;', 'const old=currentPitcherName(),oldSecret=t.secret,oldHomer=t.fcHomerSecret;')
  exact('let next=randSecret();for(let attempt=0;attempt<20&&next===oldSecret;attempt++)next=randSecret();', 'let next=randSecret();for(let attempt=0;attempt<100&&(oldHomer?!fcThreeChanged(oldHomer,next):next===oldSecret);attempt++)next=randSecret();if(oldHomer&&!fcThreeChanged(oldHomer,next))next=ALL_NUMBERS.find(x=>fcThreeChanged(oldHomer,x));')
 # ensure all guard-displayed text correctly clarifies the 3-position condition
 # update board HR display; deliberately regular scores still show
 exact("$('secretNote').textContent='🏆 홈런 수로 승리 · 볼넷 후 강제 숫자 변경 없음';", "$('secretNote').textContent='🏆 홈런 수로 승리 · 볼넷 후 강제 숫자 변경 없음';\n $('fcPrimaryBoard').innerHTML=`${teamNames[0]} HR <strong>${fcHR(0)}</strong> : <strong>${fcHR(1)}</strong> HR ${teamNames[1]}`;\n $('fcFoulStatus').textContent=`수비 투수 누적 F ${Number(staff().foulDigits||0)%FC_FOUL_TIP_DIGITS}/${FC_FOUL_TIP_DIGITS} · 2S에서 6F 도달 시 파울팁 계열 특별 아웃`;fcClockPaint();")
 # F accumulation and out-before-actions: pre-existing 2 strike then crossing F6. count F digits, not F-containing guesses
 marker="let prefix=`${guess} → ${s}S ${b}B ${f}F · `;let effect='pitch';if(s===3)"
 new="""let prefix=`${guess} → ${s}S ${b}B ${f}F · `;let effect='pitch';
 const fcBeforeF=Number(staff().foulDigits||0);
 staff().foulDigits=fcBeforeF+f;
 const fcFoulTip=f>0&&s!==3&&f!==3&&g.strikes===2&&g.strikes+s<3&&Math.floor((fcBeforeF+f)/FC_FOUL_TIP_DIGITS)>Math.floor(fcBeforeF/FC_FOUL_TIP_DIGITS);
 game.fcLastFoulTip=fcFoulTip;game.fcLast6FScene=null;
 if(fcFoulTip){
   const roll=Math.random(),scene=game.bases.some(Boolean)?'sixF_foulTip':(roll<.40?'sixF_foulTip':roll<.70?'sixF_firstSolo':roll<.90?'sixF_firstPitcher':'sixF_pitcherLiner');
   game.fcLast6FScene=scene;
   const isK=scene==='sixF_foulTip';
   const label={sixF_foulTip:'파울팁 포구 삼진',sixF_firstSolo:'1루수 직접 터치 아웃',sixF_firstPitcher:'1루수→투수 1루 커버 아웃',sixF_pitcherLiner:'투수 직선타 포구 아웃'}[scene];
   effect='out';out(prefix+'누적 6F! '+label,isK?'k':'out');
 }
 else if(s===3)"""
 exact(marker,new)
 # Home run based win + inning logic for versus and ai, attack has own inning model
 if not is_attack:
  exact('game.score[1]>game.score[0])return finish()', 'fcHR(1)>fcHR(0))return finish()')
  exact('game.score[0]!==game.score[1])return finish()', 'fcHR(0)!==fcHR(1))return finish()')
  exact('game.score[1]>game.score[0])finish();else if(game.outs>=3)endInning()', 'fcHR(1)>fcHR(0))finish();else if(game.outs>=3)endInning()')
  # final text in finish function, specific replacement one line
  one_regex(r'function finish\(\)\{decisionPending=false;game.over=true;caption\(`🏆 경기 종료!.*?\}\n',
   "function finish(){decisionPending=false;game.over=true;caption(`🏆 경기 종료 · 홈런 ${teamNames[0]} ${fcHR(0)} : ${fcHR(1)} ${teamNames[1]} · ${fcDisplayWinner()} (참고 득점 ${game.score[0]}:${game.score[1]})`,'end');if(nbDirectorResolving){nbDirectorPendingFinal=true;}else renderFinal();saveSnapshot()}\n")
  exact("game.score[1]>game.score[0])log(`🏆 끝내기 홈런!", "fcHR(1)>fcHR(0))log(`🏆 끝내기 홈런!")
  # Non-homer runs can't induce walkoff. suppress 'walkoff' captions (the code may still have run logs)
  exact("if(game.inning>=(game.targetInnings||9)&&game.half===1&&game.score[1]>game.score[0])log(`🏆 끝내기 안타! ${teamNames[1]}가 승리합니다!`,'walkoff');","")
  # postgame record winner, no truncated highlights count
  exact('winner=game.score[0]===game.score[1]?null:(game.score[0]>game.score[1]?0:1)', 'winner=fcWinner()')
  exact("homeRuns:[0,1].map(t=>(game.highlights||[]).filter(e=>e.kind==='homer'&&e.team===t).length)","homeRuns:game.homeRuns.slice()")
  exact("const winning=game.concession?.winner===0||game.concession?.winner===1?game.concession.winner:(game.score[0]===game.score[1]?-1:(game.score[0]>game.score[1]?0:1));", "const winning=fcWinner()===null?-1:fcWinner();")
  # Poster top score home runs first + runs in subcaption
  exact("text(`${game.score[0]} : ${game.score[1]}`,550,341,90,'#0a1c36','900','center');", "text(`${fcHR(0)} : ${fcHR(1)}`,550,341,90,'#0a1c36','900','center');text(`홈런 · 참고 득점 ${game.score[0]} : ${game.score[1]}`,550,384,22,'#d9e6ef','700','center');")
  exact("entries.push(`최종 스코어 · ${teamNames[0]} ${game.score[0]} : ${game.score[1]} ${teamNames[1]}`);", "entries.push(`최종 홈런 · ${teamNames[0]} ${fcHR(0)} : ${fcHR(1)} ${teamNames[1]}`);")
  # gameplay result overlay
  exact("$('finalScore').textContent=`${teamNames[0]} ${game.score[0]} : ${game.score[1]} ${teamNames[1]}`;", "$('finalScore').textContent=`🏆 홈런 ${teamNames[0]} ${fcHR(0)} : ${fcHR(1)} ${teamNames[1]} · ${fcDisplayWinner()}`;")
  exact("'정규 경기 종료';renderHighlights()", "`참고 득점 ${game.score[0]}:${game.score[1]} · 승부는 홈런으로만 결정`;renderHighlights()")
  # no auto-concession by meaningless run scores
  one_regex(r'function updateSurrenderAdvice\(\)\{.*?\n\}',"function updateSurrenderAdvice(){const tip=$('surrenderAdvice');if(!tip||!game)return;tip.textContent=game.over?'경기 종료':'홈런 개수로 승부합니다. 득점 차만으로 기권하지 마세요.';}")
  if is_ai:
   one_regex(r'function shouldAiSurrender\(\)\{.*?\n\}',"function shouldAiSurrender(){return false; /* HR challenge AI never forfeits because of the run score */ }")
  # modify live visual endings based on HR not runs (scene analyzer gets capture homeRuns?)
  exact("const ending=walkoff?'walkoffCelebrate':after.score[0]===after.score[1]?'finalTie':'finalCelebrate';", "const ending=walkoff?'walkoffCelebrate':fcHR(0)===fcHR(1)?'finalTie':'finalCelebrate';")
  # turn home-run based end over scene build walkoff from actual event, avoid false run-based
  exact("const walkoff=before.half===1&&runDelta>0&&after.score[1]>after.score[0];", "const walkoff=effect==='homer'&&before.half===1&&fcHR(1)>fcHR(0);")
  # commentary if high score in end inning to HR
  s=s.replace('Math.abs(game.score[0]-game.score[1])<=2','Math.abs(fcHR(0)-fcHR(1))<=1')
  s=s.replace('Math.abs(game.score[0]-game.score[1])<=1','Math.abs(fcHR(0)-fcHR(1))<=1')
  # prevent early finish on run-only in save by replacing any extra visible early comparisons if not already
 else:
  # Attack challenge, single offensive side only
  exact("function finish(){decisionPending=false;game.over=true;caption(`🏆 공격모드 9이닝 완료! 최종 ${game.score[0]}득점 · 투수 ${staff().pitcherNumber}명 상대. 기록을 확인해 보세요.`,'end');", "function finish(){decisionPending=false;game.over=true;caption(`🏆 홈런 챌린지 완료! ${fcHR(0)}홈런 · 참고 득점 ${game.score[0]}점 · 상대 투수 ${staff().pitcherNumber}명`,'end');")
  exact("$('finalScore').textContent=", "$('finalScore').textContent=",expected=1)  # placeholder
  # separate attack labels via update below
  s=s.replace("'정규 경기 종료';renderHighlights()", "`홈런 챌린지 종료 · HR ${fcHR(0)}개`;renderHighlights()")
  s=s.replace("const winning=game.concession?.winner===0||game.concession?.winner===1?game.concession.winner:(game.score[0]===game.score[1]?-1:(game.score[0]>game.score[1]?0:1));", "const winning=fcWinner()===null?-1:fcWinner();")
  s=s.replace("text(`${game.score[0]} : ${game.score[1]}`,550,341,90,'#0a1c36','900','center');", "text(`${fcHR(0)} HR`,550,341,90,'#0a1c36','900','center');")
  s=s.replace("const gap=Math.abs(game.score[0]-game.score[1]);", "const gap=Math.abs(fcHR(0)-fcHR(1));")
  # single offensive mode: no opposing offensive lineup; show HR challenge progress.
  s=s.replace("$('finalScore').textContent=`${teamNames[0]} ${game.score[0]} : ${game.score[1]} ${teamNames[1]}`;", "$('finalScore').textContent=`🏆 홈런 챌린지: ${fcHR(0)}홈런 · 참고 득점 ${game.score[0]}점`;")
 # Individual HRs appear in player stats, rather than requiring reconstruction from highlights.
 s=s.replace('<th>안타</th><th>타율</th><th>삼진</th>', '<th>안타</th><th>홈런</th><th>타율</th><th>삼진</th>')
 s=s.replace('<td>${p.h}</td><td>${fmt(p.ab?', '<td>${p.h}</td><td>${p.hr||0}</td><td>${fmt(p.ab?')
 s=s.replace('<td>${x.h}</td><td>${fmt(x.ab?', '<td>${x.h}</td><td>${x.hr||0}</td><td>${fmt(x.ab?')
 # Reject importing an old score-wins save into the new HR-wins save system.
 exact("if(!s||s.version!==7||!g||!Array.isArray(g.score)", "if(!s||s.version!==7||!g||!Array.isArray(g.homeRuns)||g.homeRuns.length!==2||!g.homeRuns.every(v=>Number.isInteger(v)&&v>=0)||!Array.isArray(g.score)")
 # replace scoreboard mini in director and side with HR; existing game score remains in R column
 exact("$('pitchno').textContent=`PITCH ${t.pitchCount}`;", "$('pitchno').textContent=`PITCH ${t.pitchCount} · HR ${fcHR(0)}:${fcHR(1)}`;")
 # Clock declarations and functions injected before fresh to cover all functions
 anchor='const fresh=()=>'
 clock_js='''// One human at-bat: first guess 60s, later guesses 45s. Timer pauses for UI/animation.
let fcClockMs=60000,fcClockLast=0;
function fcClockPaint(){const el=document.getElementById('fcClock');if(!el)return;const secs=Math.ceil(Math.max(0,fcClockMs)/1000);el.textContent=`${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;el.classList.toggle('fc-urgent',secs<=10);}
function fcClockReset(){fcClockMs=game?.atBatStart?60000:45000;fcClockLast=performance.now();fcClockPaint()}
function fcClockAllowed(){return !!game&&!game.over&&!!staff().secret&&!busy&&document.visibilityState!=='hidden'&&document.getElementById('setupOverlay')?.style.display==='none'&&document.getElementById('guard')?.classList.contains('hidden')&&document.getElementById('finalstats')?.classList.contains('hidden')&&document.getElementById('surrenderOverlay')?.classList.contains('hidden')&&__FC_AI_TURN_GUARD__true;}
function fcClockTimeout(){
 if(!fcClockAllowed())return;
 if(game.strikes>=2){out('⏱️ 피치클락 위반으로 삼진!','k');}
 else {game.strikes++;game.atBatStart=false;caption(`⏱️ 피치클락 위반! 스트라이크 추가 (${game.strikes}S)`,'count');}
 fcClockReset();update();saveSnapshot();
}
setInterval(()=>{if(!game){fcClockLast=performance.now();return;}const now=performance.now();const delta=fcClockLast?Math.min(1000,Math.max(0,now-fcClockLast)):0;fcClockLast=now;if(fcClockAllowed()){fcClockMs=Math.max(0,fcClockMs-delta);if(fcClockMs<=0){fcClockTimeout();return;}}fcClockPaint()},150);
'''
 clock_js=clock_js.replace('__FC_AI_TURN_GUARD__', 'game.half===0&&' if is_ai else '')
 exact(anchor,clock_js+anchor)
 # reset initial clock after fresh and on save return from secret entry
 exact('game=fresh();game.targetInnings=', 'game=fresh();fcClockReset();game.targetInnings=')
 # resume / timer after defense returning; all 3 have resumeGuard maybe with AI variant altered, append to function tail for user-visible running
 one_regex(r'(function resumeGuard\(\)\{.*?\n\})', lambda m: m.group(0)+'\n// Clock begins only when a user can actually submit a guess.\n', ) if False else None
 # insert callback fcClockReset as soon as the prior animation finishes, by hooking return callback before update+save.
 if is_ai:
  exact('if(game.half===1)clearGuess();\n   update();saveSnapshot();', 'if(game.half===1)clearGuess();\n   fcClockReset();update();saveSnapshot();')
 elif is_attack:
  exact('pendingManagerVisit=false;postPitchUnlock=false;\n     update();saveSnapshot();', 'pendingManagerVisit=false;postPitchUnlock=false;\n     fcClockReset();update();saveSnapshot();')
 else:
  exact('postPitchUnlock=false;\n   update();saveSnapshot();', 'postPitchUnlock=false;\n   fcClockReset();update();saveSnapshot();')
 # Ensure timer starts upon resuming from protected secret screen. insert at start of resume function (will pause until guard hidden)
 exact('function resumeGuard(){', 'function resumeGuard(){fcClockReset();')
 # remaining time is persistent on manual saves; a paused background tab never consumes clock.
 exact('savedAt:new Date().toISOString(),game:', 'savedAt:new Date().toISOString(),fcClockRemaining:fcClockMs,game:')
 # reset after load; call after restore, but clock set at initial 60/45
 exact('clearGuess();update();setCamera();renderLiveFeed();', 'clearGuess();fcClockReset();if(Number.isFinite(s.fcClockRemaining))fcClockMs=Math.max(1000,Math.min(fcClockMs,s.fcClockRemaining));update();setCamera();renderLiveFeed();')
 # final status when over right after note
 # add HTML helper for user to see rules at setup
 exact('경기 길이</label>', '경기 길이</label>') if False else None
 exact('</nav><div id="resumeBox"', '</nav><div class="fc-note">🏆 승리 기준: 홈런(3S) 최다 · 일반 득점은 참고 기록 · 투수 누적 6F 특별 아웃 · 피치클락 첫 60초/이후 45초</div><div id="resumeBox"')
 # remove v42-only message of goal in main header? Keep original but add HR rules text
 # distinct autonomous saves and no dual mode crossover for v42
 p.write_text(s)
 print(name,len(s))
