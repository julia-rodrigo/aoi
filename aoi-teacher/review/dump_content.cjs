// Dumps every Teacher lesson and every quiz set with a content fingerprint.
// Run from anywhere: node aoi-teacher/review/dump_content.cjs  -> review/content_now.json
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const crypto=require('crypto');
const APP=path.resolve(__dirname,'..');const TMP=path.join(APP,'_review_tmp.html');
let src=fs.readFileSync(path.join(APP,'index.html'),'utf8');
const m='    startSession("category", catId);\n    return true;\n  }\n};\n\n})();';
if(src.split(m).length!==2) throw new Error('hook point not found in index.html');
src=src.replace(m,m.slice(0,-5)+'window.__rv={SUBJECTS:SUBJECTS,TEACHER_SECTIONS:TEACHER_SECTIONS,startLearn:startLearn,useSubject:useSubject,learnParts:learnParts,catQuestions:catQuestions,getLesson:function(){return LESSON;}};\n})();');
fs.writeFileSync(TMP,src);
const strip=h=>String(h).replace(/<style[\s\S]*?<\/style>/g,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#39;|&apos;/g,"'").replace(/&quot;/g,'"').replace(/\s+/g,' ').trim();
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
try{
await p.goto('file://'+TMP);await p.waitForTimeout(1500);
const raw=await p.evaluate(()=>{const D=window.__rv;const lessons=[];const quizzes=[];
 const grab=(sec,secTitle,title)=>{const L=D.getLesson();const beats=(L.beats||[]).map(bt=>({text:bt.text||'',visual:typeof bt.visual==='string'?bt.visual:(typeof bt.visual==='function'?(()=>{try{return String(bt.visual()||'');}catch(e){return '';}})():'')}));lessons.push({section:sec,sectionTitle:secTitle,title,beats});};
 for(const S of D.TEACHER_SECTIONS){ if(S.id==='ppl'||S.id==='gk') continue; let mods=[]; try{mods=S.modules();}catch(e){continue;}
  for(const M of mods){ if(!M.start) continue; const before=D.getLesson(); try{M.start();}catch(e){continue;} const L=D.getLesson(); if(L===before) continue; grab(S.id,S.title||S.id,M.title); } }
 for(const k of ['ppl','gk']){ D.useSubject(k); const S=D.SUBJECTS[k];
  for(const c of S.cats){ const parts=D.learnParts(D.catQuestions(S,c.id)); for(let pi=0;pi<parts.length;pi++){ D.startLearn(c.id,pi,'teacher'); grab(k,S.name,c.name+' (part '+(pi+1)+')'); } } }
 for(const k of Object.keys(D.SUBJECTS)){ const S=D.SUBJECTS[k]; for(const c of (S.cats||[])){ const qs=D.catQuestions(S,c.id); if(qs.length) quizzes.push({subject:k,subjectName:S.name,category:c.name,questions:qs}); } }
 return {lessons,quizzes};});
const sha=s=>crypto.createHash('sha256').update(s).digest('hex').slice(0,16);
const out={lessons:{},quizzes:{}};
for(const L of raw.lessons){const id=L.section+' / '+L.title;const content=L.beats.map(x=>x.text+'\n'+strip(x.visual)).join('\n---\n');
 out.lessons[id]={section:L.sectionTitle,title:L.title,beats:L.beats.length,hash:sha(content),text:L.beats.map(x=>x.text).filter(Boolean),visualText:L.beats.map(x=>strip(x.visual)).filter(Boolean)};}
for(const Q of raw.quizzes){const id='quiz: '+Q.subject+' / '+Q.category;out.quizzes[id]={subject:Q.subjectName,category:Q.category,count:Q.questions.length,hash:sha(JSON.stringify(Q.questions)),questions:Q.questions};}
fs.writeFileSync(path.join(__dirname,'content_now.json'),JSON.stringify(out,null,1));
console.log('lessons',Object.keys(out.lessons).length,'quiz sets',Object.keys(out.quizzes).length,'page errors',errs.slice(0,3));
}finally{await b.close();fs.unlinkSync(TMP);}})();
