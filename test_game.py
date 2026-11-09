from playwright.sync_api import sync_playwright
from pathlib import Path
ROOT=Path('/mnt/data/NB3D_FULL_COUNT_HR_WIN_v1')
def run(page,js): return page.evaluate('(code) => window.__nbtest.exec(code)',js)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for mode in ['index','ai','attack']:
  page=browser.new_page(viewport={'width':1320,'height':850})
  errs=[];page.on('pageerror',lambda e: errs.append(str(e)));page.route('**/*',lambda route:route.abort())
  src=(ROOT/(mode+'.html')).read_text()
  src=src.replace('\n})();\n', "\nwindow.__nbtest={exec:(code)=>eval('(()=>{'+code+'})()')};\n})();\n", 1)
  assert 'window.__nbtest' in src
  page.set_content(src,wait_until='domcontentloaded',timeout=20000)
  page.locator('#startMatch').click()
  run(page,"document.getElementById('guard').classList.add('hidden');game.teams[0].secret='456';game.teams[1].secret='123';busy=false;game.half=0;game.lines[0][0]=0;fcClockReset();update()")
  data=run(page,"const eff=resolve('123','swing');return {effect:eff,homeRuns:game.homeRuns,score:game.score,atBat:game.atBatStart,board:document.getElementById('fcPrimaryBoard').textContent}")
  print(mode,'HOMER',data,'errors',errs)
  assert data['homeRuns'][0]==1,mode
  data=run(page,"game.half=0;game.teams[1].secret='123';game.teams[1].foulDigits=5;game.strikes=2;game.outs=0;game.atBatStart=false;const preK=pitcherStat().k;const eff=resolve('245','swing');return {effect:eff,f:game.teams[1].foulDigits,outs:game.outs,k:pitcherStat().k-preK,scene:game.fcLast6FScene}")
  print(mode,'6F',data,'errors',errs)
  assert data['f']==7 and data['outs']==1 and data['scene'].startswith('sixF_'),mode
  data=run(page,"game.half=0;game.strikes=2;game.outs=0;game.over=false;game.atBatStart=false;busy=false;document.getElementById('guard').classList.add('hidden');document.getElementById('setupOverlay').style.display='none';document.getElementById('surrenderOverlay').classList.add('hidden');document.getElementById('finalstats').classList.add('hidden');fcClockTimeout();return {outs:game.outs,clock:document.getElementById('fcClock').textContent}")
  print(mode,'CLOCK',data,'errors',errs)
  assert data['outs']==1,mode
  if mode!='attack':
   data=run(page,"game.concession=null;game.homeRuns=[1,2];game.score=[100,3];game.inning=9;game.half=0;game.outs=3;game.over=false;endInning();return {winner:fcWinner(),over:game.over,homeRuns:game.homeRuns,score:game.score,final:document.getElementById('finalScore').textContent}")
   print(mode,'WIN BY HR',data,'errors',errs)
   assert data['over'] and data['winner']==1,mode
   assert '홈런' in data['final'] and '100' not in data['final'],mode
  assert not errs,(mode,errs)
  page.close()
 browser.close()
